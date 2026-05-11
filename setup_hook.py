# PyInstaller 运行时 hook
# 在 exe 启动时自动将 src 目录加入 sys.path,
# 这样 main.py 中的 from gui.main_window import main 能正确解析
import sys, os
_src_dir = os.path.join(sys._MEIPASS, 'src') if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
if os.path.exists(_src_dir) and _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)
