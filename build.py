"""
sshcomposer 构建脚本
在项目根目录运行: python build.py
输出: dist/SSHComposer.exe
"""
import os, sys, shutil
import PyInstaller.__main__

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_DIR, 'src')

def clean():
    """清理旧的构建文件"""
    for d in ['build', 'dist']:
        path = os.path.join(PROJECT_DIR, d)
        try:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
        except:
            pass
    spec = os.path.join(PROJECT_DIR, 'SSHComposer.spec')
    if os.path.exists(spec):
        os.remove(spec)

def build():
    clean()

    args = [
        'main.py',
        '--name=SSHComposer',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--workpath=build',
        '--distpath=dist',
        f'--paths={SRC_DIR}',
        # hidden imports
        '--hidden-import=src.main',
        '--hidden-import=src.gui.main_window',
        '--hidden-import=src.gui.widgets',
        '--hidden-import=src.gui.styles',
        '--hidden-import=src.core.ssh_client',
        '--hidden-import=src.core.deployer',
        '--hidden-import=src.core.validator',
        '--hidden-import=src.utils.logger',
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=paramiko',
        '--hidden-import=scp',
    ]

    # 运行时 hook: exe 启动时把 src 加入 sys.path
    hook = os.path.join(PROJECT_DIR, 'setup_hook.py')
    if os.path.exists(hook):
        args.append(f'--runtime-hook={hook}')

    # 图标
    icon = os.path.join(PROJECT_DIR, 'resources', 'icon.ico')
    if os.path.exists(icon):
        args.append(f'--icon={icon}')

    print(f"项目目录: {PROJECT_DIR}")
    print(f"源码目录: {SRC_DIR}")
    print("构建参数:", ' '.join(args[:6]), "...")

    PyInstaller.__main__.run(args)

    exe = os.path.join(PROJECT_DIR, 'dist', 'SSHComposer.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✓ 构建成功: dist/SSHComposer.exe ({size_mb:.1f} MB)")
    else:
        print("\n✗ 构建失败")
        sys.exit(1)

if __name__ == '__main__':
    build()
