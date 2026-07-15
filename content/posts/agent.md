---
title: 'Agent'
date: 2026-07-09
lastmod: 2026-07-09
author: "giftia"
description: "从 Function Call 到 A2A，理清 Agent 的核心概念与生态协议。"
draft: false
categories: ["杂谈"]
tags: ["Agent", "LLM", "Function Call", "MCP", "A2A"]
---

Agent 是目前 LLM 应用最核心的范式。简单说，**Agent = LLM + 工具 + 自主决策循环**。

但围绕 Agent 衍生了大量概念——Function Call、MCP、Skills、A2A，很多人搞不清它们分别解决什么问题。这篇就来把这些概念逐一理清。

## Agent 是什么

一句话定义：**让 LLM 在循环中自主调用工具完成任务**。

传统 LLM 使用方式是你问我答，一轮结束。Agent 则是：

1. 接收任务
2. 自己判断需要什么工具
3. 调用工具获取结果
4. 根据结果决定下一步
5. 重复直到任务完成

关键区别在于 **"自主决策"**——LLM 自己决定什么时候停、什么时候继续、调用什么工具。

## Agent 和 Workflow 的区别

这是最容易混淆的两个概念：

| 对比维度 | Agent | Workflow |
|---|---|---|
| 决策方式 | LLM 自主判断下一步 | 预定义步骤，按图执行 |
| 灵活性 | 高，可应对未知情况 | 低，只能走固定路径 |
| 适用场景 | 开放式任务（调研、编码） | 确定性流程（审批、ETL） |
| 可控性 | 较低，结果不完全可预测 | 高，每一步可预期 |

可以这么理解：

- **Workflow** 是"流程图"，你有几条路，都画好了，LLM 只是其中的一个节点。
- **Agent** 是"自主雇员"，你给目标和工具，它自己想办法。

实际项目中两者经常混用：用 Workflow 做主干流程保证可控，关键节点嵌入 Agent 处理灵活子任务。

## Agent 工作模式

Agent 工作模式决定了"怎么决策、怎么执行"。常见五种：

### 1. ReAct

最经典的"边走边看"模式——想一步、做一步、看结果、再想：

```
观察 → 思考 → 行动 → 观察 → 思考 → 行动 → ...
```

适合动态探索型任务，代价是每步都要等 LLM 推理，串行慢。

### 2. Plan-and-Execute

先出完整计划再执行："先画地图再走路"。

```
生成计划 → 执行步骤 1 → 执行步骤 2 → ... → 完成
```

全局观好，但计划是静态的，遇意外不能灵活调整。

### 3. ReWOO

把推理和执行拆分：一次性规划所有工具调用，然后批量并行执行，最后汇总。减少 LLM 推理轮次，适合工具调用间无依赖的场景。

### 4. LLM Compiler

ReWOO 的进阶版——LLM 生成 DAG 描述工具调用依赖关系，最大化并行：

```
A（查天气）──┐
B（查日历）──┼──→ D（汇总建议）
C（查路况）──┘
```

### 5. Reflexion

在 ReAct 基础上加"反思-重试"闭环：执行完后评估结果，不满足则分析失败原因再重试，适合对质量要求高的任务。

### 一句话选型

| 模式 | 特点 | 一句话 |
|---|---|---|
| ReAct | 串行、灵活 | 走一步看一步 |
| Plan-and-Execute | 串行、可预见 | 先画地图再走 |
| ReWOO | 并行、独立 | 一次规划批量执行 |
| LLM Compiler | 并行、有依赖 | 编译成 DAG 再跑 |
| Reflexion | 重试、高质量 | 不满意就反思重来 |

实际框架通常是组合使用：Plan-and-Execute 定主流程，ReAct 执行节点，Reflexion 兜底重试。

## Function Call

**Function Call 是 Agent 调用工具的机制。**

LLM 本身不能执行代码、不能查数据库、不能发 HTTP 请求。Function Call 让 LLM 能够"告诉系统"：我想调用这个函数，参数是这个。

