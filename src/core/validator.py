"""
验证器模块
提供各种验证功能
"""
import re
import ipaddress


class Validator:
    """输入验证器"""
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        验证IP地址
        
        Args:
            ip: IP地址字符串
            
        Returns:
            bool: 是否有效
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_port(port: str) -> tuple:
        """
        验证端口号
        
        Args:
            port: 端口号字符串
            
        Returns:
            tuple: (是否有效, 错误信息, 端口号)
        """
        try:
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return True, "", port_num
            else:
                return False, "端口号必须在 1-65535 之间", 0
        except ValueError:
            return False, "端口号必须是数字", 0
    
    @staticmethod
    def validate_username(username: str) -> tuple:
        """
        验证用户名
        
        Args:
            username: 用户名
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not username:
            return False, "用户名不能为空"
        
        if len(username) > 32:
            return False, "用户名长度不能超过32个字符"
        
        # 用户名只能包含字母、数字、下划线、连字符
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "用户名只能包含字母、数字、下划线和连字符"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> tuple:
        """
        验证密码
        
        Args:
            password: 密码
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not password:
            return False, "密码不能为空"
        
        return True, ""
    
    @staticmethod
    def validate_remote_path(path: str) -> tuple:
        """
        验证远程路径
        
        Args:
            path: 路径字符串
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not path:
            return False, "目标目录不能为空"
        
        if not path.startswith('/'):
            return False, "目标目录必须是绝对路径（以 / 开头）"
        
        # 检查非法字符
        if re.search(r'[;|&`$]', path):
            return False, "路径包含非法字符"
        
        return True, ""
