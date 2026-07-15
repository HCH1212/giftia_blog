---
title: 'go语言main包的一个小tip'
date: 2026-01-05
author: "giftia"
description: "Go语言package main的使用规则及多文件编译问题的解决方案"
draft: false
categories: ["Go"]
tags: ["go", "package", "main", "build"]
---

## package main 的规则

- Go 中包分两种：**main 包**（可编译为可执行文件）和**非 main 包**（库包）
- `import` 导入的是路径，而非包名
- 习惯上包名与目录名保持一致
- 同一目录下所有源文件必须使用同一包名
- 同一 package 下不同文件间可直接调用
- 大写开头的变量/方法暴露到包外
- 多个 go 文件在 main 包下无法相互调用，需用 `go run *.go` 或 `go run .`

## 常见问题

多个 go 文件在 main 包下，直接 `go run main.go` 会报 `undefined`，但编译器不报错。

**解决**：使用 `go run .` 或 `go run *.go`。
