# PKBM构建目录清理脚本
Write-Host "清理PKBM构建目录..." -ForegroundColor Green
Write-Host ""

# 检查并删除build目录
if (Test-Path "build") {
    Write-Host "删除build目录..." -ForegroundColor Yellow
    try {
        Remove-Item -Path "build" -Recurse -Force
        Write-Host "✓ build目录已删除" -ForegroundColor Green
    } catch {
        Write-Host "✗ 删除build目录失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "尝试强制删除..." -ForegroundColor Yellow
        
        # 强制删除
        try {
            Get-ChildItem -Path "build" -Recurse | Remove-Item -Force -Recurse
            Remove-Item -Path "build" -Force
            Write-Host "✓ build目录已强制删除" -ForegroundColor Green
        } catch {
            Write-Host "✗ 强制删除失败，请手动删除build目录" -ForegroundColor Red
        }
    }
} else {
    Write-Host "build目录不存在" -ForegroundColor Gray
}

# 检查并删除dist目录
if (Test-Path "dist") {
    Write-Host "删除dist目录..." -ForegroundColor Yellow
    try {
        Remove-Item -Path "dist" -Recurse -Force
        Write-Host "✓ dist目录已删除" -ForegroundColor Green
    } catch {
        Write-Host "✗ 删除dist目录失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "尝试强制删除..." -ForegroundColor Yellow
        
        # 强制删除
        try {
            Get-ChildItem -Path "dist" -Recurse | Remove-Item -Force -Recurse
            Remove-Item -Path "dist" -Force
            Write-Host "✓ dist目录已强制删除" -ForegroundColor Green
        } catch {
            Write-Host "✗ 强制删除失败，请手动删除dist目录" -ForegroundColor Red
        }
    }
} else {
    Write-Host "dist目录不存在" -ForegroundColor Gray
}

Write-Host ""
Write-Host "清理完成！现在可以运行 python build_exe.py" -ForegroundColor Green
Write-Host "按任意键继续..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
