#!/usr/bin/env python3
"""
PKBM 后端服务管理脚本
用于启动、停止、监控Go后端服务
"""

import os
import sys
import time
import signal
import subprocess
import requests
from pathlib import Path

class BackendManager:
    def __init__(self):
        self.backend_dir = Path("backend")
        self.backend_process = None
        self.api_url = "http://127.0.0.1:8080/api/stats"
        
    def check_go_environment(self):
        """检查Go环境"""
        try:
            result = subprocess.run(["go", "version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Go环境检查通过: {result.stdout.strip()}")
                return True
            else:
                print("❌ Go环境检查失败")
                return False
        except FileNotFoundError:
            print("❌ 未找到Go环境，请先安装Go")
            return False
    
    def check_backend_code(self):
        """检查后端代码"""
        if not self.backend_dir.exists():
            print("❌ 后端目录不存在")
            return False
        
        main_go = self.backend_dir / "main.go"
        if not main_go.exists():
            print("❌ 后端主文件不存在")
            return False
        
        print("✅ 后端代码检查通过")
        return True
    
    def start_backend(self):
        """启动后端服务"""
        if not self.check_go_environment() or not self.check_backend_code():
            return False
        
        try:
            print("🚀 正在启动后端服务...")
            
            # 切换到后端目录
            os.chdir(self.backend_dir)
            
            # 启动Go服务
            self.backend_process = subprocess.Popen(
                ["go", "run", "main.go"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待服务启动
            print("⏳ 等待服务启动...")
            time.sleep(3)
            
            # 检查服务状态
            if self.check_service_status():
                print("✅ 后端服务启动成功")
                print(f"📊 服务PID: {self.backend_process.pid}")
                print(f"🔗 API地址: {self.api_url}")
                return True
            else:
                print("❌ 后端服务启动失败")
                self.stop_backend()
                return False
                
        except Exception as e:
            print(f"❌ 启动后端服务失败: {e}")
            return False
        finally:
            # 返回原目录
            os.chdir("..")
    
    def stop_backend(self):
        """停止后端服务"""
        if self.backend_process:
            try:
                print("🛑 正在停止后端服务...")
                self.backend_process.terminate()
                
                # 等待进程结束
                try:
                    self.backend_process.wait(timeout=5)
                    print("✅ 后端服务已停止")
                except subprocess.TimeoutExpired:
                    print("⚠️ 服务未及时停止，强制终止...")
                    self.backend_process.kill()
                    self.backend_process.wait()
                    print("✅ 后端服务已强制停止")
                
                self.backend_process = None
                
            except Exception as e:
                print(f"❌ 停止后端服务失败: {e}")
    
    def check_service_status(self):
        """检查服务状态"""
        try:
            response = requests.get(self.api_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def show_status(self):
        """显示服务状态"""
        if self.check_service_status():
            try:
                response = requests.get(self.api_url, timeout=5)
                if response.status_code == 200:
                    stats = response.json()
                    print("🟢 后端服务运行中")
                    print(f"📊 条目总数: {stats.get('total_items', 0)}")
                    print(f"📁 分类总数: {stats.get('total_categories', 0)}")
                    print(f"🔗 API地址: {self.api_url}")
                else:
                    print("⚠️ 后端服务响应异常")
            except Exception as e:
                print(f"❌ 获取状态失败: {e}")
        else:
            print("🔴 后端服务未运行")
    
    def monitor_service(self):
        """监控服务状态"""
        print("📊 开始监控后端服务...")
        print("按 Ctrl+C 停止监控")
        
        try:
            while True:
                if self.check_service_status():
                    print(f"🟢 [{time.strftime('%H:%M:%S')}] 服务正常")
                else:
                    print(f"🔴 [{time.strftime('%H:%M:%S')}] 服务异常")
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
    
    def cleanup(self):
        """清理资源"""
        if self.backend_process:
            self.stop_backend()

def main():
    """主函数"""
    manager = BackendManager()
    
    # 注册信号处理器
    def signal_handler(signum, frame):
        print("\n🛑 收到退出信号，正在清理...")
        manager.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) < 2:
        print("PKBM 后端服务管理脚本")
        print("\n使用方法:")
        print("  python start_backend.py start     # 启动后端")
        print("  python start_backend.py stop      # 停止后端")
        print("  python start_backend.py status    # 查看状态")
        print("  python start_backend.py monitor   # 监控服务")
        print("  python start_backend.py restart   # 重启服务")
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "start":
            if manager.start_backend():
                print("\n💡 提示:")
                print("  - 使用 'python start_backend.py status' 查看状态")
                print("  - 使用 'python start_backend.py stop' 停止服务")
                print("  - 使用 'python start_backend.py monitor' 监控服务")
                
                # 保持脚本运行
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 收到退出信号")
                    
        elif command == "stop":
            manager.stop_backend()
            
        elif command == "status":
            manager.show_status()
            
        elif command == "monitor":
            manager.monitor_service()
            
        elif command == "restart":
            print("🔄 重启后端服务...")
            manager.stop_backend()
            time.sleep(2)
            manager.start_backend()
            
        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: start, stop, status, monitor, restart")
            
    except Exception as e:
        print(f"❌ 执行命令失败: {e}")
    finally:
        manager.cleanup()

if __name__ == "__main__":
    main() 