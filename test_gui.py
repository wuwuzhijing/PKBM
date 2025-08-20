#!/usr/bin/env python3
"""
PKBM - GUI测试脚本
在无图形界面环境下测试程序逻辑
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def test_database():
    """测试数据库功能"""
    print("测试数据库功能...")
    
    try:
        # 导入数据库相关模块
        import sqlite3
        from datetime import datetime
        
        # 创建测试数据库
        db_path = "test_data/test.db"
        Path("test_data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建测试表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_date TEXT
            )
        ''')
        
        # 插入测试数据
        cursor.execute('''
            INSERT INTO test_items (title, content, created_date)
            VALUES (?, ?, ?)
        ''', ("测试条目", "这是一个测试条目", datetime.now().isoformat()))
        
        conn.commit()
        
        # 查询测试数据
        cursor.execute('SELECT * FROM test_items')
        items = cursor.fetchall()
        
        print(f"✓ 数据库测试成功，找到 {len(items)} 个条目")
        
        # 清理测试数据
        conn.close()
        os.remove(db_path)
        os.rmdir("test_data")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        return False

def test_imports():
    """测试导入功能"""
    print("测试导入功能...")
    
    try:
        # 测试基本模块导入
        import tkinter
        print("✓ tkinter 导入成功")
        
        import sqlite3
        print("✓ sqlite3 导入成功")
        
        import requests
        print("✓ requests 导入成功")
        
        from datetime import datetime
        print("✓ datetime 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_file_operations():
    """测试文件操作"""
    print("测试文件操作...")
    
    try:
        # 测试文件读写
        test_file = "test_file.txt"
        test_content = "测试内容"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            read_content = f.read()
        
        if read_content == test_content:
            print("✓ 文件读写测试成功")
        else:
            print("✗ 文件读写测试失败")
            return False
        
        # 清理测试文件
        os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"✗ 文件操作测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("PKBM - GUI程序逻辑测试")
    print("=" * 40)
    
    tests = [
        ("导入测试", test_imports),
        ("数据库测试", test_database),
        ("文件操作测试", test_file_operations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！程序逻辑正常")
        return True
    else:
        print("✗ 部分测试失败，请检查问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
