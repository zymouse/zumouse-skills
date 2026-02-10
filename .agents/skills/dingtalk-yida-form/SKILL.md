---
name: dingtalk-yida-form
description: 钉钉宜搭(YiDa)云表单实例的增删查改操作。Use when user needs to interact with DingTalk YiDa form instances via Go API, including creating, reading, updating, deleting form data, batch operations, querying form instances, updating sub-tables, or managing form data programmatically.
---

# DingTalk YiDa Form Skill

钉钉宜搭云表单实例的 Go API 操作指南。

## Quick Start

### 1. 安装依赖

```bash
go get github.com/alibabacloud-go/dingtalk/yida_2_0
go get github.com/alibabacloud-go/darabonba-openapi/v2/client
go get github.com/alibabacloud-go/tea-utils/v2/service
go get github.com/alibabacloud-go/tea/tea
```

### 2. 初始化客户端

```go
import (
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
    "github.com/alibabacloud-go/tea/tea"
)

func CreateClient() (*yida_2_0.Client, error) {
    config := &openapi.Config{}
    config.Protocol = tea.String("https")
    config.RegionId = tea.String("central")
    return yida_2_0.NewClient(config)
}
```

### 3. 通用调用模式

所有 API 调用遵循以下模式：

```go
// 1. 创建客户端
client, err := CreateClient()

// 2. 设置请求头（包含 AccessToken）
headers := &yida_2_0.XXXHeaders{}
headers.XAcsDingtalkAccessToken = tea.String("<access_token>")

// 3. 构建请求参数
request := &yida_2_0.XXXRequest{
    AppType:     tea.String("APP_XXXXX"),
    SystemToken: tea.String("xxxxx"),
    UserId:      tea.String("user123"),
    FormUuid:    tea.String("FORM-XXXXX"),
    // ... 其他参数
}

// 4. 执行调用
response, err := client.XXXWithOptions(request, headers, &util.RuntimeOptions{})
```

## Core Operations

### 创建表单实例

使用 `SaveFormData` 创建新实例：

```go
request := &yida_2_0.SaveFormDataRequest{
    AppType:      tea.String("APP_XXX"),
    SystemToken:  tea.String("token"),
    UserId:       tea.String("user123"),
    FormUuid:     tea.String("FORM-XXX"),
    FormDataJson: tea.String(`{"textField_xxx": "value"}`),
}
response, err := client.SaveFormDataWithOptions(request, headers, &util.RuntimeOptions{})
```

### 查询表单实例列表

使用 `SearchFormDatas` 查询多条数据：

```go
request := &yida_2_0.SearchFormDatasRequest{
    AppType:         tea.String("APP_XXX"),
    SystemToken:     tea.String("token"),
    FormUuid:        tea.String("FORM-XXX"),
    CurrentPage:     tea.Int32(1),
    PageSize:        tea.Int32(10),
    SearchFieldJson: tea.String(`{"textField_xxx": "searchValue"}`),
}
response, err := client.SearchFormDatasWithOptions(request, headers, &util.RuntimeOptions{})
```

### 查询单条表单数据

使用 `GetFormDataByID` 根据实例ID查询：

```go
request := &yida_2_0.GetFormDataByIDRequest{
    AppType:     tea.String("APP_XXX"),
    SystemToken: tea.String("token"),
    UserId:      tea.String("user123"),
    FormUuid:    tea.String("FORM-XXX"),
    UseAlias:    tea.Bool(true),
}
// formInstId 作为路径参数
response, err := client.GetFormDataByIDWithOptions(
    tea.String("FORM_INST_12345"),
    request,
    headers,
    &util.RuntimeOptions{},
)
```

### 更新表单数据

使用 `UpdateFormData` 更新现有实例：

```go
request := &yida_2_0.UpdateFormDataRequest{
    AppType:          tea.String("APP_XXX"),
    SystemToken:      tea.String("token"),
    UserId:           tea.String("user123"),
    FormInstanceId:   tea.String("FORM_INST_12345"),
    UpdateFormDataJson: tea.String(`{"textField_xxx": "newValue"}`),
    UseLatestVersion: tea.Bool(false),
}
response, err := client.UpdateFormDataWithOptions(request, headers, &util.RuntimeOptions{})
```

### 删除表单数据

使用 `DeleteFormData` (yida_1_0) 删除实例：

```go
import "github.com/alibabacloud-go/dingtalk/yida_1_0"

request := &yida_1_0.DeleteFormDataRequest{
    AppType:        tea.String("APP_XXX"),
    SystemToken:    tea.String("token"),
    UserId:         tea.String("user123"),
    FormInstanceId: tea.String("FORM_INST_12345"),
}
response, err := client.DeleteFormDataWithOptions(request, headers, &util.RuntimeOptions{})
```

## Version Selection

钉钉宜搭 API 有两个版本，根据操作类型选择：

| 操作类型 | 推荐版本 | 原因 |
|---------|---------|------|
| 单条 CRUD | yida_2_0 | 功能更完善，支持更多参数 |
| 批量操作 | yida_1_0 | 批量 API 仅在 1.0 中提供 |
| 删除操作 | yida_1_0 | DeleteFormData 仅在 1.0 中提供 |

## Common Parameters

所有 API 共用的核心参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `X-Acs-Dingtalk-Access-Token` | Header | 是 | 钉钉访问令牌 |
| `AppType` | Body | 是 | 应用类型/ID，如 APP_XXXXX |
| `SystemToken` | Body | 是 | 系统令牌 |
| `UserId` | Body | 是 | 操作用户ID |
| `FormUuid` | Body | 是 | 表单UUID，如 FORM-XXXXX |
| `Language` | Body | 否 | 语言，默认 zh_CN |

## Error Handling

统一错误处理模式：

```go
tryErr := func()(_e error) {
    defer func() {
        if r := tea.Recover(recover()); r != nil {
            _e = r
        }
    }()
    _, err = client.XXXWithOptions(request, headers, &util.RuntimeOptions{})
    return err
}()

if tryErr != nil {
    var sdkErr = &tea.SDKError{}
    if t, ok := tryErr.(*tea.SDKError); ok {
        sdkErr = t
        // sdkErr.Code 和 sdkErr.Message 包含错误详情
    }
}
```

## References

- **完整 API 列表和参数说明**: 见 [references/api-reference.md](references/api-reference.md)
- **详细代码示例**: 见 [references/code-examples.md](references/code-examples.md)
