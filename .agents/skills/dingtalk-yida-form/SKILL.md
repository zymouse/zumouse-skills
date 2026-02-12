---
name: dingtalk-yida-form
description: 钉钉宜搭(YiDa)云表单实例的增删查改操作。Use when user needs to interact with DingTalk YiDa form instances via Go or Python API, including creating, reading, updating, deleting form data, batch operations, querying form instances, updating sub-tables, or managing form data programmatically.
---

# DingTalk YiDa Form Skill

钉钉宜搭云表单实例的 Go/Python API 操作指南。

## Quick Start

### Go

#### 1. 安装依赖

```bash
go get github.com/alibabacloud-go/dingtalk/yida_2_0
go get github.com/alibabacloud-go/darabonba-openapi/v2/client
go get github.com/alibabacloud-go/tea-utils/v2/service
go get github.com/alibabacloud-go/tea/tea
```

#### 2. 初始化客户端

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

### Python

#### 1. 安装依赖

```bash
pip install alibabacloud_dingtalk
```

#### 2. 初始化客户端

```python
from alibabacloud_dingtalk.yida_2_0.client import Client as dingtalkyida_2_0Client
from alibabacloud_tea_openapi import models as open_api_models

config = open_api_models.Config()
config.protocol = 'https'
config.region_id = 'central'
client = dingtalkyida_2_0Client(config)
```

## Core Operations

### 创建表单实例

**Go:**
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

**Python:**
```python
from alibabacloud_dingtalk.yida_2_0 import models as dingtalkyida__2__0_models

request = dingtalkyida__2__0_models.SaveFormDataRequest(
    app_type='APP_XXX',
    system_token='token',
    user_id='user123',
    form_uuid='FORM-XXX',
    form_data_json='{"textField_xxx": "value"}'
)
response = client.save_form_data_with_options(request, headers, util_models.RuntimeOptions())
```

### 查询表单实例列表

**Go:**
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

**Python:**
```python
request = dingtalkyida__2__0_models.SearchFormDatasRequest(
    app_type='APP_XXX',
    system_token='token',
    form_uuid='FORM-XXX',
    current_page=1,
    page_size=10,
    search_field_json='{"textField_xxx": "searchValue"}'
)
response = client.search_form_datas_with_options(request, headers, util_models.RuntimeOptions())
```

### 更新表单数据

**Go:**
```go
request := &yida_2_0.UpdateFormDataRequest{
    AppType:            tea.String("APP_XXX"),
    SystemToken:        tea.String("token"),
    UserId:             tea.String("user123"),
    FormInstanceId:   tea.String("FORM_INST_12345"),
    UpdateFormDataJson: tea.String(`{"textField_xxx": "newValue"}`),
    UseLatestVersion: tea.Bool(false),
}
response, err := client.UpdateFormDataWithOptions(request, headers, &util.RuntimeOptions{})
```

**Python:**
```python
request = dingtalkyida__2__0_models.UpdateFormDataRequest(
    app_type='APP_XXX',
    system_token='token',
    user_id='user123',
    form_instance_id='FORM_INST_12345',
    update_form_data_json='{"textField_xxx": "newValue"}',
    use_latest_version=False
)
response = client.update_form_data_with_options(request, headers, util_models.RuntimeOptions())
```

### 删除表单数据

**Go:**
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

**Python:**
```python
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models

request = dingtalkyida__1__0_models.DeleteFormDataRequest(
    app_type='APP_XXX',
    system_token='token',
    user_id='user123',
    form_instance_id='FORM_INST_12345'
)
response = client.delete_form_data_with_options(request, headers, util_models.RuntimeOptions())
```

## Version Selection

钉钉宜搭 API 有两个版本，根据操作类型选择：

| 操作类型 | 推荐版本 | 原因 |
|---------|---------|------|
| 单条 CRUD | yida_2_0 | 功能更完善，支持更多参数 |
| 批量操作 | yida_1_0 | 批量 API 仅在 1.0 中提供 |
| 删除操作 | yida_1_0 | DeleteFormData 仅在 1.0 中提供 |

**Go 导入:**
- yida_2_0: `github.com/alibabacloud-go/dingtalk/yida_2_0`
- yida_1_0: `github.com/alibabacloud-go/dingtalk/yida_1_0`

**Python 导入:**
- yida_2_0: `from alibabacloud_dingtalk.yida_2_0.client import Client as dingtalkyida_2_0Client`
- yida_1_0: `from alibabacloud_dingtalk.yida_1_0.client import Client as dingtalkyida_1_0Client`

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

**Go:**
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

**Python:**
```python
from alibabacloud_tea_util.client import Client as UtilClient

try:
    response = client.xxx_with_options(request, headers, util_models.RuntimeOptions())
except Exception as err:
    if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
        # err.code 和 err.message 包含错误详情
        pass
```

## References

- **完整 API 列表和参数说明**: 见 [references/api-reference.md](references/api-reference.md)
- **详细代码示例 (Go + Python)**: 见 [references/code-examples.md](references/code-examples.md)
- **官方 API 代码示例**: 见 [references/1.md](references/1.md)
