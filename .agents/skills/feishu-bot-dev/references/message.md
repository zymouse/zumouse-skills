# 消息相关 API

## 发送消息

支持消息类型: text、post、image、file、audio、media、sticker、interactive、share_chat、share_user

```go
import (
    "context"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

req := larkim.NewCreateMessageReqBuilder().
    Body(larkim.NewCreateMessageReqBodyBuilder().
        ReceiveId("ou_xxx").          // 接收者 ID
        MsgType("text").              // 消息类型
        Content(`{"text":"test content"}`).
        Uuid("unique-uuid").          // 可选，防重复
        Build()).
    Build()

resp, err := client.Im.V1.Message.Create(context.Background(), req)
```

## 转发消息

```go
req := larkim.NewForwardMessageReqBuilder().
    Body(larkim.NewForwardMessageReqBodyBuilder().
        ReceiveId("ou_xxx").
        Build()).
    Build()

resp, err := client.Im.V1.Message.Forward(context.Background(), req, messageId)
```

## 合并转发消息

```go
req := larkim.NewMergeForwardMessageReqBuilder().
    Body(larkim.NewMergeForwardMessageReqBodyBuilder().
        ReceiveId("oc_xxx").
        MessageIdList([]string{"om_xxx", "om_yyy"}).
        Build()).
    Build()

resp, err := client.Im.V1.Message.MergeForward(context.Background(), req)
```

## 回复消息

```go
req := larkim.NewReplyMessageReqBuilder().
    Body(larkim.NewReplyMessageReqBodyBuilder().
        Content(`{"text":"reply content"}`).
        MsgType("text").
        ReplyInThread(true).          // 是否以话题形式回复
        Uuid("unique-uuid").
        Build()).
    Build()

resp, err := client.Im.V1.Message.Reply(context.Background(), req, messageId)
```

## 撤回消息

```go
resp, err := client.Im.V1.Message.Delete(context.Background(), messageId)
```

## 添加表情回复

```go
req := larkim.NewCreateMessageReactionReqBuilder().
    Body(larkim.NewCreateMessageReactionReqBodyBuilder().
        ReactionType(larkim.NewEmojiBuilder().
            EmojiType("SMILE").       // 表情类型
            Build()).
        Build()).
    Build()

resp, err := client.Im.V1.MessageReaction.Create(context.Background(), req, messageId)
```

## 消息内容格式

### 文本消息
```json
{"text":"Hello World"}
```

### 富文本消息
```json
{
    "zh_cn": {
        "title": "标题",
        "content": [
            [{"tag": "text", "text": "普通文本"}],
            [{"tag": "a", "href": "https://open.feishu.cn", "text": "链接"}],
            [{"tag": "at", "user_id": "ou_xxx"}]
        ]
    }
}
```
