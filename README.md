Docker Compose 部署工具

📦 简介
Docker Compose 部署工具是一个基于 PyQt5 的图形化应用程序，旨在简化将 Docker Compose 项目部署到远程服务器的过程。通过直观的用户界面，用户可以轻松配置服务器连接信息、选择 Compose 文件，并一键完成部署操作。

✨ 核心功能
服务器连接管理：

支持 SSH 连接配置（IP、端口、用户名、密码）

自动处理 sudo 权限提升

文件传输：

本地 Docker Compose 文件上传到远程服务器

自定义目标部署目录

服务管理：

在远程服务器上执行 docker compose up -d

自动验证服务启动状态

可视化反馈：

实时部署进度显示

彩色日志输出（信息、警告、错误）

详细错误报告

🛠️ 系统要求
客户端（运行本工具）
操作系统：Windows 10/11, macOS 10.15+, Linux

Python：3.8 或更高版本

依赖库：PyQt5, Paramiko, SCP

目标服务器
操作系统：支持 SSH 的 Linux 发行版

必备组件：

Docker Engine 20.10+

Docker Compose v2.0+

支持 sudo 权限的 SSH 用户


🖥️ 界面使用指南
配置区域
服务器信息：

IP地址：目标服务器的IP地址（如 192.168.1.100）

端口：SSH端口（默认 22）

用户名：SSH登录用户名（需有sudo权限）

密码：SSH登录密码（也是sudo密码）

文件选择：

点击"浏览"按钮选择本地 docker-compose.yaml 文件

目标目录：

指定服务器上的部署路径（如 /opt/docker）

部署按钮：

点击"开始部署"启动部署流程

日志区域
实时显示部署过程的所有操作和结果

不同颜色标识不同级别的消息：

黑色：普通信息

绿色：成功操作

橙色：警告信息

红色：错误信息

支持清空日志功能

⚙️ 技术架构
图表
代码








🔒 安全说明
凭据处理：

密码仅存储在内存中，部署完成后立即清除

不会在磁盘上保存任何敏感信息

连接安全：

使用SSH协议进行加密通信

支持服务器密钥验证

权限控制：

仅执行必要的特权命令

部署完成后自动关闭连接

🌐 应用场景
开发环境部署
快速将本地开发的Docker Compose配置部署到测试服务器

持续交付
作为CI/CD流水线的手动审批环节，可视化控制部署过程

多环境管理
轻松管理开发、测试和生产环境的Docker服务

边缘计算
在远程设备上部署和管理Docker服务

❓ 常见问题解答
Q: 为什么连接服务器失败？
A: 请检查：

服务器IP和端口是否正确

防火墙是否允许SSH连接

服务器SSH服务是否正常运行

Q: 为什么sudo权限获取失败？
A: 请确认：

使用的密码是正确的sudo密码

SSH用户在sudoers列表中

服务器允许密码验证（检查/etc/ssh/sshd_config）

Q: 文件上传成功但服务未启动？
A: 请检查：

目标服务器是否安装Docker Compose

Compose文件语法是否正确

服务器资源是否充足（内存、磁盘空间）

Q: 如何查看详细错误信息？
A: 部署失败时会显示详细错误对话框，包含完整的错误堆栈信息。

📜 开源许可
本项目采用 MIT 许可证 开源，允许自由使用、修改和分发。

👥 贡献指南
欢迎通过 Issue 和 Pull Request 贡献代码：

Fork 项目仓库

创建特性分支 (git checkout -b feature/your-feature)

提交更改 (git commit -am 'Add some feature')

推送分支 (git push origin feature/your-feature)

创建 Pull Request

📬 联系信息
如有任何问题或建议，请联系：
baggy1917@gmail.com
