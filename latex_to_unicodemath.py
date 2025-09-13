import re
from typing import Dict

# Common Greek and operator symbols
_SYMBOLS: Dict[str, str] = {
    "\\alpha": "α", "\\beta": "β", "\\gamma": "γ", "\\delta": "δ", "\\epsilon": "ϵ", "\\varepsilon": "ε",
    "\\zeta": "ζ", "\\eta": "η", "\\theta": "θ", "\\vartheta": "ϑ", "\\iota": "ι", "\\kappa": "κ",
    "\\lambda": "λ", "\\mu": "μ", "\\nu": "ν", "\\xi": "ξ", "\\pi": "π", "\\varpi": "ϖ",
    "\\rho": "ρ", "\\varrho": "ϱ", "\\sigma": "σ", "\\varsigma": "ς", "\\tau": "τ", "\\upsilon": "υ",
    "\\phi": "φ", "\\varphi": "ϕ", "\\chi": "χ", "\\psi": "ψ", "\\omega": "ω",
    "\\Gamma": "Γ", "\\Delta": "Δ", "\\Theta": "Θ", "\\Lambda": "Λ", "\\Xi": "Ξ", "\\Pi": "Π",
    "\\Sigma": "Σ", "\\Upsilon": "Υ", "\\Phi": "Φ", "\\Psi": "Ψ", "\\Omega": "Ω",
    "\\pm": "±", "\\mp": "∓", "\\times": "×", "\\cdot": "⋅", "\\div": "÷", "\\leq": "≤", "\\geq": "≥", "\\neq": "≠",
    "\\approx": "≈", "\\sim": "∼", "\\propto": "∝", "\\infty": "∞", "\\partial": "∂", "\\nabla": "∇",
    "\\rightarrow": "→", "\\leftarrow": "←", "\\leftrightarrow": "↔", "\\Rightarrow": "⇒", "\\Leftarrow": "⇐", "\\Leftrightarrow": "⇔",
    "\\to": "→", "\\sum": "∑", "\\prod": "∏", "\\int": "∫", "\\iint": "∬", "\\iiint": "∭",
    "\\cdots": "⋯", "\\ldots": "…", "\\dots": "…",
}

# Common function names, output as plain text (UnicodeMath uses same identifiers)
_FUNCS = [
    "sin", "cos", "tan", "cot", "sec", "csc",
    "arcsin", "arccos", "arctan",
    "sinh", "cosh", "tanh", "coth",
    "log", "ln", "exp", "max", "min",
]

# Regex patterns
_DEFOP_RE = re.compile(r"\\operatorname\*?\{([^}]+)\}")
_FRAC_CAP_RE = re.compile(r"\\frac\s*\{([^}]*)\}\s*\{([^}]*)\}")
_SQRT_RE = re.compile(r"\\sqrt\s*\{([^}]*)\}")
_SQRT_N_RE = re.compile(r"\\sqrt\s*\[([^\]]+)\]\s*\{([^}]*)\}")
_TEXT_RM_RE = re.compile(r"\\mathrm\s*\{([^}]*)\}")
_TEXT_RE = re.compile(r"\\text\s*\{([^}]*)\}")
_BINOM_RE = re.compile(r"\\binom\s*\{([^}]*)\}\s*\{([^}]*)\}")
_MATHBB_RE = re.compile(r"\\mathbb\s*\{([A-Za-z])\}")
# Large operator sub/sup
_LARGE_OP_SUB = re.compile(r"\\(sum|prod)\s*_\{([^}]*)\}")
_LARGE_OP_SUP = re.compile(r"(∑|∏)\s*\^\{([^}]*)\}")
# lim with subscript
_LIM_SUB = re.compile(r"\\lim\s*_\{([^}]*)\}")
# generic ^/_ brace collapsing
_SUP_BRACED = re.compile(r"\^\{([^}]*)\}")
_SUB_BRACED = re.compile(r"_\{([^}]*)\}")

# Combining marks
_COMB_OVERLINE = "\u0305"
_COMB_HAT = "\u0302"
_COMB_DOT = "\u0307"
_COMB_DDOT = "\u0308"
_COMB_VEC = "\u20D7"

