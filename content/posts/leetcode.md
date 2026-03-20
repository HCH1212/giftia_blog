---
title: 'Leetcode'
date: 2026-03-09
lastmod: 2026-03-09
author: 'giftia'
description: 'LeetCode'
draft: false
categories: ['go']
tags: ['算法', 'LeetCode', 'go']
---

### 1

- LeetCode: https://leetcode.cn/problems/two-sum/description/?envType=study-plan-v2&envId=top-100-liked

```go
package one

func twoSum(nums []int, target int) []int {
	m := map[int]int{} // 元素：下标

	for i := 0; i < len(nums); i++ {
		other := target - nums[i]
		if index, ok := m[other]; ok {
			return []int{i, index}
		}
		m[nums[i]] = i
	}

	return nil
}
```

### 2

- LeetCode: https://leetcode.cn/problems/add-two-numbers/description/?envType=study-plan-v2&envId=top-100-liked

```go
package two

type ListNode struct {
	Val  int
	Next *ListNode
}

func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	dummy := &ListNode{}
	cur := dummy
	carry := 0 // 进位

	for l1 != nil || l2 != nil {
		v1, v2 := 0, 0
		if l1 != nil {
			v1 = l1.Val
			l1 = l1.Next
		}
		if l2 != nil {
			v2 = l2.Val
			l2 = l2.Next
		}

		sum := (v1 + v2 + carry) % 10
		carry = (v1 + v2 + carry) / 10

		newNode := &ListNode{Val: sum}
		cur.Next = newNode
		cur = cur.Next
	}

	if carry > 0 {
		newNode := &ListNode{Val: carry}
		cur.Next = newNode
	}

	return dummy.Next
}
```

### 3

- LeetCode: https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/?envType=study-plan-v2&envId=top-100-liked

```go
package three

func lengthOfLongestSubstring(s string) int {
	if len(s) == 0 {
		return 0
	}

	temp := map[byte]int{}
	left, right := 0, 0
	res := 0

	for ; right < len(s); right++ {
		temp[s[right]]++

		for temp[s[right]] > 1 {
			temp[s[left]]--
			left++
		}

		res = max(res, right-left+1)
	}

	return res
}
```

### 11

- LeetCode: https://leetcode.cn/problems/container-with-most-water/description/?envType=study-plan-v2&envId=top-100-liked

```go
package oneone

func maxArea(height []int) int {
	res := 0
	left, right := 0, len(height)-1

	for left <= right {
		area := (right - left) * min(height[left], height[right])
		res = max(res, area)

		if height[left] < height[right] {
			left++
		} else {
			right--
		}
	}

	return res
}
```

### 15

- LeetCode: https://leetcode.cn/problems/3sum/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefive

import "sort"

func threeSum(nums []int) [][]int {
	sort.Ints(nums)
	res := [][]int{}

	for i := 0; i < len(nums)-2; i++ {
		if i > 0 && nums[i] == nums[i-1] {
			continue
		}

		// 两数之和（有序）
		v1 := nums[i]
		left, right := i+1, len(nums)-1

		for left < right {
			sum := v1 + nums[left] + nums[right]
			if sum == 0 {
				res = append(res, []int{v1, nums[left], nums[right]})
				// 这里需要内部去重
				left++
				right--
				for left < right && nums[left] == nums[left-1] {
					left++
				}
				for left < right && nums[right] == nums[right+1] {
					right--
				}
			} else if sum > 0 {
				right--
			} else {
				left++
			}
		}
	}

	return res
}
```

### 19

- LeetCode: https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onenine

type ListNode struct {
	Val  int
	Next *ListNode
}

func removeNthFromEnd(head *ListNode, n int) *ListNode {
	if head == nil || head.Next == nil {
		return nil
	}

	// 快慢指针，快指针先走n步
	fast, slow := head, head
	for n > 0 {
		fast = fast.Next
		n--
	}

	// 是否要删除头节点
	if fast == nil {
		return head.Next
	}

	// 再同时走
	for fast.Next != nil {
		fast = fast.Next
		slow = slow.Next
	}

	// slow的下一个节点就是要删除的节点
	slow.Next = slow.Next.Next

	return head
}
```

### 20

- LeetCode: https://leetcode.cn/problems/valid-parentheses/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twozero

func isValid(s string) bool {
	if len(s)%2 == 1 {
		return false
	}

	m := map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
	}
	stack := []rune{}

	for _, v := range s {
		if other, ok := m[v]; ok {
			if len(stack) > 0 && stack[len(stack)-1] == other {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		} else {
			stack = append(stack, v)
		}
	}

	if len(stack) > 0 {
		return false
	}
	return true
}
```

### 21

- LeetCode: https://leetcode.cn/problems/merge-two-sorted-lists/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twoone

type ListNode struct {
	Val  int
	Next *ListNode
}

func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {
	if list1 == nil {
		return list2
	}
	if list2 == nil {
		return list1
	}

	// 递归
	if list1.Val < list2.Val {
		list1.Next = mergeTwoLists(list1.Next, list2)
		return list1
	} else {
		list2.Next = mergeTwoLists(list1, list2.Next)
		return list2
	}
}
```

### 23

- LeetCode: https://leetcode.cn/problems/merge-k-sorted-lists/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothree

type ListNode struct {
	Val  int
	Next *ListNode
}

// // 递归合并
// func mergeKLists(lists []*ListNode) *ListNode {
// 	if len(lists) == 0 {
// 		return nil
// 	}

// 	return mergeTwoLists(lists[0], mergeKLists(lists[1:]))
// }

// 两两迭代合并
func mergeKLists(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}

	for len(lists) > 1 {
		temp := []*ListNode{}

		for i := 0; i < len(lists); i += 2 {
			var l1, l2 *ListNode
			l1 = lists[i]
			if i+1 < len(lists) {
				l2 = lists[i+1]
			}
			temp = append(temp, mergeTwoLists(l1, l2))
		}

		lists = temp
	}

	return lists[0]
}

// 合并两个有序链表
func mergeTwoLists(l1, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}

	if l1.Val < l2.Val {
		l1.Next = mergeTwoLists(l1.Next, l2)
		return l1
	} else {
		l2.Next = mergeTwoLists(l1, l2.Next)
		return l2
	}
}
```

### 24

- LeetCode: https://leetcode.cn/problems/swap-nodes-in-pairs/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twofour

type ListNode struct {
	Val  int
	Next *ListNode
}

func swapPairs(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}

	// 递归
	newHead := head.Next
	head.Next = swapPairs(newHead.Next)
	newHead.Next = head

	return newHead
}
```

### 25

- LeetCode: https://leetcode.cn/problems/reverse-nodes-in-k-group/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twofive

type ListNode struct {
	Val  int
	Next *ListNode
}

