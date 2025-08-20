"""
数据库模型定义
定义PKBM系统的所有数据表结构
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "data/pkbm.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库，创建所有必要的表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建格言与方法论表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT,
                field TEXT,
                tags TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attachments TEXT
            )
        ''')
        
        # 创建科技名词缩写表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tech_abbreviations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                abbreviation TEXT NOT NULL,
                full_name TEXT NOT NULL,
                chinese_name TEXT,
                description TEXT,
                category TEXT,
                tags TEXT,
                examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建书籍记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                isbn TEXT,
                publisher TEXT,
                publish_date DATE,
                description TEXT,
                category TEXT,
                tags TEXT,
                rating INTEGER DEFAULT 0,
                status TEXT DEFAULT 'unread',
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建标签表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#007ACC',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建分类表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                parent_id INTEGER,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        ''')
        
        # 创建附件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                mime_type TEXT,
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建搜索历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                result_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建设置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引以提高搜索性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_quotes_content ON quotes_methods(content)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_quotes_tags ON quotes_methods(tags)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_abbr_abbr ON tech_abbreviations(abbreviation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)


class QuoteMethod:
    """格言与方法论模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, title: str, content: str, author: str = "", field: str = "", 
            tags: List[str] = None, source: str = "", attachments: List[str] = None) -> int:
        """添加新的格言或方法论"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags or [], ensure_ascii=False)
        attachments_str = json.dumps(attachments or [], ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO quotes_methods (title, content, author, field, tags, source, attachments)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, author, field, tags_str, source, attachments_str))
        
        quote_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return quote_id
    
    def get_by_id(self, quote_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取格言"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM quotes_methods WHERE id = ?', (quote_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索格言"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        search_query = f'%{query}%'
        cursor.execute('''
            SELECT * FROM quotes_methods 
            WHERE title LIKE ? OR content LIKE ? OR author LIKE ? OR field LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (search_query, search_query, search_query, search_query, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        columns = ['id', 'title', 'content', 'author', 'field', 'tags', 'source', 
                  'created_at', 'updated_at', 'attachments']
        result = dict(zip(columns, row))
        
        # 解析JSON字段
        if result['tags']:
            result['tags'] = json.loads(result['tags'])
        if result['attachments']:
            result['attachments'] = json.loads(result['attachments'])
        
        return result


class TechAbbreviation:
    """科技名词缩写模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, abbreviation: str, full_name: str, chinese_name: str = "", 
            description: str = "", category: str = "", tags: List[str] = None, 
            examples: str = "") -> int:
        """添加新的科技名词缩写"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags or [], ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO tech_abbreviations (abbreviation, full_name, chinese_name, 
                                         description, category, tags, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (abbreviation, full_name, chinese_name, description, category, tags_str, examples))
        
        abbr_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return abbr_id
    
    def get_by_abbreviation(self, abbr: str) -> Optional[Dict[str, Any]]:
        """根据缩写获取名词"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tech_abbreviations WHERE abbreviation = ?', (abbr,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索科技名词缩写"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        search_query = f'%{query}%'
        cursor.execute('''
            SELECT * FROM tech_abbreviations 
            WHERE abbreviation LIKE ? OR full_name LIKE ? OR chinese_name LIKE ? 
                  OR description LIKE ? OR category LIKE ?
            ORDER BY abbreviation
            LIMIT ?
        ''', (search_query, search_query, search_query, search_query, search_query, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        columns = ['id', 'abbreviation', 'full_name', 'chinese_name', 'description', 
                  'category', 'tags', 'examples', 'created_at', 'updated_at']
        result = dict(zip(columns, row))
        
        if result['tags']:
            result['tags'] = json.loads(result['tags'])
        
        return result


class Book:
    """书籍记录模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, title: str, author: str = "", isbn: str = "", publisher: str = "", 
            publish_date: str = "", description: str = "", category: str = "", 
            tags: List[str] = None, rating: int = 0, status: str = "unread", 
            file_path: str = "") -> int:
        """添加新的书籍记录"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags or [], ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO books (title, author, isbn, publisher, publish_date, 
                             description, category, tags, rating, status, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, isbn, publisher, publish_date, description, 
              category, tags_str, rating, status, file_path))
        
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return book_id
    
    def get_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取书籍"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索书籍"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        search_query = f'%{query}%'
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR description LIKE ? 
                  OR category LIKE ? OR isbn LIKE ?
            ORDER BY title
            LIMIT ?
        ''', (search_query, search_query, search_query, search_query, search_query, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        columns = ['id', 'title', 'author', 'isbn', 'publisher', 'publish_date', 
                  'description', 'category', 'tags', 'rating', 'status', 'file_path', 
                  'created_at', 'updated_at']
        result = dict(zip(columns, row))
        
        if result['tags']:
            result['tags'] = json.loads(result['tags'])
        
        return result


class Tag:
    """标签模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, name: str, color: str = "#007ACC", description: str = "") -> int:
        """添加新标签"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tags (name, color, description)
                VALUES (?, ?, ?)
            ''', (name, color, description))
            
            tag_id = cursor.lastrowid
            conn.commit()
            return tag_id
        except sqlite3.IntegrityError:
            # 标签已存在
            return None
        finally:
            conn.close()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有标签"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tags ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'name', 'color', 'description', 'created_at']
        return [dict(zip(columns, row)) for row in rows]


class Category:
    """分类模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, name: str, parent_id: int = None, description: str = "") -> int:
        """添加新分类"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO categories (name, parent_id, description)
                VALUES (?, ?, ?)
            ''', (name, parent_id, description))
            
            category_id = cursor.lastrowid
            conn.commit()
            return category_id
        except sqlite3.IntegrityError:
            # 分类已存在
            return None
        finally:
            conn.close()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有分类"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'name', 'parent_id', 'description', 'created_at']
        return [dict(zip(columns, row)) for row in rows]


class Attachment:
    """附件模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, filename: str, original_name: str, file_path: str, file_size: int,
            file_type: str, mime_type: str, entity_type: str, entity_id: int) -> int:
        """添加新附件"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attachments (filename, original_name, file_path, file_size, 
                                   file_type, mime_type, entity_type, entity_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (filename, original_name, file_path, file_size, file_type, mime_type, 
              entity_type, entity_id))
        
        attachment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return attachment_id
    
    def get_by_entity(self, entity_type: str, entity_id: int) -> List[Dict[str, Any]]:
        """获取实体的所有附件"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM attachments 
            WHERE entity_type = ? AND entity_id = ?
            ORDER BY created_at
        ''', (entity_type, entity_id))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'filename', 'original_name', 'file_path', 'file_size', 
                  'file_type', 'mime_type', 'entity_type', 'entity_id', 'created_at']
        return [dict(zip(columns, row)) for row in rows]


class SearchHistory:
    """搜索历史模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, query: str, result_count: int = 0):
        """添加搜索历史"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_history (query, result_count)
            VALUES (?, ?)
        ''', (query, result_count))
        
        conn.commit()
        conn.close()
    
    def get_recent(self, limit: int = 10) -> List[str]:
        """获取最近的搜索记录"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT query FROM search_history 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]


class Settings:
    """设置模型"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get(self, key: str, default: str = "") -> str:
        """获取设置值"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else default
    
    def set(self, key: str, value: str):
        """设置值"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        
        conn.commit()
        conn.close()
