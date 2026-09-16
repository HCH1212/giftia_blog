---
title: 'Mysql合集'
date: 2026-09-07
author: "giftia"
description: ""
draft: false
categories: ["face"]
tags: []
---

## 数据库三范式
- 第一范式：每列的原子性，每列字段不应该是可再分的
- 第二范式：1基础上，所有非主键依赖主键的全部字段（联合主键）
- 第三范式：2基础上，所有非主键必须直接依赖主键，不能间接依赖

## 行级锁（锁索引）
- 记录锁：锁单行
- 间隙锁：锁相邻的开区间
- 临键锁：记录锁+间隙锁，锁相邻的左开右闭

## redolog undolog binlog
如果有一个 insert 操作
1. 写内存 buffer pool
2. 写 undolog，记录反操作，如 delete，用于事务回滚和 mvcc 快照读
3. 写 redolog（prepare），用于 崩溃恢复
4. 写 binlog，记录逻辑变更，用于主从同步和数据恢复
5. 写 redolog（commit），说明事务成功提交

## 慢查询优化
1. 开启慢查询日志，然后找到慢的 sql
2. 使用 explain 分析 sql，下面是一些重点参数
- type：all/index 表示全表或全索引扫描
- key：索引，null 表示无索引
- rows：预计扫描行数
- extra：会有一些优化信号，如 filesort
3. 优化方式：加索引、回表操作尽量索引覆盖、优化 sql 等

