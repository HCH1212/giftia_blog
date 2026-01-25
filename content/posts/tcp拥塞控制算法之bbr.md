---
title: 'Tcp拥塞控制算法之bbr'
date: 2026-01-20
lastmod: 2026-01-20
author: "giftia"
description: ""
draft: false
categories: ["网络"]
tags: []
---

## 一. 环境

1. vmware虚拟机
2. iso镜像：ubuntu-22.04.5-live-server-amd64.iso
3. 配置：2核4G

## 二. 默认算法

### 1. 查看当前的拥塞控制算法

```bash
$ sysctl net.ipv4.tcp_congestion_control
> net.ipv4.tcp_congestion_control = cubic
```

可见，默认的算法是cubic

### 2. cubic算法

主要是通过丢包来调整窗口的的大小，控制传输速率

a. 慢启动

每收到一个ack，拥塞窗口（cwnd）就指数增长

cwnd：1-2-4-8-16-32...

b. 拥塞避免

cubic的核心部分，使用三次函数来增长窗口（reno这里是线性增长）

```plain
W(t) = C × (t - K)³ + W_max
```

c. 快重传

收到三个重复ack，立即重传丢失的包，不等待超时

d. 快恢复

快重传后，ssthresh=cwnd*β（一般是0.7）, cwnd=ssthresh，然后直接进入拥塞避免阶段（跳过慢启动）

## 三. 切换为bbr

### 1. 查看当前支持的拥塞控制算法

```bash
$ sysctl net.ipv4.tcp_available_congestion_control
> net.ipv4.tcp_available_congestion_control = reno cubic
```

发现并没有bbr，难道是不支持吗

查看一下内核版本

```bash
$ uname -r
> 5.15.0-119-generic
```

内核版本>4.9就支持bbr，所以需要我们手动加载bbr模块

```bash
$ sudo modprobe tcp_bbr
```

再次查看

```bash
$ sysctl net.ipv4.tcp_available_congestion_control
> net.ipv4.tcp_available_congestion_control = reno cubic bbr
```

### 2. 切换为bbr算法

我这里使用临时切换（重启后失效）

```bash
$ sudo sysctl -w net.core.default_qdisc=fq
$ sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
> net.core.default_qdisc = fq
> net.ipv4.tcp_congestion_control = bbr
```

再检查一下是否切换

```bash
$ sysctl net.ipv4.tcp_congestion_control
> net.ipv4.tcp_congestion_control = bbr
```

## 四. bbr

bbr不同于传统的拥塞控制算法，它并不是通过丢包来判断是否需要改动窗口，而是会主动去测量网络状况

### 1. 两个指标

BtlBw (Bottleneck Bandwidth)- 瓶颈带宽

```plain
发送数据包 → 测量实际传输速率 → 记录最大值
```

RTprop (Round-trip propagation time)- 最小往返时延

```plain
发送数据包 → 测量往返时间 → 记录最小值
```

## 2. 计算最优发送速率

```plain
最优发送窗口 = BtlBw × RTprop
```

这就是带宽延迟积（BDP），是理论上的最佳值

### 3. 不同的四个阶段

![img](/other/bbr.png)

### 4. 对比

通俗的说，以开车为示例

a. cubic

```plain
踩油门 → 撞墙(丢包) → 急刹车 → 再踩油门 → 又撞墙
```

b. bbr

```plain
看速度表和路况 → 保持在限速以下 → 偶尔试探一下能不能更快
```

## 五. 性能对比

两台虚拟机，分别是发起方和接受方（后面叫做服务器 客户端）

### 1. 服务端配置

1.1 安装iperf3

```bash
$ sudo apt update
$ sudo apt install -y iperf3
```

1.2 启动iperf3服务器（保持启动）

```bash
$ iperf3 -s
> 
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```

1.3 查看服务器ip

```bash
$ ip addr
> 192.168.226.130
```

### 2. 客户端配置

2.1 安装工具

```bash
$ sudo apt update
$ sudo apt install -y iperf3
```

2.2 测试连通性

