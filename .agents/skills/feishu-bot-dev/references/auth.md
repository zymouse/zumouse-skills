# 认证相关 API

## 获取 tenant_access_token

用于调用应用所在租户内的 API，最大有效期 2 小时。

```go
import (
    "context"
    "fmt"
    lark "github.com/larksuite/oapi-sdk-go/v3"
    larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
    larkauth "github.com/larksuite/oapi-sdk-go/v3/service/auth/v3"
)

client := lark.NewClient("YOUR_APP_ID", "YOUR_APP_SECRET")

req := larkauth.NewInternalTenantAccessTokenReqBuilder().
    Body(larkauth.NewInternalTenantAccessTokenReqBodyBuilder().
        AppId("cli_xxx").
        AppSecret("xxx").
        Build()).
    Build()

resp, err := client.Auth.V3.TenantAccessToken.Internal(context.Background(), req)
if err != nil {
    fmt.Println(err)
    return
}
if !resp.Success() {
    fmt.Printf("error: %s\n", larkcore.Prettify(resp.CodeError))
    return
}

fmt.Println(larkcore.Prettify(resp))
// resp.Data.TenantAccessToken - 访问令牌
// resp.Data.Expire - 过期时间(秒)
```

## 获取 app_access_token

用于调用应用级别的 API，最大有效期 2 小时。

```go
req := larkauth.NewInternalAppAccessTokenReqBuilder().
    Body(larkauth.NewInternalAppAccessTokenReqBodyBuilder().
        AppId("cli_xxx").
        AppSecret("xxx").
        Build()).
    Build()

resp, err := client.Auth.V3.AppAccessToken.Internal(context.Background(), req)
```

## 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "tenant_access_token": "t-caecc734c2e3328a62489fe0648c4b98779515d3",
    "expire": 7200
}
```

## 注意事项

- 剩余有效期小于 30 分钟时调用，会返回新的 token
- 剩余有效期大于等于 30 分钟时调用，返回原有 token
- 建议缓存 token，避免频繁调用
