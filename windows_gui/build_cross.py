#!/usr/bin/env python3
"""
PKBM - 跨平台构建脚本
在Linux上构建Windows兼容版本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_cross_platform():
    """跨平台构建"""
    print("PKBM - 跨平台构建脚本")
    print("=" * 40)
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("安装 PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 清理目录
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
    
    print("开始构建...")
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=PKBM",
        f"--add-data=../data:data",
        "--hidden-import=tkinter",
        "--hidden-import=sqlite3",
        "--hidden-import=requests",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=Path(__file__).parent)
        
        # 检查结果
        exe_file = Path("dist/PKBM")
        if exe_file.exists():
            print(f"✓ 构建完成: {exe_file}")
            
            # 重命名为.exe
            exe_file_renamed = Path("dist/PKBM.exe")
            shutil.copy2(exe_file, exe_file_renamed)
            print(f"✓ 重命名为: {exe_file_renamed}")
            
            # 复制数据目录
            if Path("../data").exists():
                shutil.copytree("../data", Path("dist/data"), dirs_exist_ok=True)
                print("✓ 数据目录已复制")
            
            print("\n🎉 跨平台构建完成！")
            print("文件位置: dist/")
            print("使用方法:")
            print("1. Linux: ./PKBM")
            print("2. Windows: PKBM.exe")
            print("3. 复制dist目录到目标系统")
            
            return True
        else:
            print("✗ 构建失败")
            return False
            
    except Exception as e:
        print(f"✗ 构建失败: {e}")
        return False

if __name__ == "__main__":
    success = build_cross_platform()
    sys.exit(0 if success else 1)
