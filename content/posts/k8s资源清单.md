---
title: 'K8s资源清单'
date: 2026-06-01
author: "giftia"
description: "用最小例子理解 Kubernetes 资源清单（YAML）怎么写、怎么用。"
draft: false
categories: ["运维"]
tags: ["Kubernetes", "YAML", "Deployment", "Service"]
---

在 Kubernetes 里，**资源清单**就是一份 YAML 文件，用来描述“我希望集群里有什么资源、这些资源是什么配置”。

你不需要手工点点点创建服务，只要维护好清单文件，再执行：

```bash
kubectl apply -f xxx.yaml
```

就可以把“期望状态”交给集群。

## 资源清单的通用结构

一个清单通常长这样：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-web
  namespace: default
spec:
  replicas: 2
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

可以先记住这几个字段：

- `apiVersion`：资源属于哪个 API 版本。
- `kind`：资源类型，比如 `Deployment`、`Service`。
- `metadata`：资源名字、命名空间、标签等。
- `spec`：你真正关心的配置内容。
- `status`：系统回填的运行状态（通常不手写）。

## 常见资源清单一览

### 1. Pod

最小运行单元，适合临时测试，不建议直接长期维护裸 Pod。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: web
      image: nginx:1.27
      ports:
        - containerPort: 80
```

### 2. Deployment

最常用，负责副本管理、滚动发布、回滚。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      containers:
        - name: web
          image: nginx:1.27
```

### 3. Service

给一组 Pod 提供稳定访问入口。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-svc
spec:
  selector:
    app: demo
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

### 4. ConfigMap

放配置，不放敏感信息。

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  APP_ENV: "prod"
```

### 5. Secret

放敏感信息（数据库密码、token 等）。

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_USER: "root"
  DB_PASS: "123456"
```

## 一次性管理多个资源

实际项目里，经常把 Deployment 和 Service 放在一个文件里，用 `---` 分隔：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      containers:
        - name: web
          image: nginx:1.27
---
apiVersion: v1
kind: Service
metadata:
  name: demo
spec:
  selector:
    app: demo
  ports:
    - port: 80
      targetPort: 80
```

这样可以一条命令统一创建或更新。

## 最常用操作命令

```bash
# 创建或更新
kubectl apply -f app.yaml

# 查看资源
kubectl get deploy,po,svc

# 查看详情
kubectl describe deploy demo

# 删除资源
kubectl delete -f app.yaml
```

## `kubectl explain` 为什么很有用

写清单时，最常见的问题是：字段名记不住、字段层级写错、某个字段到底支不支持。

`kubectl explain` 就是官方“结构说明书”，可以直接在命令行查看资源字段和含义。

常见用法：

```bash
# 查看 Deployment 的顶层字段
kubectl explain deployment

# 查看 Deployment.spec
kubectl explain deployment.spec

# 继续深入看 Pod 模板
kubectl explain deployment.spec.template.spec

# 查看某个具体字段
kubectl explain deployment.spec.strategy

# 查看字段的详细描述（递归）
kubectl explain deployment.spec --recursive
```

一个简单的实践方式：

1. 先写一个最小 YAML。
2. 不确定字段时，用 `kubectl explain <资源>.<路径>` 查结构。
3. 写完后再 `kubectl apply -f`。

这样做的好处是：你不用频繁切网页查文档，写错字段的概率会明显降低。

## 写清单时的实用建议

1. 先从最小可用版本开始，再逐步加探针、资源限制等配置。
2. 业务资源尽量都打上统一标签（如 `app`、`env`），后续排查会轻松很多。
3. `spec.selector` 和 Pod 模板里的 `labels` 必须对应，不然 Service 找不到 Pod。
4. 配置和密钥分开：普通配置放 `ConfigMap`，敏感信息放 `Secret`。

你可以把资源清单理解成“基础设施代码”。写清楚它，集群就能按你的意思稳定地跑起来。
