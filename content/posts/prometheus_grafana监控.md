---
title: 'Prometheus_grafana监控'
date: 2026-01-03
lastmod: 2026-01-03
author: "giftia"
description: ""
draft: false
categories: ["技术"]
tags: []
---

这里的指标以进程导出的指标为例，环境是Linux
<https://github.com/ncabatoff/process-exporter>

## 一. 导出指标

1. 安装

```bash
wget https://github.com/ncabatoff/process-exporter/releases/download/v0.8.7/process-exporter-0.8.7.linux-amd64.tar.gz
tar xvfz process-exporter-0.8.7.linux-amd64.tar.gz
cd process-exporter-0.8.7.linux-amd64
./process-exporter --help
```

2. 编写配置文件*config.yaml*

*查看进程名*

```bash
ps -e -o comm
```

*配置文件里填需要监控的进程*

```yaml
process_names:
  # 监控所有 LovaniaServer 进程
  - name: "LovaniaServer"
    cmdline:
    - 'LovaniaServer'
```

3. 运行

```bash
./process-exporter --config.path=config.yaml
```

然后检查指标

```bash
curl http://localhost:9256/metrics
```

## 二. prometheus采集指标

1. 安装

```bash
wget https://github.com/prometheus/prometheus/releases/download/v3.5.0/prometheus-3.5.0.linux-amd64.tar.gz
tar xvf prometheus-3.5.0.linux-amd64.tar.gz
cd prometheus-3.5.0.linux-amd64
```

2. 编写配置文件*prometheus.yaml*

```yaml
global:
  scrape_interval: 15s

scrape_configs:
- job_name: node
  static_configs:
  - targets: ['localhost:9256']
```

3. 启动

```bash
./prometheus --config.file=./prometheus.yaml
```

4. 打开浏览器查看web：[http://localhost:9090/](https://link.zhihu.com/?target=http%3A//localhost%3A9090/)

在query栏中输入查询指标就可获取对应数据

## 三. [grafana](https://zhida.zhihu.com/search?content_id=265994044&content_type=Article&match_order=1&q=grafana&zhida_source=entity)可视化配置

1. 安装

```bash
# 下载 Grafana
wget https://dl.grafana.com/oss/release/grafana-12.2.1.linux-amd64.tar.gz
tar -zxvf grafana-12.2.1.linux-amd64.tar.gz
cd grafana-12.2.1

# 启动 Grafana
./bin/grafana-server
```

2. 访问

- 打开浏览器访问 [http://localhost:3000](https://link.zhihu.com/?target=http%3A//localhost%3A9090/)/
- 用户名：admin
- 密码：admin（首次登录会要求修改）

3. 添加prometheus数据源

- 点击左侧菜单的 Connections -> Data Sources -> Add data source -> Prometheus
- 配置数据源：
    - Name: Prometheus
    - URL: http://localhost:9090（如果 Grafana 和 Prometheus 在同一台机器）
- 点击底部的 "Save & Test"，看到绿色的 ✅ "Successfully queried the Prometheus API." 即成功

4. 仪表板配置

- 点击左侧菜单的 Dashboards
- 然后点击右上角 new -> import
- 输入id 249或715，这是为process-exporter配置好的（也可以自己写一个模板导入，详情问ai）
- 然后就能看到可视化的各项数据指标了
