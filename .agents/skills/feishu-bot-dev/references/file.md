# 文件相关 API

## 上传文件

```go
import (
    "context"
    "os"
    larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

file, _ := os.Open("/path/to/file.pdf")

req := larkim.NewCreateFileReqBuilder().
    Body(larkim.NewCreateFileReqBodyBuilder().
        FileType("pdf").              // 文件类型: pdf, doc, xls, ppt, stream
        FileName("document.pdf").
        File(file).
        Build()).
    Build()

resp, err := client.Im.V1.File.Create(context.Background(), req)
// resp.Data.FileKey - 文件唯一标识
```

## 下载文件

```go
resp, err := client.Im.V1.File.Get(context.Background(), fileKey)
if err != nil {
    return err
}

// 保存到本地
resp.WriteFile("/path/to/save/filename")
```

## 上传图片

```go
image, _ := os.Open("/path/to/image.png")

req := larkim.NewCreateImageReqBuilder().
    Body(larkim.NewCreateImageReqBodyBuilder().
        ImageType("message").         // message: 消息图片, avatar: 头像
        Image(image).
        Build()).
    Build()

resp, err := client.Im.V1.Image.Create(context.Background(), req)
// resp.Data.ImageKey - 图片唯一标识
```

## 获取消息中的资源文件

```go
resp, err := client.Im.V1.MessageResource.Get(context.Background(), messageId, fileKey)
if err != nil {
    return err
}

resp.WriteFile("/path/to/save/filename")
```

## 文件类型说明

| FileType | 说明 |
|----------|------|
| pdf | PDF 文档 |
| doc | Word 文档 |
| xls | Excel 表格 |
| ppt | PPT 文档 |
| stream | 流式文件（音频、视频等）|

## 图片类型说明

| ImageType | 说明 |
|-----------|------|
| message | 用于发送消息的图片 |
| avatar | 头像图片 |
