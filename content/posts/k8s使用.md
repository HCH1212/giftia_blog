---
title: "K8s基础使用"
date: 2026-03-03
lastmod: 2026-03-03
author: "giftia"
description: "Kubernetes 入门概念与常用 kubectl 命令示例。"
draft: false
categories: ["技术"]
tags: ["Kubernetes", "K8s", "容器"]
---

Kubernetes（简称 K8s）是一个开源的容器编排平台，主要用于自动化部署、弹性扩缩容和容器化应用管理。

## 基础概念

- Pod：K8s 中最小的调度单元。一个 Pod 通常运行一个容器，也可以运行一组紧密协作的容器。
- Deployment：用于管理 Pod 副本和版本，支持滚动更新与回滚。
- Service：为一组 Pod 提供稳定访问入口。由于 Pod IP 会变化，Service 可以提供固定地址并做负载均衡。
- Namespace：逻辑隔离机制，用于在同一集群中划分开发、测试、生产等环境。

## 操作流程

1. 编写 YAML 配置文件 `nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-home
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

2. 提交到集群

```bash
kubectl apply -f nginx-deployment.yaml
```

3. 查看状态

```bash
kubectl get pods
kubectl get deployments
```

## 常用命令

1. 查询资源

```bash
kubectl get pods,svc,nodes
```

2. 查看详情

```bash
kubectl describe pod <pod-name>
```

3. 查看日志

```bash
kubectl logs -f <pod-name>
```

4. 进入容器

```bash
kubectl exec -it <pod-name> -- sh
```

5. 调整副本数

```bash
kubectl scale deployment <name> --replicas=5
```

6. 删除资源

```bash
kubectl delete -f <file.yaml>
```