```bash
$ ping 192.168.226.130 -c 4
> 
PING 192.168.226.130 (192.168.226.130) 56(84) bytes of data.
64 bytes from 192.168.226.130: icmp_seq=1 ttl=64 time=0.512 ms
64 bytes from 192.168.226.130: icmp_seq=2 ttl=64 time=0.295 ms
64 bytes from 192.168.226.130: icmp_seq=3 ttl=64 time=0.250 ms
64 bytes from 192.168.226.130: icmp_seq=4 ttl=64 time=0.317 ms

--- 192.168.226.130 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3074ms
rtt min/avg/max/mdev = 0.250/0.343/0.512/0.100 ms
```

### 3. 创建测试脚本

3.1 创建文件（vim可替换为自己熟悉的）

```bash
$ vim bbr_test.sh
```

3.2 粘贴脚本（ai写的，可根据需求灵活更改）

```bash
#!/bin/bash

# ========================================
# CUBIC vs BBR 性能对比测试脚本
# ========================================

# 配置参数
SERVER_IP="192.168.226.130"  # ⚠️ 修改为你的服务器IP
TEST_DURATION=30            # 每次测试持续时间（秒）
TEST_ROUNDS=3               # 每个算法测试次数

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 结果目录
RESULT_DIR="test_results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULT_DIR"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}       CUBIC vs BBR 性能对比测试${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "服务器地址: $SERVER_IP"
echo "测试时长: ${TEST_DURATION}秒"
echo "测试轮数: ${TEST_ROUNDS}次"
echo "结果目录: $RESULT_DIR"
echo ""

# 检查服务器连通性
echo -e "${YELLOW}检查服务器连通性...${NC}"
if ! ping -c 2 $SERVER_IP >/dev/null 2>&1; then
    echo -e "${RED}错误: 无法连接到服务器 $SERVER_IP${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 服务器连通正常${NC}"
echo ""

# 检查BBR模块
echo -e "${YELLOW}检查BBR模块...${NC}"
if ! lsmod | grep -q tcp_bbr; then
    echo "加载BBR模块..."
    sudo modprobe tcp_bbr
fi
echo -e "${GREEN}✓ BBR模块已加载${NC}"
echo ""

# 函数：执行单次测试
run_single_test() {
    local algo=$1
    local round=$2
    local output_file="$RESULT_DIR/${algo}_round${round}.txt"
    
    echo -e "${BLUE}► [$algo] 第 $round 轮测试中...${NC}"
    
    # 切换算法
    sudo sysctl -w net.ipv4.tcp_congestion_control=$algo >/dev/null 2>&1
    sleep 1
    
    # 运行iperf3测试
    iperf3 -c $SERVER_IP -t $TEST_DURATION -C $algo > "$output_file" 2>&1
    
    # 提取关键数据
    local bandwidth=$(grep "receiver" "$output_file" | awk '{print $(NF-2), $(NF-1)}')
    local retrans=$(grep "sender" "$output_file" | awk '{print $(NF-1)}')
    local retrans=${retrans:-0}
    
    echo -e "  带宽: ${GREEN}$bandwidth${NC}"
    echo -e "  重传: ${YELLOW}${retrans}${NC}"
    echo ""
    
    # 保存到汇总文件
    echo "$algo,$round,$bandwidth,$retrans" >> "$RESULT_DIR/raw_data.csv"
    
    sleep 3
}

# 函数：测试指定算法
test_algorithm() {
    local algo=$1
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  测试算法: $algo${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    for i in $(seq 1 $TEST_ROUNDS); do
        run_single_test $algo $i
    done
}

# 初始化CSV文件
echo "算法,轮次,带宽,单位,重传次数" > "$RESULT_DIR/raw_data.csv"

# 开始测试
echo -e "${YELLOW}开始测试...${NC}"
echo ""

# 测试CUBIC
test_algorithm "cubic"

# 测试BBR
test_algorithm "bbr"

# 生成测试报告
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}            测试完成！${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 计算平均值
echo -e "${BLUE}正在生成报告...${NC}"

cat > "$RESULT_DIR/summary.txt" << EOF
===== CUBIC vs BBR 性能对比报告 =====
测试时间: $(date)
服务器: $SERVER_IP
测试时长: ${TEST_DURATION}秒/轮
测试轮数: ${TEST_ROUNDS}轮

----- CUBIC 测试结果 -----
EOF

grep "cubic" "$RESULT_DIR/raw_data.csv" | while IFS=',' read algo round bw unit retrans; do
    echo "  第${round}轮: ${bw} ${unit}, 重传: ${retrans}" >> "$RESULT_DIR/summary.txt"
done

cat >> "$RESULT_DIR/summary.txt" << EOF

----- BBR 测试结果 -----
EOF

grep "bbr" "$RESULT_DIR/raw_data.csv" | while IFS=',' read algo round bw unit retrans; do
    echo "  第${round}轮: ${bw} ${unit}, 重传: ${retrans}" >> "$RESULT_DIR/summary.txt"
done

echo "" >> "$RESULT_DIR/summary.txt"
echo "详细数据请查看: $RESULT_DIR/" >> "$RESULT_DIR/summary.txt"

# 显示报告
cat "$RESULT_DIR/summary.txt"

echo ""
echo -e "${GREEN}✓ 所有测试结果已保存到: $RESULT_DIR/${NC}"
echo ""
echo -e "${YELLOW}查看详细数据:${NC}"
echo "  cat $RESULT_DIR/summary.txt"
echo "  cat $RESULT_DIR/raw_data.csv"
```

