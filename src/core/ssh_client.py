"""
SSH 客户端模块
处理与远程服务器的 SSH 连接
"""
import paramiko
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import socket


class SSHClientWrapper:
    """SSH 客户端包装器"""
    
    def __init__(self):
        self.client: SSHClient = None
        self.scp: SCPClient = None
        self.connected = False
    
    def connect(self, host: str, port: int, username: str, password: str, timeout: int = 10) -> bool:
        """
        连接远程服务器
        
        Args:
            host: 服务器IP地址
            port: SSH端口
            username: 用户名
            password: 密码
            timeout: 超时时间（秒）
            
        Returns:
            bool: 连接是否成功
        """
        try:
            self.client = SSHClient()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                hostname=host,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                look_for_keys=False,
                allow_agent=False
            )
            
            # 创建 SCP 客户端
            self.scp = SCPClient(self.client.get_transport())
            self.connected = True
            return True
            
        except paramiko.AuthenticationException:
            raise ConnectionError("认证失败：用户名或密码错误")
        except paramiko.SSHException as e:
            raise ConnectionError(f"SSH连接错误：{str(e)}")
        except socket.timeout:
            raise ConnectionError("连接超时：请检查IP地址和端口")
        except Exception as e:
            raise ConnectionError(f"连接失败：{str(e)}")
    
    def execute_command(self, command: str, sudo: bool = False, password: str = None) -> tuple:
        """
        执行远程命令
        
        Args:
            command: 要执行的命令
            sudo: 是否使用sudo
            password: sudo密码
            
        Returns:
            tuple: (stdout, stderr, exit_code)
        """
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        try:
            if sudo and password:
                # 使用 sudo 执行
                command = f"echo '{password}' | sudo -S {command}"
            
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            
            out = stdout.read().decode('utf-8', errors='replace').strip()
            err = stderr.read().decode('utf-8', errors='replace').strip()
            
            return out, err, exit_code
            
        except Exception as e:
            raise RuntimeError(f"命令执行失败：{str(e)}")
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        上传文件到远程服务器
        
        Args:
            local_path: 本地文件路径
            remote_path: 远程目标路径
            
        Returns:
            bool: 上传是否成功
        """
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        try:
            self.scp.put(local_path, remote_path)
            return True
        except Exception as e:
            raise RuntimeError(f"文件上传失败：{str(e)}")
    
    def check_docker(self) -> bool:
        """检查远程服务器是否安装了 Docker"""
        try:
            out, err, code = self.execute_command("docker --version")
            return code == 0
        except:
            return False
    
    def check_docker_compose(self) -> bool:
        """检查远程服务器是否安装了 Docker Compose"""
        try:
            # 先检查 docker compose 子命令（v2）
            out, err, code = self.execute_command("docker compose version")
            if code == 0:
                return True
            
            # 再检查 docker-compose 命令（v1）
            out, err, code = self.execute_command("docker-compose --version")
            return code == 0
        except:
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.scp:
            self.scp.close()
        if self.client:
            self.client.close()
        self.connected = False
    
    def __del__(self):
        """析构时断开连接"""
        self.disconnect()
