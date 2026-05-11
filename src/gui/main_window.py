"""
Main window module
"""
import sys
import os

# Handle imports for both development and PyInstaller
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_dir = os.path.dirname(sys.executable)
    src_dir = os.path.join(base_dir, 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QTextEdit, QPushButton, QLabel, 
                             QProgressBar, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor

from gui.styles import MAIN_STYLE
from gui.widgets import FileSelector, ServerConfigWidget
from core.deployer import Deployer
from core.validator import Validator
from utils.logger import Logger, LogEmitter


class DeployThread(QThread):
    """Deploy thread"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, deployer, config):
        super().__init__()
        self.deployer = deployer
        self.config = config
    
    def run(self):
        """Execute deploy"""
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
            if success:
                self.finished.emit(True, "Deploy success!")
            else:
                self.finished.emit(False, "Deploy failed: unknown error")
        except Exception as e:
            self.finished.emit(False, str(e))


class MainWindow(QMainWindow):
    """Main window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Composer - Docker Compose Deploy Tool")
        self.setMinimumSize(800, 600)
        
        # Init logger
        self.log_emitter = LogEmitter()
        self.logger = Logger(self.log_emitter)
        self.log_emitter.log_signal.connect(self.append_log)
        
        # Init deployer
        self.deployer = Deployer(self.logger)
        self.deploy_thread = None
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Init UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        # Server config
        server_group = QGroupBox("Server Config")
        server_layout = QVBoxLayout(server_group)
        self.server_config = ServerConfigWidget()
        server_layout.addWidget(self.server_config)
        left_layout.addWidget(server_group)
        
        # File selector
        file_group = QGroupBox("Docker Compose File")
        file_layout = QVBoxLayout(file_group)
        self.file_selector = FileSelector()
        file_layout.addWidget(self.file_selector)
        left_layout.addWidget(file_group)
        
        # Target dir
        dir_group = QGroupBox("Target Directory")
        dir_layout = QVBoxLayout(dir_group)
        self.dir_input = QTextEdit()
        self.dir_input.setPlaceholderText("/opt/docker")
        self.dir_input.setMaximumHeight(40)
        self.dir_input.setText("/opt/docker")
        dir_layout.addWidget(self.dir_input)
        left_layout.addWidget(dir_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.deploy_btn = QPushButton("Deploy")
        self.deploy_btn.setObjectName("deployButton")
        self.deploy_btn.clicked.connect(self.start_deploy)
        btn_layout.addWidget(self.deploy_btn)
        
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.clicked.connect(self.clear_log)
        btn_layout.addWidget(self.clear_btn)
        
        left_layout.addLayout(btn_layout)
        left_layout.addStretch()
        
        # Right panel - Log
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        log_group = QGroupBox("Deploy Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.WidgetWidth)
        log_layout.addWidget(self.log_text)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        log_layout.addWidget(self.progress)
        
        right_layout.addWidget(log_group)
        
        # Add to main layout
        main_layout.addWidget(left_panel, stretch=1)
        main_layout.addWidget(right_panel, stretch=2)
    
    def apply_styles(self):
        """Apply styles"""
        self.setStyleSheet(MAIN_STYLE)
    
    def append_log(self, message: str, level: str):
        """Append log to text"""
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
        """Validate inputs"""
        # Get server config
        server_config = self.server_config.get_config()
        
        # Validate IP
        if not server_config['host']:
            raise ValueError("Please enter server IP")
        
        if not Validator.validate_ip(server_config['host']):
            raise ValueError("Invalid IP format")
        
        # Validate port
        valid, error, port = Validator.validate_port(server_config['port'])
        if not valid:
            raise ValueError(f"Port error: {error}")
        server_config['port'] = port
        
        # Validate username
        valid, error = Validator.validate_username(server_config['username'])
        if not valid:
            raise ValueError(f"Username error: {error}")
        
        # Validate password
        valid, error = Validator.validate_password(server_config['password'])
        if not valid:
            raise ValueError(f"Password error: {error}")
        
        # Validate file
        local_file = self.file_selector.get_path()
        if not local_file:
            raise ValueError("Please select Docker Compose file")
        
        # Validate target dir
        remote_dir = self.dir_input.toPlainText().strip()
        if not remote_dir:
            remote_dir = "/opt/docker"
        
        valid, error = Validator.validate_remote_path(remote_dir)
        if not valid:
            raise ValueError(f"Target dir error: {error}")
        
        return {
            **server_config,
            'local_file': local_file,
            'remote_dir': remote_dir,
            'use_sudo': True
        }
    
    def start_deploy(self):
        """Start deploy"""
        try:
            # Validate inputs
            config = self.validate_inputs()
            
            # Disable button
            self.deploy_btn.setEnabled(False)
            self.deploy_btn.setText("Deploying...")
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)
            
            # Clear log
            self.clear_log()
            self.logger.info("Starting deploy...")
            
            # Create deploy thread
            self.deploy_thread = DeployThread(self.deployer, config)
            self.deploy_thread.finished.connect(self.deploy_finished)
            self.deploy_thread.start()
            
        except Exception as e:
            QMessageBox.warning(self, "Input Error", str(e))
            self.reset_ui()
    
    def deploy_finished(self, success: bool, message: str):
        """Deploy finished callback"""
        self.progress.setVisible(False)
        self.reset_ui()
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Failed", message)
    
    def reset_ui(self):
        """Reset UI state"""
        self.deploy_btn.setEnabled(True)
        self.deploy_btn.setText("Deploy")
        self.progress.setVisible(False)
    
    def clear_log(self):
        """Clear log"""
        self.log_text.clear()
        self.logger.info("Log cleared")


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set app info
    app.setApplicationName("SSH Composer")
    app.setApplicationVersion("1.0.6")
    app.setOrganizationName("fkdls112")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
