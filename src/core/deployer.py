"""
部署器模块
处理 Docker Compose 部署逻辑
"""
import os
from .ssh_client import SSHClientWrapper
from ..utils.logger import Logger


class Deployer:
    """Docker Compose 部署器"""
    
    def __init__(self, logger: Logger = None):
        self.ssh = SSHClientWrapper()
        self.logger = logger or Logger()
    
    def validate_local_file(self, file_path: str) -> bool:
        """
        验证本地文件
        
        Args:
            file_path: 本地文件路径
            
        Returns:
            bool: 验证是否通过
        """
        if not file_path:
            raise ValueError("请选择 Docker Compose 文件")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"路径不是文件：{file_path}")
        
        # 检查文件名
        filename = os.path.basename(file_path).lower()
        valid_names = ['docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml']
        
        if filename not in valid_names:
            self.logger.warning(f"文件名建议为 docker-compose.yml 或 compose.yml")
        
        return True
    
    def validate_remote_path(self, path: str) -> bool:
        """
        验证远程路径
        
        Args:
            path: 远程路径
            
        Returns:
            bool: 验证是否通过
        """
        if not path:
            raise ValueError("请输入目标部署目录")
        
        if not path.startswith('/'):
            raise ValueError("目标目录必须是绝对路径（如 /opt/docker）")
        
        return True
    
    def deploy(self, host: str, port: int, username: str, password: str,
               local_file: str, remote_dir: str, use_sudo: bool = True) -> bool:
        """
        执行部署
        
        Args:
            host: 服务器IP
            port: SSH端口
            username: 用户名
            password: 密码
            local_file: 本地 Compose 文件路径
            remote_dir: 远程部署目录
            use_sudo: 是否使用sudo
            
        Returns:
            bool: 部署是否成功
        """
        try:
            # 1. 验证本地文件
            self.logger.info("验证本地文件...")
            self.validate_local_file(local_file)
            self.logger.success("本地文件验证通过")
            
            # 2. 验证远程路径
            self.logger.info("验证远程路径...")
            self.validate_remote_path(remote_dir)
            self.logger.success("远程路径验证通过")
            
            # 3. 连接服务器
            self.logger.info(f"连接服务器 {host}:{port}...")
            self.ssh.connect(host, port, username, password)
            self.logger.success("服务器连接成功")
            
            # 4. 检查 Docker
            self.logger.info("检查 Docker 环境...")
            if not self.ssh.check_docker():
                raise RuntimeError("远程服务器未安装 Docker")
            self.logger.success("Docker 已安装")
            
            if not self.ssh.check_docker_compose():
                raise RuntimeError("远程服务器未安装 Docker Compose")
            self.logger.success("Docker Compose 已安装")
            
            # 5. 创建远程目录
            self.logger.info(f"创建远程目录 {remote_dir}...")
            mkdir_cmd = f"mkdir -p {remote_dir}"
            if use_sudo:
                out, err, code = self.ssh.execute_command(mkdir_cmd, sudo=True, password=password)
            else:
                out, err, code = self.ssh.execute_command(mkdir_cmd)
            
            if code != 0:
                raise RuntimeError(f"创建目录失败：{err}")
            self.logger.success("远程目录创建成功")
            
            # 6. 上传文件
            self.logger.info("上传 Docker Compose 文件...")
            remote_file = f"{remote_dir}/{os.path.basename(local_file)}"
            self.ssh.upload_file(local_file, remote_file)
            self.logger.success("文件上传成功")
            
            # 7. 执行部署
            self.logger.info("执行 Docker Compose 部署...")
            compose_cmd = f"cd {remote_dir} && docker compose up -d"
            
            # 如果 docker compose 不行，尝试 docker-compose
            check_cmd = "docker compose version"
            out, err, code = self.ssh.execute_command(check_cmd)
            if code != 0:
                compose_cmd = f"cd {remote_dir} && docker-compose up -d"
            
            if use_sudo:
                out, err, code = self.ssh.execute_command(compose_cmd, sudo=True, password=password)
            else:
                out, err, code = self.ssh.execute_command(compose_cmd)
            
            if code != 0:
                raise RuntimeError(f"部署失败：{err}\n{out}")
            
            self.logger.success("Docker Compose 部署成功")
            
            # 8. 验证服务状态
            self.logger.info("验证服务状态...")
            ps_cmd = f"cd {remote_dir} && docker compose ps"
            if use_sudo:
                out, err, code = self.ssh.execute_command(ps_cmd, sudo=True, password=password)
            else:
                out, err, code = self.ssh.execute_command(ps_cmd)
            
            if out:
                self.logger.info("服务状态：\n" + out)
            
            self.logger.success("部署完成！")
            return True
            
        except Exception as e:
            self.logger.error(f"部署失败：{str(e)}")
            raise
        
        finally:
            # 断开连接
            if self.ssh.connected:
                self.ssh.disconnect()
                self.logger.info("已断开服务器连接")