3.3 添加执行权限

```bash
$ chmod +x bbr_test.sh
```

### 4. 执行第一轮测试

4.1 运行脚本

```bash
$ sh ./bbr_test.sh
```

4.2 测试输出

```bash
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_090605

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 8.20 Gbits/sec
-e   重传: 559

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 7.48 Gbits/sec
-e   重传: 296

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 7.21 Gbits/sec
-e   重传: 294

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 3.51 Gbits/sec
-e   重传: 0

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 3.35 Gbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 3.31 Gbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 09:09:31 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 8.20 Gbits/sec 559, 重传: 
  第2轮: 7.48 Gbits/sec 296, 重传: 
  第3轮: 7.21 Gbits/sec 294, 重传: 

----- BBR 测试结果 -----
  第1轮: 3.51 Gbits/sec 0, 重传: 
  第2轮: 3.35 Gbits/sec 0, 重传: 
  第3轮: 3.31 Gbits/sec 0, 重传: 

详细数据请查看: test_results_20251031_090605/

-e ✓ 所有测试结果已保存到: test_results_20251031_090605/

-e 查看详细数据:
  cat test_results_20251031_090605/summary.txt
  cat test_results_20251031_090605/raw_data.csv
```

4.3 结果分析

这里我测试了多次，就不粘贴上来了（后续结果都是如此）

除了个别测试，差别都不大，可见cubic的带宽明显优于bbr，但是bbr不会丢包且较稳定

第一轮可以算cubic胜利，但是注意现在是内网环境，并启没有配置延迟和丢包率

接下来我们继续测试

### 5. 第二轮测试（高延迟）

5.1 服务端配置：150ms + 0.5%丢包

```bash
$ sudo tc qdisc add dev ens33 root netem delay 150ms loss 0.5%
```

5.2 验证是否生效

```bash
$ sudo tc qdisc show dev ens33
> qdisc netem 8001: root refcnt 2 limit 1000 delay 150ms loss 0.5%
```

5.3 启动服务端监听

```bash
$ iperf3 -s
```

5.4 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

5.5 结果输出（这里的重传次数不对，一开始脚本写错了，请自己再测试一下）

```plain
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_070346

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 150 Mbits/sec
-e   重传: 0

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 151 Mbits/sec
-e   重传: 0

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 151 Mbits/sec
-e   重传: 0

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 151 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 151 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 149 Mbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 07:07:22 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 150 Mbits/sec , 重传: 
  第2轮: 151 Mbits/sec , 重传: 
  第3轮: 151 Mbits/sec , 重传: 

----- BBR 测试结果 -----
  第1轮: 151 Mbits/sec , 重传: 
  第2轮: 151 Mbits/sec , 重传: 
  第3轮: 149 Mbits/sec , 重传: 

详细数据请查看: test_results_20251031_070346/

-e ✓ 所有测试结果已保存到: test_results_20251031_070346/

-e 查看详细数据:
  cat test_results_20251031_070346/summary.txt
  cat test_results_20251031_070346/raw_data.csv
```

