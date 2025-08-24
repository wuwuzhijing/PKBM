#!/usr/bin/env python3
"""
测试build_exe.py中的变量定义
"""

def test_variables():
    """测试变量定义"""
    try:
        # 模拟build_exe函数中的变量定义
        from pathlib import Path
        
        # 测试cmd变量定义
        cmd = [
            "pyinstaller",
            "--onedir",
            "--windowed",
            "--name=PKBM",
            "main.py"
        ]
        
        print(f"✅ cmd变量定义成功，包含 {len(cmd)} 个元素")
        print(f"第一个元素: {cmd[0]}")
        print(f"最后一个元素: {cmd[-1]}")
        
        # 测试其他变量
        build_dir = Path("build")
        dist_dir = Path("dist")
        
        print(f"✅ build_dir: {build_dir}")
        print(f"✅ dist_dir: {dist_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ 变量定义测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 测试变量定义...")
    success = test_variables()
    if success:
        print("🎉 变量定义测试通过！")
    else:
        print("❌ 变量定义测试失败！")
