#!/usr/bin/env python3
"""
数据库修复工具
修复categories表缺少color列的问题
"""

import sqlite3
import os
from pathlib import Path

def fix_database():
    """修复数据库"""
    db_path = "data/pkbm.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    print(f"🔧 修复数据库: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表结构
        cursor.execute("PRAGMA table_info(categories)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"当前categories表列: {columns}")
        
        if 'color' not in columns:
            print("➕ 添加color列...")
            cursor.execute('ALTER TABLE categories ADD COLUMN color TEXT DEFAULT "#3498db"')
            
            # 更新现有分类的颜色
            color_map = {
                '格言警句': '#e74c3c',
                '方法论': '#f39c12',
                '技术文档': '#3498db',
                '学习笔记': '#9b59b6',
                '工作记录': '#1abc9c',
                '生活感悟': '#e67e22',
                '书籍摘要': '#34495e',
                '其他': '#95a5a6'
            }
            
            for name, color in color_map.items():
                cursor.execute('UPDATE categories SET color = ? WHERE name = ?', (color, name))
                print(f"  ✓ 更新分类 '{name}' 颜色为 {color}")
            
            conn.commit()
            print("✅ color列添加完成！")
        else:
            print("✅ color列已存在")
        
        # 验证修复结果
        cursor.execute("PRAGMA table_info(categories)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"修复后categories表列: {columns}")
        
        # 检查数据
        cursor.execute('SELECT name, description, color FROM categories LIMIT 5')
        sample_data = cursor.fetchall()
        print(f"样本数据: {sample_data}")
        
        conn.close()
        print("🎉 数据库修复完成！")
        return True
        
    except Exception as e:
        print(f"❌ 数据库修复失败: {e}")
        return False

def backup_database():
    """备份数据库"""
    db_path = "data/pkbm.db"
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup"
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✅ 数据库已备份到: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    return False

def main():
    """主函数"""
    print("PKBM - 数据库修复工具")
    print("=" * 40)
    
    # 备份数据库
    if backup_database():
        # 修复数据库
        if fix_database():
            print("\n🎉 修复成功！现在可以重新运行程序")
        else:
            print("\n❌ 修复失败，请检查错误信息")
    else:
        print("\n❌ 备份失败，无法继续修复")

if __name__ == "__main__":
    main()
