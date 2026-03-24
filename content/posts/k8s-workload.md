---
title: 'K8s Workload'
date: 2026-03-24
lastmod: 2026-03-24
author: 'giftia'
description: '理解 Kubernetes Workload 的核心模型、选型方法与实践建议。'
draft: false
categories: ['技术']
tags: ['Kubernetes', 'Workload', 'Deployment', 'StatefulSet', 'Job']
---

## Workload 是什么

在 Kubernetes 里，`Workload` 可以理解为“应用运行方式的声明”。

我们并不直接操作 Pod，而是通过 Workload 对象告诉集群：

- 需要运行什么程序
- 需要多少副本
- 失败后如何恢复
- 以什么方式发布新版本

Kubernetes 控制器会持续把“实际状态”拉回到“期望状态”。这也是它和传统手工运维最大的区别。

## 为什么不直接管理 Pod

Pod 是最小调度单位，但它是易失的：

- 节点重启，Pod 可能被重新调度
- Pod 异常退出，需要重新拉起
- 版本发布需要有序替换

如果直接用裸 Pod，所有生命周期管理都要自己处理。Workload 的价值，就是把这些重复工作交给控制器。

## Kubernetes 常见 Workload

### 1. Deployment

最常见的无状态应用控制器，适合 Web 服务、API 服务、网关等。

核心能力：

- 副本管理（Replica）
- 滚动更新（RollingUpdate）
- 回滚（Rollback）
- 声明式扩缩容

### 2. StatefulSet

面向有状态应用，适合数据库、消息队列、分布式存储。

核心特征：

- 稳定网络标识（固定 Pod 名）
- 稳定存储绑定（常配 PVC）
- 有序创建与有序删除

如果你的应用强依赖实例身份（如主从编号、分片编号），优先考虑 StatefulSet。

### 3. DaemonSet

保证每个节点（或指定节点）都运行一个 Pod。

典型场景：

- 日志采集 Agent
- 节点监控 Agent
- CNI / CSI 相关组件

它更像“节点级服务”，而不是业务服务。

### 4. Job

一次性任务，运行完成即结束。

常见用途：

- 数据迁移
- 批处理
- 初始化任务

关键点是“完成次数”和“失败重试次数”可控。

### 5. CronJob

按时间计划触发的 Job。

适合：

- 定时备份
- 定时报表
- 周期性清理任务

本质是 `Cron + Job`，关注调度窗口、并发策略和历史保留策略。

## 如何选型

一个实用决策顺序：

1. 是否是持续在线服务？是则优先 `Deployment` 或 `StatefulSet`。
2. 是否依赖稳定身份/存储？是则选 `StatefulSet`。
3. 是否需要每个节点都运行一份？选 `DaemonSet`。
4. 是否一次性执行后结束？选 `Job`。
5. 是否按固定周期执行？选 `CronJob`。

简单来说：

- 在线无状态：`Deployment`
- 在线有状态：`StatefulSet`
- 节点守护：`DaemonSet`
- 一次任务：`Job`
- 定时任务：`CronJob`

## 一个最小 Deployment 示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: demo-web
  template:
    metadata:
      labels:
        app: demo-web
    spec:
      containers:
        - name: web
          image: nginx:1.27
          ports:
            - containerPort: 80
```

这个配置表达的是：期望始终有 3 个 `demo-web` Pod 运行。若某个 Pod 异常退出，控制器会自动补齐。

## 生产实践建议

1. 不要省略 `requests/limits`，避免资源争抢导致节点抖动。
2. 为在线服务配置 `readinessProbe/livenessProbe`，减少发布和故障期间的流量损失。
3. 给 Deployment 配置合理的滚动更新参数（如 `maxUnavailable`、`maxSurge`）。
4. 关键有状态服务必须绑定持久化存储，并验证恢复流程。
5. Job/CronJob 需要设置历史保留和重试策略，避免任务对象无限堆积。
