import re
from typing import Optional, Tuple, List, Dict

INLINE_PATTERN = re.compile(r"\$(.+?)\$", re.DOTALL)
DISPLAY_PATTERN = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
FENCED_MATH_PATTERN = re.compile(r"```(?:math|latex)\n([\s\S]+?)\n```", re.IGNORECASE)


def extract_first_formula_latex(markdown_text: str) -> Tuple[Optional[str], Optional[str]]:
    text = markdown_text.strip()
    # prefer fenced block, then display, then inline
    fenced = FENCED_MATH_PATTERN.search(text)
    if fenced:
        content = fenced.group(1).strip()
        return content, "display"
    display = DISPLAY_PATTERN.search(text)
    if display:
        content = display.group(1).strip()
        return content, "display"
    inline = INLINE_PATTERN.search(text)
    if inline:
        content = inline.group(1).strip()
        return content, "inline"
    # as a fallback, treat the whole text as latex if it seems latex-like
    if any(token in text for token in ["\\frac", "\\sum", "\\int", "\\alpha", "\\beta", "\\gamma", "^", "_"]):
        return text, "inline"
    return None, None


def extract_all_formulas(markdown_text: str) -> List[Dict[str, str]]:
    """提取所有公式，返回包含公式内容和类型信息的列表"""
    text = markdown_text.strip()
    formulas = []
    
    # 提取 fenced 代码块
    for match in FENCED_MATH_PATTERN.finditer(text):
        content = match.group(1).strip()
        formulas.append({
            'content': content,
            'type': 'fenced',
            'display_mode': 'display',
            'start': match.start(),
            'end': match.end()
        })
    
    # 提取显示公式
    for match in DISPLAY_PATTERN.finditer(text):
        content = match.group(1).strip()
        formulas.append({
            'content': content,
            'type': 'display',
            'display_mode': 'display',
            'start': match.start(),
            'end': match.end()
        })
    
    # 提取行内公式
    for match in INLINE_PATTERN.finditer(text):
        content = match.group(1).strip()
        formulas.append({
            'content': content,
            'type': 'inline',
            'display_mode': 'inline',
            'start': match.start(),
            'end': match.end()
        })
    
    # 按位置排序
    formulas.sort(key=lambda x: x['start'])
    return formulas


def normalize_latex_for_word(latex: str) -> str:
    """标准化 LaTeX 以适配 Word"""
    s = latex.replace("\r", "").strip()
    # 合并换行符
    s = re.sub(r"\n+", " ", s)
    # 常见替换
    s = s.replace("\\dfrac", "\\frac")
    s = s.replace("\\left(", "(")
    s = s.replace("\\right)", ")")
    s = s.replace("\\left[", "[")
    s = s.replace("\\right]", "]")
    return s


def validate_latex(latex: str) -> Tuple[bool, str]:
    """验证 LaTeX 语法"""
    if not latex.strip():
        return False, "空公式"
    
    # 检查括号匹配
    paren_count = 0
    bracket_count = 0
    brace_count = 0
    
    for char in latex:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        elif char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
    
    if paren_count != 0:
        return False, f"括号不匹配：缺少 {abs(paren_count)} 个 {'(' if paren_count > 0 else ')'}"
    if bracket_count != 0:
        return False, f"方括号不匹配：缺少 {abs(bracket_count)} 个 {'[' if bracket_count > 0 else ']'}"
    if brace_count != 0:
        return False, f"花括号不匹配：缺少 {abs(brace_count)} 个 {'{' if brace_count > 0 else '}'}"
    
    return True, "语法正确"
