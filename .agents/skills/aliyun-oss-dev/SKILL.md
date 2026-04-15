---
name: aliyun-oss-dev
description: 阿里云OSS（对象存储服务）开发指南，支持Go、Python和C++ SDK。Use when user needs to develop applications using Alibaba Cloud OSS, including bucket operations, object upload/download, multipart upload, presigned URLs, client-side encryption, or any OSS-related development tasks in Go, Python, or C++.
---

# 阿里云OSS开发指南

本Skill提供阿里云对象存储服务（OSS）的开发指导，支持Go、Python和C++三种语言的SDK。

## SDK安装

### Go SDK
```bash
go get github.com/aliyun/alibabacloud-oss-go-sdk-v2
```

### Python SDK
```bash
pip install alibabacloud-oss-v2
```

### C++ SDK
从 GitHub 下载或克隆源码后与项目一起编译：
```bash
git clone https://github.com/aliyun/aliyun-oss-cpp-sdk.git
```

## 快速开始

### 1. 配置客户端

**Go:**
```go
import (
    "github.com/aliyun/alibabacloud-oss-go-sdk-v2/oss"
    "github.com/aliyun/alibabacloud-oss-go-sdk-v2/oss/credentials"
)

provider := credentials.NewEnvironmentVariableCredentialsProvider()
cfg := oss.LoadDefaultConfig().
    WithCredentialsProvider(provider).
    WithRegion("cn-hangzhou")
client := oss.NewClient(cfg)
```

**Python:**
```python
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = "cn-hangzhou"
client = oss.Client(cfg)
```

**C++:**
```cpp
#include <alibabacloud/oss/OssClient.h>
using namespace AlibabaCloud::OSS;

int main(void)
{
    std::string Endpoint = "yourEndpoint";
    std::string Region = "yourRegion";

    InitializeSdk();
    ClientConfiguration conf;
    conf.signatureVersion = SignatureVersionType::V4;
    conf.maxConnections = 20;
    conf.requestTimeoutMs = 8000;
    conf.connectTimeoutMs = 8000;

    auto credentialsProvider = std::make_shared<EnvironmentVariableCredentialsProvider>();
    OssClient client(Endpoint, credentialsProvider, conf);
    client.SetRegion(Region);

    // ... 执行业务操作 ...

    ShutdownSdk();
    return 0;
}
```

### 2. 凭证配置方式

| 方式 | Go | Python | C++ |
|-----|-----|--------|-----|
| 环境变量 | `credentials.NewEnvironmentVariableCredentialsProvider()` | `oss.credentials.EnvironmentVariableCredentialsProvider()` | `EnvironmentVariableCredentialsProvider()` |
| 静态凭证 | `credentials.NewStaticCredentialsProvider(ak, sk)` | `oss.credentials.StaticCredentialsProvider(ak, sk)` | `SimpleCredentialsProvider(ak, sk)` |
| ECS实例角色 | `credentials.NewEcsRoleCredentialsProvider()` | 需配合credentials-python库 | 需自行实现 |
| RAM角色 | 需配合credentials-go库 | 需配合credentials-python库 | 需自行实现 |

环境变量名：`OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`, `OSS_SESSION_TOKEN`(可选)

## 核心操作

### Bucket操作

**创建Bucket:**
```go
// Go
result, err := client.PutBucket(context.TODO(), &oss.PutBucketRequest{
    Bucket: oss.Ptr("bucket-name"),
    Acl:    oss.BucketACLPrivate,
    CreateBucketConfiguration: &oss.CreateBucketConfiguration{
        StorageClass: oss.StorageClassIA,
    },
})
```

```python
# Python
result = client.put_bucket(oss.PutBucketRequest(
    bucket="bucket-name",
    acl='private',
    create_bucket_configuration=oss.CreateBucketConfiguration(
        storage_class='IA'
    )
))
```

**列举Buckets:**
```go
p := client.NewListBucketsPaginator(&oss.ListBucketsRequest{})
for p.HasNext() {
    page, _ := p.NextPage(context.TODO())
    for _, b := range page.Buckets {
        fmt.Println(oss.ToString(b.Name))
    }
}
```

```python
paginator = client.list_buckets_paginator()
for page in paginator.iter_page(oss.ListBucketsRequest()):
    for b in page.buckets:
        print(b.name)
```

### 对象上传

**简单上传（最大5GiB）:**
```go
result, err := client.PutObject(context.TODO(), &oss.PutObjectRequest{
    Bucket: oss.Ptr("bucket"),
    Key:    oss.Ptr("key"),
    Body:   bytes.NewReader(data),
})
```

```python
result = client.put_object(oss.PutObjectRequest(
    bucket="bucket",
    key="key",
    body=data
))
```

