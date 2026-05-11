"""
SSH Composer — Docker Compose 远程部署工具
主入口
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from gui.main_window import main

if __name__ == '__main__':
    main()
