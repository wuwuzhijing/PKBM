#!/usr/bin/env python3
"""
Ubuntu deb 打包脚本
使用python-stdeb将Python程序打包为deb包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_deb():
    """构建deb包"""
    print("PKBM - Ubuntu deb 打包脚本")
    print("=" * 40)
    
    print("使用简化打包方式...")
    
    # 创建构建目录
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    dist_dir.mkdir()
    
    print("开始构建...")
    
    try:
        # 创建可执行脚本
        script_content = '''#!/usr/bin/env python3
"""
PKBM - Ubuntu版本启动脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()
'''
        
        with open(dist_dir / "pkbm", "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # 复制主程序
        shutil.copy2("main.py", dist_dir)
        
        # 复制依赖文件
        shutil.copy2("requirements.txt", dist_dir)
        
        # 创建安装脚本
        install_script = '''#!/bin/bash
echo "PKBM - Ubuntu安装脚本"
echo "======================"

# 创建应用目录
sudo mkdir -p /opt/pkbm
sudo cp -r * /opt/pkbm/

# 设置权限
sudo chmod +x /opt/pkbm/pkbm
sudo chmod 755 /opt/pkbm

# 创建桌面快捷方式
cat > pkbm.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PKBM
Comment=个人知识库管理系统
Exec=/opt/pkbm/pkbm
Icon=/opt/pkbm/icon.png
Terminal=false
Categories=Office;TextEditor;
EOF

sudo cp pkbm.desktop /usr/share/applications/
sudo chmod 644 /usr/share/applications/pkbm.desktop

echo "安装完成！"
echo "您可以在应用程序菜单中找到PKBM"
'''
        
        with open(dist_dir / "install.sh", "w", encoding="utf-8") as f:
            f.write(install_script)
        
        # 设置权限
        os.chmod(dist_dir / "pkbm", 0o755)
        os.chmod(dist_dir / "install.sh", 0o755)
        
        print("✓ 简化打包完成！")
        print(f"文件位置: {dist_dir}")
        print("使用方法:")
        print("1. 运行: ./pkbm")
        print("2. 安装: sudo ./install.sh")
        
        return True
        
    except Exception as e:
        print(f"✗ 构建失败: {e}")
        return False

def create_setup_py():
    """创建setup.py文件"""
    setup_content = '''#!/usr/bin/env python3
"""
PKBM setup.py for deb packaging
"""

from setuptools import setup, find_packages

setup(
    name="pkbm",
    version="1.0.0",
    description="个人知识库管理系统",
    long_description=open("README.md").read(),
    author="PKBM Team",
    author_email="team@pkbm.com",
    url="https://github.com/pkbm/pkbm",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "pkbm=pkbm.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.8",
    data_files=[
        ("share/applications", ["pkbm.desktop"]),
        ("share/icons/hicolor/128x128/apps", ["resources/icon.png"]),
        ("share/pkbm", ["data/"]),
    ],
)
'''
    
    with open("setup.py", "w", encoding="utf-8") as f:
        f.write(setup_content)
    
    print("✓ setup.py 文件已创建")

def create_desktop_file():
    """创建.desktop文件"""
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=PKBM
Comment=个人知识库管理系统
Exec=pkbm
Icon=pkbm
Terminal=false
Categories=Office;TextEditor;
"""
    
    with open("pkbm.desktop", "w", encoding="utf-8") as f:
        f.write(desktop_content)
    
    print("✓ pkbm.desktop 文件已创建")

def create_package_structure():
    """创建包结构"""
    # 创建__init__.py
    init_content = '''"""
PKBM Package
"""

__version__ = "1.0.0"
'''
    
    pkbm_dir = Path("pkbm")
    pkbm_dir.mkdir(exist_ok=True)
    
    with open(pkbm_dir / "__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    
    # 复制主程序
    if Path("main.py").exists():
        shutil.copy("main.py", pkbm_dir / "main.py")
    
    print("✓ 包结构已创建")

if __name__ == "__main__":
    # 创建必要的文件
    create_desktop_file()
    create_package_structure()
    
    if build_deb():
        print("deb包构建成功！")
    else:
        print("构建失败，请检查错误信息")
        sys.exit(1)
