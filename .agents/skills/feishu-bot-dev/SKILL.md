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

### 使用长连接接收事件

#### 注意事项

在开始配置之前，你需要确保已了解以下注意事项：

- 长连接模式仅支持企业自建应用。商店应用事件订阅方式参考将事件发送至开发者服务器。
- 长连接模式下接收到消息后，需要在 3 秒内处理完成且不抛出异常，否则会触发超时重推机制。
- 每个应用最多建立 50 个连接（在配置长连接时，每初始化一个 client 就是一个连接）。
- 长连接模式的消息推送为集群模式，不支持广播，即如果同一应用部署了多个客户端（client），那么只有其中随机一个客户端会收到消息。

#### 开发流程

1. 构建 API Client 用于调用 OpenAPI。
2. 通过 `dispatcher.NewEventDispatcher` 注册事件处理器，接收消息事件（`OnP2MessageReceiveV1`），并解析数据。
3. 检查消息类型是否为纯文本消息（text），是则进行下一步，不是则提示用户需要发送文本消息。
4. 通过判断条件 `if *event.Event.Message.ChatType == "p2p"` 区分单聊与群聊。
5. 如果是单聊（p2p），则调用发送消息接口向对应用户发送消息。
   如果是群聊，则调用回复消息接口，回复用户在群组内 @机器人的消息。
6. 配置长连接功能，并关联事件处理器。长连接用于建立项目与开放平台的数据连接通道，用于订阅、接收事件。

#### 完整示例代码

```go
package main

import (
        "context"
        "encoding/json"
        "fmt"
        "os"

        lark "github.com/larksuite/oapi-sdk-go/v3"
        larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
        "github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
        larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
        larkws "github.com/larksuite/oapi-sdk-go/v3/ws"
)

func main() {
        app_id := os.Getenv("APP_ID")
        app_secret := os.Getenv("APP_SECRET")

        /**
         * 创建 LarkClient 对象，用于请求OpenAPI。
         * Create LarkClient object for requesting OpenAPI
         */
        client := lark.NewClient(app_id, app_secret)

        /**
         * 注册事件处理器。
         * Register event handler.
         */
        eventHandler := dispatcher.NewEventDispatcher("", "").
                /**
                 * 注册接收消息事件，处理接收到的消息。
                 * Register event handler to handle received messages.
                 * https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
                 */
                OnP2MessageReceiveV1(func(ctx context.Context, event *larkim.P2MessageReceiveV1) error {
                        fmt.Printf("[OnP2MessageReceiveV1 access], data: %s\n", larkcore.Prettify(event))
                        /**
                         * 解析用户发送的消息。
                         * Parse the message sent by the user.
                         */
                        var respContent map[string]string
                        err := json.Unmarshal([]byte(*event.Event.Message.Content), &respContent)
                        /**
                         * 检查消息类型是否为文本
                         * Check if the message type is text
                         */
                        if err != nil || *event.Event.Message.MessageType != "text" {
                                respContent = map[string]string{
                                        "text": "解析消息失败，请发送文本消息\nparse message failed, please send text message",
                                }
                        }

                        /**
                         * 构建回复消息
                         * Build reply message
                         */
                        content := larkim.NewTextMsgBuilder().
                                TextLine("收到你发送的消息: " + respContent["text"]).
                                TextLine("Received message: " + respContent["text"]).
                                Build()

                        if *event.Event.Message.ChatType == "p2p" {
                                /**
                                 * 使用SDK调用发送消息接口。 Use SDK to call send message interface.
                                 * https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
                                 */
                                resp, err := client.Im.Message.Create(context.Background(), larkim.NewCreateMessageReqBuilder().
                                        ReceiveIdType(larkim.ReceiveIdTypeChatId). // 消息接收者的 ID 类型，设置为会话ID。 ID type of the message receiver, set to chat ID.
                                        Body(larkim.NewCreateMessageReqBodyBuilder().
                                                MsgType(larkim.MsgTypeText).            // 设置消息类型为文本消息。 Set message type to text message.
                                                ReceiveId(*event.Event.Message.ChatId). // 消息接收者的 ID 为消息发送的会话ID。 ID of the message receiver is the chat ID of the message sending.
                                                Content(content).
                                                Build()).
                                        Build())

                                if err != nil || !resp.Success() {
                                        fmt.Println(err)
                                        fmt.Println(resp.Code, resp.Msg, resp.RequestId())
                                        return nil
                                }

                        } else {
                                /**
                                 * 使用SDK调用回复消息接口。 Use SDK to call send message interface.
                                 * https://open.feishu.cn/document/server-docs/im-v1/message/reply
                                 */
                                resp, err := client.Im.Message.Reply(context.Background(), larkim.NewReplyMessageReqBuilder().
                                        MessageId(*event.Event.Message.MessageId).
                                        Body(larkim.NewReplyMessageReqBodyBuilder().
                                                MsgType(larkim.MsgTypeText). // 设置消息类型为文本消息。 Set message type to text message.
                                                Content(content).
                                                Build()).
                                        Build())
                                if err != nil || !resp.Success() {
                                        fmt.Printf("logId: %s, error response: \n%s", resp.RequestId(), larkcore.Prettify(resp.CodeError))
                                        return nil
                                }
                        }

                        return nil
                })

        /**
         * 启动长连接，并注册事件处理器。
         * Start long connection and register event handler.
         */
        cli := larkws.NewClient(app_id, app_secret,
                larkws.WithEventHandler(eventHandler),
                larkws.WithLogLevel(larkcore.LogLevelDebug),
        )
        err := cli.Start(context.Background())
        if err != nil {
                panic(err)
        }
}
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