5.6 结果分析

cubic和bbr都稳定在150左右的带宽，这是一个奇怪的数据，首先想到的就是带宽达到了一个上限，所以我们需要找到原因并调整上限

5.7 查找原因

检查虚拟机带宽上限（不是这个原因）

```bash
$ ethtool ens33 | grep -i speed
> Speed: 1000Mb/s
```

检查tcp缓冲区配置（原因就在这里）

```bash
echo "当前配置:"
echo "  rmem_max: $(sysctl -n net.core.rmem_max | numfmt --to=iec)"
echo "  wmem_max: $(sysctl -n net.core.wmem_max | numfmt --to=iec)"
echo ""
sysctl net.ipv4.tcp_rmem
sysctl net.ipv4.tcp_wmem
echo ""
echo "150ms延迟下达到1Gbps需要:"
echo "  BDP = 1 Gbps × 0.3s = 37.5 MB"
echo ""
if [ $(sysctl -n net.core.rmem_max) -lt 37500000 ]; then
    echo "⚠️  缓冲区不足！这就是被限制在150Mbps的原因"
else
    echo "✓ 缓冲区足够"
fi
```

问题分析

```plain
当前TCP缓冲区上限:
  rmem_max: 208 KB  (接收)
  wmem_max: 208 KB  (发送)
  tcp_rmem最大: 6 MB
  tcp_wmem最大: 4 MB

实际限制:
  rmem_max和wmem_max是硬上限！
  即使tcp_rmem设置了6MB，也会被208KB限制住
  
在150ms延迟下:
  需要: 37.5 MB
  实际: 6 MB (被208KB限制后可能更小)
  理论带宽 = 6 MB / 0.3s ≈ 20 MB/s = 160 Mbps
  
这就是150 Mbps瓶颈
```

5.8 优化两台虚拟机的tcp缓存区上限

```bash
# ============================================
# TCP缓冲区优化（临时生效）
# ============================================

echo "优化TCP缓冲区..."

# 1. 增大缓冲区硬上限到64MB
sudo sysctl -w net.core.rmem_max=67108864
sudo sysctl -w net.core.wmem_max=67108864

# 2. 增大TCP缓冲区到64MB
sudo sysctl -w net.ipv4.tcp_rmem="4096 131072 67108864"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 67108864"

# 3. 确保窗口缩放启用
sudo sysctl -w net.ipv4.tcp_window_scaling=1

# 4. 验证配置
echo ""
echo "=== 优化后的配置 ==="
echo "接收缓冲最大值: $(sysctl -n net.core.rmem_max | numfmt --to=iec)"
echo "发送缓冲最大值: $(sysctl -n net.core.wmem_max | numfmt --to=iec)"
sysctl net.ipv4.tcp_rmem
sysctl net.ipv4.tcp_wmem
echo ""
echo "✓ 优化完成！现在缓冲区支持高延迟下的高速传输"
```

5.9 重启服务端iperf3

```bash
$ killall iperf3
$ iperf3 -s
```

5.9 客户端再次运行测试脚本

```bash
$ sh ./bbr_test.sh
```

5.10 结果输出

```plain
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_091141

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 563 Mbits/sec
-e   重传: 14632

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 333 Mbits/sec
-e   重传: 1090

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 374 Mbits/sec
-e   重传: 2544

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 866 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 737 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 758 Mbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 09:15:16 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 563 Mbits/sec 14632, 重传: 
  第2轮: 333 Mbits/sec 1090, 重传: 
  第3轮: 374 Mbits/sec 2544, 重传: 

----- BBR 测试结果 -----
  第1轮: 866 Mbits/sec 0, 重传: 
  第2轮: 737 Mbits/sec 0, 重传: 
  第3轮: 758 Mbits/sec 0, 重传: 

详细数据请查看: test_results_20251031_091141/

-e ✓ 所有测试结果已保存到: test_results_20251031_091141/

-e 查看详细数据:
  cat test_results_20251031_091141/summary.txt
  cat test_results_20251031_091141/raw_data.csv
```

