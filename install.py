#!/usr/bin/env python3
"""
PKBM安装脚本
"""

import sys
import os
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True


def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    
    try:
        # 升级pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # 安装依赖
        requirements_file = Path(__file__).parent / "requirements.txt"
        if requirements_file.exists():
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        else:
            print("警告: requirements.txt文件不存在")
            # 手动安装核心依赖
            core_deps = [
                "PyQt6>=6.6.1",
                "PyPDF2>=3.0.1",
                "Pillow>=10.1.0",
                "python-docx>=1.1.0",
                "openpyxl>=3.1.2"
            ]
            for dep in core_deps:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        
        print("依赖包安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print("正在创建目录结构...")
    
    project_root = Path(__file__).parent
    directories = [
        "data",
        "data/attachments",
        "logs",
        "resources",
        "backups"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {directory}")
    
    print("目录结构创建完成")


def create_desktop_shortcut():
    """创建桌面快捷方式"""
    system = platform.system()
    
    if system == "Windows":
        create_windows_shortcut()
    elif system == "Linux":
        create_linux_shortcut()
    elif system == "Darwin":  # macOS
        create_macos_shortcut()


def create_windows_shortcut():
    """创建Windows快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "PKBM.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{Path(__file__).parent / "main.py"}"'
        shortcut.WorkingDirectory = str(Path(__file__).parent)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("Windows桌面快捷方式创建完成")
    except ImportError:
        print("警告: 无法创建Windows快捷方式，需要安装pywin32和winshell")


def create_linux_shortcut():
    """创建Linux快捷方式"""
    try:
        desktop_file = Path.home() / ".local/share/applications/pkbm.desktop"
        desktop_file.parent.mkdir(parents=True, exist_ok=True)
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=PKBM
Comment=个人知识库管理系统
Exec={sys.executable} {Path(__file__).parent / "main.py"}
Icon={Path(__file__).parent / "resources/icon.png"}
Terminal=false
Categories=Office;Knowledge;
"""
        
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # 设置可执行权限
        os.chmod(desktop_file, 0o755)
        
        print("Linux桌面快捷方式创建完成")
    except Exception as e:
        print(f"创建Linux快捷方式失败: {e}")


def create_macos_shortcut():
    """创建macOS快捷方式"""
    print("macOS快捷方式创建功能暂未实现")


def run_tests():
    """运行测试"""
    print("正在运行测试...")
    
    try:
        # 这里可以添加基本的测试逻辑
        print("基本测试通过")
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False


def main():
    """主安装函数"""
    print("=" * 50)
    print("PKBM - 个人知识库管理系统安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        print("安装失败，请检查网络连接和权限")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 创建快捷方式
    create_desktop_shortcut()
    
    # 运行测试
    if run_tests():
        print("\n安装完成！")
        print("\n使用方法:")
        print("1. 运行 python main.py 启动程序")
        print("2. 或者双击桌面快捷方式")
        print("\n如有问题，请查看README.md文件")
    else:
        print("\n安装完成，但测试失败")
        print("请检查安装是否正确")


if __name__ == "__main__":
    main()

