"""
样式模块
定义应用程序的样式
"""

MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #3498db;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #3498db;
}

QLabel {
    color: #2c3e50;
    font-size: 12px;
}

QLineEdit {
    padding: 8px;
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
    font-size: 12px;
}

QLineEdit:focus {
    border-color: #3498db;
}

QLineEdit:disabled {
    background-color: #ecf0f1;
    color: #7f8c8d;
}

QPushButton {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: #3498db;
    color: white;
    font-weight: bold;
    font-size: 12px;
    cursor: pointer;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1a5276;
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
    cursor: not-allowed;
}

QPushButton#deployButton {
    background-color: #27ae60;
    font-size: 14px;
    padding: 12px 30px;
}

QPushButton#deployButton:hover {
    background-color: #229954;
}

QPushButton#deployButton:pressed {
    background-color: #1e8449;
}

QPushButton#clearButton {
    background-color: #e74c3c;
}

QPushButton#clearButton:hover {
    background-color: #c0392b;
}

QPushButton#browseButton {
    background-color: #9b59b6;
    padding: 8px 15px;
}

QPushButton#browseButton:hover {
    background-color: #8e44ad;
}

QTextEdit {
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background-color: #2c3e50;
    color: #ecf0f1;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    padding: 10px;
}

QProgressBar {
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 3px;
}

QCheckBox {
    font-size: 12px;
    color: #2c3e50;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QScrollBar:vertical {
    border: none;
    background: #ecf0f1;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #bdc3c7;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #95a5a6;
}
"""