```cpp
// C++ 上传本地文件
std::string BucketName = "examplebucket";
std::string ObjectName = "exampledir/exampleobject.txt";
std::shared_ptr<std::iostream> content = std::make_shared<std::fstream>(
    "D:\\localpath\\examplefile.txt", std::ios::in | std::ios::binary);
PutObjectRequest request(BucketName, ObjectName, content);

auto outcome = client.PutObject(request);
if (!outcome.isSuccess()) {
    std::cout << "PutObject fail" <<
    ",code:" << outcome.error().Code() <<
    ",message:" << outcome.error().Message() <<
    ",requestId:" << outcome.error().RequestId() << std::endl;
    return -1;
}
```

**文件上传:**
```go
result, err := client.PutObjectFromFile(context.TODO(), 
    &oss.PutObjectRequest{Bucket: oss.Ptr("bucket"), Key: oss.Ptr("key")},
    "/local/path/to/file")
```

```python
result = client.put_object_from_file(
    oss.PutObjectRequest(bucket="bucket", key="key"),
    "/local/path/to/file"
)
```

**追加上传:**
```cpp
// C++ 追加上传
auto meta = ObjectMetaData();
meta.setContentType("text/plain");

std::shared_ptr<std::iostream> content1 = std::make_shared<std::stringstream>();
*content1 << "Thank you for using Aliyun Object Storage Service!";
AppendObjectRequest request(BucketName, ObjectName, content1, meta);
request.setPosition(0L);

auto result = client.AppendObject(request);
if (!result.isSuccess()) { /* 异常处理 */ }

std::shared_ptr<std::iostream> content2 = std::make_shared<std::stringstream>();
*content2 << "Thank you for using Aliyun Object Storage Service!";
auto position = result.result().Length();
AppendObjectRequest appendObjectRequest(BucketName, ObjectName, content2);
appendObjectRequest.setPosition(position);
auto outcome = client.AppendObject(appendObjectRequest);
```

### 对象下载

**流式下载:**
```go
result, err := client.GetObject(context.TODO(), &oss.GetObjectRequest{
    Bucket: oss.Ptr("bucket"),
    Key:    oss.Ptr("key"),
})
defer result.Body.Close()
data, _ := io.ReadAll(result.Body)
```

```python
result = client.get_object(oss.GetObjectRequest(
    bucket="bucket",
    key="key"
))
data = result.body.read()
```

**下载到文件:**
```go
result, err := client.GetObjectToFile(context.TODO(),
    &oss.GetObjectRequest{Bucket: oss.Ptr("bucket"), Key: oss.Ptr("key")},
    "/local/path/to/file")
```

```python
result = client.get_object_to_file(
    oss.GetObjectRequest(bucket="bucket", key="key"),
    "/local/path/to/file"
)
```

### 大文件传输（Uploader/Downloader）

**上传大文件（支持断点续传）:**
```go
u := client.NewUploader(func(uo *oss.UploaderOptions) {
    uo.PartSize = 10 * 1024 * 1024  // 10MB分片
    uo.ParallelNum = 5
    uo.EnableCheckpoint = true
    uo.CheckpointDir = "/local/checkpoint/dir"
})

result, err := u.UploadFile(context.TODO(),
    &oss.PutObjectRequest{Bucket: oss.Ptr("bucket"), Key: oss.Ptr("key")},
    "/local/large/file")
```

```python
uploader = client.uploader(
    part_size=10*1024*1024,
    parallel_num=5,
    enable_checkpoint=True,
    checkpoint_dir="/local/checkpoint/dir"
)

result = uploader.upload_file(
    oss.PutObjectRequest(bucket="bucket", key="key"),
    filepath="/local/large/file"
)
```

**下载大文件（支持断点续传）:**
```go
d := client.NewDownloader(func(do *oss.DownloaderOptions) {
    do.PartSize = 10 * 1024 * 1024
    do.ParallelNum = 5
    do.EnableCheckpoint = true
})

result, err := d.DownloadFile(context.TODO(),
    &oss.GetObjectRequest{Bucket: oss.Ptr("bucket"), Key: oss.Ptr("key")},
    "/local/output/file")
```

```python
downloader = client.downloader(
    part_size=10*1024*1024,
    parallel_num=5,
    enable_checkpoint=True
)

result = downloader.download_file(
    oss.GetObjectRequest(bucket="bucket", key="key"),
    filepath="/local/output/file"
)
```

### 预签名URL

**生成临时访问URL:**
```go
result, err := client.Presign(context.TODO(), &oss.GetObjectRequest{
    Bucket: oss.Ptr("bucket"),
    Key:    oss.Ptr("key"),
}, oss.PresignExpires(30*time.Minute))
// result.URL 即为预签名URL
```

