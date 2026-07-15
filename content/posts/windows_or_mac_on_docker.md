---
title: 'Docker 运行 Windows/Mac 虚拟机'
date: 2026-01-05
author: "giftia"
description: "在 Docker 中运行 Windows/Mac 虚拟机的轻量方案"
draft: false
categories: ["运维"]
tags: ["docker", "virtualization", "windows", "linux"]
---

## 如何在 Linux 上运行 Windows 虚拟机

相比 VMware 的繁琐安装，使用 Docker 更轻便。

前提：Docker 已安装。

### 步骤

```shell
# 1. 拉取镜像
docker pull dockurr/windows

# 2. 编写 docker-compose.yaml
```

```yaml
services:
  windows:
    image: dockurr/windows
    container_name: windows
    environment:
      VERSION: "11"
      RAM_SIZE: "8G"
      CPU_CORES: "8"
    devices:
      - /dev/kvm
      - /dev/net/tun
    cap_add:
      - NET_ADMIN
    ports:
      - 8006:8006
      - 3389:3389/tcp
      - 3389:3389/udp
    volumes:
      - ./windows:/storage
    restart: always
    stop_grace_period: 2m
```

```shell
# 3. 启动
docker compose up -d

# 4. 访问 http://127.0.0.1:8006，首次等待 Windows 安装

# 5. 关闭
docker compose down
```

也有 Mac 版本：[dockur/macos](https://github.com/dockur/macos)

GitHub：<https://github.com/dockur/windows>
