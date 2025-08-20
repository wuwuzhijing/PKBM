@echo off
chcp 65001 >nul
echo PKBM - 个人知识库管理系统
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖包安装失败，请检查网络连接
        pause
        exit /b 1
    )
)

REM 启动程序
echo 启动PKBM...

REM 检查是否指定了端口
if not "%1"=="" (
    echo 使用端口: %1
    set PKBM_PORT=%1
    set PKBM_HOST=127.0.0.1
    set PKBM_NETWORK_ENABLED=true
) else (
    echo 使用默认配置启动GUI应用
    set PKBM_NETWORK_ENABLED=false
)

python main.py

if errorlevel 1 (
    echo 程序运行出错，请检查错误信息
    pause
)

echo.
echo 程序已退出
pause

