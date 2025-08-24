#!/usr/bin/env python3
"""
测试构建脚本 - 验证PyInstaller是否正常工作
"""

import subprocess
import sys
import time

def test_pyinstaller():
    """测试PyInstaller是否正常工作"""
    print("🧪 测试PyInstaller环境...")
    print("=" * 50)
    
    try:
        # 测试PyInstaller版本
        result = subprocess.run(["pyinstaller", "--version"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ PyInstaller版本: {result.stdout.strip()}")
        else:
            print(f"❌ PyInstaller版本检查失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ PyInstaller版本检查超时")
        return False
    except FileNotFoundError:
        print("❌ 未找到PyInstaller，请先安装")
        return False
    except Exception as e:
        print(f"❌ PyInstaller测试失败: {e}")
        return False
    
    # 测试简单构建
    print("\n🧪 测试简单构建...")
    try:
        test_cmd = [
            "pyinstaller",
            "--onefile",
            "--name=test",
            "--distpath=test_dist",
            "--workpath=test_build",
            "--specpath=test_spec",
            "--clean",
            "--noconfirm",
            "main.py"
        ]
        
        print("开始测试构建...")
        start_time = time.time()
        
        process = subprocess.Popen(
            test_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # 监控输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                if "ERROR:" in output or "WARNING:" in output:
                    print(f"⚠️  {output.strip()}")
                elif "Building" in output or "Processing" in output:
                    print(f"🔄 {output.strip()}")
                elif "Build complete" in output:
                    print(f"✅ {output.strip()}")
                    break
            
            # 检查超时
            if time.time() - start_time > 120:  # 2分钟超时
                process.terminate()
                print("⏰ 测试构建超时")
                return False
            
            time.sleep(0.1)
        
        return_code = process.wait()
        test_time = time.time() - start_time
        
        if return_code == 0:
            print(f"✅ 测试构建成功！用时: {test_time:.1f}秒")
            
            # 清理测试文件
            import shutil
            import os
            for path in ["test_dist", "test_build", "test.spec"]:
                if os.path.exists(path):
                    shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            print("🧹 测试文件已清理")
            
            return True
        else:
            print(f"❌ 测试构建失败，返回码: {return_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试构建异常: {e}")
        return False

def main():
    """主函数"""
    print("PKBM - PyInstaller环境测试")
    print("=" * 50)
    
    if test_pyinstaller():
        print("\n🎉 环境测试通过！可以运行 python build_exe.py")
        return True
    else:
        print("\n❌ 环境测试失败！请检查PyInstaller安装")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
