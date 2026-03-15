# Kimi Agent SDK - 消息类型速查表

## 概述

本文档详细列出了 Kimi Agent SDK (`wire` 包) 中所有的消息类型，按来源分类，帮助开发者理解 Agent 与大模型之间的通信机制。


---

## 一、大模型 (LLM) 发出的消息

> 这些消息通过 MCP 协议从 Kimi 大模型发送到 Agent/SDK

| 消息类型 | 用途 | 来源 | 方向 | 关键字段 |
|---------|------|------|------|---------|
| `ContentPart` (Think) | 模型的思考过程（内部推理） | 大模型 | → Agent | `Type="think"`, `Think` |
| `ContentPart` (Text) | 模型的最终文本回复 | 大模型 | → Agent | `Type="text"`, `Text` |
| `ContentPart` (ImageURL) | 图片 URL 输出 | 大模型 | → Agent | `Type="image_url"`, `ImageURL` |
| `ContentPart` (AudioURL) | 音频 URL 输出 | 大模型 | → Agent | `Type="audio_url"`, `AudioURL` |
| `ContentPart` (VideoURL) | 视频 URL 输出 | 大模型 | → Agent | `Type="video_url"`, `VideoURL` |
| `ToolCall` | 请求调用外部工具 | 大模型 | → Agent → Skill | `ID`, `Function.Name`, `Arguments` |
| `ToolCallPart` | 工具参数的分片传输（流式） | 大模型 | → Agent | `ArgumentsPart` |

---

## 二、Agent/SDK 发出的消息

> 这些消息由 Agent 或 SDK 主动发出，用于控制流程、返回结果或请求审批

| 消息类型 | 用途 | 来源 | 方向 | 关键字段 |
|---------|------|------|------|---------|
| `TurnBegin` | 标记一个对话回合开始 | Agent/SDK | → 大模型 | `UserInput` |
| `TurnEnd` | 标记一个对话回合结束 | Agent/SDK | → 大模型 | - |
| `StepBegin` | 标记一个执行步骤开始 | Agent/SDK | → 大模型 | `N` (步骤序号) |
| `StepInterrupted` | 标记步骤被中断 | Agent/SDK | → 大模型 | - |
| `ToolResult` | 返回工具执行结果给大模型 | Agent/SDK | → 大模型 | `ToolCallID`, `ReturnValue` |
| `StatusUpdate` | 报告 Token 使用等状态信息 | Agent/SDK | → 用户 | `TokenUsage`, `ContextUsage` |
| `CompactionBegin` | 上下文压缩开始（优化内存） | Agent/SDK | → 大模型 | - |
| `CompactionEnd` | 上下文压缩结束 | Agent/SDK | → 大模型 | - |
| `SubagentEvent` | 子 Agent 的事件通知 | Agent/SDK | → 大模型 | `TaskToolCallID`, `Event` |
| `ApprovalRequest` | 请求用户审批敏感操作 | Agent/SDK | → 用户 | `Action`, `Description` |
| `ToolCallRequest` | 向外部服务发起工具调用 | Agent/SDK | → 外部服务 | `ID`, `Name`, `Arguments` |

---

## 三、用户发出的消息

> 这些消息由用户（或用户代码）主动发起

| 消息类型 | 用途 | 来源 | 方向 | 关键字段 |
|---------|------|------|------|---------|
| `Prompt` (初始输入) | 用户的初始问题/指令 | 用户 | → Agent → 大模型 | 通过 `session.Prompt()` 发送 |
| `ApprovalResponse` | 用户对审批请求的响应 | 用户 | → Agent → 大模型 | `RequestID`, `Response` |

---

## 四、Skill/外部服务发出的消息

> 这些消息由 Skill 工具或外部服务执行后返回

| 消息类型 | 用途 | 来源 | 方向 | 关键字段 |
|---------|------|------|------|---------|
| `Tool Execution Result` | Skill 工具执行后的原始结果 | Skill | → Agent | 被封装为 `ToolResult` |

---

## MCP 协议核心消息对

| 请求方 | 请求消息 | 响应方 | 响应消息 | 说明 |
|-------|---------|-------|---------|------|
| 大模型 | `ToolCall` | Agent/SDK | `ToolResult` | 工具调用与结果返回 |
| 大模型 | `ToolCallPart` (流式) | - | - | 工具参数分片传输 |
| Agent/SDK | `ToolCallRequest` | 外部服务 | 执行结果 | 外部工具调用 |
| Agent/SDK | `ApprovalRequest` | 用户 | `ApprovalResponse` | 敏感操作审批 |

---

## 消息类型图标对照

| 图标 | 消息类型 | 说明 |
|-----|---------|------|
| 🚀 | `TurnBegin` | 回合开始 |
| 🏁 | `TurnEnd` | 回合结束 |
| 🔄 | `StepBegin` | 步骤开始 |
| ⛔ | `StepInterrupted` | 步骤中断 |
| 🤔 | `ContentPart` (Think) | 思考过程 |
| 📝 | `ContentPart` (Text) | 文本回复 |
| 🖼️ | `ContentPart` (ImageURL) | 图片 |
| 🔧 | `ToolCall` / `ToolCallPart` | 工具调用 |
| ✅ | `ToolResult` | 工具结果 |
| ⚠️ | `ApprovalRequest` | 审批请求 |
| 👍/👎 | `ApprovalResponse` | 审批响应 |
| 📊 | `StatusUpdate` | 状态更新 |
| 🗜️ | `CompactionBegin/End` | 上下文压缩 |
| 📦 | `SubagentEvent` | 子 Agent 事件 |
| 🔌 | `ToolCallRequest` | 外部工具调用 |

---

## 关键设计要点

| 设计 | 说明 |
|-----|------|
| **双向通信** | 大模型和 Agent 通过 MCP 协议双向交互 |
| **流式传输** | `ToolCallPart` 支持大数据分片，避免阻塞 |
| **请求-响应匹配** | `ToolCall.ID` 与 `ToolResult.ToolCallID` 一一对应 |
| **安全审批** | `ApprovalRequest` 机制保护敏感操作 |
| **生命周期管理** | `Turn` 和 `Step` 明确界定执行范围 |

---

## 参考

- `wire` 包源码: `go/wire/message.go`
- MCP 协议文档: [Model Context Protocol](https://modelcontextprotocol.io/)
