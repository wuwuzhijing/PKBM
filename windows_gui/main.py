#!/usr/bin/env python3
"""
PKBM - Windows GUI版本 (改进版)
使用tkinter创建跨平台兼容的界面
解决分类管理、界面美观和后端启动问题
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sqlite3
import json
import requests
import os
from pathlib import Path
from datetime import datetime
import threading
import subprocess
import sys

class PKBMImprovedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PKBM - 个人知识库管理系统 (改进版)")
        self.root.geometry("1400x900")
        
        # 配置
        self.api_base = "http://127.0.0.1:8080/api"
        self.db_path = "data/pkbm.db"
        
        # 确保数据目录存在
        Path("data").mkdir(exist_ok=True)
        
        # 设置样式
        self.setup_styles()
        
        # 初始化数据库
        self.init_database()
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_data()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 配置主题
        style.theme_use('clam')
        
        # 配置颜色
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TButton', background='#27ae60', foreground='white')
        style.configure('Primary.TButton', background='#3498db', foreground='white')
        style.configure('Warning.TButton', background='#e74c3c', foreground='white')
        
        # 配置框架样式
        style.configure('Card.TFrame', relief='solid', borderwidth=1)
        style.configure('Panel.TFrame', background='#ecf0f1')
        
    def init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    category TEXT,
                    tags TEXT,
                    created_date TEXT,
                    updated_date TEXT,
                    file_path TEXT,
                    file_type TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    color TEXT DEFAULT '#3498db'
                )
            ''')
            
            # 插入默认分类
            default_categories = [
                ('格言警句', '经典格言和警句', '#e74c3c'),
                ('方法论', '各种方法和理论', '#f39c12'),
                ('技术文档', '技术相关的文档', '#3498db'),
                ('学习笔记', '学习过程中的笔记', '#9b59b6'),
                ('工作记录', '工作相关的记录', '#1abc9c'),
                ('生活感悟', '生活中的感悟和思考', '#e67e22'),
                ('书籍摘要', '读书笔记和摘要', '#34495e'),
                ('其他', '其他类型的内容', '#95a5a6')
            ]
            
            for name, desc, color in default_categories:
                try:
                    cursor.execute('INSERT INTO categories (name, description, color) VALUES (?, ?, ?)', (name, desc, color))
                except sqlite3.IntegrityError:
                    pass
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("错误", f"数据库初始化失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, style='Panel.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 创建标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="📚 PKBM 个人知识库管理系统", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Personal Knowledge Base Management System", 
                                 font=('Arial', 10), foreground='#7f8c8d')
        subtitle_label.pack()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建工具栏
        self.create_toolbar(main_frame)
        
        # 创建主内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # 左侧面板
        left_panel = ttk.Frame(content_frame, width=350, style='Card.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # 搜索框
        search_frame = ttk.LabelFrame(left_panel, text="🔍 搜索", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 15))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(fill=tk.X, pady=(5, 0))
        search_entry.bind('<KeyRelease>', self.search_items)
        
        # 分类管理
        category_frame = ttk.LabelFrame(left_panel, text="📁 分类管理", padding=10)
        category_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 分类操作按钮
        category_buttons_frame = ttk.Frame(category_frame)
        category_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(category_buttons_frame, text="➕ 新建", 
                  command=self.new_category, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(category_buttons_frame, text="✏️ 编辑", 
                  command=self.edit_category, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(category_buttons_frame, text="🗑️ 删除", 
                  command=self.delete_category, style='Warning.TButton').pack(side=tk.LEFT)
        
        # 分类树
        self.category_tree = ttk.Treeview(category_frame, show="tree", height=15)
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        self.category_tree.bind('<<TreeviewSelect>>', self.on_category_select)
        self.category_tree.bind('<Double-Button-1>', self.on_category_double_click)
        
        # 右侧内容区域
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 内容列表
        list_frame = ttk.LabelFrame(right_panel, text="📝 知识条目", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建列表和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 使用Treeview替代Listbox，提供更好的显示效果
        columns = ('标题', '分类', '标签', '更新时间')
        self.item_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=20)
        
        # 设置列标题和宽度
        for col in columns:
            self.item_tree.heading(col, text=col)
            if col == '标题':
                self.item_tree.column(col, width=300)
            elif col == '分类':
                self.item_tree.column(col, width=100)
            elif col == '标签':
                self.item_tree.column(col, width=150)
            else:
                self.item_tree.column(col, width=150)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)
        
        self.item_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_tree.bind('<Double-Button-1>', self.on_item_double_click)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("✅ 系统就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, 
                             font=('Arial', 9), foreground='#7f8c8d')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 加载数据
        self.load_categories()
        self.load_items()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 文件", menu=file_menu)
        file_menu.add_command(label="🆕 新建条目", command=self.new_item)
        file_menu.add_command(label="📥 导入文件", command=self.import_file)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 退出", command=self.root.quit)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="✏️ 编辑", menu=edit_menu)
        edit_menu.add_command(label="✏️ 编辑条目", command=self.edit_item)
        edit_menu.add_command(label="🗑️ 删除条目", command=self.delete_item)
        
        # 分类菜单
        category_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📂 分类", menu=category_menu)
        category_menu.add_command(label="➕ 新建分类", command=self.new_category)
        category_menu.add_command(label="✏️ 编辑分类", command=self.edit_category)
        category_menu.add_command(label="🗑️ 删除分类", command=self.delete_category)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 工具", menu=tools_menu)
        tools_menu.add_command(label="🚀 启动后端服务", command=self.start_backend)
        tools_menu.add_command(label="🔗 检查连接", command=self.check_connection)
        tools_menu.add_separator()
        tools_menu.add_command(label="🔄 刷新数据", command=self.refresh_data)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ 视图", menu=view_menu)
        view_menu.add_command(label="📊 统计信息", command=self.show_stats)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ 帮助", menu=help_menu)
        help_menu.add_command(label="ℹ️ 关于", command=self.show_about)
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ttk.Frame(parent, style='Card.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 20))
        
        # 主要操作按钮
        ttk.Button(toolbar, text="🆕 新建条目", command=self.new_item, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=(10, 5), pady=10)
        ttk.Button(toolbar, text="✏️ 编辑", command=self.edit_item, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 5), pady=10)
        ttk.Button(toolbar, text="🗑️ 删除", command=self.delete_item, 
                  style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 5), pady=10)
        
        # 分隔符
        ttk.Separator(toolbar, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        # 系统操作按钮
        ttk.Button(toolbar, text="🚀 启动后端", command=self.start_backend, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 5), pady=10)
        ttk.Button(toolbar, text="🔄 刷新", command=self.refresh_data).pack(side=tk.LEFT, padx=(0, 5), pady=10)
        ttk.Button(toolbar, text="📊 统计", command=self.show_stats).pack(side=tk.LEFT, padx=(0, 10), pady=10)

    def load_data(self):
        """加载数据"""
        self.load_categories()
        self.load_items()
    
    def load_categories(self):
        """加载分类数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name, description, color FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.category_tree.get_children():
                self.category_tree.delete(item)
            
            # 添加分类
            for name, desc, color in categories:
                self.category_tree.insert('', 'end', text=name, values=(name, desc, color))
                
        except Exception as e:
            print(f"加载分类失败: {e}")
            messagebox.showerror("错误", f"加载分类失败: {e}")
    
    def load_items(self, category=None):
        """加载知识条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category and category != "全部":
                cursor.execute('''
                    SELECT title, category, tags, updated_date 
                    FROM knowledge_items 
                    WHERE category = ? 
                    ORDER BY updated_date DESC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT title, category, tags, updated_date 
                    FROM knowledge_items 
                    ORDER BY updated_date DESC
                ''')
            
            items = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.item_tree.get_children():
                self.item_tree.delete(item)
            
            # 添加条目
            for title, cat, tags, updated in items:
                # 格式化更新时间
                if updated:
                    try:
                        dt = datetime.fromisoformat(updated)
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_date = updated
                else:
                    formatted_date = "未知"
                
                self.item_tree.insert('', 'end', values=(title, cat or "未分类", tags or "", formatted_date))
                
        except Exception as e:
            print(f"加载条目失败: {e}")
            messagebox.showerror("错误", f"加载条目失败: {e}")

    def load_data(self):
        """加载数据"""
        self.load_categories()
        self.load_items()
    
    def load_categories(self):
        """加载分类数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name, description, color FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.category_tree.get_children():
                self.category_tree.delete(item)
            
            # 添加分类
            for name, desc, color in categories:
                self.category_tree.insert('', 'end', text=name, values=(name, desc, color))
                
        except Exception as e:
            print(f"加载分类失败: {e}")
            messagebox.showerror("错误", f"加载分类失败: {e}")
    
    def load_items(self, category=None):
        """加载知识条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category and category != "全部":
                cursor.execute('''
                    SELECT title, category, tags, updated_date 
                    FROM knowledge_items 
                    WHERE category = ? 
                    ORDER BY updated_date DESC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT title, category, tags, updated_date 
                    FROM knowledge_items 
                    ORDER BY updated_date DESC
                ''')
            
            items = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.item_tree.get_children():
                self.item_tree.delete(item)
            
            # 添加条目
            for title, cat, tags, updated in items:
                # 格式化更新时间
                if updated:
                    try:
                        dt = datetime.fromisoformat(updated)
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_date = updated
                else:
                    formatted_date = "未知"
                
                self.item_tree.insert('', 'end', values=(title, cat or "未分类", tags or "", formatted_date))
                
        except Exception as e:
            print(f"加载条目失败: {e}")
            messagebox.showerror("错误", f"加载条目失败: {e}")
    
    def search_items(self, event=None):
        """搜索条目"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_items()
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, category, tags, updated_date FROM knowledge_items 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_date DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            items = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.item_tree.get_children():
                self.item_tree.delete(item)
            
            # 添加搜索结果
            for title, cat, tags, updated in items:
                if updated:
                    try:
                        dt = datetime.fromisoformat(updated)
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_date = updated
                else:
                    formatted_date = "未知"
                
                self.item_tree.insert('', 'end', values=(title, cat or "未分类", tags or "", formatted_date))
                
        except Exception as e:
            print(f"搜索失败: {e}")
            messagebox.showerror("错误", f"搜索失败: {e}")
    
    def on_category_select(self, event):
        """分类选择事件"""
        selection = self.category_tree.selection()
        if selection:
            category = self.category_tree.item(selection[0])['text']
            self.load_items(category)
            self.status_var.set(f"📁 当前分类: {category}")
    
    def on_category_double_click(self, event):
        """分类双击事件"""
        self.edit_category()
    
    def on_item_double_click(self, event):
        """条目双击事件"""
        selection = self.item_tree.selection()
        if selection:
            title = self.item_tree.item(selection[0])['values'][0]
            self.edit_item_by_title(title)
    
    def new_item(self):
        """新建条目"""
        self.show_item_dialog()
    
    def edit_item(self):
        """编辑条目"""
        selection = self.item_tree.selection()
        if selection:
            title = self.item_tree.item(selection[0])['values'][0]
            self.edit_item_by_title(title)
        else:
            messagebox.showwarning("警告", "请先选择一个条目")
    
    def edit_item_by_title(self, title):
        """根据标题编辑条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM knowledge_items WHERE title = ?', (title,))
            item = cursor.fetchone()
            conn.close()
            
            if item:
                self.show_item_dialog(item)
            else:
                messagebox.showerror("错误", "条目不存在")
                
        except Exception as e:
            messagebox.showerror("错误", f"获取条目信息失败: {e}")
    
    def delete_item(self):
        """删除条目"""
        selection = self.item_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个条目")
            return
        
        title = self.item_tree.item(selection[0])['values'][0]
        if messagebox.askyesno("确认删除", f"确定要删除条目 '{title}' 吗？"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM knowledge_items WHERE title = ?', (title,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("成功", "条目删除成功")
                self.load_items()
                
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")
    
    def new_category(self):
        """新建分类"""
        self.show_category_dialog()
    
    def edit_category(self):
        """编辑分类"""
        selection = self.category_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类")
            return
        
        category_name = self.category_tree.item(selection[0])['text']
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories WHERE name = ?', (category_name,))
            category = cursor.fetchone()
            conn.close()
            
            if category:
                self.show_category_dialog(category)
            else:
                messagebox.showerror("错误", "分类不存在")
                
        except Exception as e:
            messagebox.showerror("错误", f"获取分类信息失败: {e}")
    
    def delete_category(self):
        """删除分类"""
        selection = self.category_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个分类")
            return
        
        category_name = self.category_tree.item(selection[0])['text']
        
        # 检查是否有条目使用此分类
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM knowledge_items WHERE category = ?', (category_name,))
            count = cursor.fetchone()[0]
            conn.close()
            
            if count > 0:
                messagebox.showwarning("警告", f"分类 '{category_name}' 下还有 {count} 个条目，无法删除")
                return
                
        except Exception as e:
            messagebox.showerror("错误", f"检查分类使用情况失败: {e}")
            return
        
        if messagebox.askyesno("确认删除", f"确定要删除分类 '{category_name}' 吗？"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM categories WHERE name = ?', (category_name,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("成功", "分类删除成功")
                self.load_categories()
                
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")
    
    def show_category_dialog(self, category=None):
        """显示分类编辑对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑分类" if category else "新建分类")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 分类名
        ttk.Label(form_frame, text="分类名:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_var = tk.StringVar(value=category[1] if category else "")
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30, font=('Arial', 10))
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 描述
        ttk.Label(form_frame, text="描述:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=10)
        desc_var = tk.StringVar(value=category[2] if category else "")
        desc_entry = ttk.Entry(form_frame, textvariable=desc_var, width=30, font=('Arial', 10))
        desc_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 颜色选择
        ttk.Label(form_frame, text="颜色:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=10)
        color_var = tk.StringVar(value=category[3] if category else "#3498db")
        colors = ["#e74c3c", "#f39c12", "#3498db", "#9b59b6", "#1abc9c", "#e67e22", "#34495e", "#95a5a6"]
        color_combo = ttk.Combobox(form_frame, textvariable=color_var, values=colors, width=27, font=('Arial', 10))
        color_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 按钮
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=30)
        
        def save_category():
            name = name_var.get().strip()
            description = desc_var.get().strip()
            color = color_var.get()
            
            if not name:
                messagebox.showwarning("警告", "分类名不能为空")
                return
            
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                if category:
                    # 更新现有分类
                    cursor.execute('''
                        UPDATE categories 
                        SET name = ?, description = ?, color = ? 
                        WHERE id = ?
                    ''', (name, description, color, category[0]))
                else:
                    # 创建新分类
                    cursor.execute('''
                        INSERT INTO categories (name, description, color) 
                        VALUES (?, ?, ?)
                    ''', (name, description, color))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("成功", "分类保存成功")
                dialog.destroy()
                self.load_categories()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("错误", f"分类名 '{name}' 已存在")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
        
        ttk.Button(button_frame, text="保存", command=save_category, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
        
        # 设置焦点
        name_entry.focus()
    
    def show_item_dialog(self, item=None):
        """显示条目编辑对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑条目" if item else "新建条目")
        dialog.geometry("700x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(form_frame, text="标题:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=10)
        title_var = tk.StringVar(value=item[1] if item else "")
        title_entry = ttk.Entry(form_frame, textvariable=title_var, width=50, font=('Arial', 10))
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 分类
        ttk.Label(form_frame, text="分类:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=10)
        category_var = tk.StringVar(value=item[3] if item else "其他")
        
        # 获取所有分类
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories ORDER BY name')
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
        except:
            categories = ["其他", "格言警句", "方法论", "技术文档", "学习笔记", "工作记录", "生活感悟", "书籍摘要"]
        
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                    values=categories, width=47, font=('Arial', 10))
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 标签
        ttk.Label(form_frame, text="标签:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=10)
        tags_var = tk.StringVar(value=item[4] if item else "")
        tags_entry = ttk.Entry(form_frame, textvariable=tags_var, width=50, font=('Arial', 10))
        tags_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # 内容
        ttk.Label(form_frame, text="内容:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=10)
        content_text = scrolledtext.ScrolledText(form_frame, height=20, width=50, font=('Arial', 10))
        content_text.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(10, 0))
        
        if item:
            content_text.insert(tk.END, item[2] or "")
        
        # 按钮
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_item():
            title = title_var.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            category = category_var.get()
            tags = tags_var.get().strip()
            
            if not title:
                messagebox.showwarning("警告", "标题不能为空")
                return
            
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                now = datetime.now().isoformat()
                
                if item:
                    # 更新现有条目
                    cursor.execute('''
                        UPDATE knowledge_items 
                        SET title = ?, content = ?, category = ?, tags = ?, updated_date = ?
                        WHERE id = ?
                    ''', (title, content, category, tags, now, item[0]))
                else:
                    # 创建新条目
                    cursor.execute('''
                        INSERT INTO knowledge_items (title, content, category, tags, created_date, updated_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (title, content, category, tags, now, now))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("成功", "条目保存成功")
                dialog.destroy()
                self.load_items()
                
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
        
        ttk.Button(button_frame, text="保存", command=save_item, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
        
        # 设置焦点
        title_entry.focus()
    
    def import_file(self):
        """导入文件"""
        file_path = filedialog.askopenfilename(
            title="选择要导入的文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("Markdown文件", "*.md"),
                ("所有文件", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件名作为标题
            title = os.path.splitext(os.path.basename(file_path))[0]
            
            # 创建条目
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO knowledge_items (title, content, category, created_date, updated_date, file_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, "其他", now, now, file_path))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("成功", f"文件 '{title}' 导入成功")
            self.load_items()
            
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {e}")
    
    def start_backend(self):
        """启动后端服务"""
        def start_service():
            try:
                # 尝试启动Go后端服务
                backend_path = Path("../backend")
                if backend_path.exists():
                    # 检查是否有Go后端可执行文件
                    go_files = list(backend_path.glob("*.go"))
                    if go_files:
                        try:
                            # 尝试启动Go后端
                            subprocess.run(["go", "run", "main.go"], 
                                         cwd=backend_path, 
                                         check=True, 
                                         timeout=30)
                        except subprocess.TimeoutExpired:
                            messagebox.showinfo("信息", "Go后端启动超时，可能正在运行")
                        except FileNotFoundError:
                            messagebox.showwarning("警告", "未找到Go环境，请先安装Go")
                        except Exception as e:
                            messagebox.showwarning("警告", f"启动Go后端失败: {e}")
                    else:
                        messagebox.showinfo("信息", "未找到Go后端代码，请检查backend目录")
                else:
                    messagebox.showinfo("信息", "未找到backend目录，请检查项目结构")
                
                # 检查服务状态
                try:
                    response = requests.get(f"{self.api_base}/stats", timeout=5)
                    if response.status_code == 200:
                        messagebox.showinfo("信息", "后端服务正在运行")
                    else:
                        messagebox.showwarning("警告", "后端服务响应异常")
                except requests.exceptions.RequestException:
                    messagebox.showinfo("信息", "后端服务未启动或无法连接")
                    
            except Exception as e:
                messagebox.showerror("错误", f"启动后端服务失败: {e}")
        
        threading.Thread(target=start_service, daemon=True).start()
    
    def check_connection(self):
        """检查连接状态"""
        try:
            response = requests.get(f"{self.api_base}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                messagebox.showinfo("连接状态", 
                    f"后端服务连接正常\n"
                    f"条目总数: {stats.get('total_items', 0)}\n"
                    f"分类总数: {stats.get('total_categories', 0)}")
            else:
                messagebox.showwarning("连接状态", "后端服务响应异常")
        except requests.exceptions.RequestException:
            messagebox.showerror("连接状态", "无法连接到后端服务")
    
    def refresh_data(self):
        """刷新数据"""
        self.load_categories()
        self.load_items()
        self.status_var.set("🔄 数据已刷新")
    
    def show_stats(self):
        """显示统计信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 统计条目总数
            cursor.execute('SELECT COUNT(*) FROM knowledge_items')
            total_items = cursor.fetchone()[0]
            
            # 统计分类总数
            cursor.execute('SELECT COUNT(*) FROM categories')
            total_categories = cursor.fetchone()[0]
            
            # 统计各分类条目数
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM knowledge_items 
                GROUP BY category 
                ORDER BY count DESC
            ''')
            category_stats = cursor.fetchall()
            
            conn.close()
            
            # 构建统计信息
            stats_text = f"📊 系统统计信息\n\n"
            stats_text += f"📝 条目总数: {total_items}\n"
            stats_text += f"📁 分类总数: {total_categories}\n\n"
            stats_text += "📈 分类统计:\n"
            
            for category, count in category_stats:
                stats_text += f"  {category}: {count} 条\n"
            
            messagebox.showinfo("统计信息", stats_text)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取统计信息失败: {e}")
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", 
            "PKBM - 个人知识库管理系统 (改进版)\n\n"
            "版本: 2.0.0\n"
            "使用tkinter构建，支持跨平台\n"
            "功能特性:\n"
            "• 完整的分类管理\n"
            "• 美观的界面设计\n"
            "• 强大的搜索功能\n"
            "• 文件导入支持\n"
            "• 统计信息显示\n\n"
            "后端: Go语言 + SQLite数据库")

def main():
    """主函数"""
    root = tk.Tk()
    app = PKBMImprovedGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
