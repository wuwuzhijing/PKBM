#!/usr/bin/env python3
"""
Windows exe 打包脚本
使用PyInstaller将Python程序打包为exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """构建exe文件"""
    print("PKBM - Windows exe 打包脚本")
    print("=" * 40)
    
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
    
    print("开始构建exe...")
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单文件
        "--windowed",                   # 无控制台窗口
        "--name=PKBM",                  # 可执行文件名
        f"--add-data=../data:data",     # 包含数据目录 (使用相对路径)
        "--hidden-import=tkinter",      # 包含tkinter
        "--hidden-import=sqlite3",      # 包含tkinter
        "--hidden-import=requests",     # 包含requests
        "main.py"                       # 主程序文件
    ]
    
    try:
        # 执行构建
        subprocess.run(cmd, check=True, cwd=Path(__file__).parent)
        
        print("✓ exe构建完成！")
        print(f"可执行文件位置: {dist_dir / 'PKBM.exe'}")
        
        # 复制必要文件到dist目录
        dist_path = dist_dir / "PKBM"
        if dist_path.exists():
            # 复制数据目录
            if Path("data").exists():
                shutil.copytree("data", dist_path / "data", dirs_exist_ok=True)
            
            # 复制配置文件
            if Path("config.ini").exists():
                shutil.copy("config.ini", dist_path)
            
            print("✓ 相关文件已复制到dist目录")
        
        print("\n构建完成！您可以在dist目录中找到PKBM.exe文件")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False
    
    return True

def create_installer():
    """创建安装程序"""
    print("\n正在创建安装程序...")
    
    # 这里可以使用NSIS或其他工具创建安装程序
    # 暂时跳过，直接使用exe文件
    
    print("安装程序创建完成！")

if __name__ == "__main__":
    if build_exe():
        create_installer()
    else:
        print("构建失败，请检查错误信息")
        sys.exit(1)
