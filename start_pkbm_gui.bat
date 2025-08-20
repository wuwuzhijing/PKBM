@echo off
chcp 65001 >nul
title PKBM - SSH GUI 启动器

echo PKBM - 个人知识库管理系统 (SSH GUI版本)
echo ================================================
echo.

echo 请确保您已经:
echo 1. 安装了VcXsrv或Xming等X11服务器
echo 2. 启动了X11服务器
echo 3. 配置了SSH连接
echo.

echo 设置DISPLAY环境变量...
set DISPLAY=localhost:0.0

echo 当前DISPLAY设置: %DISPLAY%
echo.

echo 请输入服务器信息:
set /p SERVER_HOST=10.10.150.29 
set /p USERNAME=sight

echo.
echo 正在连接到 %SERVER_HOST%...
echo 使用命令: ssh -X -Y %USERNAME%@%SERVER_HOST% "./start_ssh_gui.sh"
echo.

echo 如果连接成功，PKBM的GUI将在您的Windows桌面上显示
echo 按任意键开始连接...
pause >nul

echo.
echo 正在连接...
ssh -X -Y %USERNAME%@%SERVER_HOST% "./start_ssh_gui.sh"

echo.
echo 连接已结束
echo 按任意键退出...
pause >nul