func reverseKGroup(head *ListNode, k int) *ListNode {
	// 递归

	// 终止条件：不足 k 个
	cur := head
	for i := 0; i < k; i++ {
		if cur == nil {
			return head
		}
		cur = cur.Next
	}
	// 此时 cur 已经指向了第 k+1 个节点

	// 反转前 k 个节点：[head, cur)
	newHead := reverse(head, cur)

	// 反转后 head 已经变成了尾节点，连接后续节点
	head.Next = reverseKGroup(cur, k)
	
	return newHead
}

func reverse(head, tail *ListNode) *ListNode {
	if head.Next == tail {
		return head // 不能超出区间
	}

	newHead := reverse(head.Next, tail)
	head.Next.Next = head
	head.Next = nil

	return newHead
}
```

### 31

- LeetCode: https://leetcode.cn/problems/next-permutation/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threeone

func nextPermutation(nums []int) {
	// 从后遍历比大小（回溯思路）
	i := 0
	for i = len(nums) - 1; i >= 0; i-- {
		if i+1 < len(nums) && nums[i+1] > nums[i] {
			for j := len(nums) - 1; j > i; j-- {
				if nums[j] > nums[i] {
					nums[i], nums[j] = nums[j], nums[i]
					break
				}
			}
			break
		}
	}

	// 翻转候选集合
	left, right := i+1, len(nums)-1
	for left < right {
		nums[left], nums[right] = nums[right], nums[left]
		left++
		right--
	}
}
```

### 33

- LeetCode: https://leetcode.cn/problems/search-in-rotated-sorted-array/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threethree

func search(nums []int, target int) int {
	maxIndex := 0
	for i := 1; i < len(nums); i++ {
		if nums[i] < nums[i-1] {
			break
		} else {
			maxIndex = i
		}
	}

	res := -1
	if target < nums[0] {
		res = twoSearch(nums, target, maxIndex+1, len(nums)-1)
	} else {
		res = twoSearch(nums, target, 0, maxIndex)
	}
	return res
}

// 区间二分
func twoSearch(nums []int, target, left, right int) int {
	for left <= right {
		mid := (right-left)/2 + left
		if nums[mid] == target {
			return mid
		} else if nums[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	return -1
}
```

### 34

- LeetCode: https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threefour

func searchRange(nums []int, target int) []int {
	n := len(nums)
	if n == 0 {
		return []int{-1, -1}
	}

	left, right := 0, n-1

	for left <= right {
		mid := (right-left)/2 + left
		if nums[mid] >= target {
			right = mid - 1
		} else {
			left = mid + 1
		}
	}
	// 此时 left 是第一个 target 下标
	if left == n || nums[left] != target {
		return []int{-1, -1}
	}

	for right = left; right < n && nums[right] == target; right++ {
	}

	return []int{left, right - 1}
}
```

### 35

- LeetCode: https://leetcode.cn/problems/search-insert-position/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threefive

func searchInsert(nums []int, target int) int {
	left, right := 0, len(nums)-1

	for left <= right {
		mid := (right-left)/2 + left
		if nums[mid] == target {
			return mid
		} else if nums[mid] > target {
			right = mid - 1
		} else {
			left = mid + 1
		}
	}

	return left
}
```

### 41

- LeetCode: https://leetcode.cn/problems/first-missing-positive/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fourone

func firstMissingPositive(nums []int) int {
	n := len(nums)
	// 正整数：1...n
	// 让数字放在正确的位置上：nums[i] == i+1

	for i := 0; i < n; i++ {
		if nums[i] == i+1 { // 已经在正确位置
			continue
		}
		if nums[i] <= 0 || nums[i] > n { // 不在范围内
			continue
		}
		if nums[i] == nums[nums[i]-1] { // 重复的数字
			continue
		}

		nums[i], nums[nums[i]-1] = nums[nums[i]-1], nums[i]
		i-- // 交换后还要继续检查当前索引
	}

	for i := 0; i < n; i++ {
		if nums[i] != i+1 {
			return i + 1
		}
	}

	return n + 1
}
```

### 42

- LeetCode: https://leetcode.cn/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fourtwo

func trap(height []int) int {
	if len(height) == 0 {
		return 0
	}

	left, right := 0, len(height)-1           // 双指针
	maxL, maxR := height[left], height[right] // 两个边界
	sum := 0

	for left < right {
		if maxL < maxR {
			left++
			if maxL-height[left] > 0 {
				sum += maxL - height[left]
			}
			maxL = max(maxL, height[left])
		} else {
			right--
			if maxR-height[right] > 0 {
				sum += maxR - height[right]
			}
			maxR = max(maxR, height[right])
		}
	}

	return sum
}
```

### 45

- LeetCode: https://leetcode.cn/problems/jump-game-ii/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fourfive

func jump(nums []int) int {
	n := len(nums)

	// 反向
	position := n - 1
	step := 0

	for position > 0 {
		for i := 0; i < position; i++ {
			if i+nums[i] >= position {
				position = i
				step++
				break
			}
		}
	}

	return step
}
```

### 46

- LeetCode: https://leetcode.cn/problems/permutations/description/?envType=study-plan-v2&envId=top-100-liked

```go
package foursix

func permute(nums []int) [][]int {
	res := [][]int{}                // 结果
	temp := []int{}                 // 路径
	used := make([]bool, len(nums)) // nums 中使用过的

	dfs(nums, &res, temp, used)
	return res
}

func dfs(nums []int, res *[][]int, temp []int, used []bool) {
	if len(temp) == len(nums) {
		copyTemp := make([]int, len(temp))
		copy(copyTemp, temp)
		*res = append(*res, copyTemp)
	}

	for i := 0; i < len(nums); i++ {
		if used[i] {
			continue
		}

		temp = append(temp, nums[i])
		used[i] = true
		dfs(nums, res, temp, used)
		temp = temp[:len(temp)-1]
		used[i] = false
	}
}
```

### 48

- LeetCode: https://leetcode.cn/problems/rotate-image/description/?envType=study-plan-v2&envId=top-100-liked

```go
package foureight

func rotate(matrix [][]int) {
	row := len(matrix)

	// 1. 上下翻转
    for i := 0; i < row/2; i++ {
        matrix[i], matrix[row-1-i] = matrix[row-1-i], matrix[i]
    }

    // 2. 主对角线翻转
    for i := 0; i < row; i++ {
        for j := 0; j < i; j++ {
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        }
    }
}
```

### 49

- LeetCode: https://leetcode.cn/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fournine

func groupAnagrams(strs []string) [][]string {
	temp := map[[26]int][]string{}
	res := [][]string{}

	for _, v := range strs {
		temp[getCount(v)] = append(temp[getCount(v)], v)
	}
	for _, v := range temp {
		res = append(res, v)
	}

	return res
}

func getCount(s string) [26]int {
	res := [26]int{}
	for _, v := range s {
		res[v-'a']++
	}
	return res
}
```

### 53

- LeetCode: https://leetcode.cn/problems/maximum-subarray/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivethree

func maxSubArray(nums []int) int {
	// 可以dp，但这里只用到一个状态，所以直接用一个变量记录当前状态就行了
	curSum := nums[0] // 以当前元素结尾的最大子数组和，初始值为nums[0]，因为如果nums全是负数，那么结果就是最大的那个负数
	res := curSum

	for i := 1; i < len(nums); i++ {
		if curSum < 0 { // 直接舍弃之前的
			curSum = nums[i]
		} else {
			curSum += nums[i]
		}
		res = max(res, curSum)
	}

	return res
}
```

### 54

- LeetCode: https://leetcode.cn/problems/spiral-matrix/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivefour

func spiralOrder(matrix [][]int) []int {
	row := len(matrix)
	col := len(matrix[0])

	res := make([]int, 0, row*col)

	// 四个边界
	top, bottom := 0, row-1
	left, right := 0, col-1

	for top <= bottom && left <= right {
		// 上
		for j := left; j <= right; j++ {
			res = append(res, matrix[top][j])
		}
		top++
		if top > bottom || left > right {
			break
		}

		// 右
		for j := top; j <= bottom; j++ {
			res = append(res, matrix[j][right])
		}
		right--
		if top > bottom || left > right {
			break
		}

		// 下
		for j := right; j >= left; j-- {
			res = append(res, matrix[bottom][j])
		}
		bottom--
		if top > bottom || left > right {
			break
		}

		// 左
		for j := bottom; j >= top; j-- {
			res = append(res, matrix[j][left])
		}
		left++
	}

	return res
}
```

### 55

- LeetCode: https://leetcode.cn/problems/jump-game/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivefive

func canJump(nums []int) bool {
	n := len(nums)
	maxPosition := 0

	for i, v := range nums {
		if i <= maxPosition {
			maxPosition = max(maxPosition, i+v)
			if maxPosition >= n-1 { // 注意是下标的比较
				return true
			}
		}
	}

	return false
}
```

### 56

- LeetCode: https://leetcode.cn/problems/merge-intervals/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivesix

import "slices"

func merge(intervals [][]int) [][]int {
	// 按左端点排序
	slices.SortFunc(intervals, func(p, q []int) int { return p[0] - q[0] })

	res := [][]int{}
	left, right := intervals[0][0], intervals[0][1]

	for i := 1; i < len(intervals); i++ {
		if right >= intervals[i][0] { // 重叠
			right = max(right, intervals[i][1])
		} else {
			res = append(res, []int{left, right})
			left, right = intervals[i][0], intervals[i][1]
		}
	}

	res = append(res, []int{left, right}) // 加上最后一个

	return res
}
```

### 70

- LeetCode: https://leetcode.cn/problems/climbing-stairs/description/?envType=study-plan-v2&envId=top-100-liked

```go
package sevenzero

func climbStairs(n int) int {
	if n <= 1 {
		return n
	}

	one, two := 1, 1
	res := 0
	for i := 2; i <= n; i++ {
		res = one + two
		one = two
		two = res
	}
	return res
}
```

### 73

- LeetCode: https://leetcode.cn/problems/set-matrix-zeroes/description/?envType=study-plan-v2&envId=top-100-liked

```go
package seventhree

// 空间O(1)版
func setZeroes(matrix [][]int) {
	// 使用矩阵的第一行和第一列来标记，[0][0]避免复用，所以加一个变量
	row := len(matrix)
	col := len(matrix[0])

	firstCol := 1 // 第一列第一个

	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if matrix[i][j] == 0 {
				// 清晰区分第一行和第一列
				if i == 0 {
					matrix[0][0] = 0
				}
				if j == 0 {
					firstCol = 0
				}
				if i != 0 && j != 0 {
					matrix[i][0] = 0
					matrix[0][j] = 0
				}
			}
		}
	}

	for i := 1; i < row; i++ {
		for j := 1; j < col; j++ {
			if matrix[0][j] == 0 || matrix[i][0] == 0 {
				matrix[i][j] = 0
			}
		}
	}

	// 最后处理第一行和第一列
	if matrix[0][0] == 0 {
		for j := 0; j < col; j++ {
			matrix[0][j] = 0
		}
	}
	if firstCol == 0 {
		for i := 0; i < row; i++ {
			matrix[i][0] = 0
		}
	}
}

