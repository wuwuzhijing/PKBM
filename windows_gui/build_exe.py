#!/usr/bin/env python3
"""
Windows exe 打包脚本 - 便携式版本
使用PyInstaller将Python程序打包为便携式exe，无需Python环境
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """构建便携式exe文件"""
    print("PKBM - Windows 便携式exe 打包脚本")
    print("=" * 50)
    
    # 检查是否有残留的构建目录
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists() or dist_dir.exists():
        print("⚠️  发现残留的构建目录")
        print("请手动删除以下目录后重试:")
        if build_dir.exists():
            print(f"  - {build_dir.absolute()}")
        if dist_dir.exists():
            print(f"  - {dist_dir.absolute()}")
        print("\n或者运行以下命令清理:")
        print("  rmdir /s /q build")
        print("  rmdir /s /q dist")
        print("\n按Enter键继续，或Ctrl+C退出...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n用户取消操作")
            return False
    
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
    
    # 尝试清理目录
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("✓ 清理build目录")
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
            print("✓ 清理dist目录")
    except Exception as e:
        print(f"⚠️ 清理目录失败: {e}")
        print("请手动删除build和dist目录后重试")
        return False
    
    print("开始构建便携式exe...")
    print("构建阶段: 1/4 - 准备PyInstaller命令")
    
    # PyInstaller命令 - 使用--onedir而不是--onefile，更稳定
    cmd = [
        "pyinstaller",
        "--onedir",                     # 目录模式，更稳定
        "--windowed",                   # 无控制台窗口
        "--name=PKBM",                  # 可执行文件名
        "--clean",                      # 清理临时文件
        "--noconfirm",                  # 不确认覆盖
        f"--add-data=../data:data",     # 包含数据目录
        "--hidden-import=tkinter",      # 包含tkinter
        "--hidden-import=sqlite3",      # 包含sqlite3
        "--hidden-import=requests",     # 包含requests
        "--hidden-import=json",         # 包含json
        "--hidden-import=datetime",     # 包含datetime
        "--hidden-import=threading",    # 包含threading
        "--hidden-import=subprocess",   # 包含subprocess
        "--hidden-import=pathlib",      # 包含pathlib
        "--hidden-import=os",           # 包含os
        "--hidden-import=sys",          # 包含sys
        "main.py"                       # 主程序文件
    ]
    
    try:
        # 执行构建
        print("执行PyInstaller命令...")
        print("这可能需要几分钟时间，请耐心等待...")
        print("💡 提示: 如果构建时间过长，可以按 Ctrl+C 取消")
        print("正在构建中", end="", flush=True)
        
        # 使用实时输出，避免卡住
        process = subprocess.Popen(
            cmd, 
            cwd=Path(__file__).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时显示输出
        import time
        start_time = time.time()
        timeout = 300  # 5分钟超时（减少超时时间）
        last_output_time = start_time
        
        print(f"⏱️  构建开始时间: {time.strftime('%H:%M:%S')}")
        print(f"⏰  超时设置: {timeout}秒")
        print(f"⚠️  如果超过2分钟没有输出，将自动终止")
        
        while True:
            output = process.stdout.readline()
            current_time = time.time()
            
            if output == '' and process.poll() is not None:
                break
            
            if output:
                last_output_time = current_time
                # 显示关键信息
                if "INFO:" in output and ("Building" in output or "Processing" in output):
                    print(".", end="", flush=True)
                elif "ERROR:" in output or "WARNING:" in output:
                    print(f"\n⚠️  {output.strip()}")
                elif "Building EXE" in output:
                    print(f"\n🚀  {output.strip()}")
                elif "Build complete" in output:
                    print(f"\n✅  {output.strip()}")
                    break
                elif "Collecting" in output or "Analyzing" in output:
                    print(f"\n📊 {output.strip()}")
            
            # 检查超时
            if current_time - start_time > timeout:
                process.terminate()
                print(f"\n⏰ 构建超时（{timeout}秒），强制终止")
                return False
            
            # 检查是否卡住（超过2分钟没有输出）
            if current_time - last_output_time > 120:
                print(f"\n⚠️  构建似乎卡住了（超过2分钟无输出），强制终止")
                process.terminate()
                return False
            
            # 每30秒显示一次状态
            elapsed = current_time - start_time
            if elapsed > 0 and elapsed % 30 < 0.1:
                print(f"\n⏱️  构建进行中... 已用时: {elapsed:.0f}秒")
            
            time.sleep(0.1)
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            build_time = time.time() - start_time
            print(f"\n✓ exe构建完成！用时: {build_time:.1f}秒")
            print("构建阶段: 2/4 - PyInstaller构建完成")
        else:
            print(f"\n✗ PyInstaller构建失败，返回码: {return_code}")
            return False
        
        # 复制必要文件到dist目录
        print("构建阶段: 3/4 - 复制必要文件")
        dist_path = dist_dir / "PKBM"
        if dist_path.exists():
            # 复制数据目录
            data_src = Path("../data")
            if data_src.exists():
                data_dst = dist_path / "data"
                if data_dst.exists():
                    shutil.rmtree(data_dst)
                shutil.copytree(data_src, data_dst)
                print("✓ 数据目录已复制")
            
            # 复制配置文件
            config_src = Path("../config.ini")
            if config_src.exists():
                shutil.copy(config_src, dist_path)
                print("✓ 配置文件已复制")
            
            # 复制requirements文件（用于说明依赖）
            req_src = Path("requirements.txt")
            if req_src.exists():
                shutil.copy(req_src, dist_path)
                print("✓ 依赖文件已复制")
            
            # 创建便携式说明文件
            print("构建阶段: 4/4 - 创建说明文件")
            create_portable_readme(dist_path)
            
            print("✓ 便携式exe构建完成！")
            print(f"可执行文件位置: {dist_path / 'PKBM.exe'}")
            print(f"完整目录: {dist_path}")
            
        else:
            print("✗ 构建目录未找到")
            return False
        
        print("\n🎉 便携式exe构建完成！")
        print("📁 用户只需要解压整个PKBM文件夹即可使用")
        print("🚀 无需安装Python环境！")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller构建失败: {e}")
        print(f"返回码: {e.returncode}")
        if hasattr(e, 'output') and e.output:
            print(f"输出: {e.output}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"错误: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False
    
    return True

def create_portable_readme(dist_path):
    """创建便携式说明文件"""
    readme_content = """# PKBM 个人知识库管理系统 - 便携式版本

