"""
Build script using PyInstaller to create Windows executable
"""
import PyInstaller.__main__
import os
import sys


def build():
    """Build executable"""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_dir, 'src')
    
    # Add src to path
    sys.path.insert(0, src_dir)
    
    # PyInstaller arguments
    args = [
        os.path.join(src_dir, 'main.py'),
        '--name=SSHComposer',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
    ]
    
    # Add icon if exists
    icon_path = os.path.join(project_dir, 'resources', 'icon.ico')
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # Hidden imports
    args.extend([
        '--hidden-import=PyQt5',
        '--hidden-import=paramiko',
        '--hidden-import=scp',
        '--hidden-import=src.gui.main_window',
        '--hidden-import=src.gui.widgets',
        '--hidden-import=src.gui.styles',
        '--hidden-import=src.core.ssh_client',
        '--hidden-import=src.core.deployer',
        '--hidden-import=src.core.validator',
        '--hidden-import=src.utils.logger',
    ])
    
    print("Starting build...")
    print(f"Project dir: {project_dir}")
    print(f"Source dir: {src_dir}")
    
    try:
        PyInstaller.__main__.run(args)
        print("Build complete!")
        print("Output: dist/")
        
        # Check output
        exe_path = os.path.join(project_dir, 'dist', 'SSHComposer.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"File size: {size_mb:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"Build failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
