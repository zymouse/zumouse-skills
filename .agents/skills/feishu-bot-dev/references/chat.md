# 群聊管理 API

## 创建群聊

```go
req := larkim.NewCreateChatReqBuilder().
    UserIdType("open_id").
    Body(larkim.NewCreateChatReqBodyBuilder().
        Name("群聊名称").
        Description("群聊描述").
        UserIdList([]string{"ou_xxx", "ou_yyy"}).  // 初始成员
        Build()).
    Build()

resp, err := client.Im.Chat.Create(context.Background(), req)
// resp.Data.ChatId - 群聊 ID
```

## 获取群聊信息

```go
req := larkim.NewGetChatReqBuilder().
    ChatId("oc_xxx").
    Build()

resp, err := client.Im.Chat.Get(context.Background(), req)
// resp.Data.Name - 群聊名称
// resp.Data.Description - 群聊描述
// resp.Data.OwnerId - 群主 ID
```

## 更新群聊信息

```go
req := larkim.NewUpdateChatReqBuilder().
    ChatId("oc_xxx").
    Body(larkim.NewUpdateChatReqBodyBuilder().
        Name("新群聊名称").
        Description("新群聊描述").
        Build()).
    Build()

resp, err := client.Im.Chat.Update(context.Background(), req)
```

## 获取群聊历史消息

```go
req := larkim.NewListMessageReqBuilder().
    ContainerIdType("chat").          // 容器类型: chat-群聊
    ContainerId("oc_xxx").
    Build()

resp, err := client.Im.Message.List(context.Background(), req)

for _, item := range resp.Data.Items {
    senderId := *item.Sender.Id
    content := *item.Body.Content
    createTime := *item.CreateTime
    // 处理消息...
}
```

## 添加群成员

```go
req := larkim.NewCreateChatMemberReqBuilder().
    MemberIdType("open_id").
    ChatId("oc_xxx").
    Body(larkim.NewCreateChatMemberReqBodyBuilder().
        IdList([]string{"ou_xxx", "ou_yyy"}).
        Build()).
    Build()

resp, err := client.Im.ChatMember.Create(context.Background(), req)
```

## 删除群成员

```go
req := larkim.NewDeleteChatMemberReqBuilder().
    MemberIdType("open_id").
    ChatId("oc_xxx").
    Body(larkim.NewDeleteChatMemberReqBodyBuilder().
        IdList([]string{"ou_xxx"}).
        Build()).
    Build()

resp, err := client.Im.ChatMember.Delete(context.Background(), req)
```

## 解散群聊

```go
resp, err := client.Im.Chat.Delete(context.Background(), "oc_xxx")
```

## 群聊类型

| 类型 | 说明 |
|------|------|
| p2p | 单聊 |
| group | 普通群聊 |
| topic_group | 话题群 |

## 成员 ID 类型

| 类型 | 说明 |
|------|------|
| open_id | 开放 ID（推荐）|
| user_id | 用户 ID |
| union_id | 统一 ID |
| app_id | 应用 ID |
