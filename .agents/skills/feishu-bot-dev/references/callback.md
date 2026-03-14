# 回调处理

## WebSocket 长连接模式（推荐）

WebSocket 模式优势：
- 无需公网 IP 或域名
- 无需内网穿透工具
- SDK 封装鉴权逻辑
- 无需处理解密和验签

### 接收消息事件

```go
import (
    "context"
    "fmt"
    larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
    larkevent "github.com/larksuite/oapi-sdk-go/v3/event"
    "github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
    larkws "github.com/larksuite/oapi-sdk-go/v3/ws"
)

func main() {
    eventHandler := dispatcher.NewEventDispatcher("", "").
        OnP2MessageReceiveV1(func(ctx context.Context, event *larkim.P2MessageReceiveV1) error {
            fmt.Printf("[OnP2MessageReceiveV1], data: %s\n", larkcore.Prettify(event))
            
            // 获取消息内容
            msg := event.Event.Message
            chatId := *msg.ChatId
            content := *msg.Content
            
            // 处理消息...
            
            return nil
        }).
        OnCustomizedEvent("out_approval", func(ctx context.Context, event *larkevent.EventReq) error {
            // 自定义事件
            fmt.Printf("[OnCustomizedEvent], data: %s\n", string(event.Body))
            return nil
        })

    cli := larkws.NewClient("APP_ID", "APP_SECRET",
        larkws.WithEventHandler(eventHandler),
        larkws.WithLogLevel(larkcore.LogLevelDebug),
    )

    err := cli.Start(context.Background())
    if err != nil {
        panic(err)
    }
}
```

### 处理卡片回调

```go
import (
    "context"
    "fmt"
    larkcard "github.com/larksuite/oapi-sdk-go/v3/card"
    larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
    larkws "github.com/larksuite/oapi-sdk-go/v3/ws"
)

func main() {
    cardHandler := larkcard.NewCardActionHandler("", "", func(ctx context.Context, data *larkcard.CardAction) (interface{}, error) {
        fmt.Printf("[CardAction], data: %s\n", larkcore.Prettify(data))
        
        // 获取操作值
        actionValue := data.Action.Value["key"]
        openChatId := data.OpenChatId
        openUserId := data.OpenUserId
        
        // 处理卡片交互...
        
        // 返回更新后的卡片（可选）
        return nil, nil
    })

    cli := larkws.NewClient("APP_ID", "APP_SECRET",
        larkws.WithEventHandler(cardHandler),
        larkws.WithLogLevel(larkcore.LogLevelDebug),
    )

    cli.Start(context.Background())
}
```

### 组合事件和卡片处理

```go
import (
    "context"
    "fmt"
    larkcard "github.com/larksuite/oapi-sdk-go/v3/card"
    larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
    "github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
    larkws "github.com/larksuite/oapi-sdk-go/v3/ws"
)

func main() {
    // 事件处理器
    eventHandler := dispatcher.NewEventDispatcher("", "").
        OnP2MessageReceiveV1(func(ctx context.Context, event *larkim.P2MessageReceiveV1) error {
            fmt.Printf("[Message], data: %s\n", larkcore.Prettify(event))
            return nil
        })

    // 卡片处理器
    cardHandler := larkcard.NewCardActionHandler("", "", func(ctx context.Context, data *larkcard.CardAction) (interface{}, error) {
        fmt.Printf("[Card], data: %s\n", larkcore.Prettify(data))
        return nil, nil
    })

    // 创建组合处理器
    cli := larkws.NewClient("APP_ID", "APP_SECRET",
        larkws.WithEventHandler(eventHandler),
        larkws.WithLogLevel(larkcore.LogLevelDebug),
    )

    cli.Start(context.Background())
}
```

## HTTP Webhook 模式

生产环境推荐使用 Webhook，需要配置公网地址并处理签名验证。

```go
import (
    "net/http"
    larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
    "github.com/larksuite/oapi-sdk-go/v3/core/httpserverext"
    larkevent "github.com/larksuite/oapi-sdk-go/v3/event"
    "github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
)

func main() {
    eventHandler := dispatcher.NewEventDispatcher(VerificationToken, EncryptKey).
        OnP2MessageReceiveV1(DoP2ImMessageReceiveV1)

    cardHandler := larkcard.NewCardActionHandler(VerificationToken, EncryptKey, DoInteractiveCard)

    http.HandleFunc("/event", httpserverext.NewEventHandlerFunc(eventHandler,
        larkevent.WithLogLevel(larkcore.LogLevelDebug)))
    http.HandleFunc("/card", httpserverext.NewCardActionHandlerFunc(cardHandler,
        larkevent.WithLogLevel(larkcore.LogLevelDebug)))

    http.ListenAndServe(":7777", nil)
}
```

## 回调事件类型

| 事件 | 说明 |
|------|------|
| OnP2MessageReceiveV1 | 接收消息 v2.0 |
| OnP2CardActionTrigger | 卡片回传交互 |
| OnP2CardURLPreviewGet | 拉取链接预览数据 |
| OnCustomizedEvent | 自定义事件 |