工作流程：

```
User: "上海今天天气怎么样？"

LLM 输出（不是最终回答）:
{
  "function": "get_weather",
  "parameters": { "city": "上海" }
}

系统执行 get_weather("上海")，把结果返回给 LLM

LLM 基于天气数据生成最终回答
```

核心理解：

- Function Call 不是 LLM 在执行函数，是 LLM 在 **声明意图**
- 实际执行由宿主程序（你的代码 / Agent 框架）完成
- LLM 拿到执行结果后继续推理，可能再次发起 Function Call

**注意**：Function Call 只是工具调用协议的一种具体实现（如 OpenAI 的 Function Calling API），不是唯一方案。

## MCP

**MCP（Model Context Protocol）是工具和 LLM 之间的标准化通信协议。**

Function Call 解决了"怎么调用"，但没解决"工具从哪来、怎么统一管理"。MCP 就是来做这件事的。

类比理解：

- Function Call = 打电话的机制（拨号、通话）
- MCP = 统一电话号码本（所有工具按同一标准接入）

MCP 的架构：

```
LLM (Client) ←→ MCP Client ←→ MCP Server ←→ 实际工具/数据源
```

- **MCP Server**：封装工具，暴露标准接口
- **MCP Client**：在 LLM 侧发现并调用工具
- 协议统一后，换工具不需要改 LLM 侧的调用逻辑

实际价值：一次接入 MCP，所有兼容 MCP 的 LLM 客户端都能用你的工具。

## Skills

**Skills 是 Agent 的能力包，包含提示词、工具、知识的组合。**

Skill 不仅仅是一个 Function Call 工具。它通常包含：

- **提示词模板**：告诉 LLM 在什么场景下该怎么做
- **工具绑定**：这个 Skill 能调用哪些 Function / MCP 工具
- **领域知识**：特定场景下的上下文信息

可以这样理解层级关系：

```
Agent
  ├── Skill A（例如：代码审查）
  │     ├── 提示词：审查规则
  │     └── 工具：读文件、Git diff
  ├── Skill B（例如：生成 PPT）
  │     ├── 提示词：排版规范
  │     └── 工具：python-pptx 操作
  └── ...
```

Skills 解决了"Agent 能力复用"的问题——不用每次都从零写 prompt。

## A2A

**A2A（Agent-to-Agent）是 Agent 之间的协作协议。**

当任务复杂到单一 Agent 搞不定时，就需要多个 Agent 协作。A2A 定义了 Agent 之间如何通信：

- **任务分发**：主 Agent 拆解任务，分发给子 Agent
- **消息传递**：Agent 之间传递上下文和结果
- **状态同步**：多个 Agent 共享进展信息

常见模式：

```
主 Agent（协调者）
  ├── 子 Agent 1：负责后端代码
  ├── 子 Agent 2：负责前端代码
  └── 子 Agent 3：负责代码审查
```

A2A 当前还没有像 MCP 那样成熟的标准协议，更多是各 Agent 框架自行实现的协作机制。但它解决的问题是明确的：**单个 Agent 有上下文窗口、专注度的上限，多 Agent 协作是规模化必经之路。**

## 核心总结

1. **Agent** 是顶层范式，让 LLM 在循环中自主决策
2. **Function Call** 是工具调用的具体机制
3. **MCP** 让工具接入标准化，一次开发到处使用
4. **Skills** 封装经验为可复用能力包
5. **A2A** 解决多 Agent 协作问题

## 什么时候该用 Agent

并不是所有场景都需要 Agent：

- **简单问答 / 分类 / 摘要**：单轮 LLM 调用就够了，不需要 Agent
- **固定流程（审批 / ETL）**：用 Workflow 更可靠
- **开放式任务（调研 / 编码 / 排查）**：Agent 价值最大

原则：**能用确定性逻辑解决的问题，不要引入不确定性**。Agent 的灵活性是用可控性换来的，在需要它的时候再用。