5.11 结果分析

现在结果就很明显了，高延迟下bbr完胜

在高延迟网络下，bbr不仅稳定无丢包，而且带宽也接近cubic的两倍

### 6. 第三轮测试（高丢包）

6.1 服务端配置：50ms延迟 + 20ms抖动 + 3%丢包

```bash
$ sudo tc qdisc del dev ens33 root # 先删除现有规则
$ sudo tc qdisc add dev ens33 root netem delay 50ms 20ms loss 3%
```

6.2 验证是否生效

```bash
$ sudo tc qdisc show dev ens33
> qdisc netem 8002: root refcnt 2 limit 1000 delay 50ms  20ms loss 3%
```

6.3 启动服务端监听

```bash
$ iperf3 -s
```

6.4 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

6.5 结果输出

```plain
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_094524

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 1.16 Gbits/sec
-e   重传: 5196

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 1.23 Gbits/sec
-e   重传: 21015

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 1.45 Gbits/sec
-e   重传: 4591

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 342 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 240 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 354 Mbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 09:48:53 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 1.16 Gbits/sec 5196, 重传: 
  第2轮: 1.23 Gbits/sec 21015, 重传: 
  第3轮: 1.45 Gbits/sec 4591, 重传: 

----- BBR 测试结果 -----
  第1轮: 342 Mbits/sec 0, 重传: 
  第2轮: 240 Mbits/sec 0, 重传: 
  第3轮: 354 Mbits/sec 0, 重传: 

详细数据请查看: test_results_20251031_094524/

-e ✓ 所有测试结果已保存到: test_results_20251031_094524/

-e 查看详细数据:
  cat test_results_20251031_094524/summary.txt
  cat test_results_20251031_094524/raw_data.csv
```

6.7 结果分析

bbr虽然没有重传，但是带宽却比cubic低很多

是不是感觉又有点奇怪，再来找找原因

*了解bbr原理便能分析出原因：20ms抖动对bbr影响大，去掉20ms抖动试试*


6.8 服务器重新配置并启动：50ms延迟 + 3%丢包

```bash
$ sudo tc qdisc del dev ens33 root
$ sudo tc qdisc add dev ens33 root netem delay 50ms loss 3%
$ iperf3 -s
```

6.9 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

6.10 脚本输出

```plain
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_100113

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 1.04 Gbits/sec
-e   重传: 1877

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 1.05 Gbits/sec
-e   重传: 2788

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 1.71 Gbits/sec
-e   重传: 6424

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 893 Mbits/sec
-e   重传: 1172

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 948 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 867 Mbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 10:04:42 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 1.04 Gbits/sec 1877, 重传: 
  第2轮: 1.05 Gbits/sec 2788, 重传: 
  第3轮: 1.71 Gbits/sec 6424, 重传: 

----- BBR 测试结果 -----
  第1轮: 893 Mbits/sec 1172, 重传: 
  第2轮: 948 Mbits/sec 0, 重传: 
  第3轮: 867 Mbits/sec 0, 重传: 

详细数据请查看: test_results_20251031_100113/

-e ✓ 所有测试结果已保存到: test_results_20251031_100113/

-e 查看详细数据:
  cat test_results_20251031_100113/summary.txt
  cat test_results_20251031_100113/raw_data.csv
```

6.11 结果分析

去掉抖动后bbr带宽翻倍并启非常稳定，丢包也很少

但是cubic带宽略胜一筹，所以说cubic比较激进

记住一句话：**延迟抖动是BBR的克星！**

### 7. 第四轮测试（高延迟+高丢包+带宽限制）

7.1 服务端配置：100ms延迟 + 5%丢包 + 限制带宽到100Mbps

```bash
$ sudo tc qdisc del dev ens33 root
$ sudo tc qdisc add dev ens33 root netem delay 100ms loss 5% rate 100mbit
```

7.2 验证是否生效

