---
title: 'Go的singleflight'
date: 2026-07-14
lastmod: 2026-07-14
author: "giftia"
description: "golang.org/x/sync/singleflight 的原理、用法及在防止缓存击穿场景的实践"
draft: false
categories: ["Go"]
tags: ["go", "singleflight", "concurrency", "cache", "thundering-herd"]
---

## 作用

`golang.org/x/sync/singleflight` 用于**合并同一个 key 的并发请求**：当多个 goroutine 并发调用同一个 key 的函数时，只有第一个真正执行，其余等待共享结果。

## 核心 API

```go
// Group 代表一个 singleflight 分组，不同 key 的请求隔离
var g singleflight.Group

// Do：同步调用，key 相同时只执行一次 fn，返回共享结果
val, err, shared := g.Do("key", func() (any, error) {
    return fetchFromDB(), nil
})
// shared 为 true 表示结果被其他调用者共享

// DoChan：异步版本，返回 channel
ch := g.DoChan("key", func() (any, error) {
    return fetchFromDB(), nil
})
result := <-ch

// Forget：删除 key 对应的已缓存结果，下次 Do 会重新执行 fn
g.Forget("key")
```

## 典型场景：防止缓存击穿

```go
var g singleflight.Group

func GetArticle(ctx context.Context, id int64) (*Article, error) {
    // 先查 Redis 缓存
    cacheKey := fmt.Sprintf("article:%d", id)
    val, err := redis.Get(ctx, cacheKey)
    if err == nil {
        return parseArticle(val), nil
    }

    // 缓存未命中，用 singleflight 合并去数据库的请求
    // 同一篇文章 1000 个并发请求只会触发 1 次 DB 查询
    v, err, _ := g.Do(cacheKey, func() (any, error) {
        // 可能第一个请求查了 Redis 也没有，所以这里再次 double-check
        // 也可以省略，取决于是否需要
        article, err := db.QueryArticle(ctx, id)
        if err != nil {
            return nil, err
        }
        // 写入缓存
        redis.Set(ctx, cacheKey, serialize(article), 10*time.Minute)
        return article, nil
    })
    if err != nil {
        return nil, err
    }
    return v.(*Article), nil
}
```

## vs 加锁排队

防止缓存击穿的另一种常见方案是**加锁排队**——缓存未命中时抢锁，抢到的负责查库回种，没抢到的等锁释放后重试读缓存：

```go
func GetArticle(ctx context.Context, id int64) (*Article, error) {
    cacheKey := fmt.Sprintf("article:%d", id)
    val, err := redis.Get(ctx, cacheKey)
    if err == nil {
        return parseArticle(val), nil
    }

    lockKey := fmt.Sprintf("lock:article:%d", id)
    lock, err := redis.Lock(ctx, lockKey, 5*time.Second)
    if err != nil {
        time.Sleep(50 * time.Millisecond)
        return GetArticle(ctx, id) // 重试读缓存
    }
    defer lock.Unlock()

    // 双检
    if val, err := redis.Get(ctx, cacheKey); err == nil {
        return parseArticle(val), nil
    }
    return db.QueryArticle(ctx, id)
}
```

| 维度 | singleflight | 加锁排队 |
|------|-------------|---------|
| 作用范围 | **进程内**，合并同进程的 goroutine | **跨进程**，收敛所有服务实例 |
| 实现复杂度 | 一行 `g.Do()`，零依赖 | 需要 Redis/etcd + 锁超时 + 双检 |
| 性能开销 | 纯内存，纳秒级 | 网络往返，毫秒级 |
| 可靠性 | 进程挂了重启就行 | 锁超时短了误放行，长了堵死后续请求 |
| 正确性 | WaitGroup 天然保证 | 必须双检，缺了就重复查库 |

**结论**：单实例服务 singleflight 完全够用；多实例场景 singleflight 也能先收敛 80%~90% 的重复请求（每实例只发 1 次），再叠加分布式锁可收敛到全集群只发 1 次。大多数场景不值得为剩余几次重复查询引入分布式锁的复杂度。

## 原理

```go
// 简化版实现，辅助理解核心逻辑
type call struct {
    wg  sync.WaitGroup // 用于等待 fn 执行完成
    val any
    err error
}

type Group struct {
    mu sync.Mutex
    m  map[string]*call // key → 正在执行的调用
}

func (g *Group) Do(key string, fn func() (any, error)) (any, error, bool) {
    g.mu.Lock()
    if g.m == nil {
        g.m = make(map[string]*call)
    }
    // 已有正在进行中的调用 → 等结果
    if c, ok := g.m[key]; ok {
        g.mu.Unlock()
        c.wg.Wait()
        return c.val, c.err, true // shared = true
    }
    // 第一个调用者 → 新建 call 并执行
    c := new(call)
    c.wg.Add(1)
    g.m[key] = c
    g.mu.Unlock()

    c.val, c.err = fn()
    c.wg.Done()

    // 执行完毕，从 map 中删除，后续新请求可重新执行
    g.mu.Lock()
    delete(g.m, key)
    g.mu.Unlock()

    return c.val, c.err, false
}
```

核心思路：
1. 用 `sync.WaitGroup` 让后续调用者等待首次执行的结果
2. 首次执行完成后，从 map 中删除 `call`，后续新到来的请求可以重新触发新的执行
3. 返回 `shared` 布尔值让调用方知道结果来自共享还是自己执行

## 注意事项

- **key 粒度**：key 决定了合并范围。key 太粗会合并不相关的请求，key 太细则失去效果。建议用**业务标识 + 参数**作为 key
- **结果缓存时效**：单次请求内有效，结果返回后 key 即被清除。如果需要更长的缓存，自行配合本地缓存或 Redis
- **不要在 fn 内部死循环**：会造成所有等待的 goroutine 永久阻塞
- **Forget 的时机**：失败场景下可调用 `Forget` 让后续请求重试，而不是返回共享的 error
