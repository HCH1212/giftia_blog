---
title: 'sync.map'
date: 2026-01-05
author: "giftia"
description: "Go sync.Map 的读写分离原理、延迟写入机制及与手动加锁 map 的性能对比"
draft: false
categories: ["Go"]
tags: ["go", "sync-map", "concurrency"]
---

## 核心原理

```mermaid
flowchart TB
    subgraph 读路径["读路径 (Load)"]
        R1[读请求] --> R2{read 命中?}
        R2 -->|是| R3["返回 value (无锁)"]
        R2 -->|否| R4["查找 dirty (加锁)<br/>miss++"]
        R4 --> R5{miss 次数 ≥ dirty 长度?}
        R5 -->|是| R6["dirty 晋升为 read<br/>原 dirty 置 nil (O(1) 指针替换)"]
    end
    
    subgraph 写路径["写路径 (Store/Delete, 均加锁)"]
        W1[Store] --> W2{read 中有此 key?}
        W2 -->|是| W3["更新 read (atomic)"]
        W2 -->|否| W4{dirty 为 nil?}
        W4 -->|是| W5["遍历 read, 拷贝有效条目到 dirty"]
        W4 -->|否| W6["直接写入 dirty"]
        W5 --> W6
    end
```

sync.Map 适用于**读多写少**场景，通过读写分离提升性能：

- **读写分离**：内部维护只读字典（read）和读写字典（dirty）。读操作优先访问 read，miss 时才查 dirty。
- **延迟写入**：写操作只更新 dirty，不立即同步到 read。只有 misses 计数器超阈值时才将 dirty 同步到 read。
- **原子操作**：读操作大部分无锁（`atomic.Value`），写操作用 `sync.Mutex` 保护。

## vs 手动加锁 map

| 维度 | sync.Map | 手动加锁 map |
|---|---|---|
| 并发性能 | 读操作无锁，写操作延迟同步 | 读写互斥，高并发下性能差 |
| 适用场景 | 读多写少 | 读写均衡 |
| 实现复杂度 | 内置封装 | 自行管理锁 |

**结论**：读多写少场景用 sync.Map；简单场景手动加锁完全够用。
