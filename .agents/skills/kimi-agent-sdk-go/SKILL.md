---
name: kimi-agent-sdk-go
description: Kimi Agent SDK for Go 开发指南。Use when user needs to develop Go applications using the Kimi Agent SDK, including creating sessions, sending prompts, handling responses, managing external tools, approval requests, thinking mode, turn cancellation, or tracking usage and costs.
---

# Kimi Agent SDK for Go

Go SDK for programmatically controlling Kimi Agent sessions via the kimi-cli.

> **架构说明**：SDK 通过启动 `kimi-cli` 子进程，使用 JSON-RPC 2.0 协议进行通信。

## Quick Start

```bash
go get github.com/MoonshotAI/kimi-agent-sdk/go
```

**Prerequisites**: `kimi` CLI in PATH, `KIMI_API_KEY` env var set (or use `kimi.Option`)

```go
session, err := kimi.NewSession(
    kimi.WithAPIKey(os.Getenv("KIMI_API_KEY")),
    kimi.WithModel("kimi-k2-thinking-turbo"),
)
if err != nil { panic(err) }
defer session.Close()

turn, err := session.Prompt(context.Background(), wire.NewStringContent("Hello!"))
if err != nil { panic(err) }

for step := range turn.Steps {
    for msg := range step.Messages {
        if cp, ok := msg.(wire.ContentPart); ok && cp.Type == wire.ContentPartTypeText {
            fmt.Print(cp.Text.Value)
        }
    }
}

if err := turn.Err(); err != nil { panic(err) }
```

## Core Concepts

```
Session (会话)
├── Turn 1 (对话回合)
│   ├── Step 1 (执行步骤) → Messages
│   └── Step 2 → Messages
└── Turn 2 → ...
```

| Component | Description | Key Methods |
|-----------|-------------|-------------|
| `Session` | CLI 连接入口 | `Prompt()`, `Close()`, `SlashCommands` |
| `Turn` | 一轮对话往返 | `Steps`, `Err()`, `Result()`, `Usage()`, `Cancel()` |
| `Step` | Turn 内执行步骤 | `Messages` (channel) |

**PromptResult Status**: `pending`, `finished`, `cancelled`, `max_steps_reached`, `unexpected_eof`

## Configuration

```go
kimi.WithAPIKey(key)        // API key
kimi.WithBaseURL(url)       // API endpoint
kimi.WithModel(model)       // Model name
kimi.WithWorkDir(dir)       // Working directory
kimi.WithAutoApprove()      // Auto-approve all requests
kimi.WithThinking(bool)     // Enable/disable thinking mode
kimi.WithTools(tools...)    // Register external tools
```

See [references/configuration.md](references/configuration.md) for details.

## Message Types

**Events** (informational, no response needed):
- `wire.ContentPart` - Text/Think/Image/Audio/Video
- `wire.ToolCall` / `ToolCallPart` - Tool invocation
- `wire.ToolResult` - Tool execution result
- `wire.StatusUpdate` - Token usage stats

**Requests** (must call `Respond()`):
- `wire.ApprovalRequest` - Requires user approval
- `wire.ToolCallRequest` - External tool call (auto-handled)

See [references/message-types.md](references/message-types.md) for complete guide.

## Common Patterns

### Handle Approval Requests

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        if req, ok := msg.(wire.ApprovalRequest); ok {
            req.Respond(wire.ApprovalRequestResponseApprove)
            // Or: ResponseReject, ResponseApproveForSession
        }
    }
}
```

### Thinking Mode

```go
session, _ := kimi.NewSession(kimi.WithThinking(true))
// Check: cp.Type == wire.ContentPartTypeThink
```

### External Tools

```go
tool, _ := kimi.CreateTool(
    func(args MyArgs) (string, error) { return result, nil },
    kimi.WithName("my_tool"),
    kimi.WithDescription("Tool description"),
)
session, _ := kimi.NewSession(kimi.WithTools(tool))
```

### Cancel Turn

```go
turn.Cancel()
// Or: ctx, cancel := context.WithTimeout(...)
```

### Usage Tracking

```go
usage := turn.Usage()
// usage.Tokens.InputOther, Output, InputCacheRead, InputCacheCreation
```

## Important Notes

1. **Sequential**: Call `Prompt` sequentially, wait for previous turn to complete
2. **Cleanup**: Always `defer session.Close()`
3. **Consume All**: Must consume all messages before new turn
4. **Respond**: Must call `Respond()` for `ApprovalRequest`
5. **Cancel**: Cancel or consume current turn before starting new one

## References

- [Quick Start](references/quickstart.md) - Detailed getting started
- [Configuration](references/configuration.md) - All options
- [Message Types](references/message-types.md) - Complete message reference
- [Session/Turn/Step](references/session-turn-step-management.md) - Lifecycle management
- [External Tools](references/external-tools.md) - Tool creation guide
- [Approval Requests](references/approval-requests.md) - Handling approvals
- [Thinking](references/thinking.md) - Reasoning process
- [Turn Cancellation](references/turn-cancellation.md) - Cancel patterns
- [Costs and Usage](references/costs-and-usage.md) - Token tracking
- [Kimi CLI Manual](references/kimi-cli-manual.md) - CLI reference
- [Go Source](references/go-src/) - SDK source code


