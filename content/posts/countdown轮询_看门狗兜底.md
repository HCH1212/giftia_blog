---
title: 'Countdown轮询+看门狗兜底'
date: 2026-07-13
lastmod: 2026-07-13
author: "giftia"
description: "异步任务中countdown轮询与看门狗兜底机制的设计与实战"
draft: false
categories: ["运维"]
tags: ["Celery", "异步任务", "设计模式", "可靠性", "看门狗"]
---

## 为什么需要轮询

异步任务最常见的场景是：提交一个耗时操作，然后等它完成。但有一种场景更棘手——**你不知道要等多久**。

比如：调用一个异步 API 提交工单，对方处理完回调通知你。优雅的做法是起个 Webhook 接口被动接收回调。但生产环境里回调可能丢失（对方没发、网络抖动、你的服务刚好重启），于是你还需要一个主动轮询的兜底机制。

轮询最粗暴的写法：

```python
@app.task
def poll_task(task_id):
    # 轮询等结果，最多等 5 分钟
    deadline = time.time() + 300
    while time.time() < deadline:
        result = check_external_api(task_id)
        if result:
            handle_result(result)
            return
        time.sleep(10)  # 阻塞 Worker 进程长达 5 分钟
    raise TimeoutError("轮询超时")
```

`time.sleep(10)` 会死死占住一个 Worker 进程。如果有 10 个这样的轮询任务同时跑，10 个 Worker 全部被堵死，其他正常任务全部排队等候——这就是经典的"轮询阻塞"。

## Countdown 轮询：非阻塞重试

Celery 的 `countdown` 参数可以让任务延迟执行而不占用 Worker：

```python
@app.task(bind=True, max_retries=30)
def poll_with_countdown(self, task_id, deadline=None):
    """countdown 轮询：每次检查后释放 Worker，10 秒后再来"""
    if deadline is None:
        deadline = time.time() + 300  # 默认等 5 分钟
    
    if time.time() > deadline:
        raise self.MaxRetriesExceededError(
            f"任务 {task_id} 轮询超时"
        )
    
    result = check_external_api(task_id)
    if result:
        handle_result(result)
        return  # 完成
    
    # 未就绪，10 秒后重试，Worker 立即释放处理其他任务
    raise self.retry(countdown=10)
```

关键在于 `self.retry(countdown=10)`——它告诉 Broker："这个任务 10 秒后再投递一次"，当前 Worker **立即释放**去处理下一个任务。

相比 `time.sleep`：

| 方式 | Worker 占用 | 10 并发时影响 |
|---|---|---|
| `time.sleep(10)` 循环 | 持续占用 | 堵死 10 个 Worker |
| `countdown` 重试 | 仅占用瞬间 | 几乎无影响 |

## 看门狗兜底

`countdown` 解决了阻塞问题，但引入了新风险：重试依赖 Celery 自身的重试机制，如果任务意外丢失（Broker 挂了、任务被误删），重试链就断了。

看门狗的作用：**独立于任务本身的监控者**，定期扫描"卡住的中间状态"，推动它们走向终态。

```python
@app.task
def watchdog_scan():
    """看门狗：扫描处于中间状态超时的任务，强制推进"""
    stale_threshold = timezone.now() - timedelta(minutes=10)
    
    # 查找创建超过 10 分钟仍在"处理中"的任务
    stuck_tasks = TaskRecord.objects.filter(
        status=TaskStatus.PROCESSING,
        created_at__lt=stale_threshold,
    )
    
    for task in stuck_tasks:
        try:
            # 重新查询外部状态
            ext_result = check_external_api(task.external_task_id)
            if ext_result:
                handle_result(task, ext_result)
            else:
                # 外部也没结果，标记失败，触发告警
                task.mark_failed("看门狗超时")
                send_alert(f"任务 {task.id} 处理超时，已标记失败")
        except Exception as e:
            logger.exception(f"看门狗处理任务 {task.id} 失败: {e}")
    
    logger.info(f"看门狗扫描完成，处理 {len(stuck_tasks)} 个卡住任务")
```

配合 Celery Beat 定时调度：

```python
# celery.py
app.conf.beat_schedule = {
    'watchdog-scan': {
        'task': 'tasks.watchdog_scan',
        'schedule': 60.0,  # 每分钟扫一次
    },
}
```

## 完整模式

```
                    ┌─────────────┐
                    │  提交异步任务  │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Task A (countdown=10)  │
              │  check_external_api()   │
              │  未就绪 → retry         │
              └────────────┬───────────┘
                           │ 重试链
                           ▼
              ┌────────────────────────┐
              │  Task A (countdown=10)  │
              │  check_external_api()   │
              │  已就绪 → handle()      │
              └────────────────────────┘

             ═══════ 看门狗（独立） ═══════
            每分钟扫描 PROCESSING 超时任务
                    → 超时则标记失败/告警
```

两层保障：
1. **Countdown 轮询**处理正常等待场景（对方 API 慢但会返回）
2. **看门狗兜底**处理异常场景（重试链断裂、任务丢失、对方 API 彻底挂了）

> 看门狗不要和轮询任务同一个队列，避免队列阻塞时看门狗也一起被卡住。
