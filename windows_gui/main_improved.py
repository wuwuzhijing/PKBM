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
