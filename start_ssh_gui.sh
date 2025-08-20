#!/bin/bash

echo "PKBM - SSH GUI 启动脚本"
echo "========================"
echo

# 检查SSH连接
if [ -z "$SSH_CONNECTION" ]; then
    echo "错误: 此脚本只能在SSH连接中使用"
    echo "请通过SSH连接到服务器后运行此脚本"
    exit 1
fi

echo "✓ 检测到SSH连接"
echo "连接信息: $SSH_CONNECTION"

# 检查X11转发
if [ -z "$DISPLAY" ]; then
    echo "⚠ X11转发未启用"
    echo ""
    echo "要启用GUI，请使用以下方式连接:"
    echo "  ssh -X username@hostname     # 启用X11转发"
    echo "  ssh -Y username@hostname     # 启用可信X11转发"
    echo ""
    echo "在Windows上，您还需要:"
    echo "1. 安装X11服务器，如 VcXsrv 或 Xming"
    echo "2. 启动X11服务器"
    echo "3. 设置DISPLAY环境变量"
    echo ""
    echo "现在启动命令行版本..."
    python3 main_cli.py
    exit 0
fi

echo "✓ X11转发已启用 (DISPLAY=$DISPLAY)"
echo ""

# 检查GUI库可用性
echo "检查GUI库..."

if python3 -c "import PyQt6" &> /dev/null; then
    echo "✓ PyQt6 可用"
    GUI_LIB="PyQt6"
elif python3 -c "import tkinter" &> /dev/null; then
    echo "✓ Tkinter 可用"
    GUI_LIB="Tkinter"
else
    echo "✗ 没有可用的GUI库"
    echo "启动命令行版本..."
    python3 main_cli.py
    exit 0
fi

# 检查X11服务器连接
echo "测试X11连接..."
if ! xset q &> /dev/null; then
    echo "⚠ X11连接测试失败"
    echo "可能的原因:"
    echo "1. X11服务器未启动"
    echo "2. 防火墙阻止连接"
    echo "3. DISPLAY设置不正确"
    echo ""
    echo "现在启动命令行版本..."
    python3 main_cli.py
    exit 0
fi

echo "✓ X11连接测试成功"
echo ""

# 启动相应的GUI版本
case $GUI_LIB in
    "PyQt6")
        echo "启动 PyQt6 GUI 版本..."
        echo "提示: GUI窗口将在您的本地机器上显示"
        python3 main.py
        ;;
    "Tkinter")
        echo "启动 Tkinter GUI 版本..."
        echo "提示: GUI窗口将在您的本地机器上显示"
        python3 main_tkinter.py
        ;;
    *)
        echo "启动命令行版本..."
        python3 main_cli.py
        ;;
esac

echo ""
echo "程序已退出"