// func setZeroes(matrix [][]int) {
// 	row := len(matrix)
// 	col := len(matrix[0])

// 	rowFlag := make([]int, row)
// 	colFlag := make([]int, col)

// 	// 先标记
// 	for i := 0; i < row; i++ {
// 		for j := 0; j < col; j++ {
// 			if matrix[i][j] == 0 {
// 				rowFlag[i] = 1
// 				colFlag[j] = 1
// 			}
// 		}
// 	}

// 	// 再改变
// 	for i := 0; i < row; i++ {
// 		for j := 0; j < col; j++ {
// 			if rowFlag[i] == 1 || colFlag[j] == 1 {
// 				matrix[i][j] = 0
// 			}
// 		}
// 	}
// }
```

### 74

- LeetCode: https://leetcode.cn/problems/search-a-2d-matrix/description/?envType=study-plan-v2&envId=top-100-liked

```go
package sevenfour

func searchMatrix(matrix [][]int, target int) bool {
	row := len(matrix)
	col := len(matrix[0])

	i, j := 0, col-1
	for i < row && j >= 0 {
		if matrix[i][j] == target {
			return true
		} else if matrix[i][j] < target {
			i++
		} else {
			j--
		}
	}

	return false
}
```

### 75

- LeetCode: https://leetcode.cn/problems/sort-colors/description/?envType=study-plan-v2&envId=top-100-liked

```go
package sevenfive

func sortColors(nums []int) {
	// 三路快排思路
	temp1, temp2 := 0, len(nums)-1
	i := 0

	for i <= temp2 {
		switch nums[i] {
		case 1:
			i++
		case 0:
			nums[i], nums[temp1] = nums[temp1], nums[i]
			i++
			temp1++
		case 2:
			nums[i], nums[temp2] = nums[temp2], nums[i]
			temp2--
		}
	}
}
```

### 76

- LeetCode: https://leetcode.cn/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-100-liked

```go
package sevensix

func minWindow(s string, t string) string {
	if len(s) < len(t) {
		return ""
	}

	// A-Z 65-90 / a-z 97-122 / 122-65+1=58
	tempS, tempT := [58]int{}, [58]int{}
	target := 0 // t有几种字符
	for _, v := range t {
		tempT[v-'A']++
	}
	for _, v := range tempT { // 遍历tempT而不是t, 避免重复字符
		if v > 0 {
			target++
		}
	}

	res := ""
	left, right := 0, 0
	now := 0 // s窗口现在有几种字符达到条件

	for right < len(s) {
		tempS[s[right]-'A']++
		if tempS[s[right]-'A'] == tempT[s[right]-'A'] {
			now++
		}

		for now == target {
			if res == "" || right-left+1 < len(res) {
				res = s[left : right+1]
			}
			tempS[s[left]-'A']--
			if tempS[s[left]-'A'] < tempT[s[left]-'A'] {
				now--
			}
			left++
		}

		right++
	}

	return res
}
```

### 78

- LeetCode: https://leetcode.cn/problems/subsets/description/?envType=study-plan-v2&envId=top-100-liked

```go
package seveneight

