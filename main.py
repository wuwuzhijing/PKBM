#!/usr/bin/env python3
"""
PKBM - 个人知识库管理系统
主程序入口
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.gui.main_window import MainWindow


def main():
    """主函数"""
    print("使用默认配置启动GUI应用")
    
    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setApplicationName("PKBM")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PKBM Team")
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

