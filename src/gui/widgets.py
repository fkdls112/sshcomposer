"""
自定义组件模块
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QCheckBox)
from PyQt5.QtCore import Qt


class FileSelector(QWidget):
    """文件选择器组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("选择 docker-compose.yml 文件...")
        self.path_input.setReadOnly(True)
        
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setObjectName("browseButton")
        self.browse_btn.clicked.connect(self.browse_file)
        
        layout.addWidget(self.path_input, stretch=1)
        layout.addWidget(self.browse_btn)
    
    def browse_file(self):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 Docker Compose 文件",
            "",
            "YAML files (*.yml *.yaml);;All files (*.*)"
        )
        if file_path:
            self.path_input.setText(file_path)
    
    def get_path(self) -> str:
        """获取选择的文件路径"""
        return self.path_input.text()
    
    def clear(self):
        """清空选择"""
        self.path_input.clear()


class ServerConfigWidget(QWidget):
    """服务器配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # IP地址
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP地址："))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        # 端口
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口："))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("22")
        self.port_input.setText("22")
        self.port_input.setMaximumWidth(80)
        port_layout.addWidget(self.port_input)
        port_layout.addStretch()
        layout.addLayout(port_layout)
        
        # 用户名
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名："))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("root")
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)
        
        # 密码
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("密码："))
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("输入SSH密码")
        self.pass_input.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.pass_input)
        layout.addLayout(pass_layout)
        
        # sudo选项
        self.sudo_check = QCheckBox("使用 sudo 权限")
        self.sudo_check.setChecked(True)
        layout.addWidget(self.sudo_check)
    
    def get_config(self) -> dict:
        """获取服务器配置"""
        return {
            'host': self.ip_input.text().strip(),
            'port': self.port_input.text().strip(),
            'username': self.user_input.text().strip(),
            'password': self.pass_input.text(),
            'use_sudo': self.sudo_check.isChecked()
        }
    
    def clear(self):
        """清空配置"""
        self.ip_input.clear()
        self.port_input.setText("22")
        self.user_input.clear()
        self.pass_input.clear()
        self.sudo_check.setChecked(True)
