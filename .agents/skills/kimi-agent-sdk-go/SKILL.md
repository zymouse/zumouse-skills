---
name: kimi-agent-sdk-go
description: Kimi Agent SDK for Go 开发指南。Use when user needs to develop Go applications using the Kimi Agent SDK, including creating sessions, sending prompts, handling responses, managing external tools, approval requests, thinking mode, turn cancellation, or tracking usage and costs.
---

# Kimi Agent SDK for Go

Go SDK for programmatically controlling Kimi Agent sessions via the kimi-cli.

## Quick Start

### Installation

```bash
go get github.com/MoonshotAI/kimi-agent-sdk/go
```

### Prerequisites

- `kimi` CLI installed and available in PATH
- `KIMI_BASE_URL`, `KIMI_API_KEY`, `KIMI_MODEL_NAME` environment variables set, or use `kimi.Option`

### Basic Usage

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
    session, err := kimi.NewSession(
        kimi.WithAPIKey(os.Getenv("KIMI_API_KEY")),
        kimi.WithModel("kimi-k2-thinking-turbo"),
    )
    if err != nil {
        panic(err)
    }
    defer session.Close()

    turn, err := session.Prompt(context.Background(), 
        wire.NewStringContent("Hello!"))
    if err != nil {
        panic(err)
    }

    for step := range turn.Steps {
        for msg := range step.Messages {
            if cp, ok := msg.(wire.ContentPart); ok && cp.Type == wire.ContentPartTypeText {
                fmt.Print(cp.Text.Value)
            }
        }
    }

    if err := turn.Err(); err != nil {
        panic(err)
    }
}
```

## Core Concepts

### Session

A `Session` represents a connection to the Kimi CLI:

```go
session, err := kimi.NewSession(options...)
defer session.Close()
```

### Turn

A `Turn` represents a single conversation round-trip:

```go
turn, err := session.Prompt(ctx, content)
```

Key methods:
- `turn.Steps` - Channel for receiving steps
- `turn.Err()` - Returns any error that occurred
- `turn.Result()` - Returns the final prompt result
- `turn.Usage()` - Returns token usage statistics
- `turn.Cancel()` - Cancels the current turn

### Step and Messages

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        // Process messages
    }
}
```

## Configuration Options

| Option | Description |
|--------|-------------|
| `kimi.WithAPIKey(key)` | Set API key |
| `kimi.WithBaseURL(url)` | Set API endpoint |
| `kimi.WithModel(model)` | Set model name |
| `kimi.WithWorkDir(dir)` | Set working directory |
| `kimi.WithAutoApprove()` | Auto-approve all requests |
| `kimi.WithThinking(bool)` | Enable/disable thinking mode |
| `kimi.WithTools(tools...)` | Register external tools |

See [references/configuration.md](references/configuration.md) for complete configuration guide.

## Message Types

**Events** (informational):
- `wire.ContentPart` - Text, thinking, or media content
- `wire.ToolCall` - Tool invocation
- `wire.ToolResult` - Tool execution result
- `wire.StatusUpdate` - Usage statistics

**Requests** (require response):
- `wire.ApprovalRequest` - Requires user approval

## External Tools

Create tools from Go functions:

```go
// Define argument struct
type WeatherArgs struct {
    Location string `json:"location" description:"City name"`
    Unit     string `json:"unit,omitempty" description:"Temperature unit"`
}

// Create tool
tool, err := kimi.CreateTool(
    func(args WeatherArgs) (string, error) {
        return fmt.Sprintf("Weather in %s: 22°C", args.Location), nil
    },
    kimi.WithName("get_weather"),
    kimi.WithDescription("Get current weather"),
)

// Register with session
session, err := kimi.NewSession(kimi.WithTools(tool))
```

See [references/external-tools.md](references/external-tools.md) for complete guide.

## Approval Requests

Handle requests requiring user approval:

```go
for step := range turn.Steps {
    for msg := range step.Messages {
        if req, ok := msg.(wire.ApprovalRequest); ok {
            // Must respond to avoid blocking
            req.Respond(wire.ApprovalRequestResponseApprove)
            // Or: wire.ApprovalRequestResponseReject
            // Or: wire.ApprovalRequestResponseApproveForSession
        }
    }
}
```

See [references/approval-requests.md](references/approval-requests.md) for details.

## Thinking Mode

Access model's reasoning process:

```go
session, err := kimi.NewSession(
    kimi.WithThinking(true),
)

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

See [references/thinking.md](references/thinking.md) for details.

## Turn Cancellation

Cancel a turn and continue the session:

```go
// Method 1: Direct cancel
turn.Cancel()

// Method 2: Context cancellation
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
```

See [references/turn-cancellation.md](references/turn-cancellation.md) for details.

## Usage Tracking

Track token consumption:

```go
usage := turn.Usage()
if usage != nil {
    fmt.Printf("Input: %d, Output: %d\n", 
        usage.Tokens.InputOther, usage.Tokens.Output)
}
```

See [references/costs-and-usage.md](references/costs-and-usage.md) for details.

## Examples

Example programs available in `assets/examples/`:

- `contributor-hunter/` - Basic SDK usage with auto-approve
- `anime-recognizer/` - Multimodal (vision) with external tools
- `rumor-buster/` - External tools for structured data collection
- `ralph-loop/` - Iterative agent pattern with verification

## Important Notes

1. **Sequential Prompts**: Call `Prompt` sequentially. Wait for previous turn to complete.
2. **Resource Cleanup**: Always use `defer session.Close()`.
3. **Consume All Messages**: Must consume all messages before starting new turn.
4. **Respond to Requests**: Must call `Respond()` for `ApprovalRequest` messages.
5. **Cancellation**: Cancel or consume current turn before starting new one.

## Reference Documentation

- [Quick Start](references/quickstart.md) - Detailed getting started guide
- [Configuration](references/configuration.md) - All configuration options
- [External Tools](references/external-tools.md) - Creating and using tools
- [Approval Requests](references/approval-requests.md) - Handling approvals
- [Thinking](references/thinking.md) - Accessing reasoning process
- [Turn Cancellation](references/turn-cancellation.md) - Canceling turns
- [Costs and Usage](references/costs-and-usage.md) - Tracking tokens
