---
title: 'acid 脏读、幻读、不可重复读 事务隔离级别'
date: 2026-01-05
author: "giftia"
description: "数据库ACID特性、脏读/幻读/不可重复读问题及MySQL事务隔离级别详解"
draft: false
categories: ["数据库"]
tags: ["MySQL", "事务", "ACID", "隔离级别"]
---

## ACID

- **原子性（Atomicity）**：事务不可分割，操作要么全部成功，要么全部失败
- **一致性（Consistency）**：事务前后数据库保持一致状态
- **隔离性（Isolation）**：并发事务互不干扰
- **持久性（Durability）**：事务提交后数据永久保存

## 脏读（假数据）
一个事务读取到了其他事务未提交的数据。

## 不可重复读（变数据）
同一事务中多次读取同一数据，前后读取的结果不同。（事务2执行update 数据变化）

## 幻读（新数据）
同一事务中多次查询同一范围的数据，前后查询结果数量不同。（事务2执行insert/delete 数据量变化）

## 事务隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---|---|---|---|
| READ UNCOMMITTED | √ | √ | √ |
| READ COMMITTED | × | √ | √ |
| REPEATABLE READ（MySQL 默认） | × | × | √（InnoDB 可避免） |
| SERIALIZABLE | × | × | × |

> InnoDB 在 RR 级别下可以避免幻读，但快照读与当前读混用时仍可能出现幻读。

```sql
-- 查看隔离级别（MySQL 8.0+）
SELECT @@transaction_isolation;

-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ-COMMITTED;
```
