import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QFrame,
    QScrollArea,
    QGroupBox,
    QStatusBar,
    QProgressBar,
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
import pyperclip

from markdown_to_latex import extract_first_formula_latex, normalize_latex_for_word, extract_all_formulas, validate_latex
from latex_to_unicodemath import latex_to_unicodemath


class FormulaTool(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("公式转换工具 - Markdown/LaTeX 转 Word 公式")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(self._get_stylesheet())

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)

        # 标题区域
        self._create_header(main_layout)
        
        # 输入区域
        self._create_input_section(main_layout)
        
        # 选项区域
        self._create_options_section(main_layout)
        
        # 输出区域
        self._create_output_section(main_layout)
        
        # 按钮区域
        self._create_button_section(main_layout)
        
        # 状态栏
        self._create_status_bar(main_layout)

        # 连接信号
        self._connect_signals()

    def _get_stylesheet(self) -> str:
        return """
        QWidget {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #495057;
        }
        
        QTextEdit {
            border: 2px solid #e9ecef;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            background-color: white;
        }
        
        QTextEdit:focus {
            border-color: #007bff;
        }
        
        QComboBox {
            border: 2px solid #e9ecef;
            border-radius: 4px;
            padding: 6px 12px;
            background-color: white;
            min-width: 120px;
        }
        
        QComboBox:focus {
            border-color: #007bff;
        }
        
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background-color: #0056b3;
        }
        
        QPushButton:pressed {
            background-color: #004085;
        }
        
        QPushButton#copyBtn {
            background-color: #28a745;
        }
        
        QPushButton#copyBtn:hover {
            background-color: #1e7e34;
        }
        
        QLabel {
            color: #495057;
            font-weight: 500;
        }
        
        QStatusBar {
            background-color: #e9ecef;
            border-top: 1px solid #dee2e6;
        }
        """

    def _create_header(self, layout: QVBoxLayout) -> None:
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("公式转换工具")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        subtitle = QLabel("Markdown / LaTeX 转 Word 公式的图形化工具")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                background: transparent;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_frame)

    def _create_input_section(self, layout: QVBoxLayout) -> None:
        input_group = QGroupBox("输入区域")
        input_layout = QVBoxLayout(input_group)
        
        input_label = QLabel("输入文本（依据转换模式：Markdown 或 LaTeX）")
        input_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.txt_input = QTextEdit()
        self.txt_input.setPlaceholderText(
            "示例 Markdown：\n"
            "在文本中有 $E = mc^2$ 或者：\n\n"
            "$$\\lim_{n \\to \\infty} \\sum_{i=1}^{n} \\frac{1}{i^2} = \\frac{\\pi^2}{6}$$\n\n"
            "```math\n"
            "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}\n"
            "```\n\n"
            "示例 LaTeX：\n"
            "\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}"
        )
        self.txt_input.setMinimumHeight(120)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.txt_input)
        layout.addWidget(input_group)

    def _create_options_section(self, layout: QVBoxLayout) -> None:
        options_group = QGroupBox("转换选项")
        options_layout = QVBoxLayout(options_group)
        
        # 转换模式
        mode_row = QHBoxLayout()
        mode_label = QLabel("转换模式：")
        mode_label.setStyleSheet("font-weight: bold;")
        
        self.combo_mode = QComboBox()
        self.combo_mode.addItems([
            "Markdown→LaTeX",
            "Markdown→UnicodeMath", 
            "LaTeX→UnicodeMath",
        ])
        
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.combo_mode)
        mode_row.addStretch()
        
        # LaTeX 包装选项
        wrap_row = QHBoxLayout()
        wrap_label = QLabel("LaTeX 输出包装：")
        wrap_label.setStyleSheet("font-weight: bold;")
        
        self.combo_wrap = QComboBox()
        self.combo_wrap.addItems(["保持原样", "强制行内 $...$", "强制展示 $$...$$"])
        
        wrap_row.addWidget(wrap_label)
        wrap_row.addWidget(self.combo_wrap)
        wrap_row.addStretch()
        
        options_layout.addLayout(mode_row)
        options_layout.addLayout(wrap_row)
        layout.addWidget(options_group)

    def _create_output_section(self, layout: QVBoxLayout) -> None:
        output_group = QGroupBox("转换结果")
        output_layout = QVBoxLayout(output_group)
        
        output_label = QLabel("转换结果（可复制到剪贴板）")
        output_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setMinimumHeight(120)
        self.txt_output.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
            }
        """)
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.txt_output)
        layout.addWidget(output_group)

    def _create_button_section(self, layout: QVBoxLayout) -> None:
        btn_layout = QHBoxLayout()
        
        self.btn_convert = QPushButton("🔄 转换")
        self.btn_convert.setMinimumHeight(40)
        
        self.btn_copy = QPushButton("📋 复制结果")
        self.btn_copy.setObjectName("copyBtn")
        self.btn_copy.setMinimumHeight(40)
        
        btn_layout.addWidget(self.btn_convert)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)

    def _create_status_bar(self, layout: QVBoxLayout) -> None:
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("就绪")
        layout.addWidget(self.status_bar)

    def _connect_signals(self) -> None:
        self.btn_convert.clicked.connect(self.on_convert)
        self.btn_copy.clicked.connect(self.on_copy)
        self.combo_mode.currentTextChanged.connect(self.on_mode_changed)
        self.txt_input.textChanged.connect(self.on_input_changed)

    def on_mode_changed(self, mode: str) -> None:
        """转换模式改变时的处理"""
        if "LaTeX" in mode:
            self.combo_wrap.setEnabled(True)
        else:
            self.combo_wrap.setEnabled(False)
        self._update_status(f"已切换到 {mode} 模式")

    def on_input_changed(self) -> None:
        """输入文本改变时的处理"""
        text = self.txt_input.toPlainText().strip()
        if text:
            self._update_status(f"输入文本长度: {len(text)} 字符")
        else:
            self._update_status("就绪")

    def _update_status(self, message: str) -> None:
        """更新状态栏"""
        self.status_bar.showMessage(message)

    def _md_to_latex(self, md_text: str) -> str:
        """Markdown 转 LaTeX"""
        latex, display_mode = extract_first_formula_latex(md_text)
        if latex is None:
            return ""
        
        wrapping = self.combo_wrap.currentText()
        if wrapping == "强制行内 $...$":
            return f"${latex}$"
        elif wrapping == "强制展示 $$...$$":
            return f"$${latex}$$"
        else:
            return f"$${latex}$$" if display_mode == "display" else f"${latex}$"

    def _md_to_unimath(self, md_text: str) -> str:
        """Markdown 转 UnicodeMath"""
        latex, _ = extract_first_formula_latex(md_text)
        if latex is None:
            return ""
        return latex_to_unicodemath(latex)

    def _latex_to_unimath(self, latex_text: str) -> str:
        """LaTeX 转 UnicodeMath"""
        # 验证 LaTeX 语法
        is_valid, error_msg = validate_latex(latex_text)
        if not is_valid:
            raise ValueError(f"LaTeX 语法错误：{error_msg}")
        
        return latex_to_unicodemath(latex_text)

    def on_convert(self) -> None:
        """转换按钮点击事件"""
        text = self.txt_input.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "提示", "请输入 Markdown 或 LaTeX 文本。")
            return
        
        self._update_status("正在转换...")
        self.btn_convert.setEnabled(False)
        
        try:
            mode = self.combo_mode.currentText()
            if mode == "Markdown→LaTeX":
                result = self._md_to_latex(text)
                if not result:
                    QMessageBox.warning(self, "未找到公式", 
                        "未检测到 $...$、$$...$$ 或 ```math 公式块。\n\n"
                        "请检查输入格式或尝试其他转换模式。")
                    self._update_status("转换失败：未找到公式")
                    return
            elif mode == "Markdown→UnicodeMath":
                result = self._md_to_unimath(text)
                if not result:
                    QMessageBox.warning(self, "未找到公式", 
                        "未检测到 $...$、$$...$$ 或 ```math 公式块。\n\n"
                        "请检查输入格式或尝试其他转换模式。")
                    self._update_status("转换失败：未找到公式")
                    return
            else:  # LaTeX→UnicodeMath
                result = self._latex_to_unimath(text)
            
            self.txt_output.setPlainText(result)
            self._update_status(f"转换完成：{mode}")
            
        except Exception as e:
            QMessageBox.critical(self, "转换错误", f"转换过程中发生错误：\n{str(e)}")
            self._update_status("转换失败")
        finally:
            self.btn_convert.setEnabled(True)

    def on_copy(self) -> None:
        """复制按钮点击事件"""
        out = self.txt_output.toPlainText().strip()
        if not out:
            QMessageBox.information(self, "提示", "请先完成转换再复制。")
            return
        
        try:
            pyperclip.copy(out)
            QMessageBox.information(self, "复制成功", "结果已复制到剪贴板。\n\n可以直接粘贴到 Word 公式框或其他文档中。")
            self._update_status("已复制到剪贴板")
        except Exception as e:
            QMessageBox.critical(self, "复制失败", f"复制到剪贴板时发生错误：\n{str(e)}")
            self._update_status("复制失败")



def main() -> None:
    app = QApplication(sys.argv)
    w = FormulaTool()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
