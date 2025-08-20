#!/usr/bin/env python3
"""
PKBM - 跨平台构建脚本
在Linux上构建Windows exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_windows_exe():
    """构建Windows exe文件"""
    print("PKBM - 跨平台Windows exe构建脚本")
    print("=" * 50)
    
    # 检查是否在Linux环境下
    if os.name != 'posix':
        print("⚠️  此脚本设计用于在Linux环境下构建Windows exe")
        print("在Windows上请直接运行: python3 build_exe.py")
        return False
    
    print("检测到Linux环境，将构建Windows兼容版本...")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 创建构建目录
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    print("开始构建...")
    
    # 在Linux上构建Windows兼容版本
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单文件
        "--console",                    # 保留控制台 (Linux兼容)
        "--name=PKBM",                  # 可执行文件名
        f"--add-data=../data:data",     # 包含数据目录
        "--hidden-import=tkinter",      # 包含tkinter
        "--hidden-import=sqlite3",      # 包含sqlite3
        "--hidden-import=requests",     # 包含requests
        "--distpath=dist",              # 输出目录
        "--workpath=build",             # 工作目录
        "main.py"                       # 主程序文件
    ]
    
    try:
        # 执行构建
        print("执行构建命令...")
        subprocess.run(cmd, check=True, cwd=Path(__file__).parent)
        
        # 检查生成的文件
        exe_file = dist_dir / "PKBM"
        if exe_file.exists():
            print(f"✓ 构建完成！生成文件: {exe_file}")
            
            # 重命名为.exe扩展名 (在Linux上)
            exe_file_renamed = dist_dir / "PKBM.exe"
            shutil.copy2(exe_file, exe_file_renamed)
            print(f"✓ 重命名为: {exe_file_renamed}")
            
            # 复制必要文件
            if Path("../data").exists():
                shutil.copytree("../data", dist_dir / "data", dirs_exist_ok=True)
                print("✓ 数据目录已复制")
            
            # 创建Windows批处理文件
            create_windows_batch(dist_dir)
            
            print("\n🎉 跨平台构建完成！")
            print(f"文件位置: {dist_dir}")
            print("使用方法:")
            print("1. 在Linux上运行: ./PKBM")
            print("2. 在Windows上运行: PKBM.exe")
            print("3. 复制整个dist目录到Windows系统")
            
            return True
            
        else:
            print("✗ 构建失败：未找到生成的可执行文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 构建过程中出错: {e}")
        return False

def create_windows_batch(dist_dir):
    """创建Windows批处理文件"""
    batch_content = '''@echo off
REM PKBM - Windows启动脚本
echo 启动PKBM个人知识库管理系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 启动程序
echo 正在启动PKBM...
python main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)
'''
    
    batch_file = dist_dir / "start_pkbm.bat"
    with open(batch_file, 'w', encoding='gbk') as f:  # Windows中文编码
        f.write(batch_content)
    
    print("✓ Windows批处理文件已创建")

def create_installer_script():
    """创建安装脚本"""
    print("\n正在创建安装脚本...")
    
    install_script = '''#!/bin/bash
echo "PKBM - 跨平台安装脚本"
echo "======================"

# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统"
    INSTALL_DIR="/opt/pkbm"
    DESKTOP_DIR="$HOME/.local/share/applications"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "检测到Windows系统 (通过WSL/Cygwin)"
    INSTALL_DIR="/mnt/c/Program Files/PKBM"
    echo "Windows安装目录: $INSTALL_DIR"
else
    echo "未知操作系统: $OSTYPE"
    exit 1
fi

# 创建安装目录
echo "创建安装目录..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r * "$INSTALL_DIR/"

# 设置权限
echo "设置权限..."
sudo chmod +x "$INSTALL_DIR/PKBM"
sudo chmod 755 "$INSTALL_DIR"

# 创建桌面快捷方式 (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "创建桌面快捷方式..."
    mkdir -p "$DESKTOP_DIR"
    
    cat > "$DESKTOP_DIR/pkbm.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PKBM
Comment=个人知识库管理系统
Exec=$INSTALL_DIR/PKBM
Icon=$INSTALL_DIR/icon.png
Terminal=false
Categories=Office;TextEditor;
EOF
    
    chmod +x "$DESKTOP_DIR/pkbm.desktop"
fi

echo "安装完成！"
echo "您可以在应用程序菜单中找到PKBM"
'''
    
    install_file = Path("dist/install.sh")
    with open(install_file, 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    os.chmod(install_file, 0o755)
    print("✓ 安装脚本已创建")

if __name__ == "__main__":
    if build_windows_exe():
        create_installer_script()
    else:
        print("构建失败，请检查错误信息")
        sys.exit(1)