```python
pre_result = client.presign(
    oss.GetObjectRequest(bucket="bucket", key="key"),
    expires=datetime.timedelta(minutes=30)
)
# pre_result.url 即为预签名URL
```

### 分片上传

```go
// 1. 初始化分片上传
initResult, err := client.InitiateMultipartUpload(context.TODO(), &oss.InitiateMultipartUploadRequest{
    Bucket: oss.Ptr("bucket"),
    Key:    oss.Ptr("key"),
})

// 2. 上传分片
var parts oss.UploadParts
for i, chunk := range chunks {
    upResult, err := client.UploadPart(context.TODO(), &oss.UploadPartRequest{
        Bucket:     oss.Ptr("bucket"),
        Key:        oss.Ptr("key"),
        UploadId:   initResult.UploadId,
        PartNumber: int32(i + 1),
        Body:       bytes.NewReader(chunk),
    })
    parts = append(parts, oss.UploadPart{
        PartNumber: int32(i + 1),
        ETag:       upResult.ETag,
    })
}

// 3. 完成分片上传
sort.Sort(parts)
_, err = client.CompleteMultipartUpload(context.TODO(), &oss.CompleteMultipartUploadRequest{
    Bucket:   oss.Ptr("bucket"),
    Key:      oss.Ptr("key"),
    UploadId: initResult.UploadId,
    CompleteMultipartUpload: &oss.CompleteMultipartUpload{Parts: parts},
})
```

```python
# 1. 初始化分片上传
result = client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
    bucket="bucket",
    key="key"
))

# 2. 上传分片
upload_parts = []
for i, chunk in enumerate(chunks, 1):
    up_result = client.upload_part(oss.UploadPartRequest(
        bucket="bucket",
        key="key",
        upload_id=result.upload_id,
        part_number=i,
        body=chunk
    ))
    upload_parts.append(oss.UploadPart(part_number=i, etag=up_result.etag))

# 3. 完成分片上传
parts = sorted(upload_parts, key=lambda p: p.part_number)
result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
    bucket="bucket",
    key="key",
    upload_id=result.upload_id,
    complete_multipart_upload=oss.CompleteMultipartUpload(parts=parts)
))
```

### 列举文件

**C++ 列举存储空间下的文件（默认100个）:**
```cpp
ListObjectsRequest request(BucketName);
auto outcome = client.ListObjects(request);

if (!outcome.isSuccess()) {
    std::cout << "ListObjects fail" <<
    ",code:" << outcome.error().Code() <<
    ",message:" << outcome.error().Message() <<
    ",requestId:" << outcome.error().RequestId() << std::endl;
    return -1;
}
else {
    for (const auto& object : outcome.result().ObjectSummarys()) {
        std::cout << "object" <<
        ",name:" << object.Key() <<
        ",size:" << object.Size() <<
        ",last modified time:" << object.LastModified() << std::endl;
    }
}
```

## 高级功能

### 客户端加密

使用RSA主密钥进行客户端加密：

```go
import "github.com/aliyun/alibabacloud-oss-go-sdk-v2/oss/crypto"

mc, _ := crypto.CreateMasterRsa(
    map[string]string{"desc": "key description"},
    publicKey,
    privateKey,
)
eclient, _ := oss.NewEncryptionClient(client, mc)

// 使用eclient进行加密上传/下载
eclient.PutObject(context.TODO(), &oss.PutObjectRequest{...})
```

```python
mc = oss.crypto.MasterRsaCipher(
    mat_desc={"desc": "key description"},
    public_key=public_key,
    private_key=private_key
)
encryption_client = oss.EncryptionClient(client, mc)

# 使用encryption_client进行加密上传/下载
encryption_client.put_object(oss.PutObjectRequest(...))
```

### File-Like接口

**只读文件:**
```go
f, err := client.OpenFile(context.TODO(), "bucket", "key", func(oo *oss.OpenOptions) {
    oo.EnablePrefetch = true  // 启用预取模式
})
defer f.Close()

// 使用io.Copy等标准接口读取
io.Copy(io.Discard, f)
```

```python
with client.open_file("bucket", "key", enable_prefetch=True) as f:
    data = f.read()
```

**追加写文件:**
```go
f, err := client.AppendFile(context.TODO(), "bucket", "key")
defer f.Close()

f.Write([]byte("hello"))
f.Write([]byte(" world"))
```

```python
with client.append_file("bucket", "key") as f:
    f.write(b"hello")
    f.write(b" world")
```

### 进度条

**Go:**
```go
progressFn := func(written, total int64) {
    rate := int(100 * float64(written) / float64(total))
    fmt.Printf("\r%d%%", rate)
}

client.PutObject(context.TODO(), &oss.PutObjectRequest{
    Bucket:     oss.Ptr("bucket"),
    Key:        oss.Ptr("key"),
    Body:       reader,
    ProgressFn: progressFn,
})
```

