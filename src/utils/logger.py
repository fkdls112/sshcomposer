"""
日志工具模块
提供彩色日志输出功能
"""
from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime


class LogEmitter(QObject):
    """日志信号发射器"""
    log_signal = pyqtSignal(str, str)  # message, level


class Logger:
    """日志记录器"""
    
    LEVEL_INFO = "INFO"
    LEVEL_SUCCESS = "SUCCESS"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"
    
    def __init__(self, emitter: LogEmitter = None):
        self.emitter = emitter or LogEmitter()
    
    def _format_message(self, message: str, level: str) -> str:
        """格式化日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] [{level}] {message}"
    
    def info(self, message: str):
        """信息日志"""
        formatted = self._format_message(message, self.LEVEL_INFO)
        self.emitter.log_signal.emit(formatted, self.LEVEL_INFO)
    
    def success(self, message: str):
        """成功日志"""
        formatted = self._format_message(message, self.LEVEL_SUCCESS)
        self.emitter.log_signal.emit(formatted, self.LEVEL_SUCCESS)
    
    def warning(self, message: str):
        """警告日志"""
        formatted = self._format_message(message, self.LEVEL_WARNING)
        self.emitter.log_signal.emit(formatted, self.LEVEL_WARNING)
    
    def error(self, message: str):
        """错误日志"""
        formatted = self._format_message(message, self.LEVEL_ERROR)
        self.emitter.log_signal.emit(formatted, self.LEVEL_ERROR)
