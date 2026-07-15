---
title: 'Bash'
date: 2026-04-16
lastmod: 2026-04-16
author: "giftia"
description: "Bash 基础速查：基础命令、变量、条件判断、循环、函数及脚本编写。"
draft: false
categories: ["运维"]
tags: ["Bash", "Linux", "Shell", "脚本"]
---

## 基础命令

- `pwd`：显示当前目录路径
- `ls`：列出文件（`-l` 详细，`-a` 含隐藏）
- `cd`：切换目录（`cd ..` 上级）
- `mkdir`：创建目录
- `rm`：删除（`-r` 递归）

## 变量

```bash
# 等号两边不能有空格
name="World"
echo "Hello, $name!"
```

## 条件判断

常用比较符：`-eq`（等于）、`-ne`（不等于）、`-gt`（大于）、`-lt`（小于）。

```bash
score=85
if [ $score -ge 90 ]; then
    echo "优秀"
elif [ $score -ge 60 ]; then
    echo "及格"
else
    echo "不及格"
fi
```

## 循环

```bash
# for 循环
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

# while 循环
count=1
while [ $count -le 3 ]; do
    echo "Count is $count"
    count=$((count + 1))
done
```

## 函数

```bash
greet() {
    echo "Hello, $1!"  # $1 为第一个参数
}
greet "Alice"
```

## 管道与重定向

```bash
# 重定向
echo "hello" > file.txt   # 覆盖写入
echo "world" >> file.txt  # 追加写入

# 管道：前一个命令的输出作为后一个命令的输入
ls -l | grep "txt"
```

## 编写脚本

```bash
#!/bin/bash
echo "Starting..."
date
echo "Finished."
```

```bash
chmod +x hello.sh
./hello.sh
```
