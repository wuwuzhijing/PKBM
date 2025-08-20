#!/usr/bin/env python3
"""
PKBM - 个人知识库管理系统 (Tkinter版本)
备选主程序，使用Python内置的tkinter库
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime

class PKBMTkinterApp:
    """PKBM Tkinter应用主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PKBM - 个人知识库管理系统 (Tkinter版本)")
        self.root.geometry("1200x800")
        
        # 数据库连接
        self.db_path = Path("data/pkbm.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
        
        # 创建界面
        self.create_widgets()
        
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
            print("数据库初始化完成")
            
        except Exception as e:
            print(f"数据库初始化失败: {e}")
    
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
        
        self.item_list = tk.Listbox(list_container)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.item_list.yview)
        self.item_list.configure(yscrollcommand=scrollbar.set)
        
        self.item_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_list.bind('<Double-Button-1>', self.on_item_double_click)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
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
        view_menu.add_command(label="刷新", command=self.refresh_data)
        
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
        ttk.Button(toolbar, text="刷新", command=self.refresh_data).pack(side=tk.LEFT, padx=(0, 5))
    
    def load_categories(self):
        """加载分类数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            for item in self.category_tree.get_children():
                self.category_tree.delete(item)
            
            # 添加分类
            for category in categories:
                self.category_tree.insert('', 'end', text=category[0], values=(category[0],))
                
        except Exception as e:
            print(f"加载分类失败: {e}")
    
    def load_items(self, category=None):
        """加载知识条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category and category != "全部":
                cursor.execute('SELECT title FROM knowledge_items WHERE category = ? ORDER BY updated_date DESC', (category,))
            else:
                cursor.execute('SELECT title FROM knowledge_items ORDER BY updated_date DESC')
            
            items = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            self.item_list.delete(0, tk.END)
            
            # 添加条目
            for item in items:
                self.item_list.insert(tk.END, item[0])
                
        except Exception as e:
            print(f"加载条目失败: {e}")
    
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
                SELECT title FROM knowledge_items 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_date DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            items = cursor.fetchall()
            conn.close()
            
            # 清空现有项目
            self.item_list.delete(0, tk.END)
            
            # 添加搜索结果
            for item in items:
                self.item_list.insert(tk.END, item[0])
                
        except Exception as e:
            print(f"搜索失败: {e}")
    
    def on_category_select(self, event):
        """分类选择事件"""
        selection = self.category_tree.selection()
        if selection:
            category = self.category_tree.item(selection[0])['text']
            self.load_items(category)
    
    def on_item_double_click(self, event):
        """条目双击事件"""
        selection = self.item_list.curselection()
        if selection:
            title = self.item_list.get(selection[0])
            self.edit_item_by_title(title)
    
    def new_item(self):
        """新建条目"""
        self.show_item_dialog()
    
    def edit_item(self):
        """编辑条目"""
        selection = self.item_list.curselection()
        if selection:
            title = self.item_list.get(selection[0])
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
            print(f"编辑条目失败: {e}")
    
    def delete_item(self):
        """删除条目"""
        selection = self.item_list.curselection()
        if selection:
            title = self.item_list.get(selection[0])
            if messagebox.askyesno("确认", f"确定要删除条目 '{title}' 吗？"):
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM knowledge_items WHERE title = ?', (title,))
                    conn.commit()
                    conn.close()
                    
                    self.load_items()
                    self.status_var.set(f"已删除条目: {title}")
                    
                except Exception as e:
                    print(f"删除条目失败: {e}")
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
                print(f"导入文件失败: {e}")
                messagebox.showerror("错误", f"导入失败: {e}")
    
    def refresh_data(self):
        """刷新数据"""
        self.load_categories()
        self.load_items()
        self.status_var.set("数据已刷新")
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", 
            "PKBM - 个人知识库管理系统\n\n"
            "版本: 1.0.0 (Tkinter版本)\n"
            "这是一个使用Python内置tkinter库的备选版本\n"
            "当PyQt6不可用时可以使用此版本")
    
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
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=["其他", "格言警句", "方法论", "技术文档", "学习笔记", "工作记录", "生活感悟", "书籍摘要"])
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 标签
        ttk.Label(form_frame, text="标签:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tags_var = tk.StringVar(value=item[4] if item else "")
        tags_entry = ttk.Entry(form_frame, textvariable=tags_var, width=50)
        tags_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 内容
        ttk.Label(form_frame, text="内容:").grid(row=3, column=0, sticky=tk.W, pady=5)
        content_text = tk.Text(form_frame, height=15, width=50)
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
                print(f"保存条目失败: {e}")
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

def main():
    """主函数"""
    root = tk.Tk()
    app = PKBMTkinterApp(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap("resources/icon.ico")
    except:
        pass
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main()
