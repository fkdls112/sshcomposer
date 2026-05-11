"""
Main entry point
"""
import sys
import os

# Add project root to path for imports
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    project_dir = os.path.dirname(sys.executable)
else:
    # Running as script
    project_dir = os.path.dirname(os.path.abspath(__file__))

src_dir = os.path.join(project_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Now import after path setup
from gui.main_window import main

if __name__ == "__main__":
    main()
