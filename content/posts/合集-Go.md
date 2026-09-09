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
