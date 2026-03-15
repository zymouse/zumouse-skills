# Session、Turn、Step 管理指南

本文档详细介绍 Kimi Agent SDK for Go 中 Session、Turn 和 Step 的管理机制。

---

## 目录

- [Session 管理](#session-管理)
- [Turn 管理](#turn-管理)
- [Step 管理](#step-管理)
- [完整示例](#完整示例)
- [最佳实践](#最佳实践)

---

## Session 管理

Session 代表与 Kimi CLI 的连接，是所有对话的入口。

### 创建 Session

```go
session, err := kimi.NewSession(options...)
if err != nil {
    panic(err)
}
defer session.Close()
```

### 配置选项

| 选项 | 说明 |
|------|------|
| `kimi.WithAPIKey(key)` | 设置 API key |
| `kimi.WithBaseURL(url)` | 设置 API 端点 |
| `kimi.WithModel(model)` | 设置模型名称 |
| `kimi.WithWorkDir(dir)` | 设置工作目录 |
| `kimi.WithAutoApprove()` | 自动批准所有请求 |
| `kimi.WithThinking(bool)` | 启用/禁用思考模式 |
| `kimi.WithTools(tools...)` | 注册外部工具 |

### 核心方法

| 方法 | 说明 |
|------|------|
| `session.Prompt(ctx, content)` | 发起一轮对话，返回 `*Turn` |
| `session.Close()` | 关闭会话，清理资源 |

### 斜杠命令

Session 初始化后，可通过 `session.SlashCommands` 获取支持的斜杠命令：

```go
for _, cmd := range session.SlashCommands {
    fmt.Printf("Command: %s, Description: %s\n", cmd.Name, cmd.Description)
}
```

### 内部机制

- **生命周期**：通过 `context.Context` 管理
- **并发控制**：使用 `sync.RWMutex` 保护共享状态
- **取消管理**：维护 `cancellers` 列表跟踪可取消的操作
- **协议版本**：支持 Wire Protocol 1.1+，自动初始化外部工具

---

## Turn 管理

Turn 代表一轮完整的对话往返（用户输入 -> AI 处理 -> 响应完成）。

### 创建 Turn

```go
// 方式1：通过 Session 创建
turn, err := session.Prompt(ctx, content)

// 方式2：单轮快捷方式（自动管理 Session）
singleTurn, err := kimi.Prompt(ctx, content, options...)
```

### 核心属性

```go
type Turn struct {
    Steps <-chan *Step    // Step 通道，接收对话步骤
}
```

### 核心方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `turn.ID()` | `uint64` | 获取 Turn 的唯一标识 |
| `turn.Err()` | `error` | 获取执行过程中的错误 |
| `turn.Result()` | `wire.PromptResult` | 获取最终结果 |
| `turn.Usage()` | `*Usage` | 获取 Token 使用统计 |
| `turn.Cancel()` | `error` | 取消当前 Turn |

### PromptResult 状态

```go
const (
    PromptResultStatusPending         = "pending"           // 进行中
    PromptResultStatusFinished        = "finished"          // 已完成
    PromptResultStatusCancelled       = "cancelled"         // 已取消
    PromptResultStatusMaxStepsReached = "max_steps_reached" // 达到最大步数
    PromptResultStatusUnexpectedEOF   = "unexpected_eof"    // 意外结束
)
```

### Usage 统计

```go
type Usage struct {
    Context float64      // 上下文使用量
    Tokens  TokenUsage   // Token 统计
}

type TokenUsage struct {
    InputOther         int  // 普通输入 Token 数
    Output             int  // 输出 Token 数
    InputCacheRead     int  // 缓存读取 Token 数
    InputCacheCreation int  // 缓存创建 Token 数
}
```

获取使用统计：

```go
usage := turn.Usage()
if usage != nil {
    fmt.Printf("Input: %d, Output: %d\n", 
        usage.Tokens.InputOther, usage.Tokens.Output)
}
```

### 生命周期事件

| 事件 | 说明 |
|------|------|
| `TurnBegin` | Turn 开始 |
| `TurnEnd` | Turn 结束 |

### 取消 Turn

```go
// 方式1：直接取消
turn.Cancel()

// 方式2：通过 Context 取消
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
turn, err := session.Prompt(ctx, content)
```

---

## Step 管理

Step 是 Turn 内部的执行步骤，每个 Turn 可能包含多个 Step。

### Step 结构

```go
type Step struct {
    n        int               // Step 序号（从1开始）
    Messages <-chan wire.Message  // 消息通道
}
```

### 遍历 Step

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        // 处理消息
    }
}
```

### Step 生命周期事件

| 事件类型 | 说明 |
|---------|------|
| `EventTypeStepBegin` | Step 开始 |
| `EventTypeStepInterrupted` | Step 被中断 |

### 消息类型

#### Event 类型（信息性，无需响应）

| 消息类型 | 说明 |
|---------|------|
| `wire.ContentPart` | 文本/思考/媒体内容 |
| `wire.ToolCall` | 工具调用 |
| `wire.ToolResult` | 工具执行结果 |
| `wire.StatusUpdate` | 状态更新（Token 使用等） |
| `wire.ToolCallPart` | 工具调用参数片段 |
| `wire.SubagentEvent` | 子代理事件 |
| `wire.CompactionBegin/CompactionEnd` | 压缩开始/结束 |

#### Request 类型（需要响应）

| 消息类型 | 说明 |
|---------|------|
| `wire.ApprovalRequest` | 需要用户批准 |
| `wire.ToolCallRequest` | 外部工具调用请求（SDK 自动处理） |

### ContentPart 类型

```go
const (
    ContentPartTypeText     = "text"      // 文本
    ContentPartTypeThink    = "think"     // 思考内容
    ContentPartTypeImageURL = "image_url" // 图片
    ContentPartTypeAudioURL = "audio_url" // 音频
    ContentPartTypeVideoURL = "video_url" // 视频
)
```

处理 ContentPart：

```go
if cp, ok := msg.(wire.ContentPart); ok {
    switch cp.Type {
    case wire.ContentPartTypeText:
        fmt.Printf("[Text] %s\n", cp.Text.Value)
    case wire.ContentPartTypeThink:
        fmt.Printf("[Thinking] %s\n", cp.Think.Value)
    case wire.ContentPartTypeImageURL:
        fmt.Printf("[Image] %s\n", cp.ImageURL.Value.URL)
    }
}
```

### 处理 ApprovalRequest

```go
if req, ok := msg.(wire.ApprovalRequest); ok {
    // 必须响应，否则会阻塞
    req.Respond(wire.ApprovalRequestResponseApprove)
    // 或：wire.ApprovalRequestResponseReject
    // 或：wire.ApprovalRequestResponseApproveForSession
}
```

### 处理 ToolCall

```go
if tc, ok := msg.(wire.ToolCall); ok {
    fmt.Printf("Tool called: %s, Args: %s\n", 
        tc.Function.Name, tc.Function.Arguments.Value)
}
```

---

## 完整示例

### 基础示例

```go
package main

import (
    "context"
    "fmt"
    "os"

    kimi "github.com/MoonshotAI/kimi-agent-sdk/go"
    "github.com/MoonshotAI/kimi-agent-sdk/go/wire"
)

func main() {
    // 创建 Session
    session, err := kimi.NewSession(
        kimi.WithAPIKey(os.Getenv("KIMI_API_KEY")),
        kimi.WithModel("kimi-k2-thinking-turbo"),
    )
    if err != nil {
        panic(err)
    }
    defer session.Close()

    // 发起对话
    turn, err := session.Prompt(context.Background(), 
        wire.NewStringContent("Hello!"))
    if err != nil {
        panic(err)
    }

    // 遍历 Steps 和 Messages
    for step := range turn.Steps {
        for msg := range step.Messages {
            switch m := msg.(type) {
            case wire.ContentPart:
                if m.Type == wire.ContentPartTypeText {
                    fmt.Print(m.Text.Value)
                }
            case wire.ApprovalRequest:
                m.Respond(wire.ApprovalRequestResponseApprove)
            }
        }
    }

    // 检查错误
    if err := turn.Err(); err != nil {
        panic(err)
    }

    // 获取使用统计
    usage := turn.Usage()
    if usage != nil {
        fmt.Printf("\nTokens used: Input=%d, Output=%d\n", 
            usage.Tokens.InputOther, usage.Tokens.Output)
    }
}
```

### 带思考模式的示例

```go
session, err := kimi.NewSession(
    kimi.WithAPIKey(os.Getenv("KIMI_API_KEY")),
    kimi.WithThinking(true),
)
if err != nil {
    panic(err)
}
defer session.Close()

turn, err := session.Prompt(context.Background(), 
    wire.NewStringContent("Solve this problem step by step"))
if err != nil {
    panic(err)
}

for step := range turn.Steps {
    for msg := range step.Messages {
        if cp, ok := msg.(wire.ContentPart); ok {
            switch cp.Type {
            case wire.ContentPartTypeThink:
                fmt.Printf("[Thinking] %s\n", cp.Think.Value)
            case wire.ContentPartTypeText:
                fmt.Printf("[Response] %s\n", cp.Text.Value)
            }
        }
    }
}
```

### 带超时的示例

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

turn, err := session.Prompt(ctx, wire.NewStringContent("Long task..."))
if err != nil {
    panic(err)
}

for step := range turn.Steps {
    for msg := range step.Messages {
        // 处理消息...
    }
}
```

---

## 最佳实践

### 1. 资源管理

始终使用 `defer session.Close()` 确保资源释放：

```go
session, err := kimi.NewSession(options...)
if err != nil {
    return err
}
defer session.Close()
```

### 2. 顺序执行

`Prompt` 必须顺序调用，等待前一个 Turn 完成：

```go
// 正确
turn1, _ := session.Prompt(ctx, content1)
for step := range turn1.Steps { /* ... */ }

turn2, _ := session.Prompt(ctx, content2)
for step := range turn2.Steps { /* ... */ }

// 错误 - 不要并发调用
go session.Prompt(ctx, content1)
go session.Prompt(ctx, content2)
```

### 3. 消费所有消息

必须消费完所有消息才能开始新的 Turn：

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        // 处理所有消息
    }
}
// 现在可以开始新的 Turn
```

### 4. 响应 ApprovalRequest

必须对 `ApprovalRequest` 调用 `Respond()`，否则会阻塞：

```go
if req, ok := msg.(wire.ApprovalRequest); ok {
    req.Respond(wire.ApprovalRequestResponseApprove)
}
```

### 5. 错误处理

始终检查 `turn.Err()` 获取执行错误：

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        // 处理消息
    }
}

if err := turn.Err(); err != nil {
    // 处理错误
}
```

### 6. 取消管理

取消当前 Turn 后才能开始新的 Turn：

```go
// 取消当前 Turn
turn.Cancel()

// 或等待超时
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
turn, _ := session.Prompt(ctx, content)
```

### 7. 单轮快捷方式

对于单轮对话，使用 `kimi.Prompt()` 简化代码：

```go
singleTurn, err := kimi.Prompt(ctx, content, options...)
if err != nil {
    panic(err)
}
defer singleTurn.Close() // 自动关闭 Session

for step := range singleTurn.Steps {
    // 处理消息
}
```
