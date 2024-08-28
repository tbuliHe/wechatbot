# WeChatBot 使用指南

本文档介绍如何使用 WeChatBot 及其相关服务，包括如何启动 WeChat Webhook 服务、测试消息发送、启动消息接收服务器、运行应答程序以及接收消息的 JSON 格式。

## 1. 启动 WeChat Webhook 服务
链接如下
<https://github.com/danni-cool/wechatbot-webhook>
### 1.1 拉取最新镜像
首先，使用以下命令拉取最新的 WeChat Webhook Docker 镜像：
```bash
docker pull dannicool/docker-wechatbot-webhook
```

### 1.2 Docker 部署
使用以下命令启动 Docker 容器，并将日志目录映射到本地。日志按天生成，文件命名格式为 `app.YYYY-MM-DD.log`：
```bash
sudo docker run -d --name wxBotWebhook --restart unless-stopped -p 3001:3001 \
-v ~/wxBot_logs:/app/log \
-e ACCEPT_RECVD_MSG_MYSELF=true \
-e RECVD_MSG_API=http://129.150.39.xxx:3000/receive/ \
-e LOGIN_API_TOKEN=123 dannicool/docker-wechatbot-webhook
```

### 1.3 查看容器是否创建成功
使用以下命令查看容器是否成功创建：
```bash
sudo docker ps
```

### 1.4 查看日志并登录
查看日志并登录 WeChat Webhook 服务：
```bash
sudo docker logs -f wxBotWebhook
```

## 2. 测试消息发送

使用以下 `curl` 命令测试消息发送：
```bash
curl --location 'http://localhost:3001/webhook/msg/v2?token=[YOUR_PERSONAL_TOKEN]' \
--header 'Content-Type: application/json' \
--data '{ "to": "测试昵称", data: { "content": "Hello World!" }}'
```
请将 `[YOUR_PERSONAL_TOKEN]` 替换为你的个人 token。

## 3. 启动接收消息服务器

### 3.1 查看端口是否被占用
在启动接收消息服务器之前，首先查看端口 `3000` 是否被占用：
```bash
lsof -i tcp:3000
```

### 3.2 删除占用进程
如果端口被占用，使用以下命令删除占用进程：
```bash
kill -9 <PID>
```
将 `<PID>` 替换为实际的进程 ID。

### 3.3 运行 `app.js`
运行接收消息的服务器：
```bash
node app.js
```

## 4. 运行应答程序

使用以下命令运行 Python 应答程序：
```bash
python3 -u "/home/dim/code/wechatbot/receive.py"
```
按下 `Ctrl + C` 退出程序。

## 5. 接收消息 JSON 格式

当收到消息时，消息将以 JSON 格式显示。以下是一个示例：

```json
Received message:
└── [Object: null prototype]
    └── {
        ├── source: 
        │   └── {
        │       ├── room: {}
        │       ├── to: 
        │       │   ├── _events: {}
        │       │   ├── _eventsCount: 0
        │       │   ├── id: "filehelper"
        │       │   └── payload: 
        │       │       ├── address: ""
        │       │       ├── alias: ""
        │       │       ├── avatar: "http://localhost:3001/resouces?media=%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxgeticon%3Fseq%3D831630031%26username%3Dfilehelper%26skey%3D%40crypt_ff7c48e2_7e72937d384ca333e3d63b2c15a33f73"
        │       │       ├── city: ""
        │       │       ├── friend: true
        │       │       ├── gender: 0
        │       │       ├── id: "filehelper"
        │       │       ├── name: "文件传输助手"
        │       │       ├── phone: []
        │       │       ├── province: ""
        │       │       ├── signature: ""
        │       │       ├── star: false
        │       │       └── weixin: ""
        │       └── from: 
        │           ├── _events: {}
        │           ├── _eventsCount: 0
        │           ├── id: "@8dbcd335220ab48e8f4f89ae9c9faf0f4765a6eec23a03505cecba9675af0a36"
        │           └── payload: 
        │               ├── alias: ""
        │               ├── avatar: "http://localhost:3001/resouces?media=%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxgeticon%3Fseq%3D1846417495%26username%3D%408dbcd335220ab48e8f4f89ae9c9faf0f4765a6eec23a03505cecba9675af0a36%26skey%3D%40crypt_ff7c48e2_6a51a5300447fadb37147f0374293e67"
        │               ├── friend: false
        │               ├── gender: 0
        │               ├── id: "@8dbcd335220ab48e8f4f89ae9c9faf0f4765a6eec23a03505cecba9675af0a36"
        │               ├── name: "Kobe"
        │               ├── phone: []
        │               ├── signature: ""
        │               ├── star: false
        │               └── type: 1
        ├── isSystemEvent: "0"
        ├── isMentioned: "0"
        ├── isMsgFromSelf: "1"
        ├── type: "text"
        └── content: "我的超市"
    }
```
## 5. 在后台运行
```
 cd ~/code/wechatbot
 nohup node app.js > app.log 2>&1 &
 nohup python3 -u receive.py > receive.log 2>&1 &
```