func subsets(nums []int) [][]int {
	res := [][]int{}
	temp := []int{}

	// 从索引 0 开始递归
	dfs(nums, &res, temp, 0)
	return res
}

func dfs(nums []int, res *[][]int, temp []int, start int) {
	copyTemp := make([]int, len(temp))
	copy(copyTemp, temp)
	*res = append(*res, copyTemp)

	for i := start; i < len(nums); i++ {
		temp = append(temp, nums[i])
		dfs(nums, res, temp, i+1)
		temp = temp[:len(temp)-1]
	}
}
```

### 94

- LeetCode: https://leetcode.cn/problems/binary-tree-inorder-traversal/description/?envType=study-plan-v2&envId=top-100-liked

```go
package ninefour

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func inorderTraversal(root *TreeNode) []int {
	res := []int{}
	inorder(root, &res)
	return res
}

func inorder(node *TreeNode, res *[]int) {
	if node == nil {
		return
	}

	inorder(node.Left, res)
	*res = append(*res, node.Val)
	inorder(node.Right, res)
}
```

### 98

- LeetCode: https://leetcode.cn/problems/validate-binary-search-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package nineeight

import "math"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// 递归或者中序，这里用递归
func isValidBST(root *TreeNode) bool {
	return isBST(root, math.MinInt, math.MaxInt)
}

// 需要大小边界
func isBST(node *TreeNode, minV, maxV int) bool {
	if node == nil {
		return true
	}

	return (node.Val > minV && node.Val < maxV) &&
		isBST(node.Left, minV, node.Val) &&
		isBST(node.Right, node.Val, maxV)
}
```

### 101

- LeetCode: https://leetcode.cn/problems/symmetric-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onezeroone

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func isSymmetric(root *TreeNode) bool {
	if root == nil {
		return true
	}
	return isMirror(root.Left, root.Right)
}

// 两个树是否对称
func isMirror(node1, node2 *TreeNode) bool {
	if node1 == nil && node2 == nil {
		return true
	}
	if node1 == nil || node2 == nil {
		return false
	}

	return (node1.Val == node2.Val) &&
		(isMirror(node1.Left, node2.Right)) &&
		(isMirror(node1.Right, node2.Left))
}
```

### 102

- LeetCode: https://leetcode.cn/problems/binary-tree-level-order-traversal/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onezerotwo

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func levelOrder(root *TreeNode) [][]int {
	if root == nil {
		return nil
	}

	q := make([]*TreeNode, 1)
	q[0] = root
	res := [][]int{}

	for len(q) > 0 {
		n := len(q)
		temp := []int{}

		for i := 0; i < n; i++ {
			node := q[i]
			temp = append(temp, node.Val)
			if node.Left != nil {
				q = append(q, node.Left)
			}
			if node.Right != nil {
				q = append(q, node.Right)
			}
		}
		q = q[n:] // 一次性去掉计算过的一层
		res = append(res, temp)
	}

	return res
}
```

### 104

- LeetCode: https://leetcode.cn/problems/maximum-depth-of-binary-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onezerofour

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}

	return max(maxDepth(root.Left), maxDepth(root.Right)) + 1
}
```

### 105

- LeetCode: https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onezerofive

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// 递归
func buildTree(preorder []int, inorder []int) *TreeNode {
	if len(preorder) == 0 {
		return nil
	}

	head := &TreeNode{Val: preorder[0]}

	// 找左子树的节点个数
	n := 0
	for i := 0; i < len(inorder); i++ {
		if inorder[i] == preorder[0] {
			break
		} else {
			n++
		}
	}

	head.Left = buildTree(preorder[1:n+1], inorder[:n])
	head.Right = buildTree(preorder[n+1:], inorder[n+1:])
	return head
}
```

### 108

- LeetCode: https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onezeroeight

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func sortedArrayToBST(nums []int) *TreeNode {
	n := len(nums)
	if n == 0 {
		return nil
	}

	// 取中点
	mid := n / 2

	node := &TreeNode{Val: nums[mid]}
	node.Left = sortedArrayToBST(nums[:mid])
	node.Right = sortedArrayToBST(nums[mid+1:])

	return node
}
```

### 114

- LeetCode: https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/description/?envType=study-plan-v2&envId=top-100-liked

```go
package oneonefour

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// 递归
func flatten(root *TreeNode) {
	if root == nil {
		return
	}

	flatten(root.Left)
	flatten(root.Right)

	tempRight := root.Right
	root.Right = root.Left
	root.Left = nil

	// 移动到最后一个节点
	tempLeft := root
	for tempLeft.Right != nil {
		tempLeft = tempLeft.Right
	}

	tempLeft.Right = tempRight
}
```

### 118

- LeetCode: https://leetcode.cn/problems/pascals-triangle/description/?envType=study-plan-v2&envId=top-100-liked

```go
package oneoneeight

func generate(numRows int) [][]int {
	if numRows == 1 {
		return [][]int{{1}}
	}
	if numRows == 2 {
		return [][]int{{1}, {1, 1}}
	}

	res := [][]int{{1}, {1, 1}}
	for i := 2; i < numRows; i++ {
		temp := make([]int, i+1)
		temp[0], temp[i] = 1, 1
		for j := 1; j < i; j++ {
			temp[j] = res[i-1][j-1] + res[i-1][j]
		}
		res = append(res, temp)
	}

	return res
}
```

### 121

- LeetCode: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onetwoone

func maxProfit(prices []int) int {
	res := 0
	minPrice := prices[0]

	for i := 1; i < len(prices); i++ {
		res = max(res, prices[i]-minPrice)
		minPrice = min(minPrice, prices[i])
	}

	return res
}
```

### 124

- LeetCode: https://leetcode.cn/problems/binary-tree-maximum-path-sum/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onetwofour

import "math"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func maxPathSum(root *TreeNode) int {
	if root == nil {
		return 0
	}

	res := math.MinInt
	dfs(root, &res)
	return res
}

// 以当前节点为根的最大路径和以及节点贡献值（贡献值用于递归）
func dfs(node *TreeNode, res *int) int {
	if node == nil {
		return 0
	}

	maxL := max(0, dfs(node.Left, res))
	maxR := max(0, dfs(node.Right, res))

	*res = max(*res, node.Val+maxL+maxR)
	return node.Val + max(maxL, maxR) // 避免一个节点重复使用
}
```

### 128

- LeetCode: https://leetcode.cn/problems/longest-consecutive-sequence/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onetwoeight

func longestConsecutive(nums []int) int {
	res := 0
	temp := map[int]bool{}

	// 全部加到map
	for _, v := range nums {
		temp[v] = true
	}

	// 遍历map，可去重
	for k := range temp {
		if temp[k-1] { // 不是开头避免计算
			continue
		}

		curL := 1
		curN := k + 1

		for {
			if temp[curN] {
				curL++
				curN++
			} else {
				break
			}
		}

		res = max(res, curL)
	}

	return res
}
```

