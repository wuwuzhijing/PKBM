"""
自定义Widget组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class SearchWidget(QWidget, QAction):
    """搜索组件"""
    
    search_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 搜索标签
        search_label = QLabel("搜索:")
        search_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(search_label)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入搜索关键词...")
        self.search_input.returnPressed.connect(self._on_search)
        layout.addWidget(self.search_input)
        
        # 搜索按钮
        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self._on_search)
        layout.addWidget(search_btn)
    
    def _on_search(self):
        """搜索事件"""
        query = self.search_input.text().strip()
        if query:
            self.search_requested.emit(query)
    
    def focus_search(self):
        """聚焦到搜索框"""
        self.search_input.setFocus()
        self.search_input.selectAll()


class ContentViewer(QWidget):
    """内容查看器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题标签
        self.title_label = QLabel("内容标题")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 内容显示区域
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        layout.addWidget(self.content_text)
        
        # 元信息标签
        self.meta_label = QLabel("元信息")
        self.meta_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.meta_label)
    
    def display_content(self, data):
        """显示内容"""
        if not data:
            return
        
        # 显示标题
        title = data.get('title', '') or data.get('abbreviation', '') or '无标题'
        self.title_label.setText(title)
        
        # 显示内容
        content = data.get('content', '') or data.get('description', '') or '无内容'
        self.content_text.setPlainText(content)
        
        # 显示元信息
        meta_info = []
        if 'author' in data and data['author']:
            meta_info.append(f"作者: {data['author']}")
        if 'field' in data and data['field']:
            meta_info.append(f"领域: {data['field']}")
        if 'category' in data and data['category']:
            meta_info.append(f"分类: {data['category']}")
        if 'tags' in data and data['tags']:
            tags = data['tags'] if isinstance(data['tags'], list) else []
            if tags:
                meta_info.append(f"标签: {', '.join(tags)}")
        if 'created_at' in data and data['created_at']:
            meta_info.append(f"创建时间: {data['created_at']}")
        
        self.meta_label.setText(" | ".join(meta_info))


class TagWidget(QWidget):
    """标签组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标签列表
        self.tag_list = QListWidget()
        self.tag_list.setMaximumHeight(150)
        layout.addWidget(self.tag_list)
    
    def load_tags(self, tags):
        """加载标签"""
        self.tag_list.clear()
        for tag in tags:
            item = QListWidgetItem(tag['name'])
            item.setData(Qt.ItemDataRole.UserRole, tag)
            self.tag_list.addItem(item)


class CategoryWidget(QWidget):
    """分类组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 分类列表
        self.category_list = QListWidget()
        self.category_list.setMaximumHeight(150)
        layout.addWidget(self.category_list)
    
    def load_categories(self, categories):
        """加载分类"""
        self.category_list.clear()
        for category in categories:
            item = QListWidgetItem(category['name'])
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.category_list.addItem(item)


class AttachmentWidget(QWidget):
    """附件组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 附件标题
        attachment_label = QLabel("附件")
        attachment_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(attachment_label)
        
        # 附件列表
        self.attachment_list = QListWidget()
        self.attachment_list.setMaximumHeight(100)
        layout.addWidget(self.attachment_list)
        
        # 添加附件按钮
        add_btn = QPushButton("添加附件")
        add_btn.clicked.connect(self._add_attachment)
        layout.addWidget(add_btn)
    
    def _add_attachment(self):
        """添加附件"""
        # 这里可以实现文件选择逻辑
        pass
    
    def load_attachments(self, attachments):
        """加载附件列表"""
        self.attachment_list.clear()
        for attachment in attachments:
            item = QListWidgetItem(attachment['original_name'])
            item.setData(Qt.ItemDataRole.UserRole, attachment)
            self.attachment_list.addItem(item)

