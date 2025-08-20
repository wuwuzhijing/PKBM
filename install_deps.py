#!/usr/bin/env python3
"""
PKBM 依赖安装脚本
改进的依赖包安装工具
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """运行命令并处理结果"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description}成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败")
        print(f"错误信息: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def upgrade_pip():
    """升级pip"""
    return run_command("python3 -m pip install --upgrade pip", "升级pip")

def install_build_tools():
    """安装构建工具"""
    tools = [
        "setuptools",
        "wheel",
        "build"
    ]
    
    for tool in tools:
        if not run_command(f"python3 -m pip install --upgrade {tool}", f"安装{tool}"):
            print(f"警告: {tool}安装失败，继续尝试...")
    
    return True

def install_dependencies():
    """安装依赖包"""
    # 首先尝试安装核心依赖
    core_deps = [
        "PyQt6>=6.5.0",
        "PyQt6-Qt6>=6.5.0", 
        "PyQt6-sip>=13.5.0"
    ]
    
    print("\n正在安装核心依赖...")
    for dep in core_deps:
        if not run_command(f"python3 -m pip install {dep}", f"安装{dep}"):
            print(f"错误: 核心依赖{dep}安装失败")
            return False
    
    # 然后安装其他依赖
    other_deps = [
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11", 
        "openpyxl>=3.1.0",
        "Pillow>=9.5.0",
        "lxml>=4.9.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0"
    ]
    
    print("\n正在安装其他依赖...")
    for dep in other_deps:
        if not run_command(f"python3 -m pip install {dep}", f"安装{dep}"):
            print(f"警告: {dep}安装失败，继续尝试...")
    
    return True

def verify_installation():
    """验证安装"""
    print("\n正在验证安装...")
    
    try:
        import PyQt6
        print("✓ PyQt6 安装成功")
    except ImportError:
        print("✗ PyQt6 安装失败")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 安装成功")
    except ImportError:
        print("✗ PyPDF2 安装失败")
    
    try:
        import PIL
        print("✓ Pillow 安装成功")
    except ImportError:
        print("✗ Pillow 安装失败")
    
    return True

def main():
    """主函数"""
    print("PKBM - 依赖安装脚本")
    print("=" * 40)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 升级pip
    if not upgrade_pip():
        print("警告: pip升级失败，继续尝试...")
    
    # 安装构建工具
    install_build_tools()
    
    # 安装依赖
    if not install_dependencies():
        print("\n错误: 依赖安装失败")
        print("请尝试以下解决方案:")
        print("1. 检查网络连接")
        print("2. 使用国内镜像源: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/")
        print("3. 升级Python和pip")
        print("4. 检查系统依赖库")
        sys.exit(1)
    
    # 验证安装
    if verify_installation():
        print("\n✓ 所有依赖安装完成！")
        print("现在可以运行 ./start.sh 启动程序")
    else:
        print("\n⚠ 部分依赖安装可能有问题，但程序可能仍能运行")
        print("建议检查错误信息并手动安装失败的包")

if __name__ == "__main__":
    main()
