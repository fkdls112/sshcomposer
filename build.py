# 打包脚本
import PyInstaller.__main__
import os
import shutil

def build():
    # 清理旧构建
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # PyInstaller 参数
    args = [
        'src/main.py',
        '--name=SSHComposer',
        '--windowed',
        '--onefile',
        '--icon=resources/icon.ico',
        '--add-data=resources;resources',
        '--clean',
        '--noconfirm',
    ]
    
    PyInstaller.__main__.run(args)
    
    print("✅ 构建完成！输出目录: dist/")

if __name__ == "__main__":
    build()
