#!/usr/bin/env python3
"""
PKBM启动脚本
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """主函数"""
    try:
        # 检查依赖
        check_dependencies()
        
        # 导入并运行主程序
        from main import main
        main()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有必要的依赖包:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"启动错误: {e}")
        sys.exit(1)

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()

