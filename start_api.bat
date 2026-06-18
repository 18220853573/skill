@echo off
chcp 65001 >nul
title WeChat API Service
echo ========================================
echo  微信文章API服务 - 一键启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查Python依赖...
pip install -r requirements.txt --quiet 2>nul
if %ERRORLEVEL% EQU 0 (
    echo 依赖检查完成 ✓
) else (
    echo 依赖安装中...
    pip install -r requirements.txt
)

echo.
echo [2/2] 启动服务...
echo 服务启动后可通过以下地址访问：
echo   http://localhost:5000
echo   http://localhost:5000/admin.html
echo.

python app.py

pause
