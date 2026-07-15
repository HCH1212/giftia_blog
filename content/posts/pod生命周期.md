---
title: 'Pod生命周期'
date: 2026-06-01
author: "giftia"
description: "以三种探针为主线，理解 Pod 生命周期中的健康检查与流量切换。"
draft: false
categories: ["运维"]
tags: ["Kubernetes", "Pod", "livenessProbe", "readinessProbe", "startupProbe"]
---

Pod 生命周期里，最容易影响线上稳定性的部分，往往不是“能不能启动”，而是**探针配得对不对**。

这篇就重点讲三个探针：

- `livenessProbe`
- `readinessProbe`
- `startupProbe`

## 先记住三句话

1. `livenessProbe` 失败：容器会被重启。
2. `readinessProbe` 失败：容器不接流量，但不一定重启。
3. `startupProbe` 生效期间：`liveness/readiness` 会被暂时屏蔽，给慢启动应用“保护期”。

## 三个探针分别解决什么问题

### 1. livenessProbe：进程还“活着”吗

它解决的是“程序假死”问题。

比如：进程还在，但线程卡死、连接池耗尽、接口永远不返回。这个时候容器看起来在运行，但其实已经不可用。

`livenessProbe` 连续失败后，kubelet 会重启容器。

适合场景：

- 进程可能进入死锁/卡死
- 希望通过重启自愈

### 2. readinessProbe：现在能接流量吗

它解决的是“服务可用性”问题。

即使进程活着，也可能暂时不能服务，比如：

- 应用刚启动，缓存还没预热
- 依赖数据库暂时不可达
- 正在做优雅下线

`readinessProbe` 失败时，Pod 会从 Service Endpoints 里移除，不再接收新流量。

适合场景：

- 有初始化过程
- 对外服务前有前置依赖
- 需要灰度或优雅摘流

### 3. startupProbe：给慢启动应用留时间

它解决的是“启动慢导致误杀”的问题。

有些应用启动要几十秒甚至几分钟。如果只配 `livenessProbe`，很可能应用还没起来就被判死，不断重启，最终 `CrashLoopBackOff`。

配置 `startupProbe` 后，在它成功之前，`liveness/readiness` 不会生效。

适合场景：

- Java 大应用
- 需要加载大量模型/数据
- 启动期有迁移、预热等重操作

## 一个常用的探针组合示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
        - name: app
          image: demo/app:1.0.0
          ports:
            - containerPort: 8080

          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 5
            failureThreshold: 24

          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
            timeoutSeconds: 2
            failureThreshold: 2
            successThreshold: 1
```

这个配置表达的意思：

- 先用 `startupProbe` 给启动期最多约 120 秒（`5 * 24`）保护时间。
- 启动完成后，`livenessProbe` 负责“活性检查”，失败就重启。
- `readinessProbe` 负责“是否接流量”，失败就摘流。

## 探针的三种实现方式

K8s 探针常见检查方式：

1. `httpGet`：最常用，适合 Web 服务。
2. `tcpSocket`：只检查端口可连通，不判断业务是否健康。
3. `exec`：在容器内执行命令，适合无 HTTP 服务的场景。

一般建议：

- 有 HTTP 接口优先 `httpGet`
- `tcpSocket` 只作为兜底
- `exec` 要注意命令耗时，避免探针本身变成负担

## 参数怎么理解（最容易混）

- `periodSeconds`：多久检查一次。
- `timeoutSeconds`：单次检查超时时间。
- `failureThreshold`：连续失败几次算失败。
- `successThreshold`：连续成功几次才算恢复（常用于 readiness）。
- `initialDelaySeconds`：容器启动后，延迟多久开始探测。

可以粗略理解为：

- 判定失败时间约为 `periodSeconds * failureThreshold`
- 判定恢复时间约为 `periodSeconds * successThreshold`

## 生命周期里的真实流量路径

结合探针看 Pod 生命周期，核心节点是：

1. Pod 创建并启动容器。
2. 启动阶段由 `startupProbe` 兜底，避免误重启。
3. 启动完成后，`readinessProbe` 成功，Pod 开始接流量。
4. 运行期间 `livenessProbe` 持续检查，异常则重启。
5. `readinessProbe` 可在异常时先摘流，再恢复。

这就是“先能启动，再能接流量，最后保证持续可用”的完整闭环。

## 常见误区

1. **只配 liveness，不配 readiness**
   - 结果：服务不健康时仍可能接流量，报错放大。
2. **探针过于严格**
   - 结果：偶发抖动就被判失败，频繁重启或摘流。
3. **慢启动应用没配 startup**
   - 结果：启动期被 liveness 连续误杀。
4. **readiness 与真实可用条件不一致**
   - 结果：探针通过了，但业务仍不可用。

## 排查探针问题的命令

```bash
# 看探针失败事件
kubectl describe pod <pod-name>

# 看当前与上一轮日志（排查重启）
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# 看 Pod 是否被摘流（是否 Ready）
kubectl get pod <pod-name> -o wide
```

如果你看到反复 `Unhealthy`、`Back-off restarting failed container`，优先检查探针路径、端口、超时和阈值是否合理。

## 一套简单配置建议

- 对外服务：`readinessProbe` 必配。
- 可能假死：加 `livenessProbe`。
- 启动慢：加 `startupProbe`，并放宽启动窗口。
- 探针接口尽量轻量，不要做重查询。

只要这三类探针职责清晰，Pod 生命周期里的大部分“起不来、接错流量、反复重启”问题都能明显减少。
