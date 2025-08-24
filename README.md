# PKBM - 个人知识库管理系统

## 项目概述

PKBM是一个现代化的个人知识库管理系统，支持多平台部署和跨平台使用。系统采用前后端分离架构，后端使用Go语言提供高性能API服务，前端使用Python tkinter构建跨平台GUI界面。

## 技术架构

### 后端 (Go)
- **语言**: Go 1.21+
- **数据库**: SQLite3
- **API**: RESTful API
- **特性**: 高性能、跨平台、静态编译

### 前端 (Python)
- **语言**: Python 3.8+
- **GUI框架**: tkinter (跨平台兼容)
- **数据库**: SQLite3
- **特性**: 原生界面、跨平台、易于打包

## 功能特性

### 核心功能 (0-8)
1. **查看所有条目** - 浏览所有知识条目
2. **添加新条目** - 创建新的知识条目
3. **搜索条目** - 全文搜索功能
4. **编辑条目** - 修改现有条目
5. **删除条目** - 删除不需要的条目
6. **查看分类** - 管理知识分类
7. **导入文件** - 批量导入文件
8. **数据库状态** - 查看系统状态

### 扩展功能
- **分类管理** - 自定义知识分类
- **标签系统** - 灵活的标签管理
- **文件附件** - 支持多种文件格式
- **搜索高亮** - 智能搜索结果
- **数据导出** - 支持多种导出格式
- **备份恢复** - 数据安全保护
- **图片管理** - 支持图片附件和书籍封面
- **书籍信息** - 专门的书籍元数据管理
- **后端管理** - 启动/停止/监控后端服务
- **数据同步** - 前后端数据自动同步

## 平台支持

### Windows
- **运行**: 直接运行Python脚本
- **打包**: 使用PyInstaller生成exe文件
- **安装**: 双击exe文件即可使用

### Ubuntu/Linux
- **运行**: 直接运行Python脚本
- **打包**: 使用python-stdeb生成deb包
- **安装**: `sudo dpkg -i pkbm.deb`

### 未来支持
- **iOS**: Flutter应用
- **Android**: Flutter应用
- **Web**: 浏览器访问

## 快速开始

> 📚 **查看完整版本历史**: [VERSION_HISTORY.md](VERSION_HISTORY.md)

### 1. 环境要求
- Python 3.8+
- Go 1.21+ (仅后端)
- SQLite3

### 2. 安装依赖

#### Windows
```bash
cd windows_gui
pip install -r requirements.txt
```

#### Ubuntu
```bash
cd ubuntu_gui
pip3 install -r requirements.txt
```

### 3. 运行程序

#### 直接运行
```bash
python3 main.py
```

#### 启动后端服务 (可选)
```bash
cd backend
go run main.go
```

#### 使用GUI管理后端 (Windows)
```bash
cd windows_gui
python3 main.py
# 在GUI中点击"启动后端"按钮
```

### 4. 构建发布版本

#### Windows (生成exe)
```bash
cd windows_gui
python3 build_exe.py
```

#### Ubuntu (生成deb包)
```bash
cd ubuntu_gui
python3 build_deb.py
```

## 项目结构

```
PKBM/
├── backend/                 # Go后端
│   ├── main.go             # 主程序
│   └── go.mod              # Go模块文件
├── windows_gui/            # Windows版本
│   ├── main.py             # 主程序
│   ├── requirements.txt    # 依赖文件
│   └── build_exe.py       # 打包脚本
├── ubuntu_gui/             # Ubuntu版本
│   ├── main.py             # 主程序
│   ├── requirements.txt    # 依赖文件
│   └── build_deb.py       # 打包脚本
├── data/                   # 数据目录
│   └── pkbm.db            # SQLite数据库
├── resources/              # 资源文件
├── start.sh                # Linux启动脚本
├── start.bat               # Windows启动脚本
└── README.md               # 项目说明
```

## 数据迁移

### 从旧版本迁移
1. 备份原有数据库文件
2. 将数据库文件复制到新版本的`data/`目录
3. 启动新版本程序，系统会自动识别并加载数据

### 数据库格式
- 使用SQLite3数据库
- 支持标准SQL操作
- 兼容现有数据格式

## 开发指南

### 添加新功能
1. 在`main.py`中添加新的方法
2. 在界面中添加对应的按钮或菜单
3. 更新数据库结构（如需要）
4. 测试功能完整性

### 自定义界面
- 修改`create_widgets()`方法
- 调整布局和样式
- 添加新的控件和事件处理

### 扩展API
- 在Go后端添加新的路由
- 实现对应的处理函数
- 更新前端调用代码

## 故障排除

### 常见问题

#### 1. 数据库连接失败
- 检查`data/`目录是否存在
- 确认SQLite3已安装
- 检查文件权限

#### 2. GUI显示异常
- 确认tkinter已安装
- 检查Python版本兼容性
- 尝试重新安装依赖

#### 3. 打包失败
- 检查依赖是否完整
- 确认打包工具版本
- 查看错误日志

### 调试模式
```bash
# 启用详细日志
export PKBM_DEBUG=true
python3 main.py
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

- 项目主页: https://github.com/pkbm/pkbm
- 问题反馈: https://github.com/pkbm/pkbm/issues
- 邮箱: team@pkbm.com

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的CRUD操作
- 跨平台GUI界面
- Go后端API服务
- 数据迁移支持

---

**注意**: 本项目正在积极开发中，功能可能会有所变化。建议定期查看更新日志了解最新变化。
