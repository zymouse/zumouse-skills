# DingTalk YiDa Code Examples

钉钉宜搭表单 API 完整代码示例 (Go + Python)。

## Table of Contents

- [Client Initialization](#client-initialization)
- [Create Operations](#create-operations)
- [Read Operations](#read-operations)
- [Update Operations](#update-operations)
- [Delete Operations](#delete-operations)
- [Batch Operations](#batch-operations)
- [Complete CRUD Example](#complete-crud-example)

---

## Client Initialization

### yida_2_0 Client

**Go:**
```go
package main

import (
    "fmt"
    "os"
    
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    "github.com/alibabacloud-go/dingtalk/yida_1_0"
    openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
    "github.com/alibabacloud-go/tea-utils/v2/service"
    "github.com/alibabacloud-go/tea/tea"
)

// CreateYidaV2Client 创建 yida_2_0 客户端
func CreateYidaV2Client() (*yida_2_0.Client, error) {
    config := &openapi.Config{}
    config.Protocol = tea.String("https")
    config.RegionId = tea.String("central")
    return yida_2_0.NewClient(config)
}

// CreateYidaV1Client 创建 yida_1_0 客户端
func CreateYidaV1Client() (*yida_1_0.Client, error) {
    config := &openapi.Config{}
    config.Protocol = tea.String("https")
    config.RegionId = tea.String("central")
    return yida_1_0.NewClient(config)
}

// handleError 统一错误处理
func handleError(err error) error {
    if err == nil {
        return nil
    }
    
    var sdkErr *tea.SDKError
    if t, ok := err.(*tea.SDKError); ok {
        sdkErr = t
        fmt.Printf("SDK Error - Code: %s, Message: %s\n", tea.StringValue(sdkErr.Code), tea.StringValue(sdkErr.Message))
    } else {
        fmt.Printf("Error: %v\n", err)
    }
    return err
}
```

**Python:**
```python
from alibabacloud_dingtalk.yida_2_0.client import Client as dingtalkyida_2_0Client
from alibabacloud_dingtalk.yida_1_0.client import Client as dingtalkyida_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


def create_yida_v2_client() -> dingtalkyida_2_0Client:
    """创建 yida_2_0 客户端"""
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    return dingtalkyida_2_0Client(config)


def create_yida_v1_client() -> dingtalkyida_1_0Client:
    """创建 yida_1_0 客户端"""
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    return dingtalkyida_1_0Client(config)


def handle_error(err: Exception) -> None:
    """统一错误处理"""
    if err is None:
        return
    
    if hasattr(err, 'code') and hasattr(err, 'message'):
        if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
            print(f"SDK Error - Code: {err.code}, Message: {err.message}")
    else:
        print(f"Error: {err}")
```

---

## Create Operations

### Create Single Form Instance

**Go:**
```go
package main

import (
    "encoding/json"
    "fmt"
    
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    "github.com/alibabacloud-go/tea-utils/v2/service"
    "github.com/alibabacloud-go/tea/tea"
)

// CreateFormInstance 创建表单实例
func CreateFormInstance(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid string,
    formData map[string]interface{},
) (string, error) {
    
    client, err := CreateYidaV2Client()
    if err != nil {
        return "", err
    }
    
    // 构建请求头
    headers := &yida_2_0.SaveFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    // 序列化表单数据
    formDataJson, err := json.Marshal(formData)
    if err != nil {
        return "", err
    }
    
    // 构建请求参数
    request := &yida_2_0.SaveFormDataRequest{
        AppType:      tea.String(appType),
        SystemToken:  tea.String(systemToken),
        UserId:       tea.String(userId),
        Language:     tea.String("zh_CN"),
        FormUuid:     tea.String(formUuid),
        FormDataJson: tea.String(string(formDataJson)),
        UseAlias:     tea.Bool(false),
    }
    
    // 执行请求
    response, err := client.SaveFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return "", handleError(err)
    }
    
    return tea.StringValue(response.Body.Result), nil
}

// 使用示例
func main() {
    formData := map[string]interface{}{
        "textField_l0c1cwiu":   "单行文本值",
        "textareaField_l0c1cwiy": "多行文本值",
        "numberField_l0c1cwiz": 100,
        "radioField_l0c1cwja":  "选项一",
        "selectField_l0c1cwjb": "选项一",
        "checkboxField_l0c1cwjc": []string{"选项一", "选项二"},
        "dateField_l0c1cwjd":   1514736000000,
        "employeeField_l0c1cwje": []string{"user123"},
    }
    
    formUuid, err := CreateFormInstance(
        "<your_access_token>",
        "APP_XCE0EVXS6DYG3YDYC5RD",
        "09866181UTZVVD4R3DC955FNKIM52HVPU5WWK7",
        "ding173982232112232",
        "FORM-GX866MC1NC1VOFF6WVQW33FD16E23L3CPMKVKA",
        formData,
    )
    
    if err != nil {
        fmt.Printf("创建失败: %v\n", err)
        return
    }
    
    fmt.Printf("创建成功，表单UUID: %s\n", formUuid)
}
```

**Python:**
```python
import json
from typing import Dict, Any, Optional
from alibabacloud_dingtalk.yida_2_0 import models as dingtalkyida__2__0_models


def create_form_instance(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_data: Dict[str, Any]
) -> Optional[str]:
    """创建表单实例"""
    
    client = create_yida_v2_client()
    
    # 构建请求头
    headers = dingtalkyida__2__0_models.SaveFormDataHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    # 序列化表单数据
    form_data_json = json.dumps(form_data, ensure_ascii=False)
    
    # 构建请求参数
    request = dingtalkyida__2__0_models.SaveFormDataRequest(
        app_type=app_type,
        system_token=system_token,
        user_id=user_id,
        language='zh_CN',
        form_uuid=form_uuid,
        form_data_json=form_data_json,
        use_alias=False
    )
    
    # 执行请求
    try:
        response = client.save_form_data_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return response.body.result
    except Exception as err:
        handle_error(err)
        return None


# 使用示例
if __name__ == '__main__':
    form_data = {
        "textField_l0c1cwiu": "单行文本值",
        "textareaField_l0c1cwiy": "多行文本值",
        "numberField_l0c1cwiz": 100,
        "radioField_l0c1cwja": "选项一",
        "selectField_l0c1cwjb": "选项一",
        "checkboxField_l0c1cwjc": ["选项一", "选项二"],
        "dateField_l0c1cwjd": 1514736000000,
        "employeeField_l0c1cwje": ["user123"]
    }
    
    form_uuid = create_form_instance(
        "<your_access_token>",
        "APP_XCE0EVXS6DYG3YDYC5RD",
        "09866181UTZVVD4R3DC955FNKIM52HVPU5WWK7",
        "ding173982232112232",
        "FORM-GX866MC1NC1VOFF6WVQW33FD16E23L3CPMKVKA",
        form_data
    )
    
    if form_uuid:
        print(f"创建成功，表单UUID: {form_uuid}")
    else:
        print("创建失败")
```

### Create with Address Field

**Go:**
```go
// CreateFormWithAddress 创建包含地址字段的表单
func CreateFormWithAddress(accessToken, appType, systemToken, userId, formUuid string) (string, error) {
    client, err := CreateYidaV2Client()
    if err != nil {
        return "", err
    }
    
    headers := &yida_2_0.SaveFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    formData := map[string]interface{}{
        "textField_xxx": "测试数据",
        "addressField_l0c1cwiy": map[string]interface{}{
            "address":   "详细地址111",
            "regionIds": []int{460000, 469027, 469023401},
            "regionText": []map[string]string{
                {"en_US": "hai+nan+sheng", "zh_CN": "海南省"},
                {"en_US": "cheng+mai+xian", "zh_CN": "澄迈县"},
                {"en_US": "guo+ying+hong+gang+nong+chang", "zh_CN": "国营红岗农场"},
            },
        },
        "countrySelectField_l0c1cwiu": []map[string]string{
            {"value": "US"},
        },
    }
    
    formDataJson, _ := json.Marshal(formData)
    
    request := &yida_2_0.SaveFormDataRequest{
        AppType:      tea.String(appType),
        SystemToken:  tea.String(systemToken),
        UserId:       tea.String(userId),
        FormUuid:     tea.String(formUuid),
        FormDataJson: tea.String(string(formDataJson)),
    }
    
    response, err := client.SaveFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return "", err
    }
    
    return tea.StringValue(response.Body.Result), nil
}
```

**Python:**
```python
def create_form_with_address(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str
) -> Optional[str]:
    """创建包含地址字段的表单"""
    
    client = create_yida_v2_client()
    
    headers = dingtalkyida__2__0_models.SaveFormDataHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    form_data = {
        "textField_xxx": "测试数据",
        "addressField_l0c1cwiy": {
            "address": "详细地址111",
            "regionIds": [460000, 469027, 469023401],
            "regionText": [
                {"en_US": "hai+nan+sheng", "zh_CN": "海南省"},
                {"en_US": "cheng+mai+xian", "zh_CN": "澄迈县"},
                {"en_US": "guo+ying+hong+gang+nong+chang", "zh_CN": "国营红岗农场"}
            ]
        },
        "countrySelectField_l0c1cwiu": [
            {"value": "US"}
        ]
    }
    
    form_data_json = json.dumps(form_data, ensure_ascii=False)
    
    request = dingtalkyida__2__0_models.SaveFormDataRequest(
        app_type=app_type,
        system_token=system_token,
        user_id=user_id,
        form_uuid=form_uuid,
        form_data_json=form_data_json
    )
    
    try:
        response = client.save_form_data_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return response.body.result
    except Exception as err:
        handle_error(err)
        return None
```

---

## Read Operations

### Search Form Instances

**Go:**
```go
package main

import (
    "encoding/json"
    "fmt"
    
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    "github.com/alibabacloud-go/tea-utils/v2/service"
    "github.com/alibabacloud-go/tea/tea"
)

// SearchFormInstances 搜索表单实例
func SearchFormInstances(
    accessToken,
    appType,
    systemToken,
    formUuid string,
    searchFields map[string]interface{},
    page, pageSize int32,
) (*yida_2_0.SearchFormDatasResponseBody, error) {
    
    client, err := CreateYidaV2Client()
    if err != nil {
        return nil, err
    }
    
    headers := &yida_2_0.SearchFormDatasHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    // 构建搜索条件
    var searchFieldJson string
    if searchFields != nil {
        data, _ := json.Marshal(searchFields)
        searchFieldJson = string(data)
    }
    
    request := &yida_2_0.SearchFormDatasRequest{
        AppType:         tea.String(appType),
        SystemToken:     tea.String(systemToken),
        FormUuid:        tea.String(formUuid),
        Language:        tea.String("zh_CN"),
        CurrentPage:     tea.Int32(page),
        PageSize:        tea.Int32(pageSize),
        SearchFieldJson: tea.String(searchFieldJson),
        UseAlias:        tea.Bool(false),
    }
    
    response, err := client.SearchFormDatasWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return nil, handleError(err)
    }
    
    return response.Body, nil
}

// 使用示例
func ExampleSearch() {
    // 搜索条件
    searchFields := map[string]interface{}{
        "textField_jcr0069m": "danhang",
        "numberField_jcr0069o": []string{"1", "10"}, // 范围查询
        "dateField_jcr0069t": []int64{1514736000000, 1517414399000},
        "checkboxField_jcr0069r": []string{"选项二"},
    }
    
    result, err := SearchFormInstances(
        "<your_access_token>",
        "APP_PBKT0MFBEBTDO8T7SLVP",
        "hexxx",
        "FORM-EF6Y4G8WO2FN0SUB43TDQ3CGC3FMFQ1G9400RCJ3",
        searchFields,
        1,  // page
        10, // pageSize
    )
    
    if err != nil {
        fmt.Printf("搜索失败: %v\n", err)
        return
    }
    
    fmt.Printf("总条数: %d, 当前页: %d\n", tea.Int64Value(result.TotalCount), tea.Int32Value(result.CurrentPage))
    
    for _, item := range result.Data {
        fmt.Printf("实例ID: %s, 标题: %s\n", 
            tea.StringValue(item.FormInstanceId),
            tea.StringValue(item.Title),
        )
    }
}
```

**Python:**
```python
from typing import Dict, Any, Optional, List
from alibabacloud_dingtalk.yida_2_0 import models as dingtalkyida__2__0_models


def search_form_instances(
    access_token: str,
    app_type: str,
    system_token: str,
    form_uuid: str,
    search_fields: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> Optional[dingtalkyida__2__0_models.SearchFormDatasResponseBody]:
    """搜索表单实例"""
    
    client = create_yida_v2_client()
    
    headers = dingtalkyida__2__0_models.SearchFormDatasHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    # 构建搜索条件
    search_field_json = json.dumps(search_fields, ensure_ascii=False) if search_fields else ""
    
    request = dingtalkyida__2__0_models.SearchFormDatasRequest(
        app_type=app_type,
        system_token=system_token,
        form_uuid=form_uuid,
        language='zh_CN',
        current_page=page,
        page_size=page_size,
        search_field_json=search_field_json,
        use_alias=False
    )
    
    try:
        response = client.search_form_datas_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return response.body
    except Exception as err:
        handle_error(err)
        return None


# 使用示例
def example_search():
    # 搜索条件
    search_fields = {
        "textField_jcr0069m": "danhang",
        "numberField_jcr0069o": ["1", "10"],  # 范围查询
        "dateField_jcr0069t": [1514736000000, 1517414399000],
        "checkboxField_jcr0069r": ["选项二"]
    }
    
    result = search_form_instances(
        "<your_access_token>",
        "APP_PBKT0MFBEBTDO8T7SLVP",
        "hexxx",
        "FORM-EF6Y4G8WO2FN0SUB43TDQ3CGC3FMFQ1G9400RCJ3",
        search_fields,
        1,  # page
        10  # page_size
    )
    
    if result is None:
        print("搜索失败")
        return
    
    print(f"总条数: {result.total_count}, 当前页: {result.current_page}")
    
    for item in result.data:
        print(f"实例ID: {item.form_instance_id}, 标题: {item.title}")
```

### Get Form Instance by ID

**Go:**
```go
// GetFormInstance 根据ID获取表单实例
func GetFormInstance(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid,
    formInstId string,
    useAlias bool,
) (*yida_2_0.GetFormDataByIDResponseBody, error) {
    
    client, err := CreateYidaV2Client()
    if err != nil {
        return nil, err
    }
    
    headers := &yida_2_0.GetFormDataByIDHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    request := &yida_2_0.GetFormDataByIDRequest{
        AppType:     tea.String(appType),
        SystemToken: tea.String(systemToken),
        UserId:      tea.String(userId),
        Language:    tea.String("zh_CN"),
        UseAlias:    tea.Bool(useAlias),
        FormUuid:    tea.String(formUuid),
    }
    
    // formInstId 作为路径参数传入
    response, err := client.GetFormDataByIDWithOptions(
        tea.String(formInstId),
        request,
        headers,
        &service.RuntimeOptions{},
    )
    if err != nil {
        return nil, handleError(err)
    }
    
    return response.Body, nil
}
```

**Python:**
```python
def get_form_instance(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_inst_id: str,
    use_alias: bool = False
) -> Optional[dingtalkyida__2__0_models.GetFormDataByIDResponseBody]:
    """根据ID获取表单实例"""
    
    client = create_yida_v2_client()
    
    headers = dingtalkyida__2__0_models.GetFormDataByIDHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    request = dingtalkyida__2__0_models.GetFormDataByIDRequest(
        app_type=app_type,
        system_token=system_token,
        user_id=user_id,
        language='zh_CN',
        use_alias=use_alias,
        form_uuid=form_uuid
    )
    
    # form_inst_id 作为路径参数传入
    try:
        response = client.get_form_data_by_idwith_options(
            form_inst_id,
            request,
            headers,
            util_models.RuntimeOptions()
        )
        return response.body
    except Exception as err:
        handle_error(err)
        return None
```

---

## Update Operations

### Update Form Instance

**Go:**
```go
package main

import (
    "encoding/json"
    
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    "github.com/alibabacloud-go/tea-utils/v2/service"
    "github.com/alibabacloud-go/tea/tea"
)

// UpdateFormInstance 更新表单实例
func UpdateFormInstance(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid,
    formInstanceId string,
    updateData map[string]interface{},
    useLatestVersion bool,
) error {
    
    client, err := CreateYidaV2Client()
    if err != nil {
        return err
    }
    
    headers := &yida_2_0.UpdateFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    updateDataJson, _ := json.Marshal(updateData)
    
    request := &yida_2_0.UpdateFormDataRequest{
        AppType:            tea.String(appType),
        SystemToken:        tea.String(systemToken),
        UserId:             tea.String(userId),
        Language:           tea.String("zh_CN"),
        FormInstanceId:     tea.String(formInstanceId),
        FormUuid:           tea.String(formUuid),
        UpdateFormDataJson: tea.String(string(updateDataJson)),
        UseLatestVersion:   tea.Bool(useLatestVersion),
        UseAlias:           tea.Bool(false),
    }
    
    _, err = client.UpdateFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    return handleError(err)
}

// 使用示例
func ExampleUpdate() {
    updateData := map[string]interface{}{
        "textField_xxx":   "更新的单行文本",
        "numberField_xxx": 200,
    }
    
    err := UpdateFormInstance(
        "<your_access_token>",
        "APP_PBKTxxx",
        "hexxxx",
        "manager123",
        "FORM-AA285xxx",
        "FORM_INST_12345",
        updateData,
        false, // 不使用最新版本
    )
    
    if err != nil {
        fmt.Printf("更新失败: %v\n", err)
    } else {
        fmt.Println("更新成功")
    }
}
```

**Python:**
```python
def update_form_instance(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_instance_id: str,
    update_data: Dict[str, Any],
    use_latest_version: bool = False
) -> bool:
    """更新表单实例"""
    
    client = create_yida_v2_client()
    
    headers = dingtalkyida__2__0_models.UpdateFormDataHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    update_data_json = json.dumps(update_data, ensure_ascii=False)
    
    request = dingtalkyida__2__0_models.UpdateFormDataRequest(
        app_type=app_type,
        system_token=system_token,
        user_id=user_id,
        language='zh_CN',
        form_instance_id=form_instance_id,
        form_uuid=form_uuid,
        update_form_data_json=update_data_json,
        use_latest_version=use_latest_version,
        use_alias=False
    )
    
    try:
        client.update_form_data_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return True
    except Exception as err:
        handle_error(err)
        return False


# 使用示例
def example_update():
    update_data = {
        "textField_xxx": "更新的单行文本",
        "numberField_xxx": 200
    }
    
    success = update_form_instance(
        "<your_access_token>",
        "APP_PBKTxxx",
        "hexxxx",
        "manager123",
        "FORM-AA285xxx",
        "FORM_INST_12345",
        update_data,
        False  # 不使用最新版本
    )
    
    if success:
        print("更新成功")
    else:
        print("更新失败")
```

### Update SubTable

**Go:**
```go
// UpdateSubTableData 更新子表单数据
func UpdateSubTableData(
    accessToken,
    appType,
    systemToken,
    userId,
    formInstanceId string,
    tableFieldIds string, // 逗号分隔的子表字段ID
    subTableData map[string]interface{},
) error {
    
    client, err := CreateYidaV2Client()
    if err != nil {
        return err
    }
    
    headers := &yida_2_0.UpdateSubTableHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    updateDataJson, _ := json.Marshal(subTableData)
    
    request := &yida_2_0.UpdateSubTableRequest{
        UpdateFormDataJson:         tea.String(string(updateDataJson)),
        SystemToken:                tea.String(systemToken),
        FormInstanceId:             tea.String(formInstanceId),
        UserId:                     tea.String(userId),
        AppType:                    tea.String(appType),
        UseLatestFormSchemaVersion: tea.Bool(false),
        TableFieldIds:              tea.String(tableFieldIds),
        UseAlias:                   tea.Bool(false),
        Language:                   tea.String("zh_CN"),
        NoExecuteExpression:        tea.Bool(true),
    }
    
    _, err = client.UpdateSubTableWithOptions(request, headers, &service.RuntimeOptions{})
    return handleError(err)
}

// 使用示例
func ExampleUpdateSubTable() {
    // 子表数据：每个子表字段对应一个行数组
    subTableData := map[string]interface{}{
        "tableField_md2x1jo": []map[string]interface{}{
            {
                "textField_md2x1jo":    "子表行1文本",
                "textareaField_md2x1jo": "子表行1多行文本",
            },
            {
                "textField_md2x1jo": "子表行2文本",
            },
        },
        "tableField_md2x1jp": []map[string]interface{}{
            {
                "textField_md2x1jp": "另一个子表数据",
            },
        },
    }
    
    err := UpdateSubTableData(
        "<your_access_token>",
        "APPxxxxYC5RD",
        "098661xxxxWK7",
        "12345678",
        "FINSTxxxxSV0L24",
        "tableField_md2x1jo,tableField_md2x1jp", // 逗号分隔的子表字段ID
        subTableData,
    )
    
    if err != nil {
        fmt.Printf("更新子表失败: %v\n", err)
    } else {
        fmt.Println("更新子表成功")
    }
}
```

**Python:**
```python
def update_sub_table_data(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_instance_id: str,
    table_field_ids: str,  # 逗号分隔的子表字段ID
    sub_table_data: Dict[str, Any]
) -> bool:
    """更新子表单数据"""
    
    client = create_yida_v2_client()
    
    headers = dingtalkyida__2__0_models.UpdateSubTableHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    update_data_json = json.dumps(sub_table_data, ensure_ascii=False)
    
    request = dingtalkyida__2__0_models.UpdateSubTableRequest(
        update_form_data_json=update_data_json,
        system_token=system_token,
        form_instance_id=form_instance_id,
        user_id=user_id,
        app_type=app_type,
        use_latest_form_schema_version=False,
        table_field_ids=table_field_ids,
        use_alias=False,
        language='zh_CN',
        no_execute_expression=True
    )
    
    try:
        client.update_sub_table_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return True
    except Exception as err:
        handle_error(err)
        return False


# 使用示例
def example_update_sub_table():
    # 子表数据：每个子表字段对应一个行数组
    sub_table_data = {
        "tableField_md2x1jo": [
            {
                "textField_md2x1jo": "子表行1文本",
                "textareaField_md2x1jo": "子表行1多行文本"
            },
            {
                "textField_md2x1jo": "子表行2文本"
            }
        ],
        "tableField_md2x1jp": [
            {
                "textField_md2x1jp": "另一个子表数据"
            }
        ]
    }
    
    success = update_sub_table_data(
        "<your_access_token>",
        "APPxxxxYC5RD",
        "098661xxxxWK7",
        "12345678",
        "FINSTxxxxSV0L24",
        "tableField_md2x1jo,tableField_md2x1jp",  # 逗号分隔的子表字段ID
        sub_table_data
    )
    
    if success:
        print("更新子表成功")
    else:
        print("更新子表失败")
```

---

## Delete Operations

### Delete Single Instance

**Go:**
```go
package main

import (
    "github.com/alibabacloud-go/dingtalk/yida_1_0"
    "github.com/alibabacloud-go/tea-utils/service"
    "github.com/alibabacloud-go/tea/tea"
)

// DeleteFormInstance 删除表单实例 (使用 yida_1_0)
func DeleteFormInstance(
    accessToken,
    appType,
    systemToken,
    userId,
    formInstanceId string,
) error {
    
    client, err := CreateYidaV1Client()
    if err != nil {
        return err
    }
    
    headers := &yida_1_0.DeleteFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    request := &yida_1_0.DeleteFormDataRequest{
        AppType:        tea.String(appType),
        SystemToken:    tea.String(systemToken),
        UserId:         tea.String(userId),
        Language:       tea.String("zh_CN"),
        FormInstanceId: tea.String(formInstanceId),
    }
    
    _, err = client.DeleteFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    return handleError(err)
}
```

**Python:**
```python
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models


def delete_form_instance(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_instance_id: str
) -> bool:
    """删除表单实例 (使用 yida_1_0)"""
    
    client = create_yida_v1_client()
    
    headers = dingtalkyida__1__0_models.DeleteFormDataHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    request = dingtalkyida__1__0_models.DeleteFormDataRequest(
        app_type=app_type,
        system_token=system_token,
        user_id=user_id,
        language='zh_CN',
        form_instance_id=form_instance_id
    )
    
    try:
        client.delete_form_data_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return True
    except Exception as err:
        handle_error(err)
        return False
```

---

## Batch Operations

### Batch Create

**Go:**
```go
package main

import (
    "encoding/json"
    
    "github.com/alibabacloud-go/dingtalk/yida_1_0"
    "github.com/alibabacloud-go/tea-utils/service"
    "github.com/alibabacloud-go/tea/tea"
)

// BatchCreateFormInstances 批量创建表单实例
func BatchCreateFormInstances(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid string,
    formDataList []map[string]interface{},
    asyncExecution bool,
) ([]string, error) {
    
    client, err := CreateYidaV1Client()
    if err != nil {
        return nil, err
    }
    
    headers := &yida_1_0.BatchSaveFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    // 将数据列表转换为 JSON 字符串列表
    var formDataJsonList []*string
    for _, data := range formDataList {
        jsonBytes, _ := json.Marshal(data)
        formDataJsonList = append(formDataJsonList, tea.String(string(jsonBytes)))
    }
    
    request := &yida_1_0.BatchSaveFormDataRequest{
        NoExecuteExpression:       tea.Bool(true),
        FormUuid:                  tea.String(formUuid),
        AppType:                   tea.String(appType),
        AsynchronousExecution:     tea.Bool(asyncExecution),
        SystemToken:               tea.String(systemToken),
        KeepRunningAfterException: tea.Bool(true),
        UserId:                    tea.String(userId),
        FormDataJsonList:          formDataJsonList,
    }
    
    response, err := client.BatchSaveFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return nil, handleError(err)
    }
    
    // 转换结果
    var results []string
    for _, id := range response.Body.Result {
        results = append(results, tea.StringValue(id))
    }
    
    return results, nil
}

// 使用示例
func ExampleBatchCreate() {
    formDataList := []map[string]interface{}{
        {
            "textField_xxx":   "数据1",
            "numberField_xxx": 100,
        },
        {
            "textField_xxx":   "数据2",
            "numberField_xxx": 200,
        },
    }
    
    instanceIds, err := BatchCreateFormInstances(
        "<your_access_token>",
        "APP_XCE0EVXS6DYG3YDYC5RD",
        "09866181UTZVVD4R3DC955FNKIM52HVPU5WWK7",
        "ding173982232112232",
        "FORM-GX866MC1NC1VOFF6WVQW33FD16E23L3CPMKVKA",
        formDataList,
        true, // 异步执行
    )
    
    if err != nil {
        fmt.Printf("批量创建失败: %v\n", err)
        return
    }
    
    fmt.Printf("创建成功，实例IDs: %v\n", instanceIds)
}
```

**Python:**
```python
from typing import List
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models


def batch_create_form_instances(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_data_list: List[Dict[str, Any]],
    async_execution: bool = True
) -> Optional[List[str]]:
    """批量创建表单实例"""
    
    client = create_yida_v1_client()
    
    headers = dingtalkyida__1__0_models.BatchSaveFormDataHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    # 将数据列表转换为 JSON 字符串列表
    form_data_json_list = [
        json.dumps(data, ensure_ascii=False) for data in form_data_list
    ]
    
    request = dingtalkyida__1__0_models.BatchSaveFormDataRequest(
        no_execute_expression=True,
        form_uuid=form_uuid,
        app_type=app_type,
        asynchronous_execution=async_execution,
        system_token=system_token,
        keep_running_after_exception=True,
        user_id=user_id,
        form_data_json_list=form_data_json_list
    )
    
    try:
        response = client.batch_save_form_data_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return response.body.result
    except Exception as err:
        handle_error(err)
        return None


# 使用示例
def example_batch_create():
    form_data_list = [
        {
            "textField_xxx": "数据1",
            "numberField_xxx": 100
        },
        {
            "textField_xxx": "数据2",
            "numberField_xxx": 200
        }
    ]
    
    instance_ids = batch_create_form_instances(
        "<your_access_token>",
        "APP_XCE0EVXS6DYG3YDYC5RD",
        "09866181UTZVVD4R3DC955FNKIM52HVPU5WWK7",
        "ding173982232112232",
        "FORM-GX866MC1NC1VOFF6WVQW33FD16E23L3CPMKVKA",
        form_data_list,
        True  # 异步执行
    )
    
    if instance_ids:
        print(f"创建成功，实例IDs: {instance_ids}")
    else:
        print("批量创建失败")
```

### Batch Update

**Go:**
```go
// BatchUpdateFormInstances 批量更新表单实例
func BatchUpdateFormInstances(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid string,
    formInstanceIds []string,
    updateData map[string]interface{},
) ([]string, error) {
    
    client, err := CreateYidaV1Client()
    if err != nil {
        return nil, err
    }
    
    headers := &yida_1_0.BatchUpdateFormDataByInstanceIdHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    // 转换实例ID列表
    var idList []*string
    for _, id := range formInstanceIds {
        idList = append(idList, tea.String(id))
    }
    
    updateDataJson, _ := json.Marshal(updateData)
    
    request := &yida_1_0.BatchUpdateFormDataByInstanceIdRequest{
        NoExecuteExpression:        tea.Bool(true),
        FormUuid:                   tea.String(formUuid),
        UpdateFormDataJson:         tea.String(string(updateDataJson)),
        AppType:                    tea.String(appType),
        IgnoreEmpty:                tea.Bool(true),
        SystemToken:                tea.String(systemToken),
        UseLatestFormSchemaVersion: tea.Bool(false),
        AsynchronousExecution:      tea.Bool(true),
        FormInstanceIdList:         idList,
        UserId:                     tea.String(userId),
    }
    
    response, err := client.BatchUpdateFormDataByInstanceIdWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return nil, handleError(err)
    }
    
    var results []string
    for _, id := range response.Body.Result {
        results = append(results, tea.StringValue(id))
    }
    
    return results, nil
}
```

**Python:**
```python
def batch_update_form_instances(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_instance_ids: List[str],
    update_data: Dict[str, Any]
) -> Optional[List[str]]:
    """批量更新表单实例"""
    
    client = create_yida_v1_client()
    
    headers = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    update_data_json = json.dumps(update_data, ensure_ascii=False)
    
    request = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest(
        no_execute_expression=True,
        form_uuid=form_uuid,
        update_form_data_json=update_data_json,
        app_type=app_type,
        ignore_empty=True,
        system_token=system_token,
        use_latest_form_schema_version=False,
        asynchronous_execution=True,
        form_instance_id_list=form_instance_ids,
        user_id=user_id
    )
    
    try:
        response = client.batch_update_form_data_by_instance_id_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return response.body.result
    except Exception as err:
        handle_error(err)
        return None
```

### Batch Delete

**Go:**
```go
// BatchDeleteFormInstances 批量删除表单实例
func BatchDeleteFormInstances(
    accessToken,
    appType,
    systemToken,
    userId,
    formUuid string,
    formInstanceIds []string,
    asyncExecution bool,
) error {
    
    client, err := CreateYidaV1Client()
    if err != nil {
        return err
    }
    
    headers := &yida_1_0.BatchRemovalByFormInstanceIdListHeaders{
        XAcsDingtalkAccessToken: tea.String(accessToken),
    }
    
    // 转换实例ID列表
    var idList []*string
    for _, id := range formInstanceIds {
        idList = append(idList, tea.String(id))
    }
    
    request := &yida_1_0.BatchRemovalByFormInstanceIdListRequest{
        FormUuid:              tea.String(formUuid),
        AppType:               tea.String(appType),
        AsynchronousExecution: tea.Bool(asyncExecution),
        SystemToken:           tea.String(systemToken),
        FormInstanceIdList:    idList,
        UserId:                tea.String(userId),
        ExecuteExpression:     tea.Bool(false),
    }
    
    _, err = client.BatchRemovalByFormInstanceIdListWithOptions(request, headers, &service.RuntimeOptions{})
    return handleError(err)
}
```

**Python:**
```python
def batch_delete_form_instances(
    access_token: str,
    app_type: str,
    system_token: str,
    user_id: str,
    form_uuid: str,
    form_instance_ids: List[str],
    async_execution: bool = True
) -> bool:
    """批量删除表单实例"""
    
    client = create_yida_v1_client()
    
    headers = dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders()
    headers.x_acs_dingtalk_access_token = access_token
    
    request = dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest(
        form_uuid=form_uuid,
        app_type=app_type,
        asynchronous_execution=async_execution,
        system_token=system_token,
        form_instance_id_list=form_instance_ids,
        user_id=user_id,
        execute_expression=False
    )
    
    try:
        client.batch_removal_by_form_instance_id_list_with_options(
            request, headers, util_models.RuntimeOptions()
        )
        return True
    except Exception as err:
        handle_error(err)
        return False
```

---

## Complete CRUD Example

**Go:**
```go
package main

import (
    "encoding/json"
    "fmt"
    
    "github.com/alibabacloud-go/dingtalk/yida_1_0"
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
    openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
    "github.com/alibabacloud-go/tea-utils/v2/service"
    "github.com/alibabacloud-go/tea/tea"
)

// YidaFormClient 宜搭表单客户端
type YidaFormClient struct {
    v1Client *yida_1_0.Client
    v2Client *yida_2_0.Client
    
    // 通用配置
    AccessToken string
    AppType     string
    SystemToken string
    FormUuid    string
}

// NewYidaFormClient 创建客户端
func NewYidaFormClient(accessToken, appType, systemToken, formUuid string) (*YidaFormClient, error) {
    config := &openapi.Config{}
    config.Protocol = tea.String("https")
    config.RegionId = tea.String("central")
    
    v1Client, err := yida_1_0.NewClient(config)
    if err != nil {
        return nil, err
    }
    
    v2Client, err := yida_2_0.NewClient(config)
    if err != nil {
        return nil, err
    }
    
    return &YidaFormClient{
        v1Client:    v1Client,
        v2Client:    v2Client,
        AccessToken: accessToken,
        AppType:     appType,
        SystemToken: systemToken,
        FormUuid:    formUuid,
    }, nil
}

// Create 创建表单实例
func (c *YidaFormClient) Create(userId string, formData map[string]interface{}) (string, error) {
    headers := &yida_2_0.SaveFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(c.AccessToken),
    }
    
    dataJson, _ := json.Marshal(formData)
    
    request := &yida_2_0.SaveFormDataRequest{
        AppType:      tea.String(c.AppType),
        SystemToken:  tea.String(c.SystemToken),
        UserId:       tea.String(userId),
        FormUuid:     tea.String(c.FormUuid),
        FormDataJson: tea.String(string(dataJson)),
    }
    
    response, err := c.v2Client.SaveFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return "", err
    }
    
    return tea.StringValue(response.Body.Result), nil
}

// Search 查询表单实例列表
func (c *YidaFormClient) Search(searchFields map[string]interface{}, page, pageSize int32) (*yida_2_0.SearchFormDatasResponseBody, error) {
    headers := &yida_2_0.SearchFormDatasHeaders{
        XAcsDingtalkAccessToken: tea.String(c.AccessToken),
    }
    
    var searchFieldJson string
    if searchFields != nil {
        data, _ := json.Marshal(searchFields)
        searchFieldJson = string(data)
    }
    
    request := &yida_2_0.SearchFormDatasRequest{
        AppType:         tea.String(c.AppType),
        SystemToken:     tea.String(c.SystemToken),
        FormUuid:        tea.String(c.FormUuid),
        CurrentPage:     tea.Int32(page),
        PageSize:        tea.Int32(pageSize),
        SearchFieldJson: tea.String(searchFieldJson),
    }
    
    response, err := c.v2Client.SearchFormDatasWithOptions(request, headers, &service.RuntimeOptions{})
    if err != nil {
        return nil, err
    }
    
    return response.Body, nil
}

// GetByID 根据ID获取表单实例
func (c *YidaFormClient) GetByID(userId, formInstanceId string) (*yida_2_0.GetFormDataByIDResponseBody, error) {
    headers := &yida_2_0.GetFormDataByIDHeaders{
        XAcsDingtalkAccessToken: tea.String(c.AccessToken),
    }
    
    request := &yida_2_0.GetFormDataByIDRequest{
        AppType:     tea.String(c.AppType),
        SystemToken: tea.String(c.SystemToken),
        UserId:      tea.String(userId),
        FormUuid:    tea.String(c.FormUuid),
    }
    
    response, err := c.v2Client.GetFormDataByIDWithOptions(
        tea.String(formInstanceId),
        request,
        headers,
        &service.RuntimeOptions{},
    )
    if err != nil {
        return nil, err
    }
    
    return response.Body, nil
}

// Update 更新表单实例
func (c *YidaFormClient) Update(userId, formInstanceId string, updateData map[string]interface{}) error {
    headers := &yida_2_0.UpdateFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(c.AccessToken),
    }
    
    dataJson, _ := json.Marshal(updateData)
    
    request := &yida_2_0.UpdateFormDataRequest{
        AppType:            tea.String(c.AppType),
        SystemToken:        tea.String(c.SystemToken),
        UserId:             tea.String(userId),
        FormInstanceId:     tea.String(formInstanceId),
        FormUuid:           tea.String(c.FormUuid),
        UpdateFormDataJson: tea.String(string(dataJson)),
    }
    
    _, err := c.v2Client.UpdateFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    return err
}

// Delete 删除表单实例
func (c *YidaFormClient) Delete(userId, formInstanceId string) error {
    headers := &yida_1_0.DeleteFormDataHeaders{
        XAcsDingtalkAccessToken: tea.String(c.AccessToken),
    }
    
    request := &yida_1_0.DeleteFormDataRequest{
        AppType:        tea.String(c.AppType),
        SystemToken:    tea.String(c.SystemToken),
        UserId:         tea.String(userId),
        FormInstanceId: tea.String(formInstanceId),
    }
    
    _, err := c.v1Client.DeleteFormDataWithOptions(request, headers, &service.RuntimeOptions{})
    return err
}

// 使用示例
func main() {
    client, err := NewYidaFormClient(
        "<your_access_token>",
        "APP_XXXXX",
        "system_token",
        "FORM-XXXXX",
    )
    if err != nil {
        panic(err)
    }
    
    userId := "ding173982232112232"
    
    // 1. 创建
    formData := map[string]interface{}{
        "textField_xxx":   "测试数据",
        "numberField_xxx": 100,
    }
    
    formUuid, err := client.Create(userId, formData)
    if err != nil {
        fmt.Printf("创建失败: %v\n", err)
        return
    }
    fmt.Printf("创建成功: %s\n", formUuid)
    
    // 2. 查询列表
    searchResult, err := client.Search(nil, 1, 10)
    if err != nil {
        fmt.Printf("查询失败: %v\n", err)
        return
    }
    fmt.Printf("查询到 %d 条数据\n", tea.Int64Value(searchResult.TotalCount))
    
    // 3. 获取单条
    if len(searchResult.Data) > 0 {
        instanceId := tea.StringValue(searchResult.Data[0].FormInstanceId)
        detail, err := client.GetByID(userId, instanceId)
        if err != nil {
            fmt.Printf("获取详情失败: %v\n", err)
            return
        }
        fmt.Printf("详情: %+v\n", detail)
        
        // 4. 更新
        updateData := map[string]interface{}{
            "textField_xxx": "更新后的值",
        }
        err = client.Update(userId, instanceId, updateData)
        if err != nil {
            fmt.Printf("更新失败: %v\n", err)
            return
        }
        fmt.Println("更新成功")
        
        // 5. 删除
        err = client.Delete(userId, instanceId)
        if err != nil {
            fmt.Printf("删除失败: %v\n", err)
            return
        }
        fmt.Println("删除成功")
    }
}
```

**Python:**
```python
import json
from typing import Dict, Any, Optional, List
from alibabacloud_dingtalk.yida_1_0.client import Client as dingtalkyida_1_0Client
from alibabacloud_dingtalk.yida_2_0.client import Client as dingtalkyida_2_0Client
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models
from alibabacloud_dingtalk.yida_2_0 import models as dingtalkyida__2__0_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


class YidaFormClient:
    """宜搭表单客户端"""
    
    def __init__(
        self,
        access_token: str,
        app_type: str,
        system_token: str,
        form_uuid: str
    ):
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        
        self.v1_client = dingtalkyida_1_0Client(config)
        self.v2_client = dingtalkyida_2_0Client(config)
        
        self.access_token = access_token
        self.app_type = app_type
        self.system_token = system_token
        self.form_uuid = form_uuid
    
    def create(self, user_id: str, form_data: Dict[str, Any]) -> Optional[str]:
        """创建表单实例"""
        headers = dingtalkyida__2__0_models.SaveFormDataHeaders()
        headers.x_acs_dingtalk_access_token = self.access_token
        
        data_json = json.dumps(form_data, ensure_ascii=False)
        
        request = dingtalkyida__2__0_models.SaveFormDataRequest(
            app_type=self.app_type,
            system_token=self.system_token,
            user_id=user_id,
            form_uuid=self.form_uuid,
            form_data_json=data_json
        )
        
        try:
            response = self.v2_client.save_form_data_with_options(
                request, headers, util_models.RuntimeOptions()
            )
            return response.body.result
        except Exception as err:
            print(f"创建失败: {err}")
            return None
    
    def search(
        self,
        search_fields: Dict[str, Any],
        page: int = 1,
        page_size: int = 10
    ) -> Optional[dingtalkyida__2__0_models.SearchFormDatasResponseBody]:
        """查询表单实例列表"""
        headers = dingtalkyida__2__0_models.SearchFormDatasHeaders()
        headers.x_acs_dingtalk_access_token = self.access_token
        
        search_field_json = json.dumps(search_fields, ensure_ascii=False) if search_fields else ""
        
        request = dingtalkyida__2__0_models.SearchFormDatasRequest(
            app_type=self.app_type,
            system_token=self.system_token,
            form_uuid=self.form_uuid,
            current_page=page,
            page_size=page_size,
            search_field_json=search_field_json
        )
        
        try:
            response = self.v2_client.search_form_datas_with_options(
                request, headers, util_models.RuntimeOptions()
            )
            return response.body
        except Exception as err:
            print(f"查询失败: {err}")
            return None
    
    def get_by_id(
        self,
        user_id: str,
        form_instance_id: str
    ) -> Optional[dingtalkyida__2__0_models.GetFormDataByIDResponseBody]:
        """根据ID获取表单实例"""
        headers = dingtalkyida__2__0_models.GetFormDataByIDHeaders()
        headers.x_acs_dingtalk_access_token = self.access_token
        
        request = dingtalkyida__2__0_models.GetFormDataByIDRequest(
            app_type=self.app_type,
            system_token=self.system_token,
            user_id=user_id,
            form_uuid=self.form_uuid
        )
        
        try:
            response = self.v2_client.get_form_data_by_idwith_options(
                form_instance_id,
                request,
                headers,
                util_models.RuntimeOptions()
            )
            return response.body
        except Exception as err:
            print(f"获取详情失败: {err}")
            return None
    
    def update(
        self,
        user_id: str,
        form_instance_id: str,
        update_data: Dict[str, Any]
    ) -> bool:
        """更新表单实例"""
        headers = dingtalkyida__2__0_models.UpdateFormDataHeaders()
        headers.x_acs_dingtalk_access_token = self.access_token
        
        data_json = json.dumps(update_data, ensure_ascii=False)
        
        request = dingtalkyida__2__0_models.UpdateFormDataRequest(
            app_type=self.app_type,
            system_token=self.system_token,
            user_id=user_id,
            form_instance_id=form_instance_id,
            form_uuid=self.form_uuid,
            update_form_data_json=data_json
        )
        
        try:
            self.v2_client.update_form_data_with_options(
                request, headers, util_models.RuntimeOptions()
            )
            return True
        except Exception as err:
            print(f"更新失败: {err}")
            return False
    
    def delete(self, user_id: str, form_instance_id: str) -> bool:
        """删除表单实例"""
        headers = dingtalkyida__1__0_models.DeleteFormDataHeaders()
        headers.x_acs_dingtalk_access_token = self.access_token
        
        request = dingtalkyida__1__0_models.DeleteFormDataRequest(
            app_type=self.app_type,
            system_token=self.system_token,
            user_id=user_id,
            form_instance_id=form_instance_id
        )
        
        try:
            self.v1_client.delete_form_data_with_options(
                request, headers, util_models.RuntimeOptions()
            )
            return True
        except Exception as err:
            print(f"删除失败: {err}")
            return False


# 使用示例
if __name__ == '__main__':
    client = YidaFormClient(
        "<your_access_token>",
        "APP_XXXXX",
        "system_token",
        "FORM-XXXXX"
    )
    
    user_id = "ding173982232112232"
    
    # 1. 创建
    form_data = {
        "textField_xxx": "测试数据",
        "numberField_xxx": 100
    }
    
    form_uuid = client.create(user_id, form_data)
    if form_uuid:
        print(f"创建成功: {form_uuid}")
    else:
        print("创建失败")
        exit(1)
    
    # 2. 查询列表
    search_result = client.search(None, 1, 10)
    if search_result:
        print(f"查询到 {search_result.total_count} 条数据")
    else:
        print("查询失败")
        exit(1)
    
    # 3. 获取单条
    if search_result.data:
        instance_id = search_result.data[0].form_instance_id
        detail = client.get_by_id(user_id, instance_id)
        if detail:
            print(f"详情: {detail}")
        else:
            print("获取详情失败")
            exit(1)
        
        # 4. 更新
        update_data = {
            "textField_xxx": "更新后的值"
        }
        if client.update(user_id, instance_id, update_data):
            print("更新成功")
        else:
            print("更新失败")
            exit(1)
        
        # 5. 删除
        if client.delete(user_id, instance_id):
            print("删除成功")
        else:
            print("删除失败")
            exit(1)
```