_ACCENTS = {
    re.compile(r"\\bar\s*\{([^}]*)\}"): _COMB_OVERLINE,
    re.compile(r"\\overline\s*\{([^}]*)\}"): _COMB_OVERLINE,
    re.compile(r"\\hat\s*\{([^}]*)\}"): _COMB_HAT,
    re.compile(r"\\dot\s*\{([^}]*)\}"): _COMB_DOT,
    re.compile(r"\\ddot\s*\{([^}]*)\}"): _COMB_DDOT,
    re.compile(r"\\vec\s*\{([^}]*)\}"): _COMB_VEC,
}

# map common mathbb letters
_MATHBB_MAP = {
    "R": "ℝ", "N": "ℕ", "Z": "ℤ", "Q": "ℚ", "C": "ℂ", "H": "ℍ",
}


def _strip_formatting_tokens(s: str) -> str:
    tokens = ["\\left", "\\right", "\\;", "\\,", "\\!", "\\: ", "\\:\n", "\\quad", "\\qquad"]
    for t in tokens:
        s = s.replace(t, "")
    return s


def _apply_functions(s: str) -> str:
    for fn in _FUNCS:
        s = re.sub(rf"\\{fn}(?=\b)", fn, s)
    return s


def _apply_symbols(s: str) -> str:
    for k, v in _SYMBOLS.items():
        s = s.replace(k, v)
    return s


def _apply_text_modes(s: str) -> str:
    s = _DEFOP_RE.sub(lambda m: m.group(1), s)
    s = _TEXT_RM_RE.sub(lambda m: m.group(1), s)
    s = _TEXT_RE.sub(lambda m: m.group(1), s)
    return s


def _apply_accents(s: str) -> str:
    for regex, comb in _ACCENTS.items():
        s = regex.sub(lambda m: "".join(ch + comb for ch in m.group(1)), s)
    return s


def _apply_mathbb(s: str) -> str:
    def repl(m: re.Match) -> str:
        ch = m.group(1)
        return _MATHBB_MAP.get(ch, ch)
    return _MATHBB_RE.sub(repl, s)


def _apply_sqrt_frac_binom_iteratively(s: str) -> str:
    changed = True
    while changed:
        before = s
        s = _SQRT_N_RE.sub(lambda m: f"√[{m.group(1)}]({m.group(2)})", s)
        s = _SQRT_RE.sub(lambda m: f"√({m.group(1)})", s)
        s = _FRAC_CAP_RE.sub(lambda m: f"({m.group(1)})/({m.group(2)})", s)
        s = _BINOM_RE.sub(lambda m: f"C({m.group(1)},{m.group(2)})", s)
        changed = (s != before)
    return s


def _apply_large_ops(s: str) -> str:
    # sum/prod subscripts -> symbols with _()
    s = _LARGE_OP_SUB.sub(lambda m: ("∑" if m.group(1) == "sum" else "∏") + f"_({m.group(2)})", s)
    # superscripts for already converted symbols
    s = _LARGE_OP_SUP.sub(lambda m: m.group(1) + f"^{m.group(2)}", s)
    # lim subscript -> lim_(...)
    s = _LIM_SUB.sub(lambda m: f"lim_({m.group(1)})", s)
    return s


def _collapse_braced_sup_sub(s: str) -> str:
    # Convert a^{bc} -> a^bc; a_{ij} -> a_(ij)
    s = _SUP_BRACED.sub(lambda m: "^" + (m.group(1) if len(m.group(1)) == 1 else m.group(1)), s)
    s = _SUB_BRACED.sub(lambda m: "_" + (m.group(1) if len(m.group(1)) == 1 else f"({m.group(1)})"), s)
    return s


def latex_to_unicodemath(latex: str) -> str:
    s = latex.replace("\r", "")
    s = _strip_formatting_tokens(s)
    s = _apply_text_modes(s)
    s = _apply_functions(s)
    # core transformations
    s = _apply_sqrt_frac_binom_iteratively(s)
    s = _apply_large_ops(s)
    s = _collapse_braced_sup_sub(s)
    # accents/symbols/mathbb
    s = _apply_accents(s)
    s = _apply_symbols(s)
    s = _apply_mathbb(s)
    # whitespace normalize
    s = re.sub(r"\s+", " ", s).strip()
    return s