### 136

- LeetCode: https://leetcode.cn/problems/single-number/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onethreesix

// 异或
func singleNumber(nums []int) int {
	res := 0
	for _, v := range nums {
		res ^= v
	}
	return res
}
```

### 138

- LeetCode: https://leetcode.cn/problems/copy-list-with-random-pointer/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onethreeeight

type Node struct {
	Val    int
	Next   *Node
	Random *Node
}

func copyRandomList(head *Node) *Node {
	if head == nil {
		return nil
	}

	// 复制节点并插入到原节点后面
	cur := head
	for cur != nil {
		newNode := &Node{Val: cur.Val}
		newNode.Next = cur.Next
		cur.Next = newNode
		cur = newNode.Next
	}

	// 设置随机指针
	cur = head
	for cur != nil {
		if cur.Random == nil {
			cur.Next.Random = nil
		} else {
			cur.Next.Random = cur.Random.Next
		}
		cur = cur.Next.Next
	}

	// 分离两个链表（注意要还原旧链表）
	newHead := head.Next
	cur = head
	newCur := newHead
	for cur != nil && newCur != nil {
		cur.Next = newCur.Next
		cur = cur.Next

		if cur != nil {
			newCur.Next = cur.Next
		} else {
			newCur.Next = nil
		}
		newCur = newCur.Next
	}

	return newHead
}
```

### 141

- LeetCode: https://leetcode.cn/problems/linked-list-cycle/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefourone

type ListNode struct {
	Val  int
	Next *ListNode
}

func hasCycle(head *ListNode) bool {
	if head == nil || head.Next == nil {
		return false
	}

	// 快慢指针
	slow, fast := head, head

	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
		if slow == fast {
			return true
		}
	}

	return false
}
```

### 142

- LeetCode: https://leetcode.cn/problems/linked-list-cycle-ii/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefourtwo

type ListNode struct {
	Val  int
	Next *ListNode
}

func detectCycle(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return nil
	}

	// 快慢指针找到相遇点
	slow, fast := head, head.Next // 错开

	for slow != fast {
		if fast == nil || fast.Next == nil {
			return nil
		}
		slow = slow.Next
		fast = fast.Next.Next
	}

	// 环的周长
	c := 0
	for slow != nil {
		slow = slow.Next
		c++
		if slow == fast {
			break
		}
	}

	// 重置两个指针，让快指针从头先走一圈圆的长度，然后再两个指针再一起走，最终他们会在圆的起点相遇
    slow, fast = head, head
    for c > 0 {
        fast = fast.Next
        c--
    }

    for slow != fast {
        slow = slow.Next
        fast = fast.Next
    }

    return slow
}
```

### 146

- LeetCode: https://leetcode.cn/problems/lru-cache/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefoursix

type LRUCache struct {
	len        int
	capacity   int
	cache      map[int]*Node
	head, tail *Node // 双向链表
}

type Node struct {
	key, value int
	prev, next *Node
}

func Constructor(capacity int) LRUCache {
	head, tail := &Node{}, &Node{}
	head.next = tail
	tail.prev = head

	return LRUCache{
		len:      0,
		capacity: capacity,
		cache:    make(map[int]*Node),
		head:     head,
		tail:     tail,
	}
}

func (this *LRUCache) Get(key int) int {
	node, ok := this.cache[key]
	if !ok {
		return -1
	}

	this.deleteNode(node)
	this.addHead(node)
	return node.value
}

func (this *LRUCache) Put(key int, value int) {
	node, ok := this.cache[key]
	if ok {
		node.value = value
		this.deleteNode(node)
		this.addHead(node)
		return
	}

	newNode := &Node{
		key:   key,
		value: value,
	}
	if this.len < this.capacity {
		this.addHead(newNode)
		this.cache[key] = newNode
		this.len++
	} else {
		delete(this.cache, this.tail.prev.key)
		this.deleteNode(this.tail.prev)
		this.addHead(newNode)
		this.cache[key] = newNode
	}
}

func (this *LRUCache) addHead(node *Node) {
	node.next = this.head.next
	this.head.next.prev = node

	this.head.next = node
	node.prev = this.head
}

func (this *LRUCache) deleteNode(node *Node) {
	node.prev.next = node.next
	node.next.prev = node.prev
}
```

### 148

- LeetCode: https://leetcode.cn/problems/sort-list/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefoureight

type ListNode struct {
	Val  int
	Next *ListNode
}

func sortList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}

	// 归并排序

	// 找到链表的中点
	slow, fast := head, head.Next
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}

	// 分割链表
	mid := slow.Next
	slow.Next = nil

	return merge(sortList(head), sortList(mid))
}

// 合并两个有序链表
func merge(l1, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}

	if l1.Val < l2.Val {
		l1.Next = merge(l1.Next, l2)
		return l1
	} else {
		l2.Next = merge(l1, l2.Next)
		return l2
	}
}
```

### 153

- LeetCode: https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefivethree

func findMin(nums []int) int {
	n := len(nums)
	left, right := 0, n-1

	for left < right {
		mid := (right-left)/2 + left
		if nums[mid] < nums[n-1] {
			right = mid
		} else {
			left = mid + 1
		}
	}

	return nums[left]
}
```

### 155

- LeetCode: https://leetcode.cn/problems/min-stack/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onefivefive

type MinStack struct {
	stack    []int
	minStack []int
}

func Constructor() MinStack {
	return MinStack{
		stack:    []int{},
		minStack: []int{},
	}
}

func (this *MinStack) Push(val int) {
	this.stack = append(this.stack, val)
	if len(this.minStack) == 0 {
		this.minStack = append(this.minStack, val)
	} else {
		this.minStack = append(this.minStack, min(this.minStack[len(this.minStack)-1], val))
	}
}

func (this *MinStack) Pop() {
	n := len(this.stack)
	if n == 0 {
		return
	}
	this.stack = this.stack[:n-1]
	this.minStack = this.minStack[:n-1]
}

func (this *MinStack) Top() int {
	n := len(this.stack)
	if n == 0 {
		return 0
	}
	return this.stack[n-1]
}

func (this *MinStack) GetMin() int {
	n := len(this.minStack)
	if n == 0 {
		return 0
	}
	return this.minStack[n-1]
}
```

### 160

- LeetCode: https://leetcode.cn/problems/intersection-of-two-linked-lists/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onesixzero

type ListNode struct {
	Val  int
	Next *ListNode
}

