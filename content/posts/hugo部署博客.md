---
title: 'Hugo部署博客'
date: 2026-01-03
lastmod: 2026-01-03
author: "giftia"
description: ""
draft: false
categories: ["未分类"]
tags: []
---

## 前置条件

- 安装hugo
- 有github

## 步骤

1. 初始化（博客主题可替换）

```bash
hugo new site quickstart
cd quickstart
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml
hugo server
```

2. 新文章

```bash
hugo new content/posts/my-first-post.md
```

3. 运行（-D包含草稿）

```bash
hugo server -D
```

4. 部署

可以参考我的github，实现自动发布，giftia_blog是博客主题，hch1212.github.io是./public文件夹（展示主体）

部署yaml文件参考
```yaml
name: 发布Hugo网站到Pages（跨仓库）

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      # 步骤1：检出源码仓库（giftia_blog）的代码（含主题子模块）
      - name: 检出Hugo源码
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      # 步骤2：安装指定版本 Hugo 0.154.1
      - name: 安装Hugo 0.154.1
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.154.1'
          # extended: true  # 需SCSS/SASS支持时取消注释

      # 步骤3：构建Hugo产物（生成public目录）
      - name: 构建Hugo网站
        run: hugo --minify

      # 步骤4：跨仓库部署到 hch1212.github.io 仓库（已修正参数名）
      - name: 部署到Pages仓库
        uses: peaceiris/actions-gh-pages@v4
        with:
          # 关键修正：参数名改为 personal_token（对应 v4 版本要求）
          personal_token: ${{ secrets.TOKEN }}
          # 保持你的 Pages 仓库地址不变
          external_repository: HCH1212/hch1212.github.io
          # 部署到 Pages 仓库的 main 分支不变
          publish_branch: main
          # Hugo 构建产物目录不变
          publish_dir: ./public
          # 部署提交信息不变
          commit_message: "Deploy from giftia_blog: ${{ github.sha }}"
```

5. 其他

配置文件参考：
```yaml
# ===============================
# 基础配置
# ===============================
baseURL: "https://hch1212.github.io/"
languageCode: "zh-CN"
title: "giftiaのblog"
theme: "paper"

# 核心功能
enableInlineShortcodes: true
ignoreErrors: ["error-remote-getjson"]
enableGitInfo: true  # 配合 lastmod 使用

# ===============================
# 自动日期更新逻辑 (解决 lastmod 不更新)
# ===============================
frontmatter:
  lastmod: [":fileModTime", "lastmod", ":git", "date"]
  date: ["date", "publishDate", "lastmod"]

# ===============================
# 分页与 URL
# ===============================
pagination:
  pagerSize: 5

permalinks:
  posts: "/posts/:year/:month/:slug/"

# ===============================
# 主题参数（Paper 专用）
# ===============================
params:
  # 风格：linen / wheat / gray / light
  color: "linen"

  # 个人信息
  avatar: "https://hch1212.github.io/images/giftia.png"
  name: "giftia"
  bio: "大切な人といつかまた巡り会えますように。"

  # 社交媒体
  github: "hch1212"
  rss: true

  # 功能开关
  disableHLJS: false            # 代码高亮
  disablePostNavigation: true   # 上/下一篇文章导航
  monoDarkIcon: true            # 暗色模式下单色图标
  showSummary: true             # 首页显示摘要

  # 数学公式
  math: true
  localKatex: false             # 使用 CDN

  # 静态资源
  gravatarCdn: "https://cdn.v2ex.com/gravatar/"
  favicon: "favicon.ico"
  appleTouchIcon: "apple-touch-icon.png"
  direction: "ltr"

  # 评论
  giscus:
    repo: "HCH1212/giftia_blog"
    repoId: "R_kgDOQycHqg"
    category: "Announcements"
    categoryId: "DIC_kwDOQycHqs4C0hEV"
    mapping: "pathname"
    strict: "0"
    reactionsEnabled: "1"
    emitMetadata: "0"
    inputPosition: "bottom"
    theme: "preferred_color_scheme"
    lang: "zh-CN"
    loading: "lazy"

# ===============================
# Markdown 渲染
# ===============================
markup:
  goldmark:
    renderer:
      unsafe: true # 允许 Markdown 中使用 HTML
  highlight:
    noClasses: false

# ===============================
# 顶部导航菜单
# ===============================
menu:
  main:
    - identifier: "loves"
      name: "Loves"
      url: "/loves/"
      weight: 30
    - identifier: "links"
      name: "Links"
      url: "/links/"
      weight: 20
    - identifier: "archives"
      name: "Archives"
      url: "/archives/"
      weight: 10
    - identifier: "gallery"
      name: "Gallery"
      url: "/gallery/"
      weight: 40
    - identifier: "about"
      name: "About"
      url: "/about/"
      weight: 50

# ===============================
# 分类系统
# ===============================
taxonomies:
  category: "categories"
  tag: "tags"

```

主题的其他设置可以查看相关主题的文档
