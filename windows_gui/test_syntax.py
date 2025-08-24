#!/usr/bin/env python3
"""
测试build_exe.py的语法是否正确
"""

def test_syntax():
    """测试语法"""
    try:
        # 尝试导入build_exe模块
        import build_exe
        print("✅ 语法检查通过！")
        return True
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return False
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("🧪 测试build_exe.py语法...")
    success = test_syntax()
    if success:
        print("🎉 可以运行 python build_exe.py")
    else:
        print("❌ 请修复语法错误后再试")