func getIntersectionNode(headA, headB *ListNode) *ListNode {
	if headA == nil || headB == nil {
		return nil
	}

	// 双指针
	tempA, tempB := headA, headB

	// 相当于在链表A的末尾接上链表B，在链表B的末尾接上链表A
	for tempA != tempB {
		if tempA == nil {
			tempA = headB
		} else {
			tempA = tempA.Next
		}
		if tempB == nil {
			tempB = headA
		} else {
			tempB = tempB.Next
		}
	}

	return tempA
}
```

### 169

- LeetCode: https://leetcode.cn/problems/majority-element/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onesixnine

func majorityElement(nums []int) int {
	res, hp := 0, 0

	for _, v := range nums {
		if hp == 0 {
			res, hp = v, 1 // hp为0时初始化
		} else if v == res { // 同数加
			hp++
		} else { // 异数减
			hp--
		}
	}

	return res
}
```

### 189

- LeetCode: https://leetcode.cn/problems/rotate-array/description/?envType=study-plan-v2&envId=top-100-liked

```go
package oneeightnine

func rotate(nums []int, k int) {
	k = k % len(nums)

	reverse(nums)
	reverse(nums[:k])
	reverse(nums[k:])
}

// 反转数组
func reverse(nums []int) {
	for i := 0; i < len(nums)/2; i++ {
		nums[i], nums[len(nums)-1-i] = nums[len(nums)-1-i], nums[i]
	}
}
```

### 198

- LeetCode: https://leetcode.cn/problems/house-robber/description/?envType=study-plan-v2&envId=top-100-liked

```go
package onenineeight

func rob(nums []int) int {
	n := len(nums)
	if n == 0 {
		return 0
	}
	if n == 1 {
		return nums[0]
	}

	one, two := nums[0], max(nums[0], nums[1])
	for i := 2; i < n; i++ {
		temp := one
		one = two
		two = max(two, temp+nums[i])
	}

	return two
}
```

### 199

- LeetCode: https://leetcode.cn/problems/binary-tree-right-side-view/description/?envType=study-plan-v2&envId=top-100-liked

```go
package oneninenine

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// bfs 找每一层的最后一个
func rightSideView(root *TreeNode) []int {
	if root == nil {
		return nil
	}

	q := make([]*TreeNode, 1)
	q[0] = root
	res := []int{}

	for len(q) > 0 {
		n := len(q)
		for i := 0; i < n; i++ {
			node := q[i]
			if node.Left != nil {
				q = append(q, node.Left)
			}
			if node.Right != nil {
				q = append(q, node.Right)
			}
			if i == n-1 {
				res = append(res, node.Val)
			}
		}
		q = q[n:]
	}

	return res
}
```

### 200

- LeetCode: https://leetcode.cn/problems/number-of-islands/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twozerozero

func numIslands(grid [][]byte) int {
	row := len(grid)
	col := len(grid[0])
	res := 0

	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if grid[i][j] == '1' {
				res++
				dfs(grid, i, j)
			}
		}
	}

	return res
}

func dfs(grid [][]byte, i, j int) {
	if i < 0 || i >= len(grid) || j < 0 || j >= len(grid[0]) {
		return
	}
	if grid[i][j] == '0' {
		return
	}

	grid[i][j] = '0'

	// 必须上下左右才能覆盖
	dfs(grid, i-1, j)
	dfs(grid, i+1, j)
	dfs(grid, i, j-1)
	dfs(grid, i, j+1)
}
```

### 206

- LeetCode: https://leetcode.cn/problems/reverse-linked-list/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twozerosix

type ListNode struct {
	Val  int
	Next *ListNode
}

// func reverseList(head *ListNode) *ListNode {
// 	// 递归
// 	if head == nil || head.Next == nil {
// 		return head
// 	}

// 	newHead := reverseList(head.Next)

// 	head.Next.Next = head
// 	head.Next = nil

// 	return newHead
// }

func reverseList(head *ListNode) *ListNode {
	// 迭代
	if head == nil || head.Next == nil {
		return head
	}

	var pre *ListNode
	cur := head

	for cur != nil {
		next := cur.Next
		cur.Next = pre
		pre = cur
		cur = next
	}

	return pre
}
```

### 207

- LeetCode: https://leetcode.cn/problems/course-schedule/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twozeroseven

func canFinish(numCourses int, prerequisites [][]int) bool {
	if len(prerequisites) == 0 {
		return true
	}

	row := len(prerequisites)

	mapCourses := make(map[int][]int) // 先修课 --> 其他课
	input := make(map[int]int)        // 每个节点的入度

	// 初始化每个节点入度为0
	for i := 0; i < numCourses; i++ {
		input[i] = 0
	}
	for i := 0; i < row; i++ {
		mapCourses[prerequisites[i][1]] = append(mapCourses[prerequisites[i][1]], prerequisites[i][0])
		input[prerequisites[i][0]]++
	}

	// bfs
	q := []int{}
	for i := 0; i < numCourses; i++ {
		if input[i] == 0 {
			q = append(q, i)
		}
	}

	for len(q) > 0 {
		n := len(q)
		for i := 0; i < n; i++ {
			for _, value := range mapCourses[q[i]] {
				input[value]--
				if input[value] == 0 {
					q = append(q, value)
				}
			}
		}
		q = q[n:]
	}

	for _, v := range input {
		if v > 0 {
			return false
		}
	}
	return true
}
```

### 208

- LeetCode: https://leetcode.cn/problems/implement-trie-prefix-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twozeroeight

type Trie struct {
	children [26]*Trie
	isEnd    bool
}

func Constructor() Trie {
	return Trie{}
}

func (this *Trie) Insert(word string) {
	node := this
	for _, v := range word {
		v -= 'a'
		if node.children[v] == nil {
			node.children[v] = &Trie{}
		}
		node = node.children[v]
	}
	node.isEnd = true
}

func (this *Trie) Search(word string) bool {
	node := this
	for _, v := range word {
		v -= 'a'
		if node.children[v] == nil {
			return false
		}
		node = node.children[v]
	}
	if node.isEnd {
		return true
	} else {
		return false
	}
}

func (this *Trie) StartsWith(prefix string) bool {
	node := this
	for _, v := range prefix {
		v -= 'a'
		if node.children[v] == nil {
			return false
		}
		node = node.children[v]
	}
	return true
}
```

### 215

- LeetCode: https://leetcode.cn/problems/kth-largest-element-in-an-array/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twoonefive

import "container/heap"

type maxHeap []int

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *maxHeap) Push(x any) {
	*h = append(*h, x.(int))
}
func (h *maxHeap) Pop() any {
	res := (*h)[h.Len()-1]
	*h = (*h)[:h.Len()-1]
	return res
}

func findKthLargest(nums []int, k int) int {
	h := maxHeap{}
	heap.Init(&h)

	for _, v := range nums {
		heap.Push(&h, v)
	}
	res := 0
	for k > 0 {
		res = heap.Pop(&h).(int)
		k--
	}
	return res
}
```

### 226

- LeetCode: https://leetcode.cn/problems/invert-binary-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twotwosix

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func invertTree(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}

	// root.Left = invertTree(root.Right)
	// root.Right = invertTree(root.Left) // 这里的 root.Left 已经被覆盖

	newLeft, newRight := invertTree(root.Right), invertTree(root.Left)
	root.Left, root.Right = newLeft, newRight
	return root
}
```

