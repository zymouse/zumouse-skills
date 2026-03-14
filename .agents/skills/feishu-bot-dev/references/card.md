# 卡片消息

## 发送卡片消息

```go
import (
    "context"
    "io/ioutil"
    "strings"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

// 从文件加载卡片模板
cardJSON, _ := ioutil.ReadFile("card.json")
card := string(cardJSON)

// 替换变量
card = strings.Replace(card, "${image_key}", imageKey, -1)
card = strings.Replace(card, "${button_name}", "确认", -1)

req := larkim.NewCreateMessageReqBuilder().
    ReceiveIdType("chat_id").
    Body(larkim.NewCreateMessageReqBodyBuilder().
        ReceiveId("oc_xxx").
        MsgType("interactive").
        Content(card).
        Build()).
    Build()

resp, err := client.Im.V1.Message.Create(context.Background(), req)
```

## 卡片模板示例

```json
{
  "config": {
    "wide_screen_mode": true
  },
  "header": {
    "template": "red",
    "title": {
      "tag": "plain_text",
      "content": "报警通知"
    }
  },
  "elements": [
    {
      "tag": "div",
      "fields": [
        {
          "is_short": true,
          "text": {
            "tag": "lark_md",
            "content": "**时间：**\n2024-01-01 12:00:00"
          }
        },
        {
          "is_short": true,
          "text": {
            "tag": "lark_md",
            "content": "**级别：**\nP0"
          }
        }
      ]
    },
    {
      "tag": "img",
      "img_key": "img_xxx",
      "alt": {
        "tag": "plain_text",
        "content": "图片"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "确认"
          },
          "type": "primary",
          "value": {
            "key": "confirm"
          }
        }
      ]
    }
  ]
}
```

## 卡片组件类型

| 组件 | tag | 说明 |
|------|-----|------|
| 标题 | header | 卡片顶部标题栏 |
| 文本 | div | 普通文本区域 |
| 图片 | img | 图片展示 |
| 按钮 | button | 交互按钮 |
| 分割线 | hr | 水平分割线 |
| 备注 | note | 底部备注信息 |
| 下拉选择 | select_static | 静态选项下拉框 |
| 输入框 | input | 文本输入框 |

## 颜色模板

| 模板值 | 颜色 |
|--------|------|
| red | 红色（警告）|
| orange | 橙色（提醒）|
| yellow | 黄色 |
| green | 绿色（成功）|
| blue | 蓝色（信息）|
| indigo | 靛蓝 |
| purple | 紫色 |
| grey | 灰色 |

## 按钮类型

| 类型 | 说明 |
|------|------|
| primary | 主按钮（实心）|
| default | 默认按钮（描边）|
| danger | 危险按钮（红色）|
| text | 文本按钮 |

## 处理卡片回调

```go
import (
    "context"
    larkcard "github.com/larksuite/oapi-sdk-go/v3/card"
)

cardHandler := larkcard.NewCardActionHandler("", "", func(ctx context.Context, data *larkcard.CardAction) (interface{}, error) {
    // 获取操作值
    actionKey := data.Action.Value["key"]
    
    switch actionKey {
    case "confirm":
        // 处理确认操作
        // 可以返回新的卡片内容更新消息
        return newCardJSON, nil
    case "cancel":
        // 处理取消操作
        return nil, nil
    }
    
    return nil, nil
})
```

## 更新卡片消息

```go
// 在回调处理中返回新的卡片 JSON 即可更新消息
func handleCardAction(ctx context.Context, data *larkcard.CardAction) (interface{}, error) {
    // 构建新的卡片内容
    newCard := `{
        "config": {"wide_screen_mode": true},
        "header": {
            "template": "green",
            "title": {"tag": "plain_text", "content": "已处理"}
        },
        "elements": [
            {"tag": "div", "text": {"tag": "plain_text", "content": "问题已解决"}}
        ]
    }`
    
    return newCard, nil
}
```
