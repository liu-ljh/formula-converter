#!/usr/bin/env python3
"""
公式转换工具测试脚本
用于验证各种转换功能是否正常工作
"""

from markdown_to_latex import extract_first_formula_latex, extract_all_formulas, validate_latex
from latex_to_unicodemath import latex_to_unicodemath

def test_markdown_extraction():
    """测试 Markdown 公式提取"""
    print("=== 测试 Markdown 公式提取 ===")
    
    test_cases = [
        "行内公式：$E = mc^2$",
        "显示公式：$$\\frac{a}{b} = c$$",
        "代码块：\n```math\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n```",
        "混合：文本 $x^2$ 和 $$\\int_0^1 f(x)dx$$ 公式"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {text[:30]}...")
        latex, mode = extract_first_formula_latex(text)
        if latex:
            print(f"  提取成功: {latex}")
            print(f"  模式: {mode}")
        else:
            print("  未找到公式")
        
        # 测试多公式提取
        all_formulas = extract_all_formulas(text)
        print(f"  找到 {len(all_formulas)} 个公式")

def test_latex_validation():
    """测试 LaTeX 语法验证"""
    print("\n=== 测试 LaTeX 语法验证 ===")
    
    test_cases = [
        ("\\frac{a}{b}", True),
        ("\\sum_{i=1}^n i", True),
        ("\\frac{a}{b", False),  # 缺少右括号
        ("\\left(\\frac{a}{b}\\right)", True),
        ("\\left[\\frac{a}{b}", False),  # 括号不匹配
        ("", False),  # 空公式
    ]
    
    for latex, expected in test_cases:
        is_valid, msg = validate_latex(latex)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {latex[:20]:<20} -> {msg}")

def test_unicodemath_conversion():
    """测试 UnicodeMath 转换"""
    print("\n=== 测试 UnicodeMath 转换 ===")
    
    test_cases = [
        "\\frac{a}{b}",
        "\\sum_{i=1}^n i",
        "\\int_0^1 f(x) dx",
        "\\alpha + \\beta = \\gamma",
        "\\sqrt{x^2 + y^2}",
        "\\lim_{n \\to \\infty} \\frac{1}{n} = 0"
    ]
    
    for latex in test_cases:
        try:
            um = latex_to_unicodemath(latex)
            print(f"✓ {latex:<30} -> {um}")
        except Exception as e:
            print(f"✗ {latex:<30} -> 错误: {e}")

def test_integration():
    """测试完整转换流程"""
    print("\n=== 测试完整转换流程 ===")
    
    markdown_text = """
    这是一个测试文档，包含多个公式：
    
    行内公式：$E = mc^2$
    
    显示公式：
    $$\\lim_{n \\to \\infty} \\sum_{i=1}^{n} \\frac{1}{i^2} = \\frac{\\pi^2}{6}$$
    
    代码块公式：
    ```math
    \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
    ```
    """
    
    print("原始 Markdown:")
    print(markdown_text)
    
    # 提取所有公式
    formulas = extract_all_formulas(markdown_text)
    print(f"\n找到 {len(formulas)} 个公式:")
    
    for i, formula in enumerate(formulas, 1):
        print(f"\n公式 {i}:")
        print(f"  类型: {formula['type']}")
        print(f"  内容: {formula['content']}")
        
        # 转换为 UnicodeMath
        try:
            um = latex_to_unicodemath(formula['content'])
            print(f"  UnicodeMath: {um}")
        except Exception as e:
            print(f"  转换错误: {e}")

if __name__ == "__main__":
    print("公式转换工具 - 功能测试")
    print("=" * 50)
    
    try:
        test_markdown_extraction()
        test_latex_validation()
        test_unicodemath_conversion()
        test_integration()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
