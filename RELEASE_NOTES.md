# PKBM v1.0.0 发布说明

## 版本信息
- **版本号**: v1.0.0
- **发布日期**: 2024年8月20日
- **构建平台**: Ubuntu 20.04 LTS

## 新功能特性

### 🎯 核心功能 (0-8)
1. **查看所有条目** - 浏览所有知识条目，支持分页和排序
2. **添加新条目** - 创建新的知识条目，支持分类和标签
3. **搜索条目** - 全文搜索功能，支持标题、内容、标签搜索
4. **编辑条目** - 修改现有条目内容和属性
5. **删除条目** - 安全删除不需要的条目
6. **查看分类** - 管理知识分类系统
7. **导入文件** - 批量导入文本文件
8. **数据库状态** - 查看系统统计信息

### 🚀 技术特性
- **跨平台支持**: Windows、Ubuntu、未来支持移动端
- **现代化架构**: 前后端分离，Go后端 + Python GUI
- **数据安全**: SQLite数据库，完全兼容现有数据
- **美观界面**: 基于tkinter的现代化GUI设计
- **高性能**: Go语言后端提供快速API服务

## 平台支持

### ✅ 已支持
- **Ubuntu/Linux**: 原生支持，可打包为deb包
- **Windows**: 可打包为exe文件
- **命令行**: 无图形界面环境下的命令行版本

### 🔮 计划支持
- **iOS**: Flutter应用
- **Android**: Flutter应用
- **Web**: 浏览器访问版本

## 安装说明

### Ubuntu/Linux
```bash
# 方法1: 直接运行
cd ubuntu_gui/dist
./pkbm

# 方法2: 系统安装
sudo ./install.sh
```

### Windows
```bash
# 方法1: 直接运行
cd windows_gui
python3 main.py

# 方法2: 打包为exe
python3 build_exe.py
```

### 后端服务 (可选)
```bash
cd backend
go run main.go
# 或
go build -o pkbm-backend main.go
./pkbm-backend
```

## 数据迁移

### 从旧版本迁移
1. **备份数据**: 复制原有数据库文件
2. **放置数据**: 将数据库文件放到新版本的`data/`目录
3. **启动程序**: 新版本会自动识别并加载现有数据

### 数据库格式
- **类型**: SQLite3
- **位置**: `data/pkbm.db`
- **兼容性**: 完全兼容现有数据格式

## 系统要求

### 最低要求
- **操作系统**: Ubuntu 18.04+ / Windows 10+
- **Python**: 3.8+
- **内存**: 512MB RAM
- **存储**: 100MB 可用空间

### 推荐配置
- **操作系统**: Ubuntu 20.04+ / Windows 11
- **Python**: 3.9+
- **内存**: 2GB RAM
- **存储**: 1GB 可用空间

## 已知问题

### 已修复
- ✅ tkinter导入问题
- ✅ 数据库初始化问题
- ✅ 跨平台兼容性问题
- ✅ 构建脚本错误

### 注意事项
- 在SSH环境中运行时，GUI界面需要X11转发
- 首次运行会自动创建数据库和默认分类
- 建议定期备份数据库文件

## 更新日志

### v1.0.0 (2024-08-20)
- 🎉 初始版本发布
- ✨ 完整的CRUD操作支持
- 🌐 跨平台GUI界面
- 🗄️ SQLite数据库支持
- 🔍 全文搜索功能
- 📁 文件导入功能
- 🏷️ 分类和标签系统
- 📊 数据统计功能

## 技术支持

### 问题反馈
- GitHub Issues: [项目主页](https://github.com/pkbm/pkbm/issues)
- 邮箱支持: team@pkbm.com

### 文档资源
- 用户手册: `README.md`
- 故障排除: `TROUBLESHOOTING.md`
- SSH设置: `SSH_GUI_SETUP.md`

### 开发资源
- 项目结构: `PROJECT_STRUCTURE.md`
- 快速开始: `QUICK_START.md`
- 构建说明: `build_all.py`

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**感谢使用PKBM！** 🎉

如有问题或建议，请通过上述方式联系我们。
