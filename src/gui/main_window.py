"""
主窗口GUI界面
PKBM系统的主界面
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QTreeWidget, QListWidget, QTextEdit, QLineEdit, 
    QPushButton, QLabel, QStatusBar, QMenuBar, QToolBar, 
    QMessageBox, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QKeySequence, QAction

# 使用绝对导入
from src.database.models import DatabaseManager
from src.utils.search_utils import SearchEngine


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = None
        self.search_engine = None
        self.init_ui()
        self.init_database()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("PKBM - 个人知识库管理系统")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧导航面板
        self.create_navigation_panel(splitter)
        
        # 右侧内容区域
        self.create_content_area(splitter)
        
        # 设置分割器比例
        splitter.setSizes([300, 1100])
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
    
    def create_navigation_panel(self, parent):
        """创建左侧导航面板"""
        nav_frame = QFrame()
        nav_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        nav_layout = QVBoxLayout(nav_frame)
        
        # 搜索框
        search_label = QLabel("搜索:")
        nav_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入搜索关键词...")
        nav_layout.addWidget(self.search_input)
        
        # 内容类型树
        content_tree_label = QLabel("内容类型")
        content_tree_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        nav_layout.addWidget(content_tree_label)
        
        self.content_tree = QTreeWidget()
        self.content_tree.setHeaderHidden(True)
        self.content_tree.setMaximumHeight(200)
        nav_layout.addWidget(self.content_tree)
        
        # 标签面板
        tag_label = QLabel("标签")
        tag_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        nav_layout.addWidget(tag_label)
        
        self.tag_list = QListWidget()
        self.tag_list.setMaximumHeight(150)
        nav_layout.addWidget(self.tag_list)
        
        # 分类面板
        category_label = QLabel("分类")
        category_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        nav_layout.addWidget(category_label)
        
        self.category_list = QListWidget()
        self.category_list.setMaximumHeight(150)
        nav_layout.addWidget(self.category_list)
        
        parent.addWidget(nav_frame)
    
    def create_content_area(self, parent):
        """创建右侧内容区域"""
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        content_layout = QVBoxLayout(content_frame)
        
        # 内容标签页
        self.content_tabs = QTabWidget()
        content_layout.addWidget(self.content_tabs)
        
        # 格言与方法论标签页
        self.create_quotes_tab()
        
        # 科技名词缩写标签页
        self.create_abbreviations_tab()
        
        # 书籍记录标签页
        self.create_books_tab()
        
        # 搜索结果标签页
        self.create_search_results_tab()
        
        parent.addWidget(content_frame)
    
    def create_quotes_tab(self):
        """创建格言与方法论标签页"""
        quotes_widget = QWidget()
        quotes_layout = QVBoxLayout(quotes_widget)
        
        # 工具栏
        quotes_toolbar = QHBoxLayout()
        
        add_quote_btn = QPushButton("添加格言")
        add_quote_btn.clicked.connect(self.add_quote)
        quotes_toolbar.addWidget(add_quote_btn)
        
        quotes_toolbar.addStretch()
        
        # 搜索过滤
        filter_label = QLabel("过滤:")
        quotes_toolbar.addWidget(filter_label)
        
        self.quote_category_filter = QComboBox()
        self.quote_category_filter.addItem("所有分类")
        quotes_toolbar.addWidget(self.quote_category_filter)
        
        quotes_layout.addLayout(quotes_toolbar)
        
        # 内容列表
        self.quotes_list = QListWidget()
        quotes_layout.addWidget(self.quotes_list)
        
        # 内容查看器
        self.quotes_viewer = QTextEdit()
        self.quotes_viewer.setReadOnly(True)
        quotes_layout.addWidget(self.quotes_viewer)
        
        self.content_tabs.addTab(quotes_widget, "格言与方法论")
    
    def create_abbreviations_tab(self):
        """创建科技名词缩写标签页"""
        abbr_widget = QWidget()
        abbr_layout = QVBoxLayout(abbr_widget)
        
        # 工具栏
        abbr_toolbar = QHBoxLayout()
        
        add_abbr_btn = QPushButton("添加缩写")
        add_abbr_btn.clicked.connect(self.add_abbreviation)
        abbr_toolbar.addWidget(add_abbr_btn)
        
        abbr_toolbar.addStretch()
        
        # 搜索过滤
        filter_label = QLabel("过滤:")
        abbr_toolbar.addWidget(filter_label)
        
        self.abbr_category_filter = QComboBox()
        self.abbr_category_filter.addItem("所有分类")
        abbr_toolbar.addWidget(self.abbr_category_filter)
        
        abbr_layout.addLayout(abbr_toolbar)
        
        # 内容列表
        self.abbr_list = QListWidget()
        abbr_layout.addWidget(self.abbr_list)
        
        # 内容查看器
        self.abbr_viewer = QTextEdit()
        self.abbr_viewer.setReadOnly(True)
        abbr_layout.addWidget(self.abbr_viewer)
        
        self.content_tabs.addTab(abbr_widget, "科技名词缩写")
    
    def create_books_tab(self):
        """创建书籍记录标签页"""
        books_widget = QWidget()
        books_layout = QVBoxLayout(books_widget)
        
        # 工具栏
        books_toolbar = QHBoxLayout()
        
        add_book_btn = QPushButton("添加书籍")
        add_book_btn.clicked.connect(self.add_book)
        books_toolbar.addWidget(add_book_btn)
        
        books_toolbar.addStretch()
        
        # 搜索过滤
        filter_label = QLabel("过滤:")
        books_toolbar.addWidget(filter_label)
        
        self.book_status_filter = QComboBox()
        self.book_status_filter.addItems(["所有状态", "未读", "在读", "已读"])
        books_toolbar.addWidget(self.book_status_filter)
        
        books_layout.addLayout(books_toolbar)
        
        # 内容列表
        self.books_list = QListWidget()
        books_layout.addWidget(self.books_list)
        
        # 内容查看器
        self.books_viewer = QTextEdit()
        self.books_viewer.setReadOnly(True)
        books_layout.addWidget(self.books_viewer)
        
        self.content_tabs.addTab(books_widget, "书籍记录")
    
    def create_search_results_tab(self):
        """创建搜索结果标签页"""
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        
        # 搜索结果统计
        self.search_stats_label = QLabel("搜索结果: 0 项")
        search_layout.addWidget(self.search_stats_label)
        
        # 搜索结果列表
        self.search_results_list = QListWidget()
        search_layout.addWidget(self.search_results_list)
        
        # 内容查看器
        self.search_viewer = QTextEdit()
        self.search_viewer.setReadOnly(True)
        search_layout.addWidget(self.search_viewer)
        
        self.content_tabs.addTab(search_widget, "搜索结果")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        import_action = QAction("导入数据", self)
        import_action.setShortcut(QKeySequence.StandardKey.Open)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        export_action = QAction("导出数据", self)
        export_action.setShortcut(QKeySequence.StandardKey.Save)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        
        backup_action = QAction("备份数据", self)
        backup_action.triggered.connect(self.backup_data)
        tools_menu.addAction(backup_action)
        
        restore_action = QAction("恢复数据", self)
        restore_action.triggered.connect(self.restore_data)
        tools_menu.addAction(restore_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("主工具栏")
        
        # 添加格言
        add_quote_action = QAction("添加格言", self)
        add_quote_action.triggered.connect(self.add_quote)
        toolbar.addAction(add_quote_action)
        
        # 添加缩写
        add_abbr_action = QAction("添加缩写", self)
        add_abbr_action.triggered.connect(self.add_abbreviation)
        toolbar.addAction(add_abbr_action)
        
        # 添加书籍
        add_book_action = QAction("添加书籍", self)
        add_book_action.triggered.connect(self.add_book)
        toolbar.addAction(add_book_action)
        
        toolbar.addSeparator()
        
        # 搜索
        search_action = QAction("搜索", self)
        search_action.setShortcut(QKeySequence.StandardKey.Find)
        search_action.triggered.connect(self.focus_search)
        toolbar.addAction(search_action)
    
    def init_database(self):
        """初始化数据库"""
        try:
            self.db_manager = DatabaseManager()
            self.search_engine = SearchEngine(self.db_manager)
            self.statusBar().showMessage("数据库初始化成功")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"数据库初始化失败: {str(e)}")
            self.statusBar().showMessage("数据库初始化失败")
    
    def setup_connections(self):
        """设置信号连接"""
        # 搜索框连接
        self.search_input.returnPressed.connect(self.perform_search)
        
        # 内容列表选择连接
        self.quotes_list.itemSelectionChanged.connect(self.on_quote_selected)
        self.abbr_list.itemSelectionChanged.connect(self.on_abbreviation_selected)
        self.books_list.itemSelectionChanged.connect(self.on_book_selected)
        self.search_results_list.itemSelectionChanged.connect(self.on_search_result_selected)
    
    def perform_search(self):
        """执行搜索"""
        query = self.search_input.text().strip()
        if not query:
            return
        
        self.statusBar().showMessage(f"搜索: {query}")
    
    def add_quote(self):
        """添加格言"""
        QMessageBox.information(self, "信息", "添加格言功能将在后续版本中实现")
    
    def add_abbreviation(self):
        """添加缩写"""
        QMessageBox.information(self, "信息", "添加缩写功能将在后续版本中实现")
    
    def add_book(self):
        """添加书籍"""
        QMessageBox.information(self, "信息", "添加书籍功能将在后续版本中实现")
    
    def on_quote_selected(self):
        """格言选择事件"""
        current_item = self.quotes_list.currentItem()
        if current_item:
            self.quotes_viewer.setText(f"选中: {current_item.text()}")
    
    def on_abbreviation_selected(self):
        """缩写选择事件"""
        current_item = self.abbr_list.currentItem()
        if current_item:
            self.abbr_viewer.setText(f"选中: {current_item.text()}")
    
    def on_book_selected(self):
        """书籍选择事件"""
        current_item = self.books_list.currentItem()
        if current_item:
            self.books_viewer.setText(f"选中: {current_item.text()}")
    
    def on_search_result_selected(self):
        """搜索结果选择事件"""
        current_item = self.search_results_list.currentItem()
        if current_item:
            self.search_viewer.setText(f"选中: {current_item.text()}")
    
    def focus_search(self):
        """聚焦到搜索框"""
        self.search_input.setFocus()
    
    def import_data(self):
        """导入数据"""
        QMessageBox.information(self, "信息", "导入功能将在后续版本中实现")
    
    def export_data(self):
        """导出数据"""
        QMessageBox.information(self, "信息", "导出功能将在后续版本中实现")
    
    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "信息", "设置功能将在后续版本中实现")
    
    def backup_data(self):
        """备份数据"""
        QMessageBox.information(self, "信息", "备份功能将在后续版本中实现")
    
    def restore_data(self):
        """恢复数据"""
        QMessageBox.information(self, "信息", "恢复功能将在后续版本中实现")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.information(self, "关于PKBM", 
                              "PKBM - 个人知识库管理系统\n版本: 1.0\n\n一个帮助个人管理知识的工具")
    
    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出PKBM吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
