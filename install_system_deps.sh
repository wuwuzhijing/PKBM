#!/bin/bash

echo "PKBM - 系统依赖安装脚本"
echo "================================"
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
    echo "正在安装Ubuntu/Debian系统依赖..."
    
    # 更新包列表
    sudo apt update
    
    # 安装Qt6依赖
    sudo apt install -y \
        qt6-base-dev \
        qt6-tools-dev \
        qt6-tools-dev-tools \
        libqt6core6 \
        libqt6gui6 \
        libqt6widgets6 \
        libqt6dbus6 \
        libqt6network6 \
        libqt6svg6 \
        libqt6svg6-dev \
        libqt6opengl6 \
        libqt6opengl6-dev \
        libqt6printsupport6 \
        libqt6sql6 \
        libqt6sql6-sqlite \
        libqt6xml6 \
        libqt6xml6-dev \
        libqt6concurrent6 \
        libqt6test6 \
        libqt6test6-dev
    
    # 安装X11依赖
    sudo apt install -y \
        libxcb1 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-shm0 \
        libxcb-sync1 \
        libxcb-util1 \
        libxcb-xfixes0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libxkbcommon0
    
    # 安装其他必要依赖
    sudo apt install -y \
        libgl1-mesa-dev \
        libglu1-mesa-dev \
        libfontconfig1 \
        libfreetype6 \
        libharfbuzz0b \
        libpng16-16 \
        libjpeg-turbo8 \
        libtiff5 \
        libwebp6 \
        libopenjp2-7 \
        liblcms2-2 \
        liblz4-1 \
        libzstd1 \
        libbz2-1.0 \
        liblzma5 \
        libgif7 \
        libwmf0.2-7 \
        libwmf-dev \
        libmagickwand-6.q16-6 \
        libmagickcore-6.q16-6 \
        libmagickcore-6.q16-6-extra

# CentOS/RHEL/Fedora系统
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"Fedora"* ]]; then
    echo "正在安装CentOS/RHEL/Fedora系统依赖..."
    
    if command -v dnf &> /dev/null; then
        # Fedora/RHEL 8+
        sudo dnf install -y \
            qt6-qtbase-devel \
            qt6-qttools-devel \
            qt6-qtbase-gui \
            qt6-qtbase-widgets \
            qt6-qtbase-dbus \
            qt6-qtbase-network \
            qt6-qtbase-sql \
            qt6-qtbase-sql-sqlite \
            qt6-qtbase-xml \
            qt6-qtbase-concurrent \
            qt6-qtbase-test \
            qt6-qtsvg-devel \
            qt6-qtsvg \
            qt6-qtdeclarative-devel \
            qt6-qtdeclarative \
            libxcb-devel \
            libxcb-cursor-devel \
            mesa-libGL-devel \
            mesa-libGLU-devel \
            fontconfig-devel \
            freetype-devel \
            harfbuzz-devel \
            libpng-devel \
            libjpeg-turbo-devel \
            libtiff-devel \
            libwebp-devel \
            openjpeg2-devel \
            lcms2-devel \
            lz4-devel \
            zstd-devel \
            bzip2-devel \
            xz-devel \
            giflib-devel \
            wmf-devel \
            ImageMagick-devel
    else
        # CentOS 7
        sudo yum install -y \
            qt6-qtbase-devel \
            qt6-qttools-devel \
            libxcb-devel \
            mesa-libGL-devel \
            mesa-libGLU-devel \
            fontconfig-devel \
            freetype-devel \
            libpng-devel \
            libjpeg-turbo-devel \
            libtiff-devel \
            giflib-devel
    fi

# Arch Linux系统
elif [[ "$OS" == *"Arch"* ]] || [[ "$OS" == *"Manjaro"* ]]; then
    echo "正在安装Arch Linux系统依赖..."
    
    sudo pacman -S --noconfirm \
        qt6-base \
        qt6-tools \
        qt6-svg \
        qt6-declarative \
        xcb-util \
        xcb-util-cursor \
        xcb-util-image \
        xcb-util-keysyms \
        xcb-util-renderutil \
        xcb-util-wm \
        mesa \
        glu \
        fontconfig \
        freetype2 \
        harfbuzz \
        libpng \
        libjpeg-turbo \
        libtiff \
        libwebp \
        openjpeg2 \
        lcms2 \
        lz4 \
        zstd \
        bzip2 \
        xz \
        giflib \
        wmf \
        imagemagick

else
    echo "不支持的操作系统: $OS"
    echo "请手动安装Qt6和相关依赖"
    exit 1
fi

echo
echo "系统依赖安装完成！"
echo "现在可以尝试运行程序了"
echo
echo "如果仍有问题，请尝试："
echo "1. 重启终端"
echo "2. 检查环境变量"
echo "3. 运行: python3 main.py"
