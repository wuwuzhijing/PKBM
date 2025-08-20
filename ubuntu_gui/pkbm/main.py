#!/usr/bin/env python3
"""
PKBM - Ubuntu GUI版本
使用tkinter创建跨平台兼容的界面
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

class PKBMUbuntuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PKBM - 个人知识库管理系统 (Ubuntu版)")
        self.root.geometry("1200x800")
        
        # 配置
        self.api_base = "http://127.0.0.1:8080/api"
        self.db_path = "data/pkbm.db"
        
        # 确保数据目录存在
        Path("data").mkdir(exist_ok=True)
        
        # 初始化数据库
        self.init_database()
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_data()
        
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
                    pass
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("错误", f"数据库初始化失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建工具栏
        self.create_toolbar(main_frame)
        
        # 创建主内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 左侧面板
        left_panel = ttk.Frame(content_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # 搜索框
        search_frame = ttk.LabelFrame(left_panel, text="搜索", padding=5)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X)
        search_entry.bind('<KeyRelease>', self.search_items)
        
        # 分类树
        category_frame = ttk.LabelFrame(left_panel, text="分类", padding=5)
        category_frame.pack(fill=tk.BOTH, expand=True)
        
        self.category_tree = ttk.Treeview(category_frame, show="tree")
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        self.category_tree.bind('<<TreeviewSelect>>', self.on_category_select)
        
        # 右侧内容区域
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 内容列表
        list_frame = ttk.LabelFrame(right_panel, text="知识条目", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建列表和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview显示条目
        columns = ('ID', '标题', '分类', '标签', '创建日期', '更新日期')
        self.item_tree = ttk.Treeview(list_container, columns=columns, show='headings')
        
        # 设置列标题
        for col in columns:
            self.item_tree.heading(col, text=col)
            self.item_tree.column(col, width=100)
        
        # 调整列宽
        self.item_tree.column('ID', width=50)
        self.item_tree.column('标题', width=200)
        self.item_tree.column('分类', width=100)
        self.item_tree.column('标签', width=150)
        self.item_tree.column('创建日期', width=120)
        self.item_tree.column('更新日期', width=120)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)
        
        self.item_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_tree.bind('<Double-Button-1>', self.on_item_double_click)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建条目", command=self.new_item)
        file_menu.add_command(label="导入文件", command=self.import_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="编辑条目", command=self.edit_item)
        edit_menu.add_command(label="删除条目", command=self.delete_item)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="刷新", command=self.load_data)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="启动后端服务", command=self.start_backend)
        tools_menu.add_command(label="连接状态", command=self.check_connection)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="新建", command=self.new_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="编辑", command=self.edit_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="删除", command=self.delete_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="刷新", command=self.load_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        ttk.Button(toolbar, text="启动后端", command=self.start_backend).pack(side=tk.LEFT, padx=(0, 5))
    
    def load_data(self):
        """加载数据"""
        try:
            # 加载分类
            self.load_categories()
            
            # 加载条目
            self.load_items()
            
            self.status_var.set("数据加载完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {e}")
    
    def load_categories(self):
        """加载分类"""
        try:
            # 清空现有项目
            for item in self.category_tree.get_children():
                self.category_tree.delete(item)
            
            # 添加"全部"选项
            self.category_tree.insert('', 'end', text="全部", values=("全部",))
            
            # 从数据库加载分类
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            # 添加分类
            for category in categories:
                self.category_tree.insert('', 'end', text=category[0], values=(category[0],))
                
        except Exception as e:
            print(f"加载分类失败: {e}")
    
    def load_items(self, category=None):
        """加载条目"""
        try:
            # 清空现有项目
            for item in self.item_tree.get_children():
                self.item_tree.delete(item)
            
            # 构建查询
            query = 'SELECT id, title, category, tags, created_date, updated_date FROM knowledge_items'
            params = []
            
            if category and category != "全部":
                query += ' WHERE category = ?'
                params.append(category)
            
            query += ' ORDER BY updated_date DESC'
            
            # 从数据库查询
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, params)
            items = cursor.fetchall()
            conn.close()
            
            # 添加到树形视图
            for item in items:
                # 格式化日期
                created_date = item[4][:19] if item[4] else ""
                updated_date = item[5][:19] if item[5] else ""
                
                self.item_tree.insert('', 'end', values=(
                    item[0], item[1], item[2], item[3], created_date, updated_date
                ))
                
        except Exception as e:
            print(f"加载条目失败: {e}")
    
    def search_items(self, event=None):
        """搜索条目"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_items()
            return
        
        try:
            # 清空现有项目
            for item in self.item_tree.get_children():
                self.item_tree.delete(item)
            
            # 搜索数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, category, tags, created_date, updated_date
                FROM knowledge_items 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_date DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            items = cursor.fetchall()
            conn.close()
            
            # 显示搜索结果
            for item in items:
                created_date = item[5][:19] if item[5] else ""
                updated_date = item[6][:19] if item[6] else ""
                
                self.item_tree.insert('', 'end', values=(
                    item[0], item[1], item[2], item[3], created_date, updated_date
                ))
                
        except Exception as e:
            print(f"搜索失败: {e}")
    
    def on_category_select(self, event):
        """分类选择事件"""
        selection = self.category_tree.selection()
        if selection:
            category = self.category_tree.item(selection[0])['values'][0]
            self.load_items(category)
    
    def on_item_double_click(self, event):
        """条目双击事件"""
        selection = self.item_tree.selection()
        if selection:
            item_id = self.item_tree.item(selection[0])['values'][0]
            self.view_item(item_id)
    
    def new_item(self):
        """新建条目"""
        self.show_item_dialog()
    
    def edit_item(self):
        """编辑条目"""
        selection = self.item_tree.selection()
        if selection:
            item_id = self.item_tree.item(selection[0])['values'][0]
            self.edit_item_by_id(item_id)
        else:
            messagebox.showwarning("警告", "请先选择一个条目")
    
    def view_item(self, item_id):
        """查看条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM knowledge_items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            conn.close()
            
            if item:
                self.show_item_view(item)
            else:
                messagebox.showerror("错误", "条目不存在")
                
        except Exception as e:
            messagebox.showerror("错误", f"查看条目失败: {e}")
    
    def edit_item_by_id(self, item_id):
        """根据ID编辑条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM knowledge_items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            conn.close()
            
            if item:
                self.show_item_dialog(item)
            else:
                messagebox.showerror("错误", "条目不存在")
                
        except Exception as e:
            messagebox.showerror("错误", f"编辑条目失败: {e}")
    
    def delete_item(self):
        """删除条目"""
        selection = self.item_tree.selection()
        if selection:
            item_id = self.item_tree.item(selection[0])['values'][0]
            title = self.item_tree.item(selection[0])['values'][1]
            
            if messagebox.askyesno("确认", f"确定要删除条目 '{title}' 吗？"):
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM knowledge_items WHERE id = ?', (item_id,))
                    conn.commit()
                    conn.close()
                    
                    self.load_items()
                    self.status_var.set(f"已删除条目: {title}")
                    
                except Exception as e:
                    messagebox.showerror("错误", f"删除失败: {e}")
        else:
            messagebox.showwarning("警告", "请先选择一个条目")
    
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
        
        if file_path:
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
                
                self.load_items()
                self.status_var.set(f"已导入文件: {title}")
                
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {e}")
    
    def start_backend(self):
        """启动后端服务"""
        def start_service():
            try:
                # 这里可以启动Go后端服务
                # 或者检查服务状态
                response = requests.get(f"{self.api_base}/stats", timeout=5)
                if response.status_code == 200:
                    messagebox.showinfo("信息", "后端服务正在运行")
                else:
                    messagebox.showwarning("警告", "后端服务响应异常")
            except requests.exceptions.RequestException:
                messagebox.showinfo("信息", "后端服务未启动，请手动启动Go后端")
        
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
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", 
            "PKBM - 个人知识库管理系统\n\n"
            "版本: 1.0.0 (Ubuntu GUI版本)\n"
            "使用tkinter构建，支持跨平台\n"
            "后端: Go语言 + SQLite数据库")
    
    def show_item_dialog(self, item=None):
        """显示条目编辑对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑条目" if item else "新建条目")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(form_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_var = tk.StringVar(value=item[1] if item else "")
        title_entry = ttk.Entry(form_frame, textvariable=title_var, width=50)
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 分类
        ttk.Label(form_frame, text="分类:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar(value=item[3] if item else "其他")
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                    values=["其他", "格言警句", "方法论", "技术文档", "学习笔记", "工作记录", "生活感悟", "书籍摘要"])
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 标签
        ttk.Label(form_frame, text="标签:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tags_var = tk.StringVar(value=item[4] if item else "")
        tags_entry = ttk.Entry(form_frame, textvariable=tags_var, width=50)
        tags_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 内容
        ttk.Label(form_frame, text="内容:").grid(row=3, column=0, sticky=tk.W, pady=5)
        content_text = scrolledtext.ScrolledText(form_frame, height=15, width=50)
        content_text.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
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
                
                if item:
                    # 更新现有条目
                    cursor.execute('''
                        UPDATE knowledge_items 
                        SET title=?, content=?, category=?, tags=?, updated_date=?
                        WHERE id=?
                    ''', (title, content, category, tags, datetime.now().isoformat(), item[0]))
                else:
                    # 创建新条目
                    cursor.execute('''
                        INSERT INTO knowledge_items (title, content, category, tags, created_date, updated_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (title, content, category, tags, datetime.now().isoformat(), datetime.now().isoformat()))
                
                conn.commit()
                conn.close()
                
                self.load_items()
                self.status_var.set(f"已{'更新' if item else '创建'}条目: {title}")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="保存", command=save_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=cancel).pack(side=tk.LEFT)
        
        # 配置网格权重
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(3, weight=1)
        
        # 设置焦点
        title_entry.focus()
    
    def show_item_view(self, item):
        """显示条目查看对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"查看条目: {item[1]}")
        dialog.geometry("700x600")
        dialog.transient(self.root)
        
        # 创建内容框架
        content_frame = ttk.Frame(dialog, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(content_frame, text=item[1], font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 信息栏
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(info_frame, text=f"分类: {item[3]}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"标签: {item[4] or '无'}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"创建时间: {item[5][:19] if item[5] else ''}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"更新时间: {item[6][:19] if item[6] else ''}").pack(anchor=tk.W)
        
        # 内容
        content_label = ttk.Label(content_frame, text="内容:", font=("Arial", 12, "bold"))
        content_label.pack(anchor=tk.W, pady=(20, 5))
        
        content_text = scrolledtext.ScrolledText(content_frame, height=20, width=80, wrap=tk.WORD)
        content_text.pack(fill=tk.BOTH, expand=True)
        content_text.insert(tk.END, item[2] or "无内容")
        content_text.config(state=tk.DISABLED)
        
        # 按钮
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="编辑", 
                  command=lambda: [dialog.destroy(), self.edit_item_by_id(item[0])]).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="关闭", command=dialog.destroy).pack(side=tk.LEFT)

def main():
    """主函数"""
    root = tk.Tk()
    app = PKBMUbuntuGUI(root)
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main()
