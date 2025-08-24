# PKBM Go 后端服务

## 概述

PKBM后端服务使用Go语言开发，提供高性能的RESTful API接口，支持知识库的增删改查、分类管理、搜索等功能。

## 技术特性

- **语言**: Go 1.21+
- **数据库**: SQLite3
- **Web框架**: Gorilla Mux
- **数据库驱动**: go-sqlite3
- **架构**: RESTful API
- **性能**: 高并发、低延迟

## 功能特性

### 核心API
- **条目管理**: CRUD操作
- **分类管理**: 分类增删改查
- **搜索功能**: 全文搜索
- **统计信息**: 系统状态统计

### 数据特性
- **自动建表**: 首次运行自动创建数据库结构
- **默认分类**: 预置常用知识分类
- **数据验证**: 输入数据完整性检查
- **错误处理**: 完善的错误响应机制

## 安装和运行

### 1. 环境要求
- Go 1.21+
- SQLite3开发库

### 2. 安装依赖
```bash
# 安装Go依赖
go mod tidy

# 安装SQLite3开发库 (Ubuntu/Debian)
sudo apt-get install libsqlite3-dev

# 安装SQLite3开发库 (CentOS/RHEL)
sudo yum install sqlite-devel

# 安装SQLite3开发库 (macOS)
brew install sqlite3
```

### 3. 运行服务
```bash
# 开发模式
go run main.go

# 编译后运行
go build -o pkbm-backend main.go
./pkbm-backend

# 后台运行
nohup ./pkbm-backend > pkbm.log 2>&1 &
```

### 4. 构建发布版本
```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o pkbm-backend-linux main.go

# Windows
GOOS=windows GOARCH=amd64 go build -o pkbm-backend.exe main.go

# macOS
GOOS=darwin GOARCH=amd64 go build -o pkbm-backend-mac main.go
```

## API接口

### 基础信息
- **服务地址**: http://localhost:8080
- **API前缀**: /api
- **完整地址**: http://localhost:8080/api

### 条目管理

#### 获取所有条目
```
GET /api/items
```

#### 获取单个条目
```
GET /api/items/{id}
```

#### 创建条目
```
POST /api/items
Content-Type: application/json

{
  "title": "条目标题",
  "content": "条目内容",
  "category": "分类名称",
  "tags": "标签1,标签2"
}
```

#### 更新条目
```
PUT /api/items/{id}
Content-Type: application/json

{
  "title": "新标题",
  "content": "新内容",
  "category": "新分类",
  "tags": "新标签"
}
```

#### 删除条目
```
DELETE /api/items/{id}
```

### 分类管理

#### 获取所有分类
```
GET /api/categories
```

#### 创建分类
```
POST /api/categories
Content-Type: application/json

{
  "name": "分类名称",
  "description": "分类描述"
}
```

### 搜索功能

#### 搜索条目
```
GET /api/search?q=搜索关键词
```

### 统计信息

#### 获取系统统计
```
GET /api/stats
```

响应示例:
```json
{
  "total_items": 150,
  "total_categories": 8,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## 配置说明

### 环境变量
- `PORT`: 服务端口 (默认: 8080)
- `DB_PATH`: 数据库路径 (默认: data/pkbm.db)
- `LOG_LEVEL`: 日志级别 (默认: info)

### 数据库配置
- **类型**: SQLite3
- **路径**: data/pkbm.db
- **自动创建**: 是
- **备份建议**: 定期备份data目录

## 部署说明

### 开发环境
```bash
# 直接运行
go run main.go

# 热重载 (需要安装air)
air
```

### 生产环境
```bash
# 编译
go build -ldflags="-s -w" -o pkbm-backend main.go

# 使用systemd服务
sudo cp pkbm-backend /usr/local/bin/
sudo cp pkbm.service /etc/systemd/system/
sudo systemctl enable pkbm
sudo systemctl start pkbm
```

### Docker部署
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o pkbm-backend main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates sqlite
WORKDIR /root/
COPY --from=builder /app/pkbm-backend .
EXPOSE 8080
CMD ["./pkbm-backend"]
```

## 监控和维护

### 健康检查
```bash
# 检查服务状态
curl http://localhost:8080/api/stats

# 检查进程
ps aux | grep pkbm-backend
```

### 日志管理
- **日志位置**: 控制台输出
- **日志级别**: 可配置
- **建议**: 使用logrotate或systemd管理日志

### 性能监控
- **内存使用**: 监控Go进程内存
- **CPU使用**: 监控CPU占用
- **数据库性能**: 监控SQL查询性能

## 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 查看端口占用
netstat -tlnp | grep :8080

# 杀死占用进程
sudo kill -9 <PID>
```

#### 2. 数据库权限问题
```bash
# 检查目录权限
ls -la data/

# 修复权限
chmod 755 data/
chmod 644 data/pkbm.db
```

#### 3. 依赖库问题
```bash
# 清理Go模块缓存
go clean -modcache

# 重新下载依赖
go mod download
```

### 调试模式
```bash
# 启用详细日志
export LOG_LEVEL=debug
go run main.go
```

## 更新日志

### v1.0.0
- ✅ 基础CRUD API
- ✅ 分类管理
- ✅ 搜索功能
- ✅ 统计接口
- ✅ 自动建表
- ✅ 默认分类

### 计划功能
- 🔄 用户认证
- 🔄 权限管理
- 🔄 数据导入导出
- 🔄 备份恢复
- 🔄 性能优化
- 🔄 集群支持

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License 