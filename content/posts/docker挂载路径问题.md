---
title: 'docker挂载路径问题'
date: 2026-01-05
author: "giftia"
description: "Docker bind mount 基于 inode 的挂载原理及删除重建目录导致挂载失效的解决方案"
draft: false
categories: ["运维"]
tags: ["Docker", "Volume", "容器", "运维"]
---

## 问题背景

`docker-compose` 启动容器后，删除宿主机挂载目录再重建，容器内报找不到文件路径。

## 原因

Docker bind mount 基于 inode 建立映射。删除重建目录会改变 inode，容器仍引用旧 inode，挂载关系断裂。

## 解决方案

### 方案1：重启容器（推荐）

```bash
docker compose restart gamerobot
# 或彻底重建
docker compose down && docker compose up -d
```

### 方案2：避免删除目录

```bash
# 错误
rm -rf /data && mkdir /data && cp files/* /data/

# 正确：只更新内容
cp -rf new_files/* /data/
```

### 方案3：使用 rsync

```bash
rsync -av --delete source/ /data/
```

## 总结

Docker 容器运行时**避免删除挂载目录**，只更新文件内容。如必须删除，务必重启容器。