## 🚀 使用方法

1. **解压整个文件夹**到任意位置
2. **双击 PKBM.exe** 即可运行
3. **无需安装Python环境**

## 📁 文件说明

- `PKBM.exe` - 主程序（双击运行）
- `data/` - 数据目录（包含数据库和附件）
- `config.ini` - 配置文件（可选）
- `requirements.txt` - 依赖说明（仅参考）

## ⚠️ 注意事项

- 不要删除data目录，否则会丢失数据
- 可以复制整个文件夹到其他电脑使用
- 支持U盘便携使用

## 🔧 故障排除

如果程序无法启动：
1. 确保Windows Defender没有拦截
2. 检查是否有杀毒软件误报
3. 尝试以管理员身份运行

## 📞 技术支持

如有问题，请联系开发者。
"""
    
    readme_path = dist_path / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ 便携式说明文件已创建")

def create_installer():
    """创建便携式压缩包"""
    print("\n正在创建便携式压缩包...")
    
    import zipfile
    from datetime import datetime
    
    # 创建压缩包
    dist_path = Path("dist/PKBM")
    if dist_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"PKBM_Portable_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in dist_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(dist_path.parent)
                    zipf.write(file_path, arcname)
        
        print(f"✓ 便携式压缩包已创建: {zip_name}")
        print("📦 用户可以直接解压使用！")
    
    print("便携式打包完成！")

if __name__ == "__main__":
    if build_exe():
        create_installer()
    else:
        print("构建失败，请检查错误信息")
        sys.exit(1)
