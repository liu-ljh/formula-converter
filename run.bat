@echo off
echo 启动公式转换工具...
echo.

REM 检查是否存在虚拟环境
if exist ".venv\Scripts\python.exe" (
    echo 使用虚拟环境启动...
    .venv\Scripts\python.exe main.py
) else (
    echo 使用系统 Python 启动...
    python main.py
)

pause
