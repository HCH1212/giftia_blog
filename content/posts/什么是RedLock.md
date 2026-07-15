---
title: '什么是RedLock'
date: 2026-01-05
author: "giftia"
description: "Redis 分布式锁 RedLock 算法的原理与注意事项"
draft: false
categories: ["数据库"]
tags: ["redis", "redlock", "distributed-lock"]
---

## 什么是 RedLock

RedLock 是 Redis 作者 Antirez 提出的分布式锁算法，使用多个独立 Redis 实例避免单点故障。

## 算法流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant R1 as Redis-1
    participant R2 as Redis-2
    participant R3 as Redis-3
    participant R4 as Redis-4
    participant R5 as Redis-5

    Note over C,R5: 加锁阶段
    par 并行请求
        C->>R1: SET lock uuid NX PX 10000
        R1-->>C: OK
    and
        C->>R2: SET lock uuid NX PX 10000
        R2-->>C: OK
    and
        C->>R3: SET lock uuid NX PX 10000
        R3-->>C: OK
    and
        C->>R4: SET lock uuid NX PX 10000
        R4-->>X: 超时
    and
        C->>R5: SET lock uuid NX PX 10000
        R5-->>C: OK
    end
    Note over C: 4/5 ≥ 3 (N/2+1) → 加锁成功<br/>有效时间 = 10s - 获取耗时

    Note over C,R5: 释放阶段
    C->>R1: DEL lock (Lua 校验 uuid)
    C->>R2: DEL lock
    C->>R3: DEL lock
    C->>R5: DEL lock
```

1. 客户端向 N 个 Redis 实例（建议 N=5）尝试获取锁，生成随机锁 ID 并使用 `SET key value NX PX timeout`
2. 设定锁过期时间，防止死锁
3. 在大多数实例（N/2+1）上成功获取锁，才算获取成功
4. 锁有效时间 = 原始过期时间 - 获取锁耗时
5. 释放锁时向所有实例发送释放命令

## 优点

- 容错性：部分实例不可用，只要满足多数规则仍可正常工作
- 无中心化：不依赖单个锁服务

## 注意事项

- 需要与多个 Redis 实例通信，延迟高于单实例锁
- 安全性部分依赖实例间时间同步，时钟偏差可能影响安全性

参考：<https://cloud.tencent.com/developer/article/2390644>
