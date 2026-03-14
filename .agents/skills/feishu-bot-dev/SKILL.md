---
name: feishu-bot-dev
description: 飞书机器人开发指南，支持 Go SDK。Use when user needs to develop Feishu/Lark bots using Go SDK, including authentication, sending messages, handling callbacks/events, managing chats, uploading files, or any Feishu bot development tasks.
---

# 飞书机器人开发指南

本 Skill 提供飞书机器人开发的完整指南，基于 Go SDK (`github.com/larksuite/oapi-sdk-go/v3`)。

## 快速开始

### 1. 环境准备

```bash
# 安装 Go SDK
go get -u github.com/larksuite/oapi-sdk-go/v3@latest
```

### 2. 创建 Client

```go
import lark "github.com/larksuite/oapi-sdk-go/v3"

client := lark.NewClient("YOUR_APP_ID", "YOUR_APP_SECRET")
```

### 3. 核心开发流程

```
1. 获取访问凭证 → 2. 发送/接收消息 → 3. 处理回调事件
```

## 功能模块

| 功能 | 说明 | 参考文档 |
|------|------|----------|
| 认证 | 获取 tenant_access_token / app_access_token | [references/auth.md](references/auth.md) |
| 消息 | 发送、转发、回复、撤回消息 | [references/message.md](references/message.md) |
| 文件 | 上传、下载文件和图片 | [references/file.md](references/file.md) |
| 回调处理 | WebSocket 长连接接收事件 | [references/callback.md](references/callback.md) |
| 群聊管理 | 创建群、获取历史消息、更新群信息 | [references/chat.md](references/chat.md) |
| 卡片消息 | 发送交互式卡片 | [references/card.md](references/card.md) |

## 常用代码模板

### 发送文本消息

```go
import (
    "context"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

req := larkim.NewCreateMessageReqBuilder().
    Body(larkim.NewCreateMessageReqBodyBuilder().
        ReceiveId("ou_xxx").          // 用户 open_id
        MsgType("text").
        Content(`{"text":"Hello World"}`).
        Build()).
    Build()

resp, err := client.Im.V1.Message.Create(context.Background(), req)
```

### WebSocket 接收消息

```go
import (
    "context"
    larkevent "github.com/larksuite/oapi-sdk-go/v3/event"
    "github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
    larkws "github.com/larksuite/oapi-sdk-go/v3/ws"
)

eventHandler := dispatcher.NewEventDispatcher("", "").
    OnP2MessageReceiveV1(func(ctx context.Context, event *larkim.P2MessageReceiveV1) error {
        // 处理消息
        return nil
    })

cli := larkws.NewClient("APP_ID", "APP_SECRET",
    larkws.WithEventHandler(eventHandler),
)
cli.Start(context.Background())
```

## 完整示例

查看 [assets/example/](assets/example/) 目录获取完整项目示例：

- `main.go` - 主程序入口，包含 HTTP 服务和 WebSocket 初始化
- `im.go` - IM 功能封装（消息、群聊、卡片）
- `card.json` - 卡片消息模板

## 开发注意事项

1. **Token 有效期**: tenant_access_token 和 app_access_token 有效期为 2 小时，建议缓存并在过期前刷新
2. **消息 ID 类型**: 支持 open_id、user_id、union_id、chat_id、email 等多种 ID 类型
3. **回调安全**: 生产环境使用 Webhook 时需验证签名，测试环境可用 WebSocket 简化开发
4. **错误处理**: 始终检查 `resp.Success()` 和 `resp.CodeError`

## 参考资源

- 飞书开放平台文档: https://open.feishu.cn/document/
- Go SDK GitHub: https://github.com/larksuite/oapi-sdk-go
