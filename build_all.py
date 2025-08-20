#!/usr/bin/env python3
"""
PKBM - 统一构建脚本
自动构建所有平台的发布版本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def detect_platform():
    """检测当前平台"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return "unknown"

def build_windows():
    """构建Windows版本"""
    print("正在构建Windows版本...")
    
    windows_dir = Path("windows_gui")
    if not windows_dir.exists():
        print("错误: Windows GUI目录不存在")
        return False
    
    try:
        # 安装依赖
        print("安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=windows_dir, check=True)
        
        # 构建exe
        print("构建exe文件...")
        subprocess.run([sys.executable, "build_exe.py"], cwd=windows_dir, check=True)
        
        print("✓ Windows版本构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Windows版本构建失败: {e}")
        return False

def build_linux():
    """构建Linux版本"""
    print("正在构建Linux版本...")
    
    ubuntu_dir = Path("ubuntu_gui")
    if not ubuntu_dir.exists():
        print("错误: Ubuntu GUI目录不存在")
        return False
    
    try:
        # 安装依赖
        print("安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=ubuntu_dir, check=True)
        
        # 构建deb包
        print("构建deb包...")
        subprocess.run([sys.executable, "build_deb.py"], cwd=ubuntu_dir, check=True)
        
        print("✓ Linux版本构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Linux版本构建失败: {e}")
        return False

def build_backend():
    """构建Go后端"""
    print("正在构建Go后端...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("错误: 后端目录不存在")
        return False
    
    try:
        # 检查Go是否安装
        result = subprocess.run(["go", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("错误: Go未安装，跳过后端构建")
            return False
        
        print("Go版本:", result.stdout.strip())
        
        # 下载依赖
        print("下载Go依赖...")
        subprocess.run(["go", "mod", "download"], cwd=backend_dir, check=True)
        
        # 构建后端
        print("构建Go后端...")
        subprocess.run(["go", "build", "-o", "pkbm-backend", "main.go"], cwd=backend_dir, check=True)
        
        print("✓ Go后端构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Go后端构建失败: {e}")
        return False
    except FileNotFoundError:
        print("错误: Go未安装，跳过后端构建")
        return False

def create_release_package():
    """创建发布包"""
    print("正在创建发布包...")
    
    import shutil
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # 复制Windows版本
    windows_dist = Path("windows_gui/dist")
    if windows_dist.exists():
        windows_release = release_dir / "windows"
        windows_release.mkdir()
        
        for file in windows_dist.glob("*.exe"):
            shutil.copy2(file, windows_release)
        
        # 复制数据目录
        if Path("data").exists():
            shutil.copytree("data", windows_release / "data")
        
        print("✓ Windows发布包创建完成")
    
    # 复制Linux版本
    ubuntu_dir = Path("ubuntu_gui")
    if ubuntu_dir.exists():
        linux_release = release_dir / "linux"
        linux_release.mkdir()
        
        # 复制deb包
        for file in ubuntu_dir.glob("*.deb"):
            shutil.copy2(file, linux_release)
        
        # 复制源码
        if Path("ubuntu_gui/main.py").exists():
            shutil.copy2("ubuntu_gui/main.py", linux_release)
            shutil.copy2("ubuntu_gui/requirements.txt", linux_release)
        
        print("✓ Linux发布包创建完成")
    
    # 复制后端
    backend_dir = Path("backend")
    if backend_dir.exists():
        backend_release = release_dir / "backend"
        backend_release.mkdir()
        
        # 复制Go源码
        for file in backend_dir.glob("*.go"):
            shutil.copy2(file, backend_release)
        
        # 复制配置文件
        for file in backend_dir.glob("*.mod"):
            shutil.copy2(file, backend_release)
        
        # 复制编译后的二进制文件
        backend_bin = backend_dir / "pkbm-backend"
        if backend_bin.exists():
            shutil.copy2(backend_bin, backend_release)
        
        print("✓ 后端发布包创建完成")
    
    # 复制文档
    docs = ["README.md", "LICENSE", "CHANGELOG.md"]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, release_dir)
    
    print("✓ 发布包创建完成")
    print(f"发布包位置: {release_dir.absolute()}")

def main():
    """主函数"""
    print("PKBM - 统一构建脚本")
    print("=" * 50)
    
    current_platform = detect_platform()
    print(f"当前平台: {current_platform}")
    
    # 构建Go后端
    build_backend()
    
    # 根据平台构建GUI
    if current_platform == "windows":
        build_windows()
    elif current_platform in ["linux", "macos"]:
        build_linux()
    else:
        print("未知平台，尝试构建所有版本...")
        build_windows()
        build_linux()
    
    # 创建发布包
    create_release_package()
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print("请查看release目录获取发布文件")

if __name__ == "__main__":
    main()
