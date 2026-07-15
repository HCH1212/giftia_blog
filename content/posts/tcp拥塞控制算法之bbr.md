---
title: 'TCP 拥塞控制算法之 BBR'
date: 2026-01-20
author: "giftia"
description: "TCP BBR 拥塞控制算法的原理、工作阶段及与 CUBIC 的性能对比"
draft: false
categories: ["网络"]
tags: ["tcp", "bbr", "congestion-control", "network"]
---

## CUBIC 算法

默认拥塞控制算法，基于丢包来调整窗口大小。

- **慢启动**：每收到 ACK，cwnd 指数增长（1→2→4→8→16...）
- **拥塞避免**：使用三次函数增长窗口：`W(t) = C × (t - K)³ + W_max`
- **快重传**：收到 3 个重复 ACK 立即重传
- **快恢复**：ssthresh = cwnd × 0.7，直接进入拥塞避免

## 切换为 BBR

```bash
# 加载 BBR 模块
sudo modprobe tcp_bbr

# 切换（临时，重启失效）
sudo sysctl -w net.core.default_qdisc=fq
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
```

## BBR 原理

不同于基于丢包的算法，BBR 主动测量网络状况。

两个核心指标：

- **BtlBw（瓶颈带宽）**：实测传输速率的最大值
- **RTprop（最小往返时延）**：实测 RTT 的最小值

最优发送窗口 = BtlBw × RTprop（BDP，带宽延迟积）。

### 四个阶段

BBR 状态机循环：STARTUP → DRAIN → PROBE_BW → PROBE_RTT → ...

以开车类比：

- **CUBIC**：踩油门 → 撞墙（丢包）→ 急刹车 → 再踩油门
- **BBR**：看速度表和路况 → 保持在限速下 → 偶尔试探能否更快

## 性能对比

在虚拟机中使用 iperf3 进行实测。

### 内网环境（无延迟/丢包）

| 算法 | 带宽 | 重传 |
|---|---|---|
| CUBIC | ~7.6 Gbps | 300-560 次 |
| BBR | ~3.4 Gbps | 0 次 |

> 低延迟下 CUBIC 更激进，带宽占优。

### 高延迟（150ms + 优化缓冲区）

| 算法 | 带宽 | 重传 |
|---|---|---|
| CUBIC | ~423 Mbps | 6000+ 次 |
| BBR | ~787 Mbps | 0 次 |

> 高延迟下 BBR 完胜，带宽近 CUBIC 的 2 倍且零重传。

### 高丢包（50ms + 3%丢包）

| 算法 | 带宽 | 重传 |
|---|---|---|
| CUBIC | ~1.3 Gbps | 5000-21000 次 |
| BBR | ~903 Mbps | 0-2 次 |

> BBR 虽带宽略低，但稳定性极佳。

### 延迟递增对比（缓冲区优化后）

| 延迟 | CUBIC | BBR |
|---|---|---|
| 50ms | ~940 Mbps | ~690 Mbps |
| 100ms | ~690 Mbps | ~746 Mbps |
| 150ms | ~525 Mbps | ~563 Mbps |
| 200ms | ~343 Mbps | ~861 Mbps |
| 300ms | ~288 Mbps | ~620 Mbps |

> 约 100ms 是临界点：延迟 >100ms 后 BBR 完胜，>200ms 时 CUBIC 接近崩溃。

## 总结

|  | CUBIC | BBR |
|---|---|---|
| 核心策略 | 基于丢包 | 主动测量带宽/RTT |
| 低延迟 | 带宽高但波动大 | 较保守 |
| 高延迟 | 性能急剧下降 | 极稳定，带宽远胜 CUBIC |
| 丢包容忍 | 差（丢包即降速） | 好（几乎不丢包） |
| 延迟抖动 | 不敏感 | **敏感（BBR 克星）** |
| 适用场景 | 数据中心内部 | 跨国通信、移动网络、直播 |

**关键结论**：延迟抖动是 BBR 的克星；>100ms 延迟或 >7% 丢包时 BBR 优势明显。
