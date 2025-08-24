#!/usr/bin/env python3
"""
简化的exe构建脚本 - 减少卡住的可能性
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_simple():
    """简化构建"""
    print("PKBM - 简化构建脚本")
    print("=" * 40)
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("❌ 请先安装 PyInstaller: pip install pyinstaller")
        return False
    
    # 清理目录
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            try:
                shutil.rmtree(dir_name)
                print(f"✓ 清理 {dir_name} 目录")
            except Exception as e:
                print(f"⚠️  清理 {dir_name} 失败: {e}")
    
    print("开始构建...")
    
    # 使用最简单的参数
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单文件模式，更简单
        "--windowed",                   # 无控制台
        "--name=PKBM",                  # 名称
        "--clean",                      # 清理
        "main.py"                       # 主文件
    ]
    
    try:
        print("执行构建命令...")
        print("命令:", " ".join(cmd))
        
        # 直接运行，不使用Popen
        result = subprocess.run(
            cmd, 
            cwd=Path(__file__).parent,
            check=True,
            timeout=300  # 5分钟超时
        )
        
        print("✓ 构建完成！")
        
        # 复制数据目录
        if Path("../data").exists():
            dist_path = Path("dist")
            if dist_path.exists():
                data_dst = dist_path / "data"
                shutil.copytree("../data", data_dst, dirs_exist_ok=True)
                print("✓ 数据目录已复制")
        
        print(f"✅ 构建成功！exe位置: {Path('dist/PKBM.exe')}")
        return True
        
    except subprocess.TimeoutExpired:
        print("⏰ 构建超时（5分钟）")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

if __name__ == "__main__":
    success = build_simple()
    sys.exit(0 if success else 1)
