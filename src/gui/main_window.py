"""
主窗口模块
"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QTextEdit, QPushButton, QLabel, 
                             QProgressBar, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor

from .styles import MAIN_STYLE
from .widgets import FileSelector, ServerConfigWidget
from ..core.deployer import Deployer
from ..core.validator import Validator
from ..utils.logger import Logger, LogEmitter


class DeployThread(QThread):
    """部署线程"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, deployer, config):
        super().__init__()
        self.deployer = deployer
        self.config = config
    
    def run(self):
        """执行部署"""
        try:
            success = self.deployer.deploy(
                host=self.config['host'],
                port=self.config['port'],
                username=self.config['username'],
                password=self.config['password'],
                local_file=self.config['local_file'],
                remote_dir=self.config['remote_dir'],
                use_sudo=self.config['use_sudo']
            )
            self.finished.emit(True, "部署成功！")
        except Exception as e:
            self.finished.emit(False, str(e))


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Composer - Docker Compose 部署工具")
        self.setMinimumSize(800, 600)
        
        # 初始化日志
        self.log_emitter = LogEmitter()
        self.logger = Logger(self.log_emitter)
        self.log_emitter.log_signal.connect(self.append_log)
        
        # 初始化部署器
        self.deployer = Deployer(self.logger)
        self.deploy_thread = None
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧配置面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        # 服务器配置组
        server_group = QGroupBox("服务器配置")
        server_layout = QVBoxLayout(server_group)
        self.server_config = ServerConfigWidget()
        server_layout.addWidget(self.server_config)
        left_layout.addWidget(server_group)
        
        # 文件选择组
        file_group = QGroupBox("Docker Compose 文件")
        file_layout = QVBoxLayout(file_group)
        self.file_selector = FileSelector()
        file_layout.addWidget(self.file_selector)
        left_layout.addWidget(file_group)
        
        # 目标目录组
        dir_group = QGroupBox("目标部署目录")
        dir_layout = QVBoxLayout(dir_group)
        self.dir_input = QTextEdit()
        self.dir_input.setPlaceholderText("/opt/docker")
        self.dir_input.setMaximumHeight(40)
        self.dir_input.setText("/opt/docker")
        dir_layout.addWidget(self.dir_input)
        left_layout.addWidget(dir_group)
        
        # 部署按钮
        btn_layout = QHBoxLayout()
        self.deploy_btn = QPushButton("开始部署")
        self.deploy_btn.setObjectName("deployButton")
        self.deploy_btn.clicked.connect(self.start_deploy)
        btn_layout.addWidget(self.deploy_btn)
        
        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.clicked.connect(self.clear_log)
        btn_layout.addWidget(self.clear_btn)
        
        left_layout.addLayout(btn_layout)
        left_layout.addStretch()
        
        # 右侧日志面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        log_group = QGroupBox("部署日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.WidgetWidth)
        log_layout.addWidget(self.log_text)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        log_layout.addWidget(self.progress)
        
        right_layout.addWidget(log_group)
        
        # 添加到主布局
        main_layout.addWidget(left_panel, stretch=1)
        main_layout.addWidget(right_panel, stretch=2)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet(MAIN_STYLE)
    
    def append_log(self, message: str, level: str):
        """添加日志到文本框"""
        color_map = {
            "INFO": "#ecf0f1",
            "SUCCESS": "#2ecc71",
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c"
        }
        
        color = color_map.get(level, "#ecf0f1")
        
        self.log_text.moveCursor(QTextCursor.End)
        self.log_text.insertHtml(f'<span style="color: {color};">{message}</span><br>')
        self.log_text.moveCursor(QTextCursor.End)
    
    def validate_inputs(self) -> dict:
        """验证输入"""
        # 获取服务器配置
        server_config = self.server_config.get_config()
        
        # 验证IP
        if not server_config['host']:
            raise ValueError("请输入服务器IP地址")
        
        if not Validator.validate_ip(server_config['host']):
            raise ValueError("IP地址格式不正确")
        
        # 验证端口
        valid, error, port = Validator.validate_port(server_config['port'])
        if not valid:
            raise ValueError(f"端口错误：{error}")
        server_config['port'] = port
        
        # 验证用户名
        valid, error = Validator.validate_username(server_config['username'])
        if not valid:
            raise ValueError(f"用户名错误：{error}")
        
        # 验证密码
        valid, error = Validator.validate_password(server_config['password'])
        if not valid:
            raise ValueError(f"密码错误：{error}")
        
        # 验证文件
        local_file = self.file_selector.get_path()
        if not local_file:
            raise ValueError("请选择 Docker Compose 文件")
        
        # 验证目标目录
        remote_dir = self.dir_input.toPlainText().strip()
        if not remote_dir:
            remote_dir = "/opt/docker"
        
        valid, error = Validator.validate_remote_path(remote_dir)
        if not valid:
            raise ValueError(f"目标目录错误：{error}")
        
        return {
            **server_config,
            'local_file': local_file,
            'remote_dir': remote_dir
        }
    
    def start_deploy(self):
        """开始部署"""
        try:
            # 验证输入
            config = self.validate_inputs()
            
            # 禁用按钮
            self.deploy_btn.setEnabled(False)
            self.deploy_btn.setText("部署中...")
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)  # 无限进度
            
            # 清空日志
            self.clear_log()
            self.logger.info("开始部署...")
            
            # 创建部署线程
            self.deploy_thread = DeployThread(self.deployer, config)
            self.deploy_thread.finished.connect(self.deploy_finished)
            self.deploy_thread.start()
            
        except Exception as e:
            QMessageBox.warning(self, "输入错误", str(e))
            self.reset_ui()
    
    def deploy_finished(self, success: bool, message: str):
        """部署完成回调"""
        self.progress.setVisible(False)
        self.reset_ui()
        
        if success:
            QMessageBox.information(self, "部署成功", message)
        else:
            QMessageBox.critical(self, "部署失败", message)
    
    def reset_ui(self):
        """重置UI状态"""
        self.deploy_btn.setEnabled(True)
        self.deploy_btn.setText("开始部署")
        self.progress.setVisible(False)
    
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.logger.info("日志已清空")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("SSH Composer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("fkdls112")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
