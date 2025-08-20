#!/bin/bash

echo "PKBM - Qt6 安装脚本"
echo "===================="
echo

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "无法检测操作系统"
    exit 1
fi

echo "检测到操作系统: $OS $VER"
echo

# Ubuntu/Debian系统
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Linux Mint"* ]]; then
    echo "正在为Ubuntu/Debian系统安装Qt6..."
    
    # 更新包列表
    sudo apt update
    
    # 添加Qt6 PPA源
    echo "正在添加Qt6 PPA源..."
    sudo add-apt-repository ppa:okirby/qt6-backports -y
    
    # 更新包列表
    sudo apt update
    
    # 安装Qt6基础包
    echo "正在安装Qt6基础包..."
    sudo apt install -y qt6-base-dev qt6-tools-dev
    
    # 如果PPA中没有Qt6包，尝试使用snap安装
    if ! dpkg -l | grep -q qt6; then
        echo "PPA中没有找到Qt6包，尝试使用snap安装..."
        sudo snap install qt6-base-dev --classic
    fi
fi

echo "Qt6安装完成！"
echo "现在可以尝试运行程序了"