```bash
$ sudo tc qdisc show dev ens33
> qdisc netem 8006: root refcnt 2 limit 1000 delay 100ms loss 5% rate 100Mbit
```

7.3 启动服务端监听

```bash
$ iperf3 -s
```

7.4 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

7.5 结果输出

```plain
-e ================================================
-e        CUBIC vs BBR 性能对比测试
-e ================================================

服务器地址: 192.168.226.130
测试时长: 30秒
测试轮数: 3次
结果目录: test_results_20251031_101021

-e 检查服务器连通性...
-e ✓ 服务器连通正常

-e 检查BBR模块...
-e ✓ BBR模块已加载

-e 开始测试...

-e ========================================
-e   测试算法: cubic
-e ========================================

-e ► [cubic] 第 1 轮测试中...
-e   带宽: 731 Mbits/sec
-e   重传: 27864

-e ► [cubic] 第 2 轮测试中...
-e   带宽: 518 Mbits/sec
-e   重传: 9024

-e ► [cubic] 第 3 轮测试中...
-e   带宽: 461 Mbits/sec
-e   重传: 693

-e ========================================
-e   测试算法: bbr
-e ========================================

-e ► [bbr] 第 1 轮测试中...
-e   带宽: 681 Mbits/sec
-e   重传: 1

-e ► [bbr] 第 2 轮测试中...
-e   带宽: 643 Mbits/sec
-e   重传: 0

-e ► [bbr] 第 3 轮测试中...
-e   带宽: 649 Mbits/sec
-e   重传: 0

-e ================================================
-e             测试完成！
-e ================================================

-e 正在生成报告...
===== CUBIC vs BBR 性能对比报告 =====
测试时间: Fri Oct 31 10:13:56 AM UTC 2025
服务器: 192.168.226.130
测试时长: 30秒/轮
测试轮数: 3轮

----- CUBIC 测试结果 -----
  第1轮: 731 Mbits/sec 27864, 重传: 
  第2轮: 518 Mbits/sec 9024, 重传: 
  第3轮: 461 Mbits/sec 693, 重传: 

----- BBR 测试结果 -----
  第1轮: 681 Mbits/sec 1, 重传: 
  第2轮: 643 Mbits/sec 0, 重传: 
  第3轮: 649 Mbits/sec 0, 重传: 

详细数据请查看: test_results_20251031_101021/

-e ✓ 所有测试结果已保存到: test_results_20251031_101021/

-e 查看详细数据:
  cat test_results_20251031_101021/summary.txt
  cat test_results_20251031_101021/raw_data.csv
```

7.6 分析结果

完美体现了bbr的优势，稳定性十分惊人，丢包基本对bbr没有影响

### 8. 第五轮测试（丢包率渐增的对比）(这里就不详细写，相信大家已经熟悉测试流程了)

8.1 服务端配置：丢包3% 5% 7% 10% 15%...

```bash
$ sudo tc qdisc del dev ens33 root
$ sudo tc qdisc add dev ens33 root netem loss 3% # 5% 7% 10% 15%...
```

8.2 启动服务端监听

```bash
$ iperf3 -s
```

8.3 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

8.4 结果输出

