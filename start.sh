#!/bin/bash

echo "PKBM - 个人知识库管理系统"
echo "================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

# 检查Python版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "错误: 需要Python 3.8或更高版本"
    echo "当前版本: $python_version"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖包..."
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "正在安装依赖包..."
    echo "如果安装失败，请尝试运行: python3 install_deps.py"
    
    # 尝试使用改进的安装脚本
    if [ -f "install_deps.py" ]; then
        echo "使用改进的安装脚本..."
        python3 install_deps.py
        if [ $? -ne 0 ]; then
            echo "依赖包安装失败，请检查错误信息"
            echo "建议手动运行: python3 install_deps.py"
            exit 1
        fi
    else
        # 回退到传统方法
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "依赖包安装失败，请检查网络连接和权限"
            echo "建议运行: python3 install_deps.py"
            exit 1
        fi
    fi
fi

# 启动程序
echo "启动PKBM..."

# 检查是否指定了端口
if [ -n "$1" ]; then
    echo "使用端口: $1"
    export PKBM_PORT=$1
    export PKBM_HOST=127.0.0.1
    export PKBM_NETWORK_ENABLED=true
else
    echo "使用默认配置启动GUI应用"
    export PKBM_NETWORK_ENABLED=false
fi

# 检查SSH连接和X11转发
if [ -n "$SSH_CONNECTION" ]; then
    echo "检测到SSH连接"
    
    # 检查X11转发
    if [ -n "$DISPLAY" ]; then
        echo "✓ X11转发已启用，可以显示GUI"
        echo "提示: 在Windows上使用X11服务器(如VcXsrv)来显示GUI"
        
        # 检查是否支持GUI
        if python3 -c "import PyQt6" &> /dev/null; then
            echo "启动PyQt6 GUI版本..."
            python3 main.py
        elif python3 -c "import tkinter" &> /dev/null; then
            echo "启动Tkinter GUI版本..."
            python3 main_tkinter.py
        else
            echo "GUI库不可用，启动命令行版本..."
            python3 main_cli.py
        fi
    else
        echo "⚠ X11转发未启用，启动命令行版本"
        echo "要启用GUI，请使用: ssh -X username@hostname"
        echo "或在Windows上使用: ssh -Y username@hostname"
        python3 main_cli.py
    fi
else
    echo "本地环境，启动GUI版本..."
    
    # 检查是否支持GUI
    if python3 -c "import PyQt6" &> /dev/null; then
        echo "启动PyQt6 GUI版本..."
        python3 main.py
    elif python3 -c "import tkinter" &> /dev/null; then
        echo "启动Tkinter GUI版本..."
        python3 main_tkinter.py
    else
        echo "GUI库不可用，启动命令行版本..."
        python3 main_cli.py
    fi
fi

if [ $? -ne 0 ]; then
    echo "程序运行出错，请检查错误信息"
fi

echo
echo "程序已退出"

