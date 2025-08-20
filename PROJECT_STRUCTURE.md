# PKBM项目结构说明

## 目录结构

```
PKBM/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包列表
├── main.py                     # 主程序入口
├── run.py                      # 启动脚本（带依赖检查）
├── install.py                  # 安装脚本
├── config.py                   # 配置文件
├── start.bat                   # Windows启动脚本
├── start.sh                    # Linux启动脚本
├── PROJECT_STRUCTURE.md        # 项目结构说明（本文件）
│
├── src/                        # 源代码目录
│   ├── __init__.py            # 包初始化文件
│   │
│   ├── core/                  # 核心功能模块
│   │   └── __init__.py        # 核心模块初始化
│   │
│   ├── database/              # 数据库模块
│   │   ├── __init__.py        # 数据库模块初始化
│   │   └── models.py          # 数据库模型定义
│   │
│   ├── gui/                   # 图形界面模块
│   │   ├── __init__.py        # GUI模块初始化
│   │   ├── main_window.py     # 主窗口
│   │   ├── dialogs.py         # 对话框
│   │   └── widgets.py         # 自定义组件
│   │
│   └── utils/                 # 工具模块
│       ├── __init__.py        # 工具模块初始化
│       ├── file_utils.py      # 文件处理工具
│       └── search_utils.py    # 搜索工具
│
├── data/                       # 数据存储目录
│   ├── attachments/           # 附件文件
│   └── backups/               # 备份文件
│
├── docs/                       # 文档目录
│   └── README.md              # 详细使用说明
│
├── tests/                      # 测试代码目录
│   └── test_basic.py          # 基本功能测试
│
├── resources/                  # 资源文件目录
│   └── icons/                 # 图标文件
│
└── logs/                       # 日志文件目录
```

## 文件说明

### 核心文件

- **main.py**: 主程序入口，创建Qt应用和主窗口
- **run.py**: 启动脚本，包含依赖检查和错误处理
- **install.py**: 安装脚本，自动安装依赖和创建快捷方式
- **config.py**: 配置文件，包含所有系统配置项

### 启动脚本

- **start.bat**: Windows批处理启动脚本
- **start.sh**: Linux Shell启动脚本

### 源代码模块

#### 数据库模块 (src/database/)
- **models.py**: 定义所有数据表结构和操作类
  - `DatabaseManager`: 数据库管理器
  - `QuoteMethod`: 格言与方法论模型
  - `TechAbbreviation`: 科技名词缩写模型
  - `Book`: 书籍记录模型
  - `Tag`: 标签模型
  - `Category`: 分类模型
  - `Attachment`: 附件模型
  - `SearchHistory`: 搜索历史模型
  - `Settings`: 设置模型

#### 图形界面模块 (src/gui/)
- **main_window.py**: 主窗口类，包含整个应用界面
- **dialogs.py**: 各种对话框类
  - `AddQuoteDialog`: 添加格言对话框
  - `AddAbbreviationDialog`: 添加缩写对话框
  - `AddBookDialog`: 添加书籍对话框
  - `SettingsDialog`: 设置对话框
  - `AboutDialog`: 关于对话框
- **widgets.py**: 自定义组件
  - `SearchWidget`: 搜索组件
  - `ContentViewer`: 内容查看器
  - `TagWidget`: 标签组件
  - `CategoryWidget`: 分类组件
  - `AttachmentWidget`: 附件组件

#### 工具模块 (src/utils/)
- **file_utils.py**: 文件处理工具
  - `FileManager`: 文件管理器
  - `DocumentProcessor`: 文档处理器
  - `ImageProcessor`: 图片处理器
- **search_utils.py**: 搜索工具
  - `SearchEngine`: 搜索引擎
  - `SearchIndexer`: 搜索索引器
  - `SearchAnalytics`: 搜索分析

### 数据目录

- **data/**: 存储所有应用数据
  - **attachments/**: 存储文件附件
  - **backups/**: 存储数据备份

### 测试和文档

- **tests/**: 包含单元测试代码
- **docs/**: 包含详细的使用文档
- **logs/**: 存储应用运行日志

## 模块依赖关系

```
main.py
├── src/gui/main_window.py
│   ├── src/database/models.py
│   ├── src/utils/search_utils.py
│   └── src/gui/dialogs.py
│       └── src/gui/widgets.py
└── src/utils/file_utils.py
```

## 技术架构

### 前端
- **PyQt6**: 现代化的Qt6 Python绑定
- **响应式设计**: 支持不同屏幕分辨率
- **模块化界面**: 可扩展的组件系统

### 后端
- **SQLite**: 轻量级本地数据库
- **ORM模式**: 对象关系映射
- **文件系统**: 本地文件存储

### 核心功能
- **数据管理**: CRUD操作
- **搜索系统**: 全文检索和过滤
- **文件处理**: 多格式文件支持
- **标签分类**: 灵活的内容组织

## 扩展性设计

### 预留接口
- 云同步功能
- 插件系统
- 多人协作
- 移动端支持

### 配置化
- 可配置的界面主题
- 可调整的搜索参数
- 可自定义的文件格式支持

## 部署说明

### 开发环境
1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 运行程序: `python main.py`

### 生产环境
1. 运行安装脚本: `python install.py`
2. 使用启动脚本: `./start.sh` 或 `start.bat`

### 打包发布
- 支持PyInstaller打包
- 支持Docker容器化
- 支持多平台部署

