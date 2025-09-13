#!/bin/bash
echo "启动公式转换工具..."
echo

# 检查是否存在虚拟环境
if [ -f ".venv/bin/python" ]; then
    echo "使用虚拟环境启动..."
    .venv/bin/python main.py
elif [ -f ".venv/Scripts/python.exe" ]; then
    echo "使用虚拟环境启动..."
    .venv/Scripts/python.exe main.py
else
    echo "使用系统 Python 启动..."
    python main.py
fi
