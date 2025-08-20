#!/bin/bash

echo "PKBM - Go环境配置脚本"
echo "======================"

# 设置Go模块代理
echo "设置Go模块代理..."
export GOPROXY=https://goproxy.cn,direct
export GOSUMDB=sum.golang.google.cn

# 或者使用阿里云镜像
# export GOPROXY=https://mirrors.aliyun.com/goproxy/,direct

echo "GOPROXY设置为: $GOPROXY"
echo "GOSUMDB设置为: $GOSUMDB"

# 下载依赖
echo "下载Go依赖..."
go mod download

# 验证依赖
echo "验证依赖..."
go mod verify

echo "Go环境配置完成！"
