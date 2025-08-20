#!/usr/bin/env python3
"""
PKBM - 简单版本 (使用tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path

class SimplePKBM:
    def __init__(self, root):
        self.root = root
        self.root.title("PKBM - 简单版本")
        self.root.geometry("800x600")
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="个人知识库管理系统", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 说明
        info_label = ttk.Label(main_frame, text="这是一个使用tkinter的简单版本，当PyQt6不可用时可以使用")
        info_label.pack(pady=(0, 20))
        
        # 按钮
        ttk.Button(main_frame, text="测试数据库连接", command=self.test_db).pack(pady=5)
        ttk.Button(main_frame, text="关于", command=self.show_about).pack(pady=5)
        
    def test_db(self):
        try:
            db_path = Path("data/pkbm.db")
            db_path.parent.mkdir(exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            conn.close()
            
            messagebox.showinfo("成功", f"数据库连接成功！\nSQLite版本: {version}")
        except Exception as e:
            messagebox.showerror("错误", f"数据库连接失败: {e}")
    
    def show_about(self):
        messagebox.showinfo("关于", "PKBM - 个人知识库管理系统\n简单版本 v1.0")

def main():
    root = tk.Tk()
    app = SimplePKBM(root)
    root.mainloop()

if __name__ == "__main__":
    main()
