"""Build EXE with PyInstaller"""
import PyInstaller.__main__
import os, sys

def build():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_dir, 'src')
    sys.path.insert(0, src_dir)

    args = [
        'main.py',
        '--name=SSHComposer',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
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
    ]

    icon = os.path.join(project_dir, 'resources', 'icon.ico')
    if os.path.exists(icon):
        args.append(f'--icon={icon}')

    print(f"Project: {project_dir}")
    print(f"Source:  {src_dir}")

    PyInstaller.__main__.run(args)

    exe = os.path.join(project_dir, 'dist', 'SSHComposer.exe')
    if os.path.exists(exe):
        print(f"OK: dist/SSHComposer.exe ({os.path.getsize(exe)/1024/1024:.1f}MB)")
    else:
        print("FAIL: no exe")
        sys.exit(1)

if __name__ == '__main__':
    build()
