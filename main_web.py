#!/usr/bin/env python3
"""
PKBM - Web版本
基于Flask的个人知识库管理系统
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pkbm-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/pkbm_web.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 确保必要的目录存在
Path("data").mkdir(exist_ok=True)
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# 初始化数据库
db = SQLAlchemy(app)

# 数据模型
class KnowledgeItem(db.Model):
    __tablename__ = 'knowledge_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

# 路由定义
@app.route('/')
def index():
    """主页"""
    # 获取统计信息
    total_items = KnowledgeItem.query.count()
    total_categories = Category.query.count()
    
    # 获取最新条目
    recent_items = KnowledgeItem.query.order_by(KnowledgeItem.updated_date.desc()).limit(5).all()
    
    # 获取分类统计
    categories = db.session.query(
        Category.name,
        db.func.count(KnowledgeItem.id).label('count')
    ).outerjoin(KnowledgeItem, Category.name == KnowledgeItem.category)\
     .group_by(Category.name).all()
    
    return render_template('index.html', 
                         total_items=total_items,
                         total_categories=total_categories,
                         recent_items=recent_items,
                         categories=categories)

@app.route('/items')
def list_items():
    """列出所有条目"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 搜索功能
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    query = KnowledgeItem.query
    
    if search:
        query = query.filter(
            db.or_(
                KnowledgeItem.title.contains(search),
                KnowledgeItem.content.contains(search),
                KnowledgeItem.tags.contains(search)
            )
        )
    
    if category_filter:
        query = query.filter(KnowledgeItem.category == category_filter)
    
    items = query.order_by(KnowledgeItem.updated_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('items.html', 
                         items=items,
                         categories=categories,
                         search=search,
                         category_filter=category_filter)

@app.route('/item/new', methods=['GET', 'POST'])
def new_item():
    """新建条目"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '其他')
        tags = request.form.get('tags', '').strip()
        
        if not title:
            flash('标题不能为空', 'error')
            return redirect(url_for('new_item'))
        
        # 处理文件上传
        file_path = None
        file_type = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_type = os.path.splitext(filename)[1]
        
        # 创建新条目
        item = KnowledgeItem(
            title=title,
            content=content,
            category=category,
            tags=tags,
            file_path=file_path,
            file_type=file_type
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash(f'条目 "{title}" 创建成功！', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    
    categories = Category.query.all()
    return render_template('item_form.html', 
                         item=None,
                         categories=categories,
                         action='new')

@app.route('/item/<int:item_id>')
def view_item(item_id):
    """查看条目"""
    item = KnowledgeItem.query.get_or_404(item_id)
    return render_template('item_view.html', item=item)

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    """编辑条目"""
    item = KnowledgeItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.title = request.form.get('title', '').strip()
        item.content = request.form.get('content', '').strip()
        item.category = request.form.get('category', '其他')
        item.tags = request.form.get('tags', '').strip()
        item.updated_date = datetime.utcnow()
        
        if not item.title:
            flash('标题不能为空', 'error')
            return redirect(url_for('edit_item', item_id=item_id))
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                item.file_path = file_path
                item.file_type = os.path.splitext(filename)[1]
        
        db.session.commit()
        flash(f'条目 "{item.title}" 更新成功！', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    
    categories = Category.query.all()
    return render_template('item_form.html', 
                         item=item,
                         categories=categories,
                         action='edit')

@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """删除条目"""
    item = KnowledgeItem.query.get_or_404(item_id)
    title = item.title
    
    # 删除关联的文件
    if item.file_path and os.path.exists(item.file_path):
        os.remove(item.file_path)
    
    db.session.delete(item)
    db.session.commit()
    
    flash(f'条目 "{title}" 删除成功！', 'success')
    return redirect(url_for('list_items'))

@app.route('/categories')
def list_categories():
    """列出所有分类"""
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/category/new', methods=['GET', 'POST'])
def new_category():
    """新建分类"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('分类名不能为空', 'error')
            return redirect(url_for('new_category'))
        
        # 检查是否已存在
        if Category.query.filter_by(name=name).first():
            flash(f'分类 "{name}" 已存在', 'error')
            return redirect(url_for('new_category'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'分类 "{name}" 创建成功！', 'success')
        return redirect(url_for('list_categories'))
    
    return render_template('category_form.html', category=None)

@app.route('/search')
def search():
    """搜索功能"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('list_items'))
    
    items = KnowledgeItem.query.filter(
        db.or_(
            KnowledgeItem.title.contains(query),
            KnowledgeItem.content.contains(query),
            KnowledgeItem.tags.contains(query)
        )
    ).order_by(KnowledgeItem.updated_date.desc()).all()
    
    return render_template('search_results.html', 
                         items=items,
                         query=query)

@app.route('/api/items')
def api_items():
    """API: 获取条目列表"""
    items = KnowledgeItem.query.order_by(KnowledgeItem.updated_date.desc()).all()
    return jsonify([{
        'id': item.id,
        'title': item.title,
        'category': item.category,
        'tags': item.tags,
        'created_date': item.created_date.isoformat(),
        'updated_date': item.updated_date.isoformat()
    } for item in items])

@app.route('/api/categories')
def api_categories():
    """API: 获取分类列表"""
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@app.route('/import', methods=['GET', 'POST'])
def import_file():
    """导入文件"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(url_for('import_file'))
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(url_for('import_file'))
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 提取文件名作为标题
            title = os.path.splitext(filename)[0]
            
            # 创建条目
            item = KnowledgeItem(
                title=title,
                content=f'导入的文件: {filename}',
                category='其他',
                file_path=file_path,
                file_type=os.path.splitext(filename)[1]
            )
            
            db.session.add(item)
            db.session.commit()
            
            flash(f'文件 "{filename}" 导入成功！', 'success')
            return redirect(url_for('view_item', item_id=item.id))
    
    return render_template('import.html')

@app.route('/download/<int:item_id>')
def download_file(item_id):
    """下载文件"""
    item = KnowledgeItem.query.get_or_404(item_id)
    
    if not item.file_path or not os.path.exists(item.file_path):
        flash('文件不存在', 'error')
        return redirect(url_for('view_item', item_id=item_id))
    
    return send_file(item.file_path, as_attachment=True)

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
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
            if not Category.query.filter_by(name=name).first():
                category = Category(name=name, description=desc)
                db.session.add(category)
        
        db.session.commit()
        print("✓ 数据库初始化完成")

def main():
    """主函数"""
    # 获取配置
    host = os.environ.get('PKBM_HOST', '127.0.0.1')
    port = int(os.environ.get('PKBM_PORT', 8080))
    debug = os.environ.get('PKBM_DEBUG', 'false').lower() == 'true'
    
    print(f"PKBM Web版本启动中...")
    print(f"访问地址: http://{host}:{port}")
    print(f"调试模式: {debug}")
    
    # 初始化数据库
    init_database()
    
    # 启动Flask应用
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
