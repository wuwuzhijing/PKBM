"""
对话框模块
包含各种输入和设置对话框
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QPushButton,
    QLabel, QCheckBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt


class AddQuoteDialog(QDialog):
    """添加格言对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加格言")
        self.setModal(True)
        self.resize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("输入格言标题")
        form_layout.addRow("标题:", self.title_edit)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("输入格言内容")
        form_layout.addRow("内容:", self.content_edit)
        
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("输入作者")
        form_layout.addRow("作者:", self.author_edit)
        
        self.field_edit = QLineEdit()
        self.field_edit.setPlaceholderText("输入领域")
        form_layout.addRow("领域:", self.field_edit)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("输入标签，用逗号分隔")
        form_layout.addRow("标签:", self.tags_edit)
        
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("输入来源")
        form_layout.addRow("来源:", self.source_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        """获取输入的数据"""
        return {
            'title': self.title_edit.text().strip(),
            'content': self.content_edit.toPlainText().strip(),
            'author': self.author_edit.text().strip(),
            'field': self.field_edit.text().strip(),
            'tags': [tag.strip() for tag in self.tags_edit.text().split(',') if tag.strip()],
            'source': self.source_edit.text().strip()
        }


class AddAbbreviationDialog(QDialog):
    """添加缩写对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加科技名词缩写")
        self.setModal(True)
        self.resize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        
        self.abbr_edit = QLineEdit()
        self.abbr_edit.setPlaceholderText("输入缩写")
        form_layout.addRow("缩写:", self.abbr_edit)
        
        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText("输入全称")
        form_layout.addRow("全称:", self.full_name_edit)
        
        self.chinese_name_edit = QLineEdit()
        self.chinese_name_edit.setPlaceholderText("输入中文名称")
        form_layout.addRow("中文名称:", self.chinese_name_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("输入描述")
        form_layout.addRow("描述:", self.description_edit)
        
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("输入分类")
        form_layout.addRow("分类:", self.category_edit)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("输入标签，用逗号分隔")
        form_layout.addRow("标签:", self.tags_edit)
        
        self.examples_edit = QTextEdit()
        self.examples_edit.setPlaceholderText("输入使用示例")
        form_layout.addRow("示例:", self.examples_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        """获取输入的数据"""
        return {
            'abbreviation': self.abbr_edit.text().strip(),
            'full_name': self.full_name_edit.text().strip(),
            'chinese_name': self.chinese_name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'category': self.category_edit.text().strip(),
            'tags': [tag.strip() for tag in self.tags_edit.text().split(',') if tag.strip()],
            'examples': self.examples_edit.toPlainText().strip()
        }


class AddBookDialog(QDialog):
    """添加书籍对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加书籍")
        self.setModal(True)
        self.resize(500, 500)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("输入书籍标题")
        form_layout.addRow("标题:", self.title_edit)
        
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("输入作者")
        form_layout.addRow("作者:", self.author_edit)
        
        self.isbn_edit = QLineEdit()
        self.isbn_edit.setPlaceholderText("输入ISBN")
        form_layout.addRow("ISBN:", self.isbn_edit)
        
        self.publisher_edit = QLineEdit()
        self.publisher_edit.setPlaceholderText("输入出版社")
        form_layout.addRow("出版社:", self.publisher_edit)
        
        self.publish_date_edit = QLineEdit()
        self.publish_date_edit.setPlaceholderText("输入出版日期 (YYYY-MM-DD)")
        form_layout.addRow("出版日期:", self.publish_date_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("输入书籍简介")
        form_layout.addRow("简介:", self.description_edit)
        
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("输入分类")
        form_layout.addRow("分类:", self.category_edit)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("输入标签，用逗号分隔")
        form_layout.addRow("标签:", self.tags_edit)
        
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(0, 5)
        self.rating_spin.setValue(0)
        form_layout.addRow("评分:", self.rating_spin)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["未读", "在读", "已读"])
        form_layout.addRow("状态:", self.status_combo)
        
        layout.addLayout(form_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        """获取输入的数据"""
        return {
            'title': self.title_edit.text().strip(),
            'author': self.author_edit.text().strip(),
            'isbn': self.isbn_edit.text().strip(),
            'publisher': self.publisher_edit.text().strip(),
            'publish_date': self.publish_date_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'category': self.category_edit.text().strip(),
            'tags': [tag.strip() for tag in self.tags_edit.text().split(',') if tag.strip()],
            'rating': self.rating_spin.value(),
            'status': self.status_combo.currentText()
        }


class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setModal(True)
        self.resize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 设置选项
        self.auto_backup_check = QCheckBox("自动备份数据")
        layout.addWidget(self.auto_backup_check)
        
        self.cloud_sync_check = QCheckBox("启用云同步")
        layout.addWidget(self.cloud_sync_check)
        
        self.search_history_check = QCheckBox("保存搜索历史")
        self.search_history_check.setChecked(True)
        layout.addWidget(self.search_history_check)
        
        layout.addStretch()
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)


class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于PKBM")
        self.setModal(True)
        self.resize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("PKBM - 个人知识库管理系统")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 版本信息
        version_label = QLabel("版本: 1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # 描述
        desc_label = QLabel(
            "PKBM是一个专为个人设计的知识库管理软件，\n"
            "帮助用户高效地组织和管理各种类型的知识内容。\n\n"
            "主要功能包括：\n"
            "• 格言与方法论管理\n"
            "• 科技名词缩写管理\n"
            "• 书籍记录管理\n"
            "• 全文搜索和标签分类\n"
            "• 文件附件支持"
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # 按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setFixedWidth(100)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)

