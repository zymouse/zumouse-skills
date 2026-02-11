# DingTalk YiDa API Reference

钉钉宜搭表单 API 完整参考文档。

## Table of Contents

- [API Version Overview](#api-version-overview)
- [Core APIs](#core-apis)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)
- [Batch Operations](#batch-operations)
- [Advanced Operations](#advanced-operations)

---

## API Version Overview

### yida_2_0 (推荐用于单条操作)

**Go:**
```go
import "github.com/alibabacloud-go/dingtalk/yida_2_0"
```

**Python:**
```python
from alibabacloud_dingtalk.yida_2_0.client import Client as dingtalkyida_2_0Client
from alibabacloud_dingtalk.yida_2_0 import models as dingtalkyida__2__0_models
```

适用场景：
- 单条表单数据创建、查询、更新
- 子表单更新
- 表单实例搜索

### yida_1_0 (用于批量和删除操作)

**Go:**
```go
import "github.com/alibabacloud-go/dingtalk/yida_1_0"
```

**Python:**
```python
from alibabacloud_dingtalk.yida_1_0.client import Client as dingtalkyida_1_0Client
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models
```

适用场景：
- 批量创建表单实例
- 批量更新表单实例
- 批量删除表单实例
- 单条/批量删除表单数据
- 批量获取表单数据

---

## Core APIs

### Create

#### SaveFormData (yida_2_0)

创建新的表单实例。

**Go:**
```go
func (client *Client) SaveFormDataWithOptions(
    request *SaveFormDataRequest,
    headers *SaveFormDataHeaders,
    runtime *util.RuntimeOptions,
) (*SaveFormDataResponse, error)
```

**Python:**
```python
def save_form_data_with_options(
    self,
    request: dingtalkyida__2__0_models.SaveFormDataRequest,
    headers: dingtalkyida__2__0_models.SaveFormDataHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.SaveFormDataResponse
```

**Request Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| AppType | string | 是 | 应用类型 |
| SystemToken | string | 是 | 系统令牌 |
| UserId | string | 是 | 用户ID |
| FormUuid | string | 是 | 表单UUID |
| FormDataJson | string | 是 | 表单数据JSON字符串 |
| Language | string | 否 | 语言，默认 zh_CN |
| UseAlias | bool | 否 | 是否使用别名 |

**Response:**

```json
{
  "result": "FORM-EF6xxx"
}
```

#### CreateOrUpdateFormData (yida_2_0)

根据条件创建或更新表单实例。

**Go:**
```go
func (client *Client) CreateOrUpdateFormDataWithOptions(
    request *CreateOrUpdateFormDataRequest,
    headers *CreateOrUpdateFormDataHeaders,
    runtime *util.RuntimeOptions,
) (*CreateOrUpdateFormDataResponse, error)
```

**Python:**
```python
def create_or_update_form_data_with_options(
    self,
    request: dingtalkyida__2__0_models.CreateOrUpdateFormDataRequest,
    headers: dingtalkyida__2__0_models.CreateOrUpdateFormDataHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.CreateOrUpdateFormDataResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| SearchCondition | string | 否 | 查询条件JSON，用于判断是创建还是更新 |
| NoExecuteExpression | bool | 否 | 是否不执行公式 |

---

### Read

#### SearchFormDatas (yida_2_0)

分页查询表单实例列表。

**Go:**
```go
func (client *Client) SearchFormDatasWithOptions(
    request *SearchFormDatasRequest,
    headers *SearchFormDatasHeaders,
    runtime *util.RuntimeOptions,
) (*SearchFormDatasResponse, error)
```

**Python:**
```python
def search_form_datas_with_options(
    self,
    request: dingtalkyida__2__0_models.SearchFormDatasRequest,
    headers: dingtalkyida__2__0_models.SearchFormDatasHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.SearchFormDatasResponse
```

**Request Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| AppType | string | 是 | 应用类型 |
| SystemToken | string | 是 | 系统令牌 |
| FormUuid | string | 是 | 表单UUID |
| UserId | string | 否 | 用户ID |
| Language | string | 否 | 语言 |
| SearchFieldJson | string | 否 | 搜索条件JSON |
| CurrentPage | int32 | 否 | 当前页码，默认1 |
| PageSize | int32 | 否 | 每页条数，默认10 |
| CreateFromTimeGMT | string | 否 | 创建开始时间，格式：2018-01-01 |
| CreateToTimeGMT | string | 否 | 创建结束时间 |
| ModifiedFromTimeGMT | string | 否 | 修改开始时间 |
| ModifiedToTimeGMT | string | 否 | 修改结束时间 |
| DynamicOrder | string | 否 | 排序规则JSON |
| UseAlias | bool | 否 | 是否使用别名 |

**SearchFieldJson Format:**

```json
{
  "textField_xxx": "searchValue",
  "numberField_xxx": ["1", "10"],
  "dateField_xxx": [1514736000000, 1517414399000],
  "selectField_xxx": "option1",
  "checkboxField_xxx": ["option1", "option2"]
}
```

**Response:**

```json
{
  "currentPage": 1,
  "totalCount": 100,
  "data": [
    {
      "dataId": 1002,
      "formInstanceId": "FINST-XXX",
      "createdTimeGMT": "2018-01-24 11:22:01",
      "modifiedTimeGMT": "2018-01-24 11:22:01",
      "formUuid": "FORM-XXX",
      "title": "张三发起的表单",
      "instanceValue": "{}",
      "version": 3,
      "creatorUserId": "1731234567",
      "modifierUserId": "1731234567"
    }
  ]
}
```

#### GetFormDataByID (yida_2_0)

根据实例ID查询单条表单数据。

**Go:**
```go
func (client *Client) GetFormDataByIDWithOptions(
    formInstId *string,  // 路径参数
    request *GetFormDataByIDRequest,
    headers *GetFormDataByIDHeaders,
    runtime *util.RuntimeOptions,
) (*GetFormDataByIDResponse, error)
```

**Python:**
```python
def get_form_data_by_idwith_options(
    self,
    form_inst_id: str,  # 路径参数
    request: dingtalkyida__2__0_models.GetFormDataByIDRequest,
    headers: dingtalkyida__2__0_models.GetFormDataByIDHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.GetFormDataByIDResponse
```

**Request Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| formInstId (path) | string | 是 | 表单实例ID，如 FORM_INST_12345 |
| AppType | string | 是 | 应用类型 |
| SystemToken | string | 是 | 系统令牌 |
| UserId | string | 否 | 用户ID |
| Language | string | 否 | 语言 |
| UseAlias | bool | 否 | 是否使用别名 |
| FormUuid | string | 是 | 表单UUID |

**Response:**

```json
{
  "originator": {
    "userId": "user123",
    "name": {
      "nameInChinese": "张三",
      "nameInEnglish": "ZhangSan",
      "type": "i18n"
    },
    "departmentName": "开发部",
    "email": "abc@alimail.com"
  },
  "modifiedTimeGMT": "2021-05-01",
  "formInstId": "FORM_INST_12345"
}
```

---

### Update

#### UpdateFormData (yida_2_0)

更新表单实例数据。

**Go:**
```go
func (client *Client) UpdateFormDataWithOptions(
    request *UpdateFormDataRequest,
    headers *UpdateFormDataHeaders,
    runtime *util.RuntimeOptions,
) (*UpdateFormDataResponse, error)
```

**Python:**
```python
def update_form_data_with_options(
    self,
    request: dingtalkyida__2__0_models.UpdateFormDataRequest,
    headers: dingtalkyida__2__0_models.UpdateFormDataHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.UpdateFormDataResponse
```

**Request Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| AppType | string | 是 | 应用类型 |
| SystemToken | string | 是 | 系统令牌 |
| UserId | string | 是 | 用户ID |
| FormInstanceId | string | 是 | 表单实例ID |
| UpdateFormDataJson | string | 是 | 更新数据JSON |
| Language | string | 否 | 语言 |
| UseLatestVersion | bool | 否 | 是否使用最新版本 |
| UseAlias | bool | 否 | 是否使用别名 |
| FormUuid | string | 是 | 表单UUID |

#### UpdateSubTable (yida_2_0)

更新子表单数据。

**Go:**
```go
func (client *Client) UpdateSubTableWithOptions(
    request *UpdateSubTableRequest,
    headers *UpdateSubTableHeaders,
    runtime *util.RuntimeOptions,
) (*UpdateSubTableResponse, error)
```

**Python:**
```python
def update_sub_table_with_options(
    self,
    request: dingtalkyida__2__0_models.UpdateSubTableRequest,
    headers: dingtalkyida__2__0_models.UpdateSubTableHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.UpdateSubTableResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| FormInstanceId | string | 是 | 主表单实例ID |
| TableFieldIds | string | 是 | 子表字段ID列表，逗号分隔 |
| UpdateFormDataJson | string | 是 | 子表数据JSON |
| UseLatestFormSchemaVersion | bool | 否 | 是否使用最新表单版本 |
| NoExecuteExpression | bool | 否 | 是否不执行公式 |

**UpdateFormDataJson Format for SubTable:**

```json
{
  "tableField_xxx": [
    {
      "textField_xxx": "子表行1数据",
      "textareaField_xxx": "子表行1多行文本"
    },
    {
      "textField_xxx": "子表行2数据"
    }
  ]
}
```

---

### Delete

#### DeleteFormData (yida_1_0)

删除单条表单数据。

**Go:**
```go
func (client *Client) DeleteFormDataWithOptions(
    request *DeleteFormDataRequest,
    headers *DeleteFormDataHeaders,
    runtime *util.RuntimeOptions,
) (*DeleteFormDataResponse, error)
```

**Python:**
```python
def delete_form_data_with_options(
    self,
    request: dingtalkyida__1__0_models.DeleteFormDataRequest,
    headers: dingtalkyida__1__0_models.DeleteFormDataHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.DeleteFormDataResponse
```

**Request Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| AppType | string | 是 | 应用类型 |
| SystemToken | string | 是 | 系统令牌 |
| UserId | string | 是 | 用户ID |
| FormInstanceId | string | 是 | 表单实例ID |
| Language | string | 否 | 语言 |

---

## Batch Operations

### BatchSaveFormData (yida_1_0)

批量创建表单实例。

**Go:**
```go
func (client *Client) BatchSaveFormDataWithOptions(
    request *BatchSaveFormDataRequest,
    headers *BatchSaveFormDataHeaders,
    runtime *util.RuntimeOptions,
) (*BatchSaveFormDataResponse, error)
```

**Python:**
```python
def batch_save_form_data_with_options(
    self,
    request: dingtalkyida__1__0_models.BatchSaveFormDataRequest,
    headers: dingtalkyida__1__0_models.BatchSaveFormDataHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.BatchSaveFormDataResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| FormDataJsonList | []string | 是 | 表单数据JSON列表 |
| AsynchronousExecution | bool | 否 | 是否异步执行 |
| NoExecuteExpression | bool | 否 | 是否不执行公式 |
| KeepRunningAfterException | bool | 否 | 异常后是否继续执行 |

**Response:**

```json
{
  "result": ["FINST-SASNOO39NSIFF780"]
}
```

### BatchGetFormDataByIdList (yida_1_0)

批量获取表单实例数据。

**Go:**
```go
func (client *Client) BatchGetFormDataByIdListWithOptions(
    request *BatchGetFormDataByIdListRequest,
    headers *BatchGetFormDataByIdListHeaders,
    runtime *util.RuntimeOptions,
) (*BatchGetFormDataByIdListResponse, error)
```

**Python:**
```python
def batch_get_form_data_by_id_list_with_options(
    self,
    request: dingtalkyida__1__0_models.BatchGetFormDataByIdListRequest,
    headers: dingtalkyida__1__0_models.BatchGetFormDataByIdListHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| FormInstanceIdList | []string | 是 | 表单实例ID列表 |
| NeedFormInstanceValue | bool | 否 | 是否需要返回表单值 |

### BatchUpdateFormDataByInstanceId (yida_1_0)

批量更新表单实例。

**Go:**
```go
func (client *Client) BatchUpdateFormDataByInstanceIdWithOptions(
    request *BatchUpdateFormDataByInstanceIdRequest,
    headers *BatchUpdateFormDataByInstanceIdHeaders,
    runtime *util.RuntimeOptions,
) (*BatchUpdateFormDataByInstanceIdResponse, error)
```

**Python:**
```python
def batch_update_form_data_by_instance_id_with_options(
    self,
    request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest,
    headers: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| FormInstanceIdList | []string | 是 | 表单实例ID列表 |
| UpdateFormDataJson | string | 是 | 更新数据JSON |
| IgnoreEmpty | bool | 否 | 是否忽略空值 |
| UseLatestFormSchemaVersion | bool | 否 | 是否使用最新表单版本 |

### BatchRemovalByFormInstanceIdList (yida_1_0)

批量删除表单实例。

**Go:**
```go
func (client *Client) BatchRemovalByFormInstanceIdListWithOptions(
    request *BatchRemovalByFormInstanceIdListRequest,
    headers *BatchRemovalByFormInstanceIdListHeaders,
    runtime *util.RuntimeOptions,
) (*BatchRemovalByFormInstanceIdListResponse, error)
```

**Python:**
```python
def batch_removal_by_form_instance_id_list_with_options(
    self,
    request: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest,
    headers: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse
```

**Additional Parameters:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| FormInstanceIdList | []string | 是 | 表单实例ID列表 |
| AsynchronousExecution | bool | 否 | 是否异步执行 |
| ExecuteExpression | bool | 否 | 是否执行公式 |

---

## Advanced Operations

### GetProcessDesign (yida_1_0)

获取流程设计结构。

**Go:**
```go
func (client *Client) GetProcessDesignWithOptions(
    processCode *string,  // 路径参数
    request *GetProcessDesignRequest,
    headers *GetProcessDesignHeaders,
    runtime *util.RuntimeOptions,
) (*GetProcessDesignResponse, error)
```

**Python:**
```python
def get_process_design_with_options(
    self,
    process_code: str,  # 路径参数
    request: dingtalkyida__1__0_models.GetProcessDesignRequest,
    headers: dingtalkyida__1__0_models.GetProcessDesignHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__1__0_models.GetProcessDesignResponse
```

### GetFormComponentAliasList (yida_2_0)

获取组件别名列表。

**Go:**
```go
func (client *Client) GetFormComponentAliasListWithOptions(
    appType *string,      // 路径参数
    formUuid *string,     // 路径参数
    request *GetFormComponentAliasListRequest,
    headers *GetFormComponentAliasListHeaders,
    runtime *util.RuntimeOptions,
) (*GetFormComponentAliasListResponse, error)
```

**Python:**
```python
def get_form_component_alias_list_with_options(
    self,
    app_type: str,      # 路径参数
    form_uuid: str,     # 路径参数
    request: dingtalkyida__2__0_models.GetFormComponentAliasListRequest,
    headers: dingtalkyida__2__0_models.GetFormComponentAliasListHeaders,
    runtime: util_models.RuntimeOptions
) -> dingtalkyida__2__0_models.GetFormComponentAliasListResponse
```

---

## Field Type Reference

### Form Field Types

| 字段类型 | 示例字段ID | 数据格式 |
|---------|-----------|---------|
| 单行文本 | textField_xxx | string |
| 多行文本 | textareaField_xxx | string |
| 数字 | numberField_xxx | number |
| 单选 | radioField_xxx | string (选项值) |
| 下拉单选 | selectField_xxx | string (选项值) |
| 复选 | checkboxField_xxx | []string (选项值数组) |
| 下拉多选 | multiSelectField_xxx | []string (选项值数组) |
| 日期 | dateField_xxx | timestamp (毫秒) |
| 级联日期 | cascadeDate_xxx | [[start, end], ...] |
| 成员 | employeeField_xxx | []string (userId数组) |
| 部门 | departmentField_xxx | number (deptId) |
| 地址 | addressField_xxx | object |
| 级联选择 | cascadeSelectField_xxx | []string (层级值数组) |
| 子表单 | tableField_xxx | []object (行数组) |
| 国家选择 | countrySelectField_xxx | [{"value": "US"}] |

### Address Field Format

```json
{
  "address": "详细地址",
  "regionIds": [460000, 469027, 469023401],
  "regionText": [
    {"en_US": "hai+nan+sheng", "zh_CN": "海南省"},
    {"en_US": "cheng+mai+xian", "zh_CN": "澄迈县"},
    {"en_US": "guo+ying+hong+gang+nong+chang", "zh_CN": "国营红岗农场"}
  ]
}
```
