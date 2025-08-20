# PKBM SSH GUI 设置指南

## 概述
本指南将帮助您在Windows上通过SSH连接到Ubuntu服务器，并运行PKBM的GUI界面。

## 系统要求

### Windows端
- Windows 10/11
- SSH客户端 (如 PuTTY, Windows Terminal, 或 Git Bash)
- X11服务器 (VcXsrv 或 Xming)

### Ubuntu服务器端
- Ubuntu 20.04+
- Python 3.8+
- PyQt6 或 Tkinter
- 启用的X11转发

## 步骤1: 在Windows上安装X11服务器

### 选项1: VcXsrv (推荐)
1. 下载 VcXsrv: https://sourceforge.net/projects/vcxsrv/
2. 安装并启动 VcXsrv
3. 配置设置:
   - Display number: 0
   - Start no client: 勾选
   - Extra settings: 勾选 "Disable access control"
   - 保存配置

### 选项2: Xming
1. 下载 Xming: https://sourceforge.net/projects/xming/
2. 安装并启动 Xming
3. 配置类似VcXsrv

## 步骤2: 配置SSH连接

### 使用PuTTY
1. 打开PuTTY
2. 在Connection > SSH > X11中:
   - 勾选 "Enable X11 forwarding"
   - X display location: localhost:0.0
3. 保存配置并连接

### 使用命令行SSH
```bash
# 启用X11转发
ssh -X username@hostname

# 启用可信X11转发 (推荐)
ssh -Y username@hostname

# 指定显示
ssh -X -Y username@hostname
```

### 使用Git Bash
```bash
# 设置DISPLAY环境变量
export DISPLAY=localhost:0.0

# 连接SSH
ssh -X -Y username@hostname
```

## 步骤3: 在Ubuntu服务器上运行PKBM

### 方法1: 使用专门的SSH GUI启动脚本
```bash
# 给脚本添加执行权限
chmod +x start_ssh_gui.sh

# 运行脚本
./start_ssh_gui.sh
```

### 方法2: 使用通用启动脚本
```bash
# 给脚本添加执行权限
chmod +x start.sh

# 运行脚本
./start.sh
```

### 方法3: 直接运行
```bash
# 检查X11转发
echo $DISPLAY

# 运行PyQt6版本
python3 main.py

# 或运行Tkinter版本
python3 main_tkinter.py
```

## 步骤4: 故障排除

### 常见问题

#### 1. X11转发未启用
**症状**: 脚本显示"X11转发未启用"
**解决方案**:
```bash
# 重新连接SSH，启用X11转发
ssh -X -Y username@hostname

# 检查DISPLAY变量
echo $DISPLAY
```

#### 2. X11连接测试失败
**症状**: "X11连接测试失败"
**解决方案**:
- 确保Windows上的X11服务器正在运行
- 检查防火墙设置
- 重新启动X11服务器

#### 3. GUI窗口不显示
**症状**: 程序启动但没有窗口显示
**解决方案**:
- 检查DISPLAY设置: `echo $DISPLAY`
- 确保X11服务器正在运行
- 尝试设置DISPLAY: `export DISPLAY=localhost:0.0`

#### 4. 权限被拒绝
**症状**: "Connection refused" 或权限错误
**解决方案**:
- 在VcXsrv中勾选 "Disable access control"
- 重启X11服务器
- 检查SSH配置中的X11设置

### 调试命令
```bash
# 检查SSH连接
echo $SSH_CONNECTION

# 检查X11转发
echo $DISPLAY

# 测试X11连接
xset q

# 检查GUI库
python3 -c "import PyQt6; print('PyQt6可用')"
python3 -c "import tkinter; print('Tkinter可用')"

# 检查网络连接
ping localhost
```

## 步骤5: 优化设置

### 创建SSH配置文件
在Windows的 `~/.ssh/config` 文件中添加:
```
Host your-server-name
    HostName your-server-ip
    User your-username
    ForwardX11 yes
    ForwardX11Trusted yes
    ForwardAgent yes
```

### 创建启动脚本
在Windows上创建批处理文件 `start_pkbm_gui.bat`:
```batch
@echo off
echo 启动PKBM GUI...
echo 请确保VcXsrv正在运行
echo.

set DISPLAY=localhost:0.0
ssh -X -Y username@hostname "./start_ssh_gui.sh"

pause
```

## 性能优化

### 网络优化
```bash
# 在SSH连接中使用压缩
ssh -C -X -Y username@hostname

# 使用SSH配置文件优化
Host your-server
    Compression yes
    ForwardX11 yes
    ForwardX11Trusted yes
```

### 显示优化
- 在VcXsrv中使用 "Native opengl" 渲染
- 启用 "Clipboard" 支持
- 调整 "Extra settings" 中的性能选项

## 安全注意事项

1. **X11转发安全**: 使用 `-Y` 标志时要小心，它允许不受信任的X11连接
2. **防火墙**: 确保SSH端口(22)开放，但限制其他端口访问
3. **用户权限**: 使用普通用户账户，避免root账户
4. **连接加密**: 使用SSH密钥而不是密码认证

## 替代方案

如果X11转发遇到问题，可以考虑:

1. **VNC**: 使用VNC服务器和客户端
2. **RDP**: 如果Ubuntu支持远程桌面
3. **Web界面**: 开发基于Web的PKBM界面
4. **命令行**: 使用命令行版本进行基本操作

## 支持

如果遇到问题:
1. 检查本指南的故障排除部分
2. 查看系统日志: `tail -f /var/log/auth.log`
3. 检查SSH配置: `sudo nano /etc/ssh/sshd_config`
4. 重启SSH服务: `sudo systemctl restart ssh`
