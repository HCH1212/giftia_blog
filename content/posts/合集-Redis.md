---
title: 'Redis合集'
date: 2026-09-07
author: "giftia"
description: ""
draft: false
categories: ["face"]
tags: []
---

## 持久化策略
- RDB：快照备份，二进制，占用小恢复快，数据缺口大
- AOF：操作日志，纯文本易读，占用大恢复慢
- 一般定期 rdb，间隔 aof

## aof 重写
- 时机：aof 文件过大时
- 触发：手动或阈值自动或定时
- 规则：去掉无效命令，合并命令结果，比如 set 1，set 2... set 100，最后只留下 set 100

## 常见数据结构和使用场景


