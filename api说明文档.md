# API 功能说明文档

### 1. 上传文件

> 端点: /api/upload  
> 请求方法: POST
> 描述: 通过 API 上传文件到服务器。

#### 请求参数:
> file: 需要上传的文件，类型为 multipart/form-data。

- 响应:
成功时返回：
```json
{
  "status": "success",
  "filename": "文件名"
}
```
失败时返回：
```json
{
  "status": "error",
  "message": "未提供文件"
}
```
### 2. 列出所有文件
> 端点: /api/files
> 请求方法: GET
> 描述: 获取服务器上所有上传文件的列表。

- 响应:
成功时返回：
```json
{
  "status": "success",
  "files": ["文件1", "文件2", "文件3"]
}
```

### 3. 获取文件详情
> 端点: /api/file/<filename>
> 请求方法: GET
> 描述: 获取指定文件的详细信息，包括 MIME 类型。

请求参数:  
`<filename>`: 文件名，作为 URL 参数。  

- 响应:
成功时返回：
```json
{
  "status": "success",
  "filename": "文件名",
  "mime_type": "文件的MIME类型"
}
```

失败时返回：
```json
{
  "status": "error",
  "message": "文件未找到"
}
```


### 4. 下载文件
> 端点: /api/download/<filename>
> 请求方法: GET
> 描述: 下载服务器上的指定文件。

请求参数:  

`<filename>`: 文件名，作为 URL 参数。

- 响应:
成功时返回文件内容，自动触发浏览器的下载行为。  
失败时返回：
```json
{
  "status": "error",
  "message": "文件未找到"
}
```


### 5. 删除文件
> 端点: /api/delete/<filename>
> 请求方法: DELETE
> 描述: 从服务器上删除指定文件。

请求参数:  

`<filename>`: 文件名，作为 URL 参数。


- 响应:
成功时返回：
```json
{
  "status": "success",
  "message": "文件 <filename> 已删除"
}
```

失败时返回：
```json
{
  "status": "error",
  "message": "文件未找到"
}
```


## 错误代码

- status: "error" 表示请求处理失败。

- message 字段会包含详细的错误信息，例如文件未找到或未提供文件等。

## 使用示例

1. 上传文件
```bash
curl -X POST -F "file=@/path/to/your/file" http://your-server-address/api/upload
```

2. 列出所有文件
```bash
curl -X GET http://your-server-address/api/files
```

3. 获取文件详情
```bash
curl -X GET http://your-server-address/api/file/your-filename
```

4. 下载文件
```bash
curl -X GET http://your-server-address/api/download/your-filename -o local-filename
```

5. 删除文件
```bash
curl -X DELETE http://your-server-address/api/delete/your-filename
```

## 安全性

请确保管理后台的密码安全，并在生产环境中考虑使用 HTTPS 来保护传输过程中的数据安全。此外，可以在服务端添加更多的认证机制，以确保 API 调用的安全性。

这份文档提供了所有新增 API 的详细信息，可以帮助开发者快速了解如何与服务进行交互。