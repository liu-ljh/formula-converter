# 公式转换工具

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个将 Markdown 和 LaTeX 公式转换为 Word 原生公式的图形化工具，支持三种转换模式，可直接插入到 Word 文档中。

## ✨ 功能特性

- 🎯 **三种转换模式**：Markdown→LaTeX、Markdown→UnicodeMath、LaTeX→UnicodeMath
- 📋 **一键复制**：转换结果直接复制到剪贴板
- 📝 **安全复制**：避免直接操作 Word，降低误操作风险
- 🔧 **智能转换**：自动识别公式语法，智能符号映射
- ⚡ **开箱即用**：无需额外依赖，所有转换模式都支持直接使用
- 🖥️ **现代化 GUI**：基于 PySide6 的直观界面，支持实时状态提示
- 🚀 **快捷启动**：支持 Windows 桌面快捷方式
- ✅ **语法验证**：自动检测 LaTeX 语法错误
- 🔄 **实时反馈**：输入时实时显示字符统计，转换时显示进度
- 🛡️ **错误处理**：详细的错误信息和恢复机制

## 📁 项目结构

```
formula-converter/
├── main.py                 # 主程序入口，GUI 界面
├── markdown_to_latex.py    # Markdown 公式提取和 LaTeX 处理
├── latex_to_unicodemath.py # LaTeX 到 UnicodeMath 转换
├── create_shortcut.py      # Windows 快捷方式创建脚本
├── test_conversion.py      # 功能测试脚本
├── requirements.txt        # Python 依赖包
├── README.md              # 项目说明文档
├── LICENSE                # MIT 开源许可证
├── .gitignore             # Git 忽略文件配置
├── preview.html           # 界面预览页面
├── run.bat               # Windows 启动脚本
├── run.sh                # Linux/Mac 启动脚本
└── .venv/                # Python 虚拟环境（创建后生成）
```

### 核心文件说明

- **`main.py`** - 主程序，包含完整的 GUI 界面和业务逻辑
- **`markdown_to_latex.py`** - 负责从 Markdown 中提取公式并转换为 LaTeX
- **`latex_to_unicodemath.py`** - 将 LaTeX 公式转换为 Word 兼容的 UnicodeMath 格式
- **`create_shortcut.py`** - 在 Windows 桌面和开始菜单创建快捷方式
- **`test_conversion.py`** - 验证所有转换功能的测试脚本

### 项目架构

```
用户输入 (Markdown/LaTeX)
    ↓
main.py (GUI 界面)
    ↓
markdown_to_latex.py (公式提取)
    ↓
latex_to_unicodemath.py (格式转换)
    ↓
输出结果 (LaTeX/UnicodeMath)
    ↓
pyperclip (复制到剪贴板)
```

### 模块依赖关系

- **main.py** 依赖 **markdown_to_latex.py** 和 **latex_to_unicodemath.py**
- **markdown_to_latex.py** 提供公式提取和验证功能
- **latex_to_unicodemath.py** 提供 LaTeX 到 UnicodeMath 的转换
- **create_shortcut.py** 独立运行，用于创建快捷方式
- **test_conversion.py** 独立运行，用于功能测试

## 🖼️ 界面预览

![界面预览](preview.html) - 在浏览器中打开 `preview.html` 查看完整界面设计

## 🛠️ 技术栈

- **Python 3.10+** - 核心语言
- **PySide6** - 图形用户界面
- **pyperclip** - 剪贴板操作
- **UnicodeMath** - Microsoft Word 原生数学格式

## 📦 安装

### 环境要求
- Windows 10/11
- Python 3.10 或更高版本

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/liu-ljh/formula-converter.git
   cd formula-converter
   ```

2. **创建虚拟环境**

   **方式一：使用 venv（推荐）**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **方式二：使用 conda**
   ```bash
   conda create -n formula-converter python=3.10
   conda activate formula-converter
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```


## 🧪 测试功能

运行测试脚本验证所有功能：
```bash
python test_conversion.py
```

## 🚀 使用方法

### 启动应用

**方式一：命令行启动**

使用 venv：
```bash
.venv\Scripts\python main.py
```

使用 conda：
```bash
conda activate formula-converter
python main.py
```

**方式二：创建快捷方式**

使用 venv：
```bash
.venv\Scripts\python create_shortcut.py
```

使用 conda：
```bash
conda activate formula-converter
python create_shortcut.py
```
执行后会在桌面创建"公式转换工具"快捷方式，双击即可启动。

### 操作步骤

1. **选择转换模式**
   - `Markdown→LaTeX`：提取 Markdown 中的公式并转换为 LaTeX
   - `Markdown→UnicodeMath`：提取并转换为 UnicodeMath 格式
   - `LaTeX→UnicodeMath`：直接转换 LaTeX 为 UnicodeMath

2. **输入公式**
   - 在输入框中粘贴 Markdown 或 LaTeX 公式
   - 支持 `$...$`、`$$...$$`、`\`\`\`math` 等格式

3. **转换与使用**
   - 点击"转换"按钮生成结果
   - 点击"复制结果"复制到剪贴板
   - 在 Word 中粘贴到公式框或文档中

## 📋 支持的公式格式

### Markdown 输入
```markdown
行内公式：$E = mc^2$

展示公式：
$$\lim_{n \to \infty} \sum_{i=1}^{n} \frac{1}{i^2} = \frac{\pi^2}{6}$$

代码块公式：
```math
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
```
```

### LaTeX 输入
```latex
\frac{-b \pm \sqrt{b^2-4ac}}{2a}
\sum_{k=1}^n k = \frac{n(n+1)}{2}
```

## 🔧 配置选项

- **LaTeX 输出包装**（仅 Markdown→LaTeX 模式）：
  - 保持原样：根据原格式自动选择
  - 强制行内：`$...$`
  - 强制展示：`$$...$$`

## ⚠️ 注意事项

### 环境与依赖
- 请在同一环境中安装依赖并运行（conda/venv 二选一）
- 建议使用：`python -m pip install -r requirements.txt` 确保 pip 与当前 python 一致
- 使用 conda 时，确保已激活正确的环境：`conda activate formula-converter`

### 快捷方式管理
- **删除开始菜单快捷方式**：
  ```powershell
  Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\公式转换工具.lnk"
  ```
- **移动桌面快捷方式**：支持，直接拖动到任意文件夹
- 项目文件夹移动后需重新运行 `create_shortcut.py` 以生成新的指向路径

### 常见问题
- **运行找不到模块**：请确认在正确环境安装依赖并运行；可执行 `where python`、`pip -V` 检查
- **conda 环境未激活**：确保执行 `conda activate formula-converter` 后再运行程序
- **PowerShell 执行策略被拦截**：
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/liu-ljh/formula-converter.git
cd formula-converter

# 创建开发环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或 .venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_conversion.py

# 启动应用
python main.py
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [PySide6](https://pypi.org/project/PySide6/) - 跨平台 GUI 框架
- [Pandoc](https://pandoc.org/) - 文档转换工具
- [pywin32](https://pypi.org/project/pywin32/) - Python Windows 扩展

## 📞 联系方式

- 项目链接：[https://github.com/liu-ljh/formula-converter](https://github.com/liu-ljh/formula-converter)
- 问题反馈：[Issues](https://github.com/liu-ljh/formula-converter/issues)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！