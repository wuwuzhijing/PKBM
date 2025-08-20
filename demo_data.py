#!/usr/bin/env python3
"""
PKBM演示数据脚本
创建一些示例数据用于测试和演示
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_demo_data():
    """创建演示数据"""
    print("正在创建演示数据...")
    
    try:
        from src.database.models import DatabaseManager, QuoteMethod, TechAbbreviation, Book, Tag, Category
        
        # 初始化数据库
        db_manager = DatabaseManager()
        
        # 创建标签
        tag_model = Tag(db_manager)
        demo_tags = ["重要", "参考", "学习", "工作", "生活", "技术", "管理", "创新"]
        
        created_tags = []
        for tag_name in demo_tags:
            tag_id = tag_model.add(tag_name, "#007ACC", f"演示标签: {tag_name}")
            if tag_id:
                created_tags.append(tag_name)
        
        print(f"创建了 {len(created_tags)} 个标签")
        
        # 创建分类
        category_model = Category(db_manager)
        demo_categories = ["格言警句", "方法论", "技术文档", "学习笔记", "工作记录", "生活感悟", "书籍摘要", "其他"]
        
        created_categories = []
        for cat_name in demo_categories:
            cat_id = category_model.add(cat_name, None, f"演示分类: {cat_name}")
            if cat_id:
                created_categories.append(cat_name)
        
        print(f"创建了 {len(created_categories)} 个分类")
        
        # 创建格言示例
        quote_model = QuoteMethod(db_manager)
        demo_quotes = [
            {
                "title": "知行合一",
                "content": "知是行之始，行是知之成。知而不行，只是未知。",
                "author": "王阳明",
                "field": "哲学",
                "tags": ["重要", "哲学", "学习"],
                "source": "《传习录》"
            },
            {
                "title": "学习之道",
                "content": "学而时习之，不亦说乎？",
                "author": "孔子",
                "field": "教育",
                "tags": ["学习", "教育", "重要"],
                "source": "《论语》"
            }
        ]
        
        created_quotes = 0
        for quote_data in demo_quotes:
            quote_id = quote_model.add(**quote_data)
            if quote_id:
                created_quotes += 1
        
        print(f"创建了 {created_quotes} 条格言")
        
        # 创建科技名词缩写示例
        abbr_model = TechAbbreviation(db_manager)
        demo_abbreviations = [
            {
                "abbreviation": "AI",
                "full_name": "Artificial Intelligence",
                "chinese_name": "人工智能",
                "description": "计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
                "category": "计算机科学",
                "tags": ["技术", "计算机科学"],
                "examples": "机器学习、自然语言处理、计算机视觉等"
            },
            {
                "abbreviation": "API",
                "full_name": "Application Programming Interface",
                "chinese_name": "应用程序编程接口",
                "description": "一组定义软件组件如何相互交互的规则和协议。",
                "category": "软件开发",
                "tags": ["技术", "软件开发"],
                "examples": "REST API、GraphQL、Web API等"
            }
        ]
        
        created_abbreviations = 0
        for abbr_data in demo_abbreviations:
            abbr_id = abbr_model.add(**abbr_data)
            if abbr_id:
                created_abbreviations += 1
        
        print(f"创建了 {created_abbreviations} 个科技名词缩写")
        
        # 创建书籍示例
        book_model = Book(db_manager)
        demo_books = [
            {
                "title": "原子习惯",
                "author": "詹姆斯·克利尔",
                "description": "本书介绍了如何通过微小的改变来创造显著的结果，是一本关于习惯养成的实用指南。",
                "category": "个人发展",
                "tags": ["个人发展", "习惯", "重要"],
                "rating": 5,
                "status": "已读"
            }
        ]
        
        created_books = 0
        for book_data in demo_books:
            book_id = book_model.add(**book_data)
            if book_id:
                created_books += 1
        
        print(f"创建了 {created_books} 本书籍记录")
        
        print("\n演示数据创建完成！")
        print(f"总计创建:")
        print(f"  - 标签: {len(created_tags)} 个")
        print(f"  - 分类: {len(created_categories)} 个")
        print(f"  - 格言: {created_quotes} 条")
        print(f"  - 缩写: {created_abbreviations} 个")
        print(f"  - 书籍: {created_books} 本")
        print("\n现在可以启动PKBM程序查看这些示例数据了！")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包")
    except Exception as e:
        print(f"创建演示数据失败: {e}")


def clear_demo_data():
    """清除演示数据"""
    print("正在清除演示数据...")
    
    # 删除数据库文件
    db_path = Path("data/pkbm.db")
    if db_path.exists():
        db_path.unlink()
        print("数据库文件已删除")
    
    print("演示数据清除完成")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_demo_data()
    else:
        create_demo_data()
