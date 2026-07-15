---
title: 'celery多队列多任务的阻塞和并发问题'
date: 2026-05-16
lastmod: 2026-05-16
author: "giftia"
description: "剖析 Celery 多队列阻塞问题的原因与解决方案"
draft: false
categories: ["运维"]
tags: ["Celery", "异步任务", "消息队列", "性能优化"]
---

## 为什么会阻塞

### 长短任务混杂

单个 Worker 处理多队列时，长任务会阻塞短任务。解决方案：**隔离队列**。

```bash
# 不同队列用独立 Worker
celery -A tasks worker --queues=fast_tasks --concurrency=10 -n fast_worker@%h
celery -A tasks worker --queues=slow_tasks --concurrency=2 -n slow_worker@%h
```

### 预取机制

`worker_prefetch_multiplier` 默认 4，Worker 会一次拉取 `并发数 × 4` 个任务到本地缓存。长任务卡住后，其他 Worker 空闲也无法接手。

**解决**：对重任务队列 `worker_prefetch_multiplier = 1`。

### 同步等待死锁

任务内部使用 `.get()` 同步等待另一个任务，并发占满时会导致死锁。

**解决**：使用 Celery Canvas 工作流：

```python
from celery import chain, group

# 链式：串行执行
workflow = chain(
    validate.s(order_id),
    deduct.s(order_id),
    notify.s(order_id)
)

# 组：并行执行
group(tasks).apply_async()
```

## 并发模式选择

| 模式 | 适用 | 注意 |
|---|---|---|
| Prefork（默认） | CPU 密集型 | 进程切换开销大 |
| Gevent | I/O 密集型 | 代码必须非阻塞 |
| Solo | 严格串行 | 并发数为 1 |

## 生产配置建议

```python
# 全局超时
app.conf.task_time_limit = 300       # 硬超时 5 分钟
app.conf.task_soft_time_limit = 270  # 软超时 4.5 分钟

# 重任务队列：关闭预取
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
```

**十六字方针**：长短分家、引擎选对、预取设小、超时设牢。
