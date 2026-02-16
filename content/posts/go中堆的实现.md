---
title: 'Go中堆的实现'
date: 2026-02-16
lastmod: 2026-02-16
author: "giftia"
description: ""
draft: false
categories: ["go"]
tags: []
---

go中堆的实现没有现成的大小根堆，需要实现相应的接口再初始化成堆

## 接口源码

```go
// heap包
type Interface interface {
	sort.Interface
	Push(x any) // Push 在集合末尾（索引 Len() 处）添加元素 x
	Pop() any   // Pop 移除并返回集合末尾（索引 Len()-1 处）的元素
}

// sort包
type Interface interface {
    // Len 返回集合中的元素个数
    Len() int

    // Less 报告索引 i 的元素是否应该排在索引 j 的元素之前
    // 对于小顶堆，这里定义的是“小于”逻辑
    // 对于大顶堆，这里定义的是“大于”逻辑
    Less(i, j int) bool

    // Swap 交换索引为 i 和 j 的元素
    Swap(i, j int)
}
```

## 小根堆

```go
package main

import "container/heap"

type MinHeap []int

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *MinHeap) Push(x any) {
	*h = append(*h, x.(int))
}
func (h *MinHeap) Pop() any {
	x := (*h)[len(*h)-1]
	*h = (*h)[:len(*h)-1]
	return x
}

func main() {
	data := []int{5, 2, 3, 1, 4}

	h := MinHeap(data)
	heap.Init(&h)
	heap.Push(&h, 0)
	res := heap.Pop(&h)
	println(res.(int))
}

```

## 大根堆

```go
package main

import "container/heap"

type MaxHeap []int

func (h MaxHeap) Len() int           { return len(h) }
func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] } // 这里相反
func (h MaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *MaxHeap) Push(x any) {
	*h = append(*h, x.(int))
}
func (h *MaxHeap) Pop() any {
	x := (*h)[len(*h)-1]
	*h = (*h)[:len(*h)-1]
	return x
}

func main() {
	data := []int{5, 2, 3, 1, 4}

	h := MaxHeap(data)
	heap.Init(&h)
	heap.Push(&h, 0)
	res := heap.Pop(&h)
	println(res.(int))
}

```

## 注意

len less swap接口不用传h的指针，因为不会改变切片地址

push pop必须传指针，会改变切片，涉及扩缩容
