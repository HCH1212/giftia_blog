---
title: 'Go合集'
date: 2026-09-07
author: "giftia"
description: ""
draft: false
categories: ["face"]
tags: []
---

## 协程 线程 进程的区别
- 进程：资源分配的基本单位，比如启动一个程序
- 线程：cpu 调度的基本单位，内核态
- 协程：用户态的轻量级线程

## make 和 new 的区别
- new 初始化任意数据类型并返回指针
- make 初始化 slice/channel/map，返回可用的数据结构本身

## slice 底层
- 指向底层数组，有长度和容量
- 扩容：cap<256 翻倍，cap>256 逐步增长到约 1.25 倍

## map 底层
- 2^B 个桶，每个桶 8 组 tophash、key、value
- 哈希冲突解决使用溢出桶
- 装载因子>6.5 或溢出桶过多触发扩容，分等量扩容和翻倍扩容，方式是渐进式哈希

## channel 底层
- 环形队列，分有缓存和无缓冲，有等待发送和等待接收队列
- 并发安全

## interface 底层
- iface：带方法的接口
- eface：空接口
