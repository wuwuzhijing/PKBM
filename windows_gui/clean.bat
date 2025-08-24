@echo off
echo 清理PKBM构建目录...
echo.

if exist build (
    echo 删除build目录...
    rmdir /s /q build
    if exist build (
        echo 删除build目录失败，请手动删除
    ) else (
        echo ✓ build目录已删除
    )
) else (
    echo build目录不存在
)

if exist dist (
    echo 删除dist目录...
    rmdir /s /q dist
    if exist dist (
        echo 删除dist目录失败，请手动删除
    ) else (
        echo ✓ dist目录已删除
    )
) else (
    echo dist目录不存在
)

echo.
echo 清理完成！现在可以运行 python build_exe.py
pause
