# .gitignore 文件说明

## 📋 概述

本项目的`.gitignore`文件已经配置好，用于忽略不需要版本控制的文件和目录。这样可以保持代码仓库的整洁，避免提交不必要的文件。

## 🚫 被忽略的文件类型

### Python相关
- `__pycache__/` - Python编译缓存目录
- `*.pyc`, `*.pyo`, `*.pyd` - Python编译文件
- `build/`, `dist/` - 构建和分发目录
- `*.egg-info/` - Python包信息
- `venv/`, `.venv/` - 虚拟环境目录

### IDE和编辑器
- `.vscode/` - VS Code配置
- `.idea/` - PyCharm配置
- `*.iml`, `*.ipr`, `*.iws` - IntelliJ项目文件
- `*.swp`, `*.swo` - Vim临时文件

### 测试和覆盖率
- `.pytest_cache/` - pytest缓存
- `.coverage` - 覆盖率报告
- `htmlcov/` - HTML覆盖率报告
- `.tox/`, `.nox/` - 测试环境

### 环境变量
- `.env` - 环境变量文件
- `*.env` - 环境变量文件

## 🗂️ PKBM特定忽略规则

### 数据文件
```gitignore
# 数据库文件
data/*.db
data/*.db-journal
data/*.db-wal
data/*.db-shm

# 用户数据（保留目录结构）
data/attachments/*
!data/attachments/.gitkeep
data/backups/*
!data/backups/.gitkeep
logs/*
!logs/.gitkeep
```

**说明**: 
- 忽略所有数据库文件（`.db`, `.db-journal`, `.db-wal`, `.db-shm`）
- 忽略用户上传的附件文件
- 忽略备份文件
- 忽略日志文件
- 使用`.gitkeep`文件保持目录结构

### 配置文件
```gitignore
# 配置文件
config.ini
secrets.json
user_preferences.json
user_settings.json
```

**说明**: 忽略可能包含敏感信息的配置文件

### 临时文件
```gitignore
# 临时文件
*.tmp
*.temp
*.bak
*.backup
temp/
tmp/
```

**说明**: 忽略各种临时文件和备份文件

### 系统文件
```gitignore
# 系统文件
.DS_Store          # macOS
Thumbs.db          # Windows
desktop.ini        # Windows
```

**说明**: 忽略操作系统生成的文件

### 大型媒体文件（可选）
```gitignore
# 大型媒体文件（可选）
*.pdf
*.doc
*.docx
*.xls
*.xlsx
*.ppt
*.pptx
*.mp3
*.mp4
*.avi
*.mov
*.jpg
*.jpeg
*.png
*.gif
*.bmp
*.tiff
*.webp
```

**说明**: 这些规则是可选的，你可以根据需要调整：
- 如果希望将某些类型的文件纳入版本控制，可以删除相应的规则
- 如果希望忽略更多文件类型，可以添加相应的规则

## 🔧 自定义配置

### 添加新的忽略规则
如果你需要忽略其他类型的文件，可以在`.gitignore`文件中添加相应的规则：

```gitignore
# 自定义规则示例
*.log              # 忽略所有日志文件
custom_data/       # 忽略自定义数据目录
*.dat              # 忽略数据文件
```

### 强制包含被忽略的文件
如果某个文件被`.gitignore`忽略，但你希望将其纳入版本控制，可以使用：

```bash
git add -f filename
```

### 检查被忽略的文件
查看哪些文件被`.gitignore`忽略：

```bash
git status --ignored
```

## 📁 目录结构保持

项目使用`.gitkeep`文件来保持空目录在git中的存在：

```
PKBM/
├── data/
│   ├── .gitkeep              # 保持data目录
│   ├── attachments/
│   │   └── .gitkeep          # 保持attachments目录
│   └── backups/
│       └── .gitkeep          # 保持backups目录
├── logs/
│   └── .gitkeep              # 保持logs目录
└── resources/
    └── .gitkeep              # 保持resources目录
```

## ⚠️ 注意事项

1. **敏感信息**: 确保不要提交包含密码、API密钥等敏感信息的文件
2. **大型文件**: 避免提交大型二进制文件，这些文件会增加仓库大小
3. **用户数据**: 用户生成的数据文件通常不应该纳入版本控制
4. **环境配置**: 本地环境配置应该保持本地，不要提交到远程仓库

## 🔄 更新.gitignore

如果你修改了`.gitignore`文件，可能需要清理已经跟踪的文件：

```bash
# 从git缓存中移除被忽略的文件
git rm -r --cached .
git add .
git commit -m "更新.gitignore规则"
```

## 📚 相关资源

- [Git官方文档 - gitignore](https://git-scm.com/docs/gitignore)
- [GitHub .gitignore模板](https://github.com/github/gitignore)
- [Python .gitignore最佳实践](https://github.com/github/gitignore/blob/main/Python.gitignore)

---

**提示**: 这个`.gitignore`文件已经为PKBM项目优化，涵盖了Python开发、桌面应用和知识库管理的常见需求。如果你有特殊需求，可以随时调整。
