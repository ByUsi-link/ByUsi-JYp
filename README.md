# ByUsi-JYp


## 项目介绍

ByUsi-JYp 是一个基于 Flask 的简单云存储项目，提供文件上传、文件列表显示、以及文件在线预览功能。项目的目标是为用户提供一个简洁易用的文件管理平台，便于文件的存储与访问。

### 功能概览

- **文件上传：** 用户可以通过简洁的网页界面上传文件，上传的文件将被保存在服务器的 `uploads` 目录中。
- **文件列表：** 上传成功后，用户可以查看所有已上传的文件列表，方便管理。
- **文件预览：** 用户可以通过点击文件列表中的链接，直接在线预览文件内容。
- **界面：** 界面设计美观。
- **演示demo：**[Demon](https://juy.hucl.link/)

### 前端项目
- **点击该链接查看前端：** [链接](https://github.com/ByUsi-link/JYp-templates)

### 安装与运行

要在本地运行 ByUsi-JYp，您可以通过以下步骤来进行设置：
> 在此之前你可能需要安装这些工具
>> `vim`, `git`, `python3`或者`python`, `python-pip`或者`python3-pip`

1. 克隆项目
    ```sh
    git clone https://github.com/ByUsi-link/ByUsi-JYp JYp
    cd JYp
    git clone https://github.com/ByUsi-link/JYp-templates templates
    ```

3. 安装依赖
   ```sh
   bash PipDependentAmpere-turn.sh
   ```

4. 修改管理员密码和管理员密码加密密钥
   ```sh
   vim JYp.py
   ```
   > 主要需要修改 `app.secret_key` 的值和 `PASSWORD` 的值
   >> 其中 `app.secret_key` 的值是**管理员密码加密密钥，`PASSWORD` 的值是**管理员密码

5. 运行 Flask 应用
    ```sh
    python JYp.py
    ```

6. 在浏览器中访问 `http://localhost:2266` 来使用应用。

7. 管理员面板的地址是 `http://localhost:2266/admin`

### 简单说明

我会积极更新该项目

### 自行研究

如果您对项目的实现感兴趣，可以自行克隆项目并进行深入研究，了解其背后的实现细节。

---

ByUsi-JYp 提供了一个简单而功能强大的云存储解决方案，适合想要轻松管理文件的用户。

---

### 注意
- **应用站站长们请注意，如果你给我的应用输入到了你的应用站，那么请标注此开源仓库的地址，感谢配合**