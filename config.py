"""
PKBM配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
ATTACHMENTS_DIR = DATA_DIR / "attachments"
DATABASE_PATH = DATA_DIR / "pkbm.db"

# 日志目录
LOG_DIR = PROJECT_ROOT / "logs"

# 资源目录
RESOURCES_DIR = PROJECT_ROOT / "resources"

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [DATA_DIR, ATTACHMENTS_DIR, LOG_DIR, RESOURCES_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# 应用配置
APP_CONFIG = {
    'name': 'PKBM',
    'version': '1.0.0',
    'description': '个人知识库管理系统',
    'author': 'PKBM Team',
    'window_title': 'PKBM - 个人知识库管理系统',
    'window_size': (1400, 900),
    'window_position': (100, 100)
}

# 数据库配置
DATABASE_CONFIG = {
    'type': 'sqlite',
    'path': str(DATABASE_PATH),
    'backup_enabled': True,
    'backup_interval': 24 * 60 * 60,  # 24小时
    'max_backup_count': 10
}

# 搜索配置
SEARCH_CONFIG = {
    'max_results': 100,
    'search_history_limit': 50,
    'highlight_enabled': True,
    'fuzzy_search_enabled': True
}

# 文件配置
FILE_CONFIG = {
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'supported_formats': [
        # 图片格式
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
        # 文档格式
        '.pdf', '.doc', '.docx', '.txt', '.rtf',
        # 表格格式
        '.xls', '.xlsx', '.csv',
        # 演示文稿
        '.ppt', '.pptx',
        # 压缩格式
        '.zip', '.rar', '.7z',
        # 其他
        '.md', '.html', '.htm'
    ],
    'thumbnail_size': (200, 200)
}

# 界面配置
UI_CONFIG = {
    'theme': 'default',
    'language': 'zh_CN',
    'font_family': 'Microsoft YaHei',
    'font_size': 9,
    'icon_theme': 'default'
}

# 同步配置（预留）
SYNC_CONFIG = {
    'enabled': False,
    'type': 'local',  # local, cloud
    'cloud_provider': None,
    'sync_interval': 60 * 60,  # 1小时
    'auto_sync': False
}

# 网络配置
NETWORK_CONFIG = {
    'enabled': False,
    'host': '127.0.0.1',
    'port': 8080,
    'debug': False,
    'allow_external_access': False
}

# 备份配置
BACKUP_CONFIG = {
    'enabled': True,
    'auto_backup': True,
    'backup_interval': 24 * 60 * 60,  # 24小时
    'backup_location': str(DATA_DIR / "backups"),
    'max_backup_count': 10,
    'include_attachments': True
}

# 日志配置
LOG_CONFIG = {
    'enabled': True,
    'level': 'INFO',
    'file': str(LOG_DIR / "pkbm.log"),
    'max_size': 10 * 1024 * 1024,  # 10MB
    'max_files': 5,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# 默认标签和分类
DEFAULT_TAGS = [
    '重要', '参考', '学习', '工作', '生活', '技术', '管理', '创新'
]

DEFAULT_CATEGORIES = [
    '格言警句',
    '方法论',
    '技术文档',
    '学习笔记',
    '工作记录',
    '生活感悟',
    '书籍摘要',
    '其他'
]

# 初始化配置
def init_config():
    """初始化配置"""
    ensure_directories()
    
    # 创建默认配置文件
    config_file = PROJECT_ROOT / "config.ini"
    if not config_file.exists():
        create_default_config(config_file)

def create_default_config(config_file):
    """创建默认配置文件"""
    config_content = """[APP]
name = PKBM
version = 1.0.0
description = 个人知识库管理系统

[DATABASE]
type = sqlite
path = data/pkbm.db
backup_enabled = true
backup_interval = 86400

[SEARCH]
max_results = 100
search_history_limit = 50
highlight_enabled = true

[UI]
theme = default
language = zh_CN
font_family = Microsoft YaHei
font_size = 9

[BACKUP]
enabled = true
auto_backup = true
backup_interval = 86400
max_backup_count = 10
"""
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)

# 获取配置值
def get_config(section, key, default=None):
    """获取配置值"""
    try:
        import configparser
        config = configparser.ConfigParser()
        config_file = PROJECT_ROOT / "config.ini"
        
        if config_file.exists():
            config.read(config_file, encoding='utf-8')
            return config.get(section, key)
    except:
        pass
    
    return default

# 设置配置值
def set_config(section, key, value):
    """设置配置值"""
    try:
        import configparser
        config = configparser.ConfigParser()
        config_file = PROJECT_ROOT / "config.ini"
        
        if config_file.exists():
            config.read(config_file, encoding='utf-8')
        
        if section not in config:
            config.add_section(section)
        
        config.set(section, key, str(value))
        
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        
        return True
    except:
        return False

