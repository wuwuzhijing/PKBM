#!/usr/bin/env python3
"""
PyInstaller环境诊断脚本
"""

import subprocess
import sys
import time
import os

def check_pyinstaller():
    """检查PyInstaller安装"""
    print("🔍 检查PyInstaller安装...")
    try:
        result = subprocess.run(["pyinstaller", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ PyInstaller版本: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ PyInstaller版本检查失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ PyInstaller检查失败: {e}")
        return False

def test_simple_build():
    """测试简单构建"""
    print("\n🧪 测试简单构建...")
    
    # 创建一个简单的测试文件
    test_file = "test_simple.py"
    with open(test_file, "w") as f:
        f.write('print("Hello, World!")\n')
    
    try:
        cmd = [
            "pyinstaller",
            "--onefile",
            "--name=test_simple",
            "--distpath=test_dist",
            "--workpath=test_build",
            "--clean",
            "--noconfirm",
            test_file
        ]
        
        print("开始测试构建...")
        start_time = time.time()
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # 监控输出
        timeout = 60  # 1分钟超时
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                print(f"📝 {output.strip()}")
            
            # 检查超时
            if time.time() - start_time > timeout:
                process.terminate()
                print("⏰ 测试构建超时")
                return False
            
            time.sleep(0.1)
        
        return_code = process.wait()
        test_time = time.time() - start_time
        
        if return_code == 0:
            print(f"✅ 测试构建成功！用时: {test_time:.1f}秒")
            return True
        else:
            print(f"❌ 测试构建失败，返回码: {return_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试构建异常: {e}")
        return False
    finally:
        # 清理测试文件
        for path in [test_file, "test_simple.spec"]:
            if os.path.exists(path):
                os.remove(path)
        
        # 清理测试目录
        import shutil
        for path in ["test_dist", "test_build"]:
            if os.path.exists(path):
                shutil.rmtree(path)

def check_system_resources():
    """检查系统资源"""
    print("\n💻 检查系统资源...")
    
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        print(f"CPU使用率: {cpu_percent}%")
        print(f"内存使用: {memory.percent}% ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)")
        
        if cpu_percent > 90:
            print("⚠️  CPU使用率过高，可能影响构建")
        if memory.percent > 90:
            print("⚠️  内存使用率过高，可能影响构建")
            
    except ImportError:
        print("ℹ️  未安装psutil，跳过资源检查")
    except Exception as e:
        print(f"⚠️  资源检查失败: {e}")

def check_network():
    """检查网络连接"""
    print("\n🌐 检查网络连接...")
    
    try:
        # 测试PyPI连接
        import urllib.request
        response = urllib.request.urlopen("https://pypi.org", timeout=10)
        print("✅ PyPI连接正常")
        return True
    except Exception as e:
        print(f"❌ PyPI连接失败: {e}")
        return False

def main():
    """主函数"""
    print("PKBM - PyInstaller环境诊断")
    print("=" * 50)
    
    # 检查各项
    pyinstaller_ok = check_pyinstaller()
    network_ok = check_network()
    check_system_resources()
    
    if pyinstaller_ok and network_ok:
        print("\n🧪 开始构建测试...")
        build_ok = test_simple_build()
        
        if build_ok:
            print("\n🎉 诊断完成！环境正常，可以运行 python build_exe.py")
            return True
        else:
            print("\n❌ 构建测试失败，请检查错误信息")
            return False
    else:
        print("\n❌ 环境检查失败，请先解决环境问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
