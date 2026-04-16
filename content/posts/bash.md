---
title: 'Bash'
date: 2026-04-16
lastmod: 2026-04-16
author: "giftia"
description: "Bash 基础指南：从入门到实用，涵盖基础命令、变量、条件判断、循环、函数及脚本编写。"
draft: false
categories: ["技术"]
tags: ["Bash", "Linux", "Shell", "脚本"]
---

# Bash 基础指南：从入门到实用

Bash (Bourne Again SHell) 是大多数 Linux 和 macOS 系统的默认命令行解释器。它不仅是一个与系统交互的界面，也是一门强大的脚本语言。本文将带你快速掌握 Bash 的核心概念和实用技巧。

## 1. 什么是 Bash？

简单来说，Bash 就像一个翻译官。你输入人类可读的命令，Bash 将其翻译成操作系统能理解的指令并执行。

## 2. 基础命令

在开始编写脚本之前，我们需要熟悉一些最常用的基础命令：

* `pwd`: 显示当前所在目录的路径 (Print Working Directory)。
* `ls`: 列出当前目录下的文件和文件夹。
  * `ls -l`: 详细列表格式。
  * `ls -a`: 显示隐藏文件。
* `cd`: 切换目录 (Change Directory)。
  * `cd /var/log`: 进入绝对路径。
  * `cd ..`: 返回上一级目录。
* `mkdir`: 创建新目录。
* `rm`: 删除文件或目录。
  * `rm file.txt`: 删除文件。
  * `rm -r folder`: 递归删除目录及其内容。

## 3. 变量

Bash 中的变量不需要声明类型，直接赋值即可。

**定义和使用变量：**

```bash
# 定义变量（注意：等号两边不能有空格）
name="World"
age=25

# 使用变量（在变量名前加 $ 符号）
echo "Hello, $name!"
echo "I am $age years old."
```

## 4. 条件判断

Bash 使用 `if` 语句进行条件控制。

**基本语法：**

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

*注意：`[` 和 `]` 内部两边必须有空格。`-ge` 表示大于等于 (greater than or equal)。*

**常用比较符：**
* `-eq`: 等于
* `-ne`: 不等于
* `-gt`: 大于
* `-lt`: 小于

## 5. 循环结构

循环用于重复执行一段代码。

**For 循环：**

```bash
# 遍历列表
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

# 遍历数字范围
for i in {1..5}; do
    echo "Number: $i"
done
```

**While 循环：**

```bash
count=1
while [ $count -le 3 ]; do
    echo "Count is $count"
    count=$((count + 1)) # 数学运算
done
```

## 6. 函数

将常用的代码块封装成函数，可以提高代码的复用性。

```bash
# 定义函数
greet() {
    # $1 表示第一个参数
    echo "Hello, $1! Welcome to Bash."
}

# 调用函数并传递参数
greet "Alice"
greet "Bob"
```

## 7. 管道与重定向

这是 Bash 中非常强大的特性，用于连接多个命令或控制输入输出。

**重定向 (`>` 和 `>>`)：**
将命令的输出保存到文件中。

```bash
# 覆盖写入
echo "This is a test" > test.txt

# 追加写入
echo "Another line" >> test.txt
```

**管道 (`|`)：**
将前一个命令的输出作为后一个命令的输入。

```bash
# 列出当前目录文件，并查找包含 "txt" 的行
ls -l | grep "txt"
```

## 8. 编写你的第一个脚本

1. 创建一个文件，例如 `hello.sh`。
2. 在第一行添加 Shebang (`#!/bin/bash`)，告诉系统使用 Bash 解释器。
3. 编写代码。
4. 赋予执行权限并运行。

**hello.sh 内容：**

```bash
#!/bin/bash
echo "Starting script..."
date
echo "Script finished."
```

**执行步骤：**

```bash
chmod +x hello.sh  # 赋予执行权限
./hello.sh         # 运行脚本
```

## 总结

Bash 是一门实践性很强的语言。掌握上述基础后，你可以通过编写简单的自动化脚本（如备份文件、批量重命名）来不断提升技能。遇到不熟悉的命令，随时使用 `man 命令名` (如 `man ls`) 查看帮助文档。
