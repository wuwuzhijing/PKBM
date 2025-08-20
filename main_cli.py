#!/usr/bin/env python3
"""
PKBM - 命令行版本
当图形界面不可用时使用此版本
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime

class PKBMCLI:
    """PKBM命令行界面"""
    
    def __init__(self):
        self.db_path = Path("data/pkbm.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建知识条目表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    category TEXT,
                    tags TEXT,
                    created_date TEXT,
                    updated_date TEXT,
                    file_path TEXT
                )
            ''')
            
            # 创建分类表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
            ''')
            
            # 插入默认分类
            default_categories = [
                ('格言警句', '经典格言和警句'),
                ('方法论', '各种方法和理论'),
                ('技术文档', '技术相关的文档'),
                ('学习笔记', '学习过程中的笔记'),
                ('工作记录', '工作相关的记录'),
                ('生活感悟', '生活中的感悟和思考'),
                ('书籍摘要', '读书笔记和摘要'),
                ('其他', '其他类型的内容')
            ]
            
            for name, desc in default_categories:
                try:
                    cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, desc))
                except sqlite3.IntegrityError:
                    pass  # 已存在
            
            conn.commit()
            conn.close()
            print("✓ 数据库初始化完成")
            
        except Exception as e:
            print(f"✗ 数据库初始化失败: {e}")
    
    def show_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "="*50)
            print("PKBM - 个人知识库管理系统 (命令行版本)")
            print("="*50)
            print("1. 查看所有条目")
            print("2. 添加新条目")
            print("3. 搜索条目")
            print("4. 编辑条目")
            print("5. 删除条目")
            print("6. 查看分类")
            print("7. 导入文件")
            print("8. 数据库状态")
            print("0. 退出")
            print("-"*50)
            
            choice = input("请选择操作 (0-8): ").strip()
            
            if choice == '0':
                print("感谢使用PKBM！")
                break
            elif choice == '1':
                self.list_items()
            elif choice == '2':
                self.add_item()
            elif choice == '3':
                self.search_items()
            elif choice == '4':
                self.edit_item()
            elif choice == '5':
                self.delete_item()
            elif choice == '6':
                self.list_categories()
            elif choice == '7':
                self.import_file()
            elif choice == '8':
                self.show_db_status()
            else:
                print("无效选择，请重新输入")
    
    def list_items(self):
        """列出所有条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, category, created_date FROM knowledge_items ORDER BY updated_date DESC')
            items = cursor.fetchall()
            conn.close()
            
            if not items:
                print("暂无知识条目")
                return
            
            print(f"\n找到 {len(items)} 个条目:")
            print("-" * 80)
            print(f"{'ID':<5} {'标题':<30} {'分类':<15} {'创建日期':<20}")
            print("-" * 80)
            
            for item in items:
                print(f"{item[0]:<5} {item[1][:29]:<30} {item[2][:14]:<15} {item[3][:19]:<20}")
                
        except Exception as e:
            print(f"列出条目失败: {e}")
    
    def add_item(self):
        """添加新条目"""
        print("\n--- 添加新条目 ---")
        
        title = input("标题: ").strip()
        if not title:
            print("标题不能为空")
            return
        
        content = input("内容 (可选): ").strip()
        category = input("分类 (可选，默认'其他'): ").strip() or "其他"
        tags = input("标签 (可选，用逗号分隔): ").strip()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge_items (title, content, category, tags, created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, category, tags, datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            print(f"✓ 条目 '{title}' 添加成功")
            
        except Exception as e:
            print(f"✗ 添加条目失败: {e}")
    
    def search_items(self):
        """搜索条目"""
        print("\n--- 搜索条目 ---")
        keyword = input("请输入搜索关键词: ").strip()
        
        if not keyword:
            print("搜索关键词不能为空")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, category, tags FROM knowledge_items 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_date DESC
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            
            items = cursor.fetchall()
            conn.close()
            
            if not items:
                print(f"未找到包含 '{keyword}' 的条目")
                return
            
            print(f"\n找到 {len(items)} 个匹配条目:")
            print("-" * 80)
            
            for item in items:
                print(f"ID: {item[0]}")
                print(f"标题: {item[1]}")
                print(f"分类: {item[3]}")
                print(f"标签: {item[4] or '无'}")
                print(f"内容: {item[2][:100]}{'...' if len(item[2]) > 100 else ''}")
                print("-" * 40)
                
        except Exception as e:
            print(f"搜索失败: {e}")
    
    def edit_item(self):
        """编辑条目"""
        print("\n--- 编辑条目 ---")
        
        # 先列出所有条目
        self.list_items()
        
        item_id = input("\n请输入要编辑的条目ID: ").strip()
        if not item_id.isdigit():
            print("无效的ID")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM knowledge_items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            conn.close()
            
            if not item:
                print("条目不存在")
                return
            
            print(f"\n当前条目信息:")
            print(f"标题: {item[1]}")
            print(f"内容: {item[2]}")
            print(f"分类: {item[3]}")
            print(f"标签: {item[4]}")
            
            # 获取新信息
            new_title = input(f"新标题 (回车保持 '{item[1]}'): ").strip() or item[1]
            new_content = input(f"新内容 (回车保持当前内容): ").strip() or item[2]
            new_category = input(f"新分类 (回车保持 '{item[3]}'): ").strip() or item[3]
            new_tags = input(f"新标签 (回车保持当前标签): ").strip() or item[4]
            
            # 更新数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE knowledge_items 
                SET title=?, content=?, category=?, tags=?, updated_date=?
                WHERE id=?
            ''', (new_title, new_content, new_category, new_tags, datetime.now().isoformat(), item_id))
            
            conn.commit()
            conn.close()
            print(f"✓ 条目更新成功")
            
        except Exception as e:
            print(f"编辑条目失败: {e}")
    
    def delete_item(self):
        """删除条目"""
        print("\n--- 删除条目 ---")
        
        # 先列出所有条目
        self.list_items()
        
        item_id = input("\n请输入要删除的条目ID: ").strip()
        if not item_id.isdigit():
            print("无效的ID")
            return
        
        confirm = input("确定要删除这个条目吗？(y/N): ").strip().lower()
        if confirm != 'y':
            print("取消删除")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 先获取标题用于显示
            cursor.execute('SELECT title FROM knowledge_items WHERE id = ?', (item_id,))
            title = cursor.fetchone()
            
            if not title:
                print("条目不存在")
                return
            
            # 删除条目
            cursor.execute('DELETE FROM knowledge_items WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            
            print(f"✓ 条目 '{title[0]}' 删除成功")
            
        except Exception as e:
            print(f"删除条目失败: {e}")
    
    def list_categories(self):
        """列出所有分类"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name, description FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            print(f"\n找到 {len(categories)} 个分类:")
            print("-" * 60)
            print(f"{'分类名':<20} {'描述':<40}")
            print("-" * 60)
            
            for category in categories:
                print(f"{category[0]:<20} {category[1][:39]:<40}")
                
        except Exception as e:
            print(f"列出分类失败: {e}")
    
    def import_file(self):
        """导入文件"""
        print("\n--- 导入文件 ---")
        file_path = input("请输入文件路径: ").strip()
        
        if not file_path or not os.path.exists(file_path):
            print("文件不存在")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件名作为标题
            title = Path(file_path).stem
            
            # 保存到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge_items (title, content, category, created_date, updated_date, file_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, "其他", datetime.now().isoformat(), datetime.now().isoformat(), file_path))
            
            conn.commit()
            conn.close()
            
            print(f"✓ 文件 '{title}' 导入成功")
            
        except Exception as e:
            print(f"导入文件失败: {e}")
    
    def show_db_status(self):
        """显示数据库状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取条目数量
            cursor.execute('SELECT COUNT(*) FROM knowledge_items')
            item_count = cursor.fetchone()[0]
            
            # 获取分类数量
            cursor.execute('SELECT COUNT(*) FROM categories')
            category_count = cursor.fetchone()[0]
            
            # 获取数据库大小
            db_size = self.db_path.stat().st_size
            
            # 获取SQLite版本
            cursor.execute('SELECT sqlite_version()')
            sqlite_version = cursor.fetchone()[0]
            
            conn.close()
            
            print(f"\n--- 数据库状态 ---")
            print(f"数据库文件: {self.db_path}")
            print(f"文件大小: {db_size} 字节")
            print(f"SQLite版本: {sqlite_version}")
            print(f"知识条目: {item_count} 个")
            print(f"分类: {category_count} 个")
            
        except Exception as e:
            print(f"获取数据库状态失败: {e}")

def main():
    """主函数"""
    print("PKBM - 个人知识库管理系统 (命令行版本)")
    print("正在初始化...")
    
    app = PKBMCLI()
    app.show_menu()

if __name__ == "__main__":
    main()