### 230

- LeetCode: https://leetcode.cn/problems/kth-smallest-element-in-a-bst/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothreezero

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func kthSmallest(root *TreeNode, k int) int {
	res := 0
	dfs(root, &k, &res)
	return res
}

// 中序
func dfs(node *TreeNode, k, res *int) {
	if node == nil {
		return
	}

	dfs(node.Left, k, res)
	*k--
	if *k == 0 {
		*res = node.Val
		return // 找到结果就提前结束递归
	}
	dfs(node.Right, k, res)
}
```

### 234

- LeetCode: https://leetcode.cn/problems/palindrome-linked-list/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothreefour

type ListNode struct {
	Val  int
	Next *ListNode
}

func isPalindrome(head *ListNode) bool {
	// 找中点
	slow, fast := head, head

	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}

	// 反转后半部分链表
	slow = reverse(slow)

	// 比较前半部分和后半部分
	for slow != nil {
		if head.Val != slow.Val {
			return false
		}
		head = head.Next
		slow = slow.Next
	}

	return true
}

func reverse(node *ListNode) *ListNode {
	if node == nil || node.Next == nil {
		return node
	}

	newNode := reverse(node.Next)

	node.Next.Next = node
	node.Next = nil

	return newNode
}
```

### 236

- LeetCode: https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothreesix

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}
	if p == root || q == root {
		return root
	}

	leftD := lowestCommonAncestor(root.Left, p, q)
	rightD := lowestCommonAncestor(root.Right, p, q)

	if leftD != nil && rightD != nil {
		return root
	}
	if leftD == nil {
		return rightD
	}
	if rightD == nil {
		return leftD
	}
	return nil
}
```

### 238

- LeetCode: https://leetcode.cn/problems/product-of-array-except-self/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothreeeight

func productExceptSelf(nums []int) []int {
	preNums := make([]int, len(nums)) // 前缀积
	sufNums := make([]int, len(nums)) // 后缀积
	preNums[0] = 1
	sufNums[len(nums)-1] = 1

	for i := 1; i < len(nums); i++ {
		preNums[i] = preNums[i-1] * nums[i-1]
		sufNums[len(nums)-1-i] = sufNums[len(nums)-i] * nums[len(nums)-i]
	}

	res := make([]int, len(nums))
	for i := 0; i < len(nums); i++ {
		res[i] = preNums[i] * sufNums[i]
	}

	return res
}
```

### 239

- LeetCode: https://leetcode.cn/problems/sliding-window-maximum/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twothreenine

// 2. 双端/单调队列
func maxSlidingWindow(nums []int, k int) []int {
	q := []int{}          // 存储元素索引，保持单调递减
	push := func(i int) { // 保持单调的push
		for len(q) > 0 && nums[i] >= nums[q[len(q)-1]] {
			q = q[:len(q)-1]
		}
		q = append(q, i)
	}

	// 第一组
	for i := 0; i < k; i++ {
		push(i)
	}

	n := len(nums)
	res := []int{}
	res = append(res, nums[q[0]])

	for i := k; i < n; i++ {
		push(i)
		for q[0] <= i-k {
			q = q[1:]
		}
		res = append(res, nums[q[0]])
	}
	return res
}

// 1. 大根堆
// import (
// 	"container/heap"
// )

// type Item struct {
// 	value int
// 	index int
// }

// type MaxHeap []Item

// func (h MaxHeap) Len() int           { return len(h) }
// func (h MaxHeap) Less(i, j int) bool { return h[i].value > h[j].value }
// func (h MaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

// func (h *MaxHeap) Push(x any) {
// 	*h = append(*h, x.(Item))
// }
// func (h *MaxHeap) Pop() any {
// 	x := (*h)[len(*h)-1]
// 	*h = (*h)[:len(*h)-1]
// 	return x
// }

// func maxSlidingWindow(nums []int, k int) []int {
// 	res := []int{}
// 	start := make([]Item, k)
// 	for i := 0; i < k; i++ {
// 		start[i] = Item{value: nums[i], index: i}
// 	}

// 	h := MaxHeap(start)
// 	heap.Init(&h)
// 	maxNum := h[0].value // 只查看堆顶，并不pop
// 	res = append(res, maxNum)

// 	for i := k; i < len(nums); i++ {
// 		heap.Push(&h, Item{value: nums[i], index: i})

// 		// 删除前面已经废用的堆顶元素
// 		for h.Len() > 0 && h[0].index <= i-k {
// 			heap.Pop(&h)
// 		}

// 		res = append(res, h[0].value)
// 	}

// 	return res
// }
```

### 240

- LeetCode: https://leetcode.cn/problems/search-a-2d-matrix-ii/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twofourzero

func searchMatrix(matrix [][]int, target int) bool {
	row := len(matrix)
	col := len(matrix[0])

	// 从右上角开始
	i, j := 0, col-1

	for i < row && j >= 0 {
		if matrix[i][j] == target {
			return true
		} else if matrix[i][j] > target {
			j--
		} else {
			i++
		}
	}

	return false
}
```

### 279

- LeetCode: https://leetcode.cn/problems/perfect-squares/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twosevennine

func numSquares(n int) int {
	dp := make([]int, n+1)

	for i := 1; i < n+1; i++ {
		// 先假设一个最大值
		minn := n + 1
		for j := 1; j*j <= i; j++ {
			minn = min(minn, dp[i-j*j])
		}
		dp[i] = minn + 1
	}

	return dp[n]
}
```

### 283

- LeetCode: https://leetcode.cn/problems/move-zeroes/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twoeightthree

func moveZeroes(nums []int) {
	left, right := 0, 1

	for right < len(nums) {
		// 四种情况
		if nums[left] != 0 && nums[right] != 0 {
			left++
			right++
			continue
		}
		if nums[left] == 0 && nums[right] == 0 {
			right++
			continue
		}
		if nums[right] == 0 {
			left++
			right++
			continue
		}
		if nums[left] == 0 {
			nums[left], nums[right] = nums[right], nums[left]
		}
	}
}
```

### 287

- LeetCode: https://leetcode.cn/problems/find-the-duplicate-number/description/?envType=study-plan-v2&envId=top-100-liked

```go
package twoeightseven

func findDuplicate(nums []int) int {
	// 转换为找环形链表的头

	// 快慢指针相遇
	slow, fast := 0, 0
	for {
		slow = nums[slow]
		fast = nums[nums[fast]]
		if slow == fast {
			break
		}
	}

	// 找环起点
	fast = 0
	for {
		slow = nums[slow]
		fast = nums[fast]
		if slow == fast {
			return slow
		}
	}
}
```