```plain
%3:
----- CUBIC 测试结果 -----
  第1轮: 7.48 Gbits/sec 589, 重传: 
  第2轮: 7.48 Gbits/sec 388, 重传: 
  第3轮: 7.40 Gbits/sec 354, 重传: 

----- BBR 测试结果 -----
  第1轮: 3.40 Gbits/sec 0, 重传: 
  第2轮: 3.62 Gbits/sec 1, 重传: 
  第3轮: 3.04 Gbits/sec 0, 重传: 

%5:
----- CUBIC 测试结果 -----
  第1轮: 7.58 Gbits/sec 403, 重传: 
  第2轮: 7.52 Gbits/sec 391, 重传: 
  第3轮: 7.56 Gbits/sec 432, 重传: 

----- BBR 测试结果 -----
  第1轮: 3.38 Gbits/sec 0, 重传: 
  第2轮: 3.47 Gbits/sec 0, 重传: 
  第3轮: 3.47 Gbits/sec 1, 重传: 

%7:
----- CUBIC 测试结果 -----
  第1轮: 7.24 Gbits/sec 506, 重传: 
  第2轮: 7.78 Gbits/sec 350, 重传: 
  第3轮: 7.55 Gbits/sec 501, 重传: 

----- BBR 测试结果 -----
  第1轮: 3.02 Gbits/sec 0, 重传: 
  第2轮: 3.08 Gbits/sec 1, 重传: 
  第3轮: 3.12 Gbits/sec 1, 重传:

%10:
----- CUBIC 测试结果 -----
  第1轮: 7.47 Gbits/sec 441, 重传: 
  第2轮: 7.78 Gbits/sec 523, 重传: 
  第3轮: 7.42 Gbits/sec 446, 重传: 

----- BBR 测试结果 -----
  第1轮: 2.90 Gbits/sec 1, 重传: 
  第2轮: 2.62 Gbits/sec 2, 重传: 
  第3轮: 2.60 Gbits/sec 3, 重传: 

%15:
----- CUBIC 测试结果 -----
  第1轮: 7.46 Gbits/sec 361, 重传: 
  第2轮: 7.50 Gbits/sec 420, 重传: 
  第3轮: 7.86 Gbits/sec 414, 重传: 

----- BBR 测试结果 -----
  第1轮: 2.65 Gbits/sec 3, 重传: 
  第2轮: 2.54 Gbits/sec 5, 重传: 
  第3轮: 2.64 Gbits/sec 0, 重传:
```

8.5 分析结果

低延迟环境下，丢包率不是关键因素

CUBIC保持2倍以上优势，且随丢包率增加优势扩大

### 9. 第六轮测试（延迟渐增的对比）

9.1 服务端配置：延迟50ms 100ms 150ms 200ms 300ms...

```bash
$ sudo tc qdisc del dev ens33 root
$ sudo tc qdisc add dev ens33 root netem delay 50ms
```

9.2 启动服务端监听

```bash
$ iperf3 -s
```

9.3 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

9.4 结果输出

```plain
50ms 
----- CUBIC 测试结果 -----
  第1轮: 1.10 Gbits/sec 50, 重传: 
  第2轮: 823 Mbits/sec 3178, 重传: 
  第3轮: 893 Mbits/sec 1466, 重传: 

----- BBR 测试结果 -----
  第1轮: 589 Mbits/sec 0, 重传: 
  第2轮: 805 Mbits/sec 0, 重传: 
  第3轮: 676 Mbits/sec 0, 重传:

100ms 
----- CUBIC 测试结果 -----
  第1轮: 785 Mbits/sec 3490, 重传: 
  第2轮: 799 Mbits/sec 2170, 重传: 
  第3轮: 490 Mbits/sec 1238, 重传: 

----- BBR 测试结果 -----
  第1轮: 684 Mbits/sec 0, 重传: 
  第2轮: 817 Mbits/sec 0, 重传: 
  第3轮: 738 Mbits/sec 0, 重传:

150ms 
----- CUBIC 测试结果 -----
  第1轮: 469 Mbits/sec 2650, 重传: 
  第2轮: 690 Mbits/sec 8, 重传: 
  第3轮: 417 Mbits/sec 758, 重传: 

----- BBR 测试结果 -----
  第1轮: 575 Mbits/sec 0, 重传: 
  第2轮: 586 Mbits/sec 0, 重传: 
  第3轮: 528 Mbits/sec 0, 重传:

200ms 
----- CUBIC 测试结果 -----
  第1轮: 274 Mbits/sec 3070, 重传: 
  第2轮: 358 Mbits/sec 1752, 重传: 
  第3轮: 396 Mbits/sec 16993, 重传: 

----- BBR 测试结果 -----
  第1轮: 872 Mbits/sec 0, 重传: 
  第2轮: 863 Mbits/sec 0, 重传: 
  第3轮: 849 Mbits/sec 0, 重传:

300ms
----- CUBIC 测试结果 -----
  第1轮: 336 Mbits/sec 7019, 重传: 
  第2轮: 362 Mbits/sec 729, 重传: 
  第3轮: 166 Mbits/sec 5207, 重传: 

----- BBR 测试结果 -----
  第1轮: 608 Mbits/sec 0, 重传: 
  第2轮: 656 Mbits/sec 0, 重传: 
  第3轮: 597 Mbits/sec 0, 重传:
```

