# DingTalk YiDa Code Examples

钉钉宜搭表单 API 完整代码示例。

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

```go
package main

import (
    "fmt"
    "os"
    
    "github.com/alibabacloud-go/dingtalk/yida_2_0"
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

---

## Create Operations

### Create Single Form Instance

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

### Create with Address Field

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

---

## Read Operations

### Search Form Instances

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

### Get Form Instance by ID

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

---

## Update Operations

### Update Form Instance

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

### Update SubTable

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

---

## Delete Operations

### Delete Single Instance

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

---

## Batch Operations

### Batch Create

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

### Batch Update

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

### Batch Delete

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

---

## Complete CRUD Example

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
