---
title: 'Go中堆的实现'
date: 2026-02-16
author: "giftia"
description: "Go container/heap 包的使用方法：实现小根堆/大根堆的 Interface 接口及注意事项"
draft: false
categories: ["Go"]
tags: ["go", "heap", "data-structure", "stdlib"]
---

Go 中没有现成的大/小根堆，需要实现 `heap.Interface` 接口后再初始化。

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

## 为什么用户 Pop 弹最后一个，heap.Pop 却返回堆顶？

这是一个常见的困惑：使用 `heap.Pop(&h)` 确实拿到的是堆顶元素（`h[0]`），但我们实现的 `Pop()` 方法里明明弹的是最后一个元素。这看似矛盾，实际上是因为 **`heap.Pop` 在调用用户 `Pop` 前后做了额外的工作**。

### heap.Pop 的完整执行流程

查看 `container/heap` 源码，`heap.Pop` 的执行顺序如下：

```go
func Pop(h Interface) any {
    n := h.Len() - 1
    h.Swap(0, n)           // 步骤 1：将堆顶（索引 0）与末尾元素交换
    down(h, 0, n)          // 步骤 2：对新的堆顶做下沉，恢复部分堆序（不含末尾）
    x := h.Pop()           // 步骤 3：调用用户实现的 Pop，移除并返回末尾元素
    return x
}
```

流程图解：

1. **Swap** — `h[0]`（真正的堆顶）与 `h[len-1]`（末尾元素）交换位置
2. **down** — 对新的 `h[0]`（原来的末尾元素）执行下沉操作，保证前 `n` 个元素重新满足堆性质
3. **用户 Pop** — 此时调用我们写的 `Pop()`，它移除切片最后一个元素（此时这个元素正是步骤 1 交换过去的原堆顶），将其返回

### 直观理解

```
初始小根堆:        Swap 后:           down 后:            Pop 后:
    1                 5                 2                  2
   / \      -->      / \       -->     / \       -->      / \
  3   2             3   2             3   5              3   5
 /                /                 /                  /
5                1                 1                  (1 被弹出)
```

整个过程中，用户只需关心“如何从切片末尾删除一个元素”，而堆性质的维护（交换、下沉）完全由 `heap` 包内部完成。这就是标准库巧妙的设计——**职责分离**。

## 注意

len less swap接口不用传h的指针，因为不会改变切片地址

push pop必须传指针，会改变切片，涉及扩缩容
