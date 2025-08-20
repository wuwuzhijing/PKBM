# PKBM 端口配置使用说明

## 概述
PKBM系统现在支持通过命令行参数指定端口，以便在需要网络功能时使用。

## 使用方法

### Linux/macOS (使用 start.sh)
```bash
# 使用默认配置启动GUI应用
./start.sh

# 指定端口启动（例如端口8080）
./start.sh 8080

# 指定其他端口
./start.sh 3000
```

### Windows (使用 start.bat)
```cmd
REM 使用默认配置启动GUI应用
start.bat

REM 指定端口启动（例如端口8080）
start.bat 8080

REM 指定其他端口
start.bat 3000
```

## 环境变量
当指定端口时，系统会自动设置以下环境变量：

- `PKBM_NETWORK_ENABLED=true` - 启用网络模式
- `PKBM_PORT=<端口号>` - 设置端口号
- `PKBM_HOST=127.0.0.1` - 设置主机地址（默认本地）

## 注意事项

1. **端口范围**: 建议使用1024-65535之间的端口
2. **权限**: 某些端口（如80、443）可能需要管理员权限
3. **防火墙**: 确保防火墙允许指定端口的访问
4. **端口冲突**: 确保指定的端口没有被其他程序占用

## 配置选项
端口配置可以在 `config.py` 文件中的 `NETWORK_CONFIG` 部分进行修改：

```python
NETWORK_CONFIG = {
    'enabled': False,
    'host': '127.0.0.1',
    'port': 8080,
    'debug': False,
    'allow_external_access': False
}
```

## 故障排除

### 端口被占用
如果遇到"端口已被占用"的错误，可以：
1. 使用 `netstat -an | grep <端口号>` 查看端口占用情况
2. 选择其他可用端口
3. 关闭占用端口的程序

### 权限不足
如果遇到权限错误：
1. 在Linux/macOS上使用 `sudo` 运行
2. 在Windows上以管理员身份运行命令提示符

### 网络访问问题
如果无法从其他设备访问：
1. 检查防火墙设置
2. 确认 `allow_external_access` 配置
3. 检查网络配置