9.5 分析结果

延迟是决定性因素

\- ≤80ms: CUBIC胜

\- >80ms: BBR完胜

\- ≥200ms: BBR优势达到2.5倍，CUBIC接近崩溃

### 10. 第七轮测试（互联网延迟下丢包率渐增的对比）

10.1 服务端配置：丢包3% 7% 15%... 延迟 50ms

```bash
$ sudo tc qdisc del dev ens33 root
$ sudo tc qdisc add dev ens33 root netem loss 3% delay 50ms
```

10.2 启动服务端监听

```bash
$ iperf3 -s
```

10.3 客户端运行测试脚本

```bash
$ sh ./bbr_test.sh
```

10.4 结果输出

```plain
%3
----- CUBIC 测试结果 -----
  第1轮: 1.28 Gbits/sec 2131, 重传: 
  第2轮: 1.03 Gbits/sec 1148, 重传: 
  第3轮: 990 Mbits/sec 2791, 重传: 

----- BBR 测试结果 -----
  第1轮: 826 Mbits/sec 0, 重传: 
  第2轮: 917 Mbits/sec 0, 重传: 
  第3轮: 830 Mbits/sec 0, 重传:

%7
----- CUBIC 测试结果 -----
  第1轮: 883 Mbits/sec 5279, 重传: 
  第2轮: 1.23 Gbits/sec 1297, 重传: 
  第3轮: 1.12 Gbits/sec 1780, 重传: 

----- BBR 测试结果 -----
  第1轮: 848 Mbits/sec 0, 重传: 
  第2轮: 817 Mbits/sec 0, 重传: 
  第3轮: 859 Mbits/sec 2082, 重传: 

%15
----- CUBIC 测试结果 -----
  第1轮: 821 Mbits/sec 1674, 重传: 
  第2轮: 734 Mbits/sec 2454, 重传: 
  第3轮: 708 Mbits/sec 1567, 重传: 

----- BBR 测试结果 -----
  第1轮: 781 Mbits/sec 0, 重传: 
  第2轮: 827 Mbits/sec 0, 重传: 
  第3轮: 818 Mbits/sec 1, 重传:
```

10.5 分析结果

50ms延迟环境下，15%是CUBIC的崩溃点

\- ≤7%丢包: CUBIC快28%，但不稳定

\- 15%丢包: BBR逆转，快7%且极稳定

\- 实际应用: BBR体验更好（稳定+低重传）

## 六. 总结

1. cubic

```plain
优势：
✓ 低延迟环境性能优异（可达8 Gbps+）
✓ 激进策略，充分利用带宽
✓ 实现简单，计算开销小
✓ 在理想网络中是王者

劣势：
✗ 高延迟环境性能急剧下降（可低至<300 Mbps）
✗ 依赖丢包信号，反应滞后
✗ 稳定性差，波动大（±15-35%）
✗ 高延迟+高丢包时接近崩溃

适用场景：
- 数据中心内部通信（<5ms）
- 局域网文件传输
- 同城CDN节点
```

2. bbr

```plain
优势：
✓ 高延迟环境性能卓越（200ms下仍可达800+ Mbps）
✓ 极致稳定性（波动±1-5%）
✓ 重传极少（通常为0）
✓ 主动测量，不依赖丢包
✓ 在复杂网络中是王者

劣势：
✗ 低延迟环境自我限制（约3-4 Gbps）
✗ 对RTT抖动敏感（±20ms会导致性能腰斩）
✗ 实现复杂度高
✗ 在局域网中"浪费"性能

适用场景：
- 跨国网络通信（>100ms）
- 移动/卫星网络
- 视频会议/直播
- 需要稳定性的应用
```

## ps

本文主要记录自己对bbr的探索和测试，对于cubic和bbr的原理讲解非常皮毛，希望大家自己找文章详细了解
