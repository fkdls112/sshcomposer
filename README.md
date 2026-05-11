# SSH Composer — Docker Compose 远程部署工具 v1.0.6

## 📦 简介  
SSH Composer 是一个基于 PyQt5 的图形化工具，通过 SSH 将 Docker Compose 项目一键部署到远程 Linux 服务器。配置服务器信息、选择 Compose 文件，点击部署即可自动完成上传、启动和验证。

## ✨ 核心功能
- **SSH 连接**：IP/端口/用户名/密码，自动 sudo 提权
- **文件上传**：本地 docker-compose.yml 通过 SCP 传输到目标目录
- **一键部署**：自动执行 `docker compose up -d`
- **环境检测**：部署前自动检查 Docker 和 Docker Compose 是否可用
- **实时日志**：彩色日志（信息/成功/警告/错误），部署进度条

## 🛠️ 系统要求  
### 客户端（运行本工具）
- **操作系统**：Windows 10/11, macOS 10.15+, Linux
- **Python**：3.8 或更高版本
- **依赖库**：PyQt5, Paramiko, SCP

### 目标服务器
- **操作系统**：支持 SSH 的 Linux 发行版
- **必备组件**：
  - Docker Engine 20.10+
  - Docker Compose v2.0+
  - 支持 sudo 权限的 SSH 用户

## 🖥️ 界面使用指南  
### 配置区域
- **服务器信息**：
  - IP地址：目标服务器的IP地址（如 `192.168.1.100`）
  - 端口：SSH端口（默认 `22`）
  - 用户名：SSH登录用户名（需有sudo权限）
  - 密码：SSH登录密码（也是sudo密码）
- **文件选择**：
  - 点击"浏览"按钮选择本地 `docker-compose.yaml` 文件
- **目标目录**：
  - 指定服务器上的部署路径（如 `/opt/docker`）
- **部署按钮**：
  - 点击"开始部署"启动部署流程

### 日志区域
- 实时显示部署过程的所有操作和结果
- 不同颜色标识不同级别的消息：
  - 黑色：普通信息
  - 绿色：成功操作
  - 橙色：警告信息
  - 红色：错误信息
- 支持清空日志功能

## 🔒 安全说明  
- **凭据处理**：
  - 密码仅存储在内存中，部署完成后立即清除
  - 不会在磁盘上保存任何敏感信息
- **连接安全**：
  - 使用SSH协议进行加密通信
  - 支持服务器密钥验证
- **权限控制**：
  - 仅执行必要的特权命令
  - 部署完成后自动关闭连接

## 🚀 快速开始

### 方法一：直接运行源码
```bash
pip install -r requirements.txt
python main.py
```

### 方法二：下载打包 EXE
从 [Releases](https://github.com/fkdls112/sshcomposer/releases) 下载最新 `SSHComposer.exe`，双击运行即可。

## 📜 开源许可  
本项目采用 **MIT 许可证** 开源，允许自由使用、修改和分发。

## 👥 贡献指南  
欢迎通过 Issue 和 Pull Request 贡献代码：
1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

## 📬 联系信息  
如有任何问题或建议，请联系：  
[baggy1917@gmail.com](mailto:baggy1917@gmail.com)