**Python:**
```python
def progress_fn(n, written, total):
    rate = int(100 * float(written) / float(total))
    print(f'\r{rate}%', end='')

client.put_object(oss.PutObjectRequest(
    bucket="bucket",
    key="key",
    body=data,
    progress_fn=progress_fn
))
```

**C++:**
```cpp
void ProgressCallback(size_t increment, int64_t transfered, int64_t total, void* userData)
{
    // increment表示本次回调发送的数据大小。
    // transfered表示已上传的数据大小。
    // total表示上传文件的总大小。
    std::cout << "ProgressCallback[" << userData << "] => " <<
    increment << " ," << transfered << "," << total << std::endl;
}

std::shared_ptr<std::iostream> content = std::make_shared<std::fstream>(
    "yourLocalFilename", std::ios::in | std::ios::binary);
PutObjectRequest request(BucketName, ObjectName, content);

TransferProgress progressCallback = { ProgressCallback , nullptr };
request.setTransferProgress(progressCallback);

auto outcome = client.PutObject(request);
```

### 上传回调

**C++ 上传回调:**
```cpp
std::string ServerName = "https://example.aliyundoc.com:23450";
std::shared_ptr<std::iostream> content = std::make_shared<std::stringstream>();
*content << "Thank you for using Aliyun Object Storage Service!";

std::string callbackBody = "bucket=${bucket}&object=${object}&etag=${etag}&size=${size}&mimeType=${mimeType}&my_var1=${x:var1}";
ObjectCallbackBuilder builder(ServerName, callbackBody, "", ObjectCallbackBuilder::Type::URL);
std::string value = builder.build();
ObjectCallbackVariableBuilder varBuilder;
varBuilder.addCallbackVariable("x:var1", "value1");
std::string varValue = varBuilder.build();
PutObjectRequest request(BucketName, ObjectName, content);
request.MetaData().addHeader("x-oss-callback", value);
request.MetaData().addHeader("x-oss-callback-var", varValue);
auto outcome = client.PutObject(request);
```

## 配置参数参考

| 参数 | Go | Python | C++ | 说明 |
|-----|-----|--------|-----|------|
| Region | `WithRegion("cn-hangzhou")` | `cfg.region = "cn-hangzhou"` | `client.SetRegion("cn-hangzhou")` | 必选 |
| Endpoint | `WithEndpoint("...")` | `cfg.endpoint = "..."` | 构造时传入 Endpoint | 自定义域名 |
| 内网域名 | `WithUseInternalEndpoint(true)` | `cfg.use_internal_endpoint = True` | - | 使用内网访问 |
| 传输加速 | `WithUseAccelerateEndpoint(true)` | `cfg.use_accelerate_endpoint = True` | - | 启用传输加速 |
| 连接超时 | `WithConnectTimeout(10*time.Second)` | `cfg.connect_timeout = 10` | `conf.connectTimeoutMs = 10000` | 默认5s(Go)/10s(Py)/5000ms(C++) |
| 读写超时 | `WithReadWriteTimeout(30*time.Second)` | `cfg.readwrite_timeout = 30` | `conf.requestTimeoutMs = 10000` | 默认10s(Go)/20s(Py)/10000ms(C++) |
| 最大连接数 | - | - | `conf.maxConnections = 16` | 默认16(C++) |
| 最大重试 | `WithRetryMaxAttempts(5)` | `cfg.retry_max_attempts = 5` | `conf.retryStrategy` | 默认3次 |
| 跳过SSL校验 | `WithInsecureSkipVerify(true)` | `cfg.insecure_skip_verify = True` | `conf.verifySSL = false` | 开发调试用 |
| CA证书路径 | - | - | `conf.caPath` / `conf.caFile` | C++ 开启SSL校验时有效 |
| CRC64校验 | - | - | `conf.enableCRC64 = true` | 默认开启(C++) |
| 时间自动修正 | - | - | `conf.enableDateSkewAdjustment = true` | 默认开启(C++) |
| 上传限速 | - | - | `conf.sendRateLimiter` | 单位 KB/s (C++) |
| 下载限速 | - | - | `conf.recvRateLimiter` | 单位 KB/s (C++) |

## 详细参考

- **Go SDK完整指南**: 参见 [references/goland-DEVGUIDE-CN.md](references/goland-DEVGUIDE-CN.md)
- **Python SDK完整指南**: 参见 [references/python3-DEVGUIDE-CN.md](references/python3-DEVGUIDE-CN.md)

包含内容：
- 完整的API接口说明
- 所有凭证配置方式（ECS角色、RAM角色、OIDC等）
- 分页器使用
- 拷贝管理器
- 数据校验（MD5/CRC64）
- 错误处理
- 迁移指南（从V1到V2）
