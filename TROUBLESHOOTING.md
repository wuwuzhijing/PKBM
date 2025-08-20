# PKBM 故障排除指南

## 常见问题及解决方案

### 1. 依赖包安装失败

#### 问题描述
```
error: subprocess-exited-with-error
Getting requirements to build wheel did not run successfully
```

#### 解决方案

**方案1: 使用改进的安装脚本**
```bash
python3 install_deps.py
```

**方案2: 升级构建工具**
```bash
python3 -m pip install --upgrade setuptools wheel build
```

**方案3: 使用国内镜像源**
```bash
# 设置清华镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者使用阿里云镜像源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

**方案4: 安装系统依赖（Ubuntu/Debian）**
```bash
sudo apt update
sudo apt install python3-dev build-essential libxml2-dev libxslt1-dev
```

**方案5: 安装系统依赖（CentOS/RHEL）**
```bash
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel libxml2-devel libxslt-devel
```

### 2. PyQt6 安装问题

#### 问题描述
```
ModuleNotFoundError: No module named 'PyQt6'
```

#### 解决方案

**方案1: 使用conda安装**
```bash
conda install -c conda-forge pyqt
```

**方案2: 安装系统Qt依赖**
```bash
# Ubuntu/Debian
sudo apt install qt6-base-dev qt6-tools-dev

# CentOS/RHEL
sudo yum install qt6-qtbase-devel qt6-qttools-devel
```

**方案3: 使用预编译包**
```bash
pip install --only-binary=all PyQt6
```

### 3. 权限问题

#### 问题描述
```
PermissionError: [Errno 13] Permission denied
```

#### 解决方案

**方案1: 使用用户安装**
```bash
pip3 install --user -r requirements.txt
```

**方案2: 使用虚拟环境**
```bash
# 创建虚拟环境
python3 -m venv pkbm_env

# 激活虚拟环境
source pkbm_env/bin/activate  # Linux/macOS
# 或
pkbm_env\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 4. 网络连接问题

#### 问题描述
```
ConnectionError: [Errno 110] Connection timed out
```

#### 解决方案

**方案1: 检查网络连接**
```bash
ping pypi.org
```

**方案2: 使用代理**
```bash
pip install --proxy http://proxy:port -r requirements.txt
```

**方案3: 离线安装**
```bash
# 下载包到本地
pip download -r requirements.txt -d ./packages

# 从本地安装
pip install --no-index --find-links ./packages -r requirements.txt
```

### 5. Python版本兼容性问题

#### 问题描述
```
SyntaxError: invalid syntax
```

#### 解决方案

**检查Python版本**
```bash
python3 --version
```

**确保使用Python 3.8+**
```bash
# 如果系统有多个Python版本
python3.8 -m pip install -r requirements.txt
python3.8 main.py
```

### 6. 端口占用问题

#### 问题描述
```
Address already in use
```

#### 解决方案

**查看端口占用**
```bash
# Linux/macOS
netstat -an | grep :8080
lsof -i :8080

# Windows
netstat -an | findstr :8080
```

**使用其他端口**
```bash
./start.sh 8081
# 或
start.bat 8081
```

## 调试技巧

### 1. 启用详细输出
```bash
pip install -v -r requirements.txt
```

### 2. 检查已安装的包
```bash
pip list
```

### 3. 检查包信息
```bash
pip show PyQt6
```

### 4. 清理缓存
```bash
pip cache purge
```

## 获取帮助

如果以上方案都无法解决问题，请：

1. 检查错误日志
2. 确认系统环境（OS版本、Python版本等）
3. 尝试在干净的环境中重新安装
4. 查看项目的GitHub Issues页面

## 预防措施

1. **定期更新**: 保持Python和pip为最新版本
2. **使用虚拟环境**: 避免包冲突
3. **备份配置**: 保存工作配置
4. **测试环境**: 在生产环境部署前充分测试