### 322

- LeetCode: https://leetcode.cn/problems/coin-change/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threetwotwo

func coinChange(coins []int, amount int) int {
	dp := make([]int, amount+1)
	// 将所有值设为 amount + 1，相当于“无穷大”，表示该金额暂时无法凑齐
	for i := 1; i < amount+1; i++ {
		dp[i] = amount + 1
	}
	// 凑齐金额 0 所需硬币数为 0
	dp[0] = 0

	for i := 1; i < amount+1; i++ {
		for j := 0; j < len(coins); j++ {
			if i-coins[j] >= 0 {
				dp[i] = min(dp[i], dp[i-coins[j]]+1)
			}
		}
	}

	if dp[amount] == amount+1 {
		return -1
	}
	return dp[amount]
}
```

### 347

- LeetCode: https://leetcode.cn/problems/top-k-frequent-elements/description/?envType=study-plan-v2&envId=top-100-liked

```go
package threefourseven

import "container/heap"

type Item struct {
	value     int
	frequency int
}

type minHeap []Item

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i].frequency < h[j].frequency }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *minHeap) Push(x any) {
	*h = append(*h, x.(Item))
}
func (h *minHeap) Pop() any {
	res := (*h)[h.Len()-1]
	*h = (*h)[:h.Len()-1]
	return res
}

func topKFrequent(nums []int, k int) []int {
	m := map[int]int{}
	for _, v := range nums {
		m[v]++
	}

	h := &minHeap{}
	heap.Init(h)

	for key, value := range m {
		heap.Push(h, Item{key, value})
		if h.Len() > k {
			heap.Pop(h)
		}
	}

	heapLen := h.Len()
	res := make([]int, heapLen)
	for i := 0; i < heapLen; i++ {
		res[i] = heap.Pop(h).(Item).value
	}
	return res
}
```

### 437

- LeetCode: https://leetcode.cn/problems/path-sum-iii/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fourthreeseven

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func pathSum(root *TreeNode, targetSum int) int {
	if root == nil {
		return 0
	}

	res := 0
	dfs(root, targetSum, &res) // 先计算根节点

	// 递归计算整棵树
	res += pathSum(root.Left, targetSum)
	res += pathSum(root.Right, targetSum)
	return res
}

// 从当前节点开始的路径
func dfs(node *TreeNode, nowTarget int, res *int) {
	if node == nil {
		return
	}

	if node.Val == nowTarget {
		*res++
		// return // 不能 return，有负数，所以一条路径可能多次满足要求
	}

	nowTarget -= node.Val

	dfs(node.Left, nowTarget, res)
	dfs(node.Right, nowTarget, res)
}
```

### 438

- LeetCode: https://leetcode.cn/problems/find-all-anagrams-in-a-string/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fourthreeeight

func findAnagrams(s string, p string) []int {
	if len(s) < len(p) {
		return nil
	}

	tempS, tempP := [26]int{}, [26]int{}
	res := []int{}

	for i := 0; i < len(p); i++ {
		tempP[p[i]-'a']++
	}

	left, right := 0, len(p)-1
	for i := left; i <= right; i++ {
		tempS[s[i]-'a']++
	}

	for right < len(s) {
		if tempS == tempP {
			res = append(res, left)
		}

		if right == len(s)-1 {
			break
		}

		// 滑动窗口
		tempS[s[left]-'a']--
		left++
		right++
		tempS[s[right]-'a']++
	}

	return res
}
```

### 543

- LeetCode: https://leetcode.cn/problems/diameter-of-binary-tree/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivefourthree

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// 计算每个节点的左右子树深度和，更新最大值为结果
func diameterOfBinaryTree(root *TreeNode) int {
	res := 0
	dfs(root, &res)
	return res
}

// 在求深度过程中更新 res
func dfs(node *TreeNode, res *int) int {
	if node == nil {
		return 0
	}

	leftH := dfs(node.Left, res)
	rightH := dfs(node.Right, res)

	*res = max(*res, leftH+rightH)

	return max(leftH, rightH) + 1
}
```

### 560

- LeetCode: https://leetcode.cn/problems/subarray-sum-equals-k/description/?envType=study-plan-v2&envId=top-100-liked

```go
package fivesixzero

func subarraySum(nums []int, k int) int {
	// 存在负数，无法使用滑动窗口
	// 前缀和 + 哈希表

	res := 0
	prefixSum := 0
	temp := map[int]int{} // 前缀和 -> 出现次数
	temp[0] = 1           // 前缀和为 0 的情况

	for i := 0; i < len(nums); i++ {
		prefixSum += nums[i]

		if v, ok := temp[prefixSum-k]; ok {
			res += v
		}
		temp[prefixSum]++
	}

	return res
}
```

### 763

- LeetCode: https://leetcode.cn/problems/partition-labels/description/?envType=study-plan-v2&envId=top-100-liked

```go
package sevensixthree

func partitionLabels(s string) []int {
	m := map[byte]int{} // 每个字母对应的最后下标
	for i := 0; i < len(s); i++ {
		m[s[i]] = i
	}

	start, end := 0, 0
	res := []int{}

	for i := 0; i < len(s); i++ {
		end = max(end, m[s[i]])
		if end == i {
			res = append(res, end-start+1)
			start, end = i+1, i+1
		}
	}

	return res
}
```

### 994

- LeetCode: https://leetcode.cn/problems/rotting-oranges/description/?envType=study-plan-v2&envId=top-100-liked

```go
package nineninefour

func orangesRotting(grid [][]int) int {
	row := len(grid)
	col := len(grid[0])
	res := 0

	type pos struct {
		i, j int
	}
	q := []pos{}

	// 先放所有烂橘子
	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if grid[i][j] == 2 {
				q = append(q, pos{i, j})
			}
		}
	}

	// bfs
	for len(q) > 0 {
		n := len(q)

		for i := 0; i < n; i++ {
			p := q[i]
			// 上
			if p.i-1 >= 0 && grid[p.i-1][p.j] == 1 {
				grid[p.i-1][p.j] = 2
				q = append(q, pos{p.i - 1, p.j})
			}
			// 下
			if p.i+1 < row && grid[p.i+1][p.j] == 1 {
				grid[p.i+1][p.j] = 2
				q = append(q, pos{p.i + 1, p.j})
			}
			// 左
			if p.j-1 >= 0 && grid[p.i][p.j-1] == 1 {
				grid[p.i][p.j-1] = 2
				q = append(q, pos{p.i, p.j - 1})
			}
			// 右
			if p.j+1 < col && grid[p.i][p.j+1] == 1 {
				grid[p.i][p.j+1] = 2
				q = append(q, pos{p.i, p.j + 1})
			}
		}
		q = q[n:]
		if len(q) != 0 {
			res++ // 表示这一轮有新的感染者
		}
	}

	// 是否还有好橘子
	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if grid[i][j] == 1 {
				return -1
			}
		}
	}

	return res
}
```


