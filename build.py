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
    for d in ['build', 'dist', '__pycache__']:
        path = os.path.join(PROJECT_DIR, d)
        if os.path.exists(path):
            shutil.rmtree(path)
    for root, dirs, files in os.walk(SRC_DIR):
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d))
    spec = os.path.join(PROJECT_DIR, 'SSHComposer.spec')
    if os.path.exists(spec):
        os.remove(spec)

def build():
    clean()

    args = [
        # 入口文件
        os.path.join(SRC_DIR, 'main.py'),
        # 输出配置
        '--name=SSHComposer',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--workpath=build',
        '--distpath=dist',
        '--specpath=.',
        # 把 src 加入搜索路径, PyInstaller 才能找到 gui/core/utils 包
        f'--paths={SRC_DIR}',
        # 入口切换目录到 src
        '--runtime-hook=setup_hook.py',
        # 显式声明所有模块, 防止漏打包
        '--hidden-import=src',
        '--hidden-import=src.main',
        '--hidden-import=src.gui',
        '--hidden-import=src.gui.main_window',
        '--hidden-import=src.gui.widgets',
        '--hidden-import=src.gui.styles',
        '--hidden-import=src.core',
        '--hidden-import=src.core.ssh_client',
        '--hidden-import=src.core.deployer',
        '--hidden-import=src.core.validator',
        '--hidden-import=src.utils',
        '--hidden-import=src.utils.logger',
        # 第三方依赖
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=paramiko',
        '--hidden-import=scp',
        '--hidden-import=ipaddress',
        # 数据文件
        '--add-data=src\\gui\\styles.py;src\\gui',
        '--add-data=src\\__init__.py;src',
        '--add-data=src\\gui\\__init__.py;src\\gui',
        '--add-data=src\\core\\__init__.py;src\\core',
        '--add-data=src\\utils\\__init__.py;src\\utils',
    ]

    # 图标
    icon = os.path.join(PROJECT_DIR, 'resources', 'icon.ico')
    if os.path.exists(icon):
        args.append(f'--icon={icon}')

    print(f"项目目录: {PROJECT_DIR}")
    print(f"源码目录: {SRC_DIR}")
    print(f"开始构建...")

    PyInstaller.__main__.run(args)

    exe = os.path.join(PROJECT_DIR, 'dist', 'SSHComposer.exe')
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / (1024 * 1024)
        print(f"\n✓ 构建成功: dist/SSHComposer.exe ({size_mb:.1f} MB)")
    else:
        print("\n✗ 构建失败, 检查上方错误信息")
        sys.exit(1)

if __name__ == '__main__':
    build()
