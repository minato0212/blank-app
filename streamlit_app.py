import streamlit as st
import random
import time
import math
from fractions import Fraction

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="数学バトル",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
    --bg:       #0d0f1a;
    --surface:  #161829;
    --card:     #1e2136;
    --border:   #2e3260;
    --accent1:  #5b7fff;
    --accent2:  #ff5b8a;
    --gold:     #ffd700;
    --green:    #3dffb0;
    --text:     #e8ecff;
    --muted:    #7880aa;
    --radius:   14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Zen Kaku Gothic New', sans-serif;
}

[data-testid="stSidebar"] { background: var(--surface) !important; }

h1,h2,h3 { color: var(--text); font-weight: 900; }

/* ボタン全般 */
.stButton > button {
    background: linear-gradient(135deg, var(--accent1), #7b5fff);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    font-family: 'Zen Kaku Gothic New', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    padding: .65rem 1.6rem;
    cursor: pointer;
    transition: transform .15s, box-shadow .15s;
    box-shadow: 0 4px 20px rgba(91,127,255,.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(91,127,255,.55);
}
.stButton > button:active { transform: translateY(0); }

/* テキスト入力 */
.stTextInput > div > div > input {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.3rem !important;
    padding: .55rem .9rem !important;
    caret-color: var(--accent1);
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent1) !important;
    box-shadow: 0 0 0 3px rgba(91,127,255,.25) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: .85rem !important; }

/* セレクトボックス */
.stSelectbox > div > div {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
}
.stMultiSelect > div > div {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* スライダー */
.stSlider { color: var(--accent1) !important; }

/* プログレスバー */
.stProgress > div > div > div { background: var(--accent1) !important; }

/* 区切り線 */
hr { border-color: var(--border) !important; }

/* カスタムカード */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.card-accent {
    border-left: 4px solid var(--accent1);
}
.card-gold {
    border-left: 4px solid var(--gold);
    background: linear-gradient(135deg, #1e2136, #25201a);
}
.card-green {
    border-left: 4px solid var(--green);
    background: linear-gradient(135deg, #1e2136, #182520);
}
.card-red {
    border-left: 4px solid var(--accent2);
    background: linear-gradient(135deg, #1e2136, #251822);
}

/* 問題文 */
.question-box {
    background: linear-gradient(135deg, #1a1d35, #1e2245);
    border: 2px solid var(--accent1);
    border-radius: var(--radius);
    padding: 1.5rem 2rem;
    font-size: 1.45rem;
    font-weight: 700;
    text-align: center;
    color: #fff;
    margin: 1rem 0;
    box-shadow: 0 0 30px rgba(91,127,255,.2);
    letter-spacing: .03em;
}

/* スコア表示 */
.score-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1rem;
}
.score-box {
    flex: 1;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: .8rem 1rem;
    text-align: center;
}
.score-label { font-size: .75rem; color: var(--muted); margin-bottom: .2rem; }
.score-value { font-size: 2rem; font-weight: 900; }
.score-player { color: var(--accent1); }
.score-ai     { color: var(--accent2); }
.score-q      { color: var(--gold); }

/* タイマー */
.timer-box {
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: .6rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    letter-spacing: .1em;
}
.timer-warn { color: var(--accent2) !important; border-color: var(--accent2) !important; }
.timer-ok   { color: var(--green) !important; }

/* 解説 */
.explanation {
    background: linear-gradient(135deg, #182028, #1a1e30);
    border: 1px solid #2e5060;
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    font-size: .95rem;
    line-height: 1.8;
    margin-top: .8rem;
}
.explanation-title {
    color: var(--gold);
    font-weight: 900;
    font-size: 1.05rem;
    margin-bottom: .5rem;
}
.step {
    background: rgba(91,127,255,.1);
    border-left: 3px solid var(--accent1);
    padding: .35rem .8rem;
    margin: .4rem 0;
    border-radius: 0 6px 6px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: .92rem;
}

/* バッジ */
.badge {
    display: inline-block;
    padding: .2rem .7rem;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 700;
}
.badge-blue   { background: rgba(91,127,255,.2); color: var(--accent1); border: 1px solid var(--accent1); }
.badge-red    { background: rgba(255,91,138,.2); color: var(--accent2); border: 1px solid var(--accent2); }
.badge-gold   { background: rgba(255,215,0,.15); color: var(--gold);   border: 1px solid var(--gold); }
.badge-green  { background: rgba(61,255,176,.15); color: var(--green);  border: 1px solid var(--green); }

/* タイトル */
.main-title {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .2rem;
}
.sub-title {
    text-align: center;
    color: var(--muted);
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* ランク表示 */
.rank-card {
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    margin-bottom: .6rem;
    cursor: pointer;
    transition: transform .15s;
    border: 2px solid transparent;
}
.rank-card:hover { transform: translateX(4px); }
.rank-easy   { background: linear-gradient(135deg, #1a2818, #1e3020); border-color: var(--green); }
.rank-normal { background: linear-gradient(135deg, #18202a, #1e2a38); border-color: var(--accent1); }
.rank-hard   { background: linear-gradient(135deg, #2a1820, #38201e); border-color: var(--accent2); }

/* アニメーション */
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.6} }
@keyframes slideIn { from{transform:translateY(-10px);opacity:0} to{transform:translateY(0);opacity:1} }
.animate-in { animation: slideIn .3s ease forwards; }

/* 正解・不正解 */
.result-correct {
    background: linear-gradient(135deg, #0d2818, #102a1e);
    border: 2px solid var(--green);
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    text-align: center;
    color: var(--green);
    font-size: 1.3rem;
    font-weight: 900;
    animation: slideIn .3s ease;
}
.result-wrong {
    background: linear-gradient(135deg, #280d18, #2a1020);
    border: 2px solid var(--accent2);
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    text-align: center;
    color: var(--accent2);
    font-size: 1.3rem;
    font-weight: 900;
    animation: slideIn .3s ease;
}

/* 無限モード */
.practice-header {
    background: linear-gradient(135deg, #1a2035, #202540);
    border: 1px solid var(--accent1);
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PROBLEM GENERATOR
# ─────────────────────────────────────────────

TOPICS = {
    "整数・分数の計算": "arithmetic",
    "文字式・方程式（1次）": "linear_eq",
    "連立方程式": "simultaneous",
    "2次方程式": "quadratic",
    "因数分解": "factoring",
    "平方根・無理数": "sqrt",
    "展開公式": "expansion",
    "比例・反比例": "proportion",
    "一次関数": "linear_func",
    "二次関数": "quadratic_func",
    "確率・場合の数": "probability",
    "数列（等差・等比）": "sequence",
    "指数・対数": "exp_log",
    "三角比": "trigonometry",
    "ベクトル基礎": "vector",
    "集合・命題": "sets",
    "不等式": "inequality",
    "整数の性質": "number_theory",
}

def _r(a, b): return random.randint(a, b)
def _rc(exclude_zero=True):
    v = _r(-9,9)
    if exclude_zero and v == 0: v = _r(1,9)
    return v

# ── 各分野ごとの問題生成 ──────────────────────

def gen_arithmetic():
    kind = random.choice(["frac_add","frac_mul","mixed","power","divisor","lcm","gcd"])
    if kind == "frac_add":
        a,b,c,d = _r(1,9),_r(2,9),_r(1,9),_r(2,9)
        while b==d: d=_r(2,9)
        f1=Fraction(a,b); f2=Fraction(c,d); ans=f1+f2
        steps=[f"{a}/{b} + {c}/{d}",f"= {a*d}/{b*d} + {c*b}/{d*b}",f"= {a*d+c*b}/{b*d}",f"= {ans.numerator}/{ans.denominator}"]
        return f"\\( \\dfrac{{{a}}}{{{b}}} + \\dfrac{{{c}}}{{{d}}} \\) を計算せよ",f"{ans.numerator}/{ans.denominator}",steps,"整数・分数"
    if kind == "frac_mul":
        a,b,c,d = _r(1,9),_r(2,9),_r(1,9),_r(2,9)
        f1=Fraction(a,b); f2=Fraction(c,d); ans=f1*f2
        steps=[f"{a}/{b} × {c}/{d}",f"= {a*c}/{b*d}",f"= {ans.numerator}/{ans.denominator} （約分）"]
        return f"\\( \\dfrac{{{a}}}{{{b}}} \\times \\dfrac{{{c}}}{{{d}}} \\) を計算せよ",f"{ans.numerator}/{ans.denominator}",steps,"整数・分数"
    if kind == "mixed":
        a,b,c = _r(2,12),_r(2,12),_r(2,12)
        ans=a*b-c
        steps=[f"{a}×{b} - {c}",f"= {a*b} - {c}",f"= {ans}"]
        return f"\\( {a} \\times {b} - {c} \\) を計算せよ",str(ans),steps,"整数・分数"
    if kind == "power":
        base=_r(2,5); exp=_r(2,4)
        ans=base**exp
        steps=[f"{base}^{exp}",f"= {' × '.join([str(base)]*exp)}",f"= {ans}"]
        return f"\\( {base}^{{{exp}}} \\) を計算せよ",str(ans),steps,"整数・分数"
    if kind in ("lcm","gcd"):
        a,b = _r(2,20),_r(2,20)
        import math as _m
        g=_m.gcd(a,b); l=a*b//g
        if kind=="gcd":
            steps=[f"ユークリッドの互除法","gcd({a},{b})","= "+str(g)]
            return f"\\( \\gcd({a},{b}) \\) を求めよ",str(g),steps,"整数・分数"
        else:
            steps=[f"lcm({a},{b}) = {a}×{b} / gcd({a},{b})",f"= {a*b}/{g}",f"= {l}"]
            return f"\\( \\mathrm{{lcm}}({a},{b}) \\) を求めよ",str(l),steps,"整数・分数"
    # divisor
    n=_r(10,60)
    divs=[i for i in range(1,n+1) if n%i==0]
    steps=[f"{n}の約数を列挙",f"1から順に確認",f"= {', '.join(map(str,divs))}"]
    return f"{n} の正の約数の個数を求めよ",str(len(divs)),steps,"整数・分数"

def gen_linear_eq():
    kinds = ["ax_b","ax_bx_c","frac","word"]
    kind = random.choice(kinds)
    if kind == "ax_b":
        a=_rc(); b=_rc(); c=a*_rc()+b
        x=(c-b)
        if a==0: a=2
        if (c-b)%a!=0:
            a=2; b=_r(-5,5); x=_r(-8,8); c=a*x+b
        ans=str((c-b)//a)
        steps=[f"{a}x + {b} = {c}",f"{a}x = {c-b}",f"x = {c-b}/{a} = {ans}"]
        return f"\\( {a}x + {b} = {c} \\) を解け",ans,steps,"1次方程式"
    if kind == "ax_bx_c":
        a=_rc(); b=_rc(); x=_r(-8,8)
        c=(a-b)*x
        steps=[f"{a}x - {b}x = {c}",f"({a-b})x = {c}",f"x = {c}/({a-b}) = {x}"]
        if a==b: a+=1; c=(a-b)*x
        return f"\\( {a}x - {b}x = {c} \\) を解け",str(x),steps,"1次方程式"
    if kind == "frac":
        x=_r(-6,6); a=_r(2,4); b=_rc()
        lhs=x+b; rhs=a*x
        steps=[f"x + {b} = {a}x",f"{b} = {a-1}x",f"x = {b}/{a-1} = {x}"]
        if a==1: a=2; rhs=a*x
        return f"\\( x + {b} = {a}x \\) を解け",str(x),steps,"1次方程式"
    # word problem
    x=_r(1,20); rate=_r(2,5)
    total=x+rate*x
    steps=[f"小さい数をxとすると",f"x + {rate}x = {total}",f"{rate+1}x = {total}",f"x = {x}"]
    return f"2つの数の和が {total} で、一方が他方の {rate} 倍のとき、小さい方を求めよ",str(x),steps,"1次方程式"

def gen_simultaneous():
    x=_r(-5,5); y=_r(-5,5)
    a1,b1=_rc(),_rc(); c1=a1*x+b1*y
    a2,b2=_rc(),_rc()
    while a1*b2==a2*b1: a2=_rc()
    c2=a2*x+b2*y
    steps=[
        f"① {a1}x + {b1}y = {c1}",
        f"② {a2}x + {b2}y = {c2}",
        f"①×{b2} - ②×{b1}",
        f"({a1*b2-a2*b1})x = {c1*b2-c2*b1}",
        f"x = {x}",
        f"代入: y = {y}"
    ]
    return (f"連立方程式を解け：\\( {a1}x + {b1}y = {c1},\\; {a2}x + {b2}y = {c2} \\) （x,yをコンマ区切りで）",
            f"{x},{y}",steps,"連立方程式")

def gen_quadratic():
    kinds = ["standard","complete_sq","vieta"]
    kind = random.choice(kinds)
    if kind == "standard":
        p,q=_r(-6,6),_r(-6,6)
        while p==0 or q==0: p,q=_r(-6,6),_r(-6,6)
        a=1; b=-(p+q); c=p*q
        bstr=f"{'+'if b>=0 else ''}{b}" if b!=0 else ""
        cstr=f"{'+'if c>=0 else ''}{c}" if c!=0 else ""
        eq=f"x^2{bstr}x{cstr} = 0"
        s1,s2=sorted([p,q])
        steps=[f"x² {bstr}x {cstr} = 0を因数分解",f"(x - {p})(x - {q}) = 0",f"x = {p} または x = {q}"]
        ans=f"{s1},{s2}" if s1!=s2 else str(s1)
        return f"\\( {eq} \\) を解け（小さい順にコンマ区切り）",ans,steps,"2次方程式"
    if kind == "complete_sq":
        p=_r(-5,5); q=_r(1,16)
        ans_val=p*p+q
        steps=[f"x² - {2*p}x + ? = 0",f"(x - {p})² = {q}",f"x - {p} = ±√{q}",f"x = {p} ± √{q}"]
        return (f"\\( x^2 - {2*p}x + {p*p - q} = 0 \\) を解け（平方完成で）",
                f"{p}-√{q},{p}+√{q}" if q>0 else str(p),steps,"2次方程式")
    # vieta
    s=_r(-8,8); pr=_r(-20,20)
    steps=[f"解の和 = {s}","解の積 = "+str(pr),f"x² - ({s})x + {pr} = 0","解の和と積から直接読み取る"]
    return (f"2次方程式の解の和が {s}、積が {pr} のとき方程式を答えよ（x²の係数1）",
            f"x^2-{s}x+{pr}=0" if s>=0 else f"x^2+{-s}x+{pr}=0",steps,"2次方程式")

def gen_factoring():
    kinds = ["diff_sq","perfect_sq","common","trinomial","grouping"]
    kind = random.choice(kinds)
    if kind == "diff_sq":
        a=_r(1,9)
        expr=f"x²-{a**2}" if a>0 else f"x²-{a**2}"
        steps=[f"x² - {a**2}","= (x+{a})(x-{a})"]
        return f"\\( x^2 - {a**2} \\) を因数分解せよ",f"(x+{a})(x-{a})",steps,"因数分解"
    if kind == "perfect_sq":
        a=_r(1,8)
        expr=f"x²+{2*a}x+{a**2}"
        steps=[f"x² + {2*a}x + {a**2}","= (x + {a})²"]
        return f"\\( x^2 + {2*a}x + {a**2} \\) を因数分解せよ",f"(x+{a})^2",steps,"因数分解"
    if kind == "common":
        a=_r(2,6); b=_r(1,8); c=_r(1,8)
        steps=[f"{a}x² + {a*b}x + {a*c}",f"= {a}(x² + {b}x + {c})","共通因数 {a} をくくり出す"]
        return f"\\( {a}x^2 + {a*b}x + {a*c} \\) を因数分解せよ",f"{a}(x^2+{b}x+{c})",steps,"因数分解"
    if kind == "trinomial":
        p,q=_r(-6,6),_r(-6,6)
        while p==0 or q==0 or p==q: p,q=_r(-6,6),_r(-6,6)
        b=p+q; c=p*q
        bstr=(f"+{b}" if b>0 else str(b)) if b!=0 else ""
        cstr=(f"+{c}" if c>0 else str(c)) if c!=0 else ""
        steps=[f"x²{bstr}x{cstr}",f"積が{c}、和が{b}になる2数を探す",f"→ {p} と {q}",f"= (x+{p})(x+{q})"]
        return f"\\( x^2{bstr}x{cstr} \\) を因数分解せよ",f"(x+{p})(x+{q})",steps,"因数分解"
    # grouping
    a,b=_r(1,6),_r(1,6)
    steps=[f"x³ + {a}x² + {b}x + {a*b}",f"= x²(x+{a}) + {b}(x+{a})",f"= (x²+{b})(x+{a})"]
    return (f"\\( x^3 + {a}x^2 + {b}x + {a*b} \\) を因数分解せよ",
            f"(x^2+{b})(x+{a})",steps,"因数分解")

def gen_sqrt():
    kinds = ["simplify","calc","rationalize","compare"]
    kind = random.choice(kinds)
    if kind == "simplify":
        squares=[4,9,16,25,36]; sq=random.choice(squares)
        k=_r(1,4); n=sq*k*k*_r(2,5)
        import sympy as _s
        ans=str(_s.sqrt(n))
        steps=[f"√{n}",f"= √({sq}×{n//sq})",f"= {int(sq**0.5)}√{n//sq}",f"= {ans}"]
        return f"\\( \\sqrt{{{n}}} \\) を簡単にせよ",ans,steps,"平方根"
    if kind == "calc":
        a,b=_r(1,5),_r(1,5)
        ans=a*b
        steps=[f"√{a**2} × √{b**2}",f"= √({a**2}×{b**2})",f"= √{(a*b)**2}",f"= {ans}"]
        return f"\\( \\sqrt{{{a**2}}} \\times \\sqrt{{{b**2}}} \\) を計算せよ",str(ans),steps,"平方根"
    if kind == "rationalize":
        a=_r(1,5); b=_r(2,5)
        num=a; den=b
        # a/√b → a√b/b
        import math as _m; g=_m.gcd(a,b)
        steps=[f"{a}/√{b}",f"= {a}×√{b} / (√{b}×√{b})",f"= {a}√{b}/{b}",f"= {a//g}√{b}/{b//g}"]
        ans=f"{a//g}√{b}/{b//g}" if b//g>1 else f"{a//g}√{b}"
        return f"\\( \\dfrac{{{a}}}{{\\sqrt{{{b}}}}} \\) を有理化せよ",ans,steps,"平方根"
    # compare
    a,b=_r(2,6),_r(2,6); c,d=_r(1,4),_r(1,4)
    v1=a**2*c; v2=b**2*d
    sym=">" if v1>v2 else ("<" if v1<v2 else "=")
    steps=[f"{c}√{a} と {d}√{b}",f"= √{v1} と √{v2}",f"∵ {v1} {sym} {v2}",f"∴ {c}√{a} {sym} {d}√{b}"]
    return f"\\( {c}\\sqrt{{{a}}} \\) と \\( {d}\\sqrt{{{b}}} \\) を比較せよ（>, <, = で答えよ）",sym,steps,"平方根"

def gen_expansion():
    kinds = ["foil","sq_sum","sq_diff","cube","double_dist"]
    kind = random.choice(kinds)
    if kind == "foil":
        a,b,c,d=_r(1,6),_r(-6,6),_r(1,6),_r(-6,6)
        ac=a*c; ad=a*d; bc=b*c; bd=b*d; mid=ad+bc
        cstr=f"{'+'if mid>=0 else ''}{mid}x" if mid!=0 else ""
        dstr=f"{'+'if bd>=0 else ''}{bd}" if bd!=0 else ""
        steps=[f"({a}x+{b})({c}x+{d})",f"= {ac}x² + {ad}x + {bc}x + {bd}",f"= {ac}x²{cstr}{dstr}"]
        ans=f"{ac}x^2{('+' if mid>=0 else '')+(str(mid) if mid!=0 else '')}x{('+' if bd>=0 else '')+(str(bd) if bd!=0 else '')}"
        return f"\\( ({a}x+{b})({c}x+{d}) \\) を展開せよ",ans,steps,"展開"
    if kind == "sq_sum":
        a,b=_r(1,8),_r(1,8)
        steps=[f"(x+{a})²","= x² + 2·x·{a} + {a}²",f"= x² + {2*a}x + {a**2}"]
        return f"\\( (x+{a})^2 \\) を展開せよ",f"x^2+{2*a}x+{a**2}",steps,"展開"
    if kind == "sq_diff":
        a=_r(1,8)
        steps=[f"(x-{a})²","= x² - 2·x·{a} + {a}²",f"= x² - {2*a}x + {a**2}"]
        return f"\\( (x-{a})^2 \\) を展開せよ",f"x^2-{2*a}x+{a**2}",steps,"展開"
    if kind == "cube":
        a=_r(1,4)
        b3=3*a; b3sq=3*a**2; acube=a**3
        steps=[f"(x+{a})³","= x³ + 3x²·{a} + 3x·{a}² + {a}³",f"= x³ + {b3}x² + {b3sq}x + {acube}"]
        return f"\\( (x+{a})^3 \\) を展開せよ",f"x^3+{b3}x^2+{b3sq}x+{acube}",steps,"展開"
    # double dist
    a,b,c=_r(1,5),_r(1,5),_r(1,5)
    ans1=a+b+c; ans2=a*b+b*c+a*c; ans3=a*b*c
    steps=[f"(x+{a})(x+{b})(x+{c})",f"先に(x+{a})(x+{b}) = x²+{a+b}x+{a*b}",f"× (x+{c}) を分配",f"= x³+{ans1}x²+{ans2}x+{ans3}"]
    return f"\\( (x+{a})(x+{b})(x+{c}) \\) を展開せよ",f"x^3+{ans1}x^2+{ans2}x+{ans3}",steps,"展開"

def gen_proportion():
    kinds = ["direct","inverse","ratio","scale"]
    kind = random.choice(kinds)
    if kind == "direct":
        k=_r(2,8); x0=_r(1,6); y0=k*x0; x1=_r(1,10)
        steps=[f"y=kxにy={y0}, x={x0}を代入",f"k = {y0}/{x0} = {k}",f"y = {k}x",f"x={x1}のとき y = {k*x1}"]
        return f"y は x に比例し、x={x0} のとき y={y0}。x={x1} のときの y を求めよ",str(k*x1),steps,"比例・反比例"
    if kind == "inverse":
        k=_r(6,30); x0=_r(1,5)
        while k%x0!=0: k=_r(6,30)
        y0=k//x0; x1=_r(2,8)
        while k%x1!=0: x1=_r(2,8)
        steps=[f"y=k/xにy={y0}, x={x0}を代入",f"k = {x0}×{y0} = {k}",f"y = {k}/x",f"x={x1}のとき y = {k//x1}"]
        return f"y は x に反比例し、x={x0} のとき y={y0}。x={x1} のときの y を求めよ",str(k//x1),steps,"比例・反比例"
    if kind == "ratio":
        a,b,total=_r(2,5),_r(2,5),0
        while True:
            total=(a+b)*_r(2,8)
            if total>20: break
        ans=a*total//(a+b)
        steps=[f"全体を {a+b} に分けると",f"1当たり {total}//{a+b} = {total//(a+b)}",f"a側 = {a}×{total//(a+b)} = {ans}"]
        return f"{total} を {a}:{b} に分けたとき、大きい方を求めよ",str(max(a*total//(a+b),(b*total)//(a+b))),steps,"比例・反比例"
    # scale
    scale=_r(2,5)*10000; real=_r(3,15)*100
    map_len=real/scale*100
    steps=[f"縮尺 1:{scale}","地図上 = 実際の距離 ÷ 縮尺",f"= {real} cm ÷ {scale}",f"= {map_len:.1f} cm"]
    return f"縮尺 1:{scale} の地図で実際の {real} cm を地図上の長さ（cm）で答えよ",f"{map_len:.1f}",steps,"比例・反比例"

def gen_linear_func():
    kinds = ["slope_intercept","two_points","parallel","intersection"]
    kind = random.choice(kinds)
    if kind == "slope_intercept":
        m=_rc(); b=_rc()
        x=_r(-5,5)
        y=m*x+b
        steps=[f"y = {m}x + {b}",f"x = {x} を代入",f"y = {m}×{x} + {b}",f"y = {y}"]
        return f"y = {m}x + {b} において、x = {x} のとき y を求めよ",str(y),steps,"一次関数"
    if kind == "two_points":
        x1,y1,x2=_r(-5,5),_r(-5,5),_r(-5,5)
        while x1==x2: x2=_r(-5,5)
        m=_rc(); b=y1-m*x1; y2=m*x2+b
        steps=[f"傾き m = ({y2}-{y1})/({x2}-{x1})",f"= {y2-y1}/{x2-x1} = {m}",f"切片 b = {y1} - {m}×{x1} = {b}",f"y = {m}x + {b}"]
        bstr=f"{'+'if b>=0 else ''}{b}"
        return f"2点({x1},{y1}),({x2},{y2})を通る直線の式を求めよ",f"y={m}x{bstr}",steps,"一次関数"
    if kind == "parallel":
        m=_rc(); b1=_rc(); b2=_rc()
        while b1==b2: b2=_rc()
        b1str=f"{'+'if b1>=0 else ''}{b1}"
        b2str=f"{'+'if b2>=0 else ''}{b2}"
        steps=[f"平行線は傾きが等しい",f"傾き = {m}","y = {m}x + b に通過点を代入して b を求める",f"y = {m}x{b2str}"]
        return f"y = {m}x{b1str} に平行で y 切片が {b2} の直線を答えよ",f"y={m}x{b2str}",steps,"一次関数"
    # intersection
    m1,b1,m2=_rc(),_rc(),_rc()
    while m1==m2: m2=_rc()
    b2=_rc()
    x_int=Fraction(b2-b1,m1-m2)
    y_int=m1*x_int+b1
    if x_int.denominator==1 and y_int.denominator==1:
        x_int=int(x_int); y_int=int(y_int)
        steps=[f"{m1}x+{b1} = {m2}x+{b2}",f"{m1-m2}x = {b2-b1}",f"x = {x_int}",f"y = {y_int}"]
        return (f"y={m1}x+{b1} と y={m2}x+{b2} の交点を求めよ（x,yをコンマ区切り）",
                f"{x_int},{y_int}",steps,"一次関数")
    # fallback
    return gen_linear_func()

def gen_quadratic_func():
    kinds = ["vertex","axis","max_min","passes"]
    kind = random.choice(kinds)
    if kind == "vertex":
        h,k=_r(-5,5),_r(-5,5); a=random.choice([-2,-1,1,2])
        sign='+' if k>=0 else ''
        hsgn='-' if h>=0 else '+'
        steps=[f"y = {a}(x-{h})² + {k}",f"頂点は (h,k) = ({h},{k})"]
        return f"\\( y = {a}(x-{h})^2+{k} \\) の頂点を求めよ（x,yをコンマ区切り）",f"{h},{k}",steps,"二次関数"
    if kind == "axis":
        h=_r(-5,5); a=random.choice([-2,-1,1,2]); k=_r(-5,5)
        steps=[f"y = {a}(x-{h})² + {k}",f"軸は x = {h}"]
        return f"\\( y = {a}(x-{h})^2+{k} \\) の対称軸を求めよ",f"x={h}",steps,"二次関数"
    if kind == "max_min":
        h,k=_r(-4,4),_r(-4,4); a=random.choice([-2,-1,1,2])
        word="最小" if a>0 else "最大"
        steps=[f"y = {a}(x-{h})² + {k}",f"a={a} {'> 0 なので下に凸' if a>0 else '< 0 なので上に凸'}",f"x={h} で{'最小' if a>0 else '最大'} = {k}"]
        return f"\\( y = {a}(x-{h})^2+{k} \\) の{word}値を求めよ",str(k),steps,"二次関数"
    # passes through
    h,k=_r(-4,4),_r(-4,4); a=random.choice([-2,-1,1,2]); x0=_r(-5,5)
    y0=a*(x0-h)**2+k
    steps=[f"y = a(x-{h})² + {k}",f"x={x0}, y={y0}を代入",f"{y0} = a×({x0-h})² + {k}",f"a = ({y0-k})/{(x0-h)**2} = {a}"]
    return (f"頂点({h},{k})で点({x0},{y0})を通る放物線の a を求めよ（y=a(x-h)²+k）",
            str(a),steps,"二次関数")

def gen_probability():
    kinds = ["dice","card","coin","combination","conditional"]
    kind = random.choice(kinds)
    if kind == "dice":
        k=_r(1,6); n=random.choice([1,2])
        if n==1:
            steps=[f"サイコロ1個を投げる",f"全事象: 6通り",f"{k}以上: {7-k}通り",f"確率 = {7-k}/6"]
            return f"サイコロを1回投げて {k} 以上の目が出る確率を求めよ（分数で）",f"{7-k}/6",steps,"確率"
        else:
            fav=0; total=36
            for i in range(1,7):
                for j in range(1,7):
                    if i+j==k+5: fav+=1
            import math as _m; g=_m.gcd(fav,total)
            steps=[f"2つのサイコロの全事象: 36通り",f"和が{k+5}になる場合を数える",f"{fav}通り",f"確率 = {fav//g}/{total//g}"]
            return f"2つのサイコロを投げて目の和が {k+5} になる確率を求めよ（分数で）",f"{fav//g}/{total//g}",steps,"確率"
    if kind == "card":
        import math as _m
        n=_r(4,6); k=_r(1,min(3,n))
        total=_m.comb(n,k)
        # 赤いカード
        red=n//2; non_red=n-red
        fav=_m.comb(red,k) if red>=k else 0
        import math as _m2; g=_m2.gcd(fav,total) if total>0 and fav>0 else 1
        steps=[f"{n}枚のカード({red}枚赤,{non_red}枚青)から{k}枚を選ぶ",f"全事象: C({n},{k}) = {total}",f"全部赤: C({red},{k}) = {fav}",f"確率 = {fav}/{total} = {fav//g}/{total//g}"]
        if fav==0 or total==0: return gen_probability()
        return f"{n}枚のカード（赤{red}枚・青{non_red}枚）から{k}枚選ぶとき全部赤の確率（分数で）",f"{fav//g}/{total//g}",steps,"確率"
    if kind == "coin":
        n=_r(3,5); k=_r(1,n-1)
        import math as _m; fav=_m.comb(n,k); total=2**n
        g=_m.gcd(fav,total)
        steps=[f"コインを{n}回投げる",f"全事象: 2^{n} = {total}",f"ちょうど{k}回表: C({n},{k}) = {fav}",f"確率 = {fav//g}/{total//g}"]
        return f"コインを{n}回投げてちょうど{k}回表が出る確率（分数で）",f"{fav//g}/{total//g}",steps,"確率"
    if kind == "combination":
        import math as _m; n=_r(5,9); k=_r(2,n-2)
        ans=_m.comb(n,k)
        steps=[f"C({n},{k}) = {n}! / ({k}! × {n-k}!)",f"= {ans}"]
        return f"C({n},{k})を計算せよ",str(ans),steps,"確率"
    # conditional
    import math as _m; n=_r(3,5)
    # 6面体、偶数が出た条件で3以上の確率
    even=[2,4,6][:n] if n<=3 else [2,4,6]
    ge3=[i for i in even if i>=3]
    import math as _m2; g=_m2.gcd(len(ge3),len(even))
    steps=["条件付き確率 P(A|B) = P(A∩B)/P(B)",f"偶数: {even}",f"偶数かつ3以上: {ge3}",f"P = {len(ge3)}/{len(even)} = {len(ge3)//g}/{len(even)//g}"]
    return (f"サイコロで偶数が出たという条件のもと、3以上の確率を求めよ",
            f"{len(ge3)//g}/{len(even)//g}",steps,"確率")

def gen_sequence():
    kinds = ["arith_nth","arith_sum","geom_nth","geom_sum","mixed"]
    kind = random.choice(kinds)
    if kind == "arith_nth":
        a=_r(1,10); d=_r(-5,5); n=_r(5,15)
        ans=a+(n-1)*d
        steps=[f"初項 a={a}, 公差 d={d}",f"第{n}項 = a + (n-1)d",f"= {a} + {n-1}×{d}",f"= {ans}"]
        return f"初項 {a}、公差 {d} の等差数列の第 {n} 項を求めよ",str(ans),steps,"数列"
    if kind == "arith_sum":
        a=_r(1,10); d=_r(1,5); n=_r(5,15)
        last=a+(n-1)*d; ans=n*(a+last)//2
        steps=[f"初項{a}, 公差{d}, 項数{n}",f"末項 = {a}+{n-1}×{d} = {last}",f"S = {n}×({a}+{last})/2 = {ans}"]
        return f"初項 {a}、公差 {d} の等差数列の第 {n} 項までの和を求めよ",str(ans),steps,"数列"
    if kind == "geom_nth":
        a=_r(1,5); r=random.choice([2,3,-2,-1]); n=_r(3,7)
        ans=a*(r**(n-1))
        steps=[f"初項 a={a}, 公比 r={r}",f"第{n}項 = a×r^(n-1)",f"= {a}×{r}^{n-1}",f"= {ans}"]
        return f"初項 {a}、公比 {r} の等比数列の第 {n} 項を求めよ",str(ans),steps,"数列"
    if kind == "geom_sum":
        a=_r(1,3); r=_r(2,3); n=_r(3,6)
        ans=a*(r**n-1)//(r-1)
        steps=[f"初項{a}, 公比{r}, 項数{n}",f"S = a(r^n-1)/(r-1)",f"= {a}×({r**n}-1)/({r-1})",f"= {ans}"]
        return f"初項 {a}、公比 {r} の等比数列の第 {n} 項までの和を求めよ",str(ans),steps,"数列"
    # mixed: find common difference
    a=_r(1,8); d=_r(2,6); n=_r(3,8); target=a+(n-1)*d
    steps=[f"a_n = a + (n-1)d",f"{target} = {a} + (n-1)d",f"(n-1)d = {target-a}",f"n={n}のとき d = {d}"]
    return f"初項 {a} の等差数列で第 {n} 項が {target} のとき公差 d を求めよ",str(d),steps,"数列"

def gen_exp_log():
    kinds = ["exp_calc","log_calc","log_eq","exp_eq","change_base"]
    kind = random.choice(kinds)
    if kind == "exp_calc":
        base=random.choice([2,3,5]); exp=_r(1,5)
        ans=base**exp
        steps=[f"{base}^{exp}",f"= {'×'.join([str(base)]*exp)}",f"= {ans}"]
        return f"\\( {base}^{{{exp}}} \\) を計算せよ",str(ans),steps,"指数・対数"
    if kind == "log_calc":
        base=random.choice([2,3,10]); n=_r(1,4)
        val=base**n
        steps=[f"log_{base} {val}",f"= {base}^x = {val} となる x",f"= {n}"]
        return f"\\( \\log_{{{base}}} {val} \\) を計算せよ",str(n),steps,"指数・対数"
    if kind == "log_eq":
        base=random.choice([2,3,10]); rhs=_r(1,4)
        lhs=base**rhs
        steps=[f"log_{base} x = {rhs}",f"x = {base}^{rhs}",f"= {lhs}"]
        return f"\\( \\log_{{{base}}} x = {rhs} \\) のとき x を求めよ",str(lhs),steps,"指数・対数"
    if kind == "exp_eq":
        base=random.choice([2,3]); n=_r(2,5)
        rhs=base**n
        steps=[f"{base}^x = {rhs}",f"右辺 = {base}^{n}",f"x = {n}"]
        return f"\\( {base}^x = {rhs} \\) を解け",str(n),steps,"指数・対数"
    # change base
    base=random.choice([2,3]); n=_r(2,4); newbase=base**n
    steps=[f"log_{newbase} x = log_{base} x / log_{base} {newbase}",f"log_{base} {newbase} = {n}",f"= log_{base} x / {n}"]
    return (f"\\( \\log_{{{newbase}}} x \\) を \\( \\log_{{{base}}} x \\) を使って表せ",
            f"log_{base}(x)/{n}",steps,"指数・対数")

def gen_trigonometry():
    kinds = ["basic_val","identity","eq","law_cosines","law_sines"]
    kind = random.choice(kinds)
    angles={0:(0,1,0),30:(1,0,1),45:(0,0,1),60:(1,0,0),90:(0,1,0)}
    sin_vals={0:"0",30:"1/2",45:"√2/2",60:"√3/2",90:"1"}
    cos_vals={0:"1",30:"√3/2",45:"√2/2",60:"1/2",90:"0"}
    tan_vals={0:"0",30:"1/√3",45:"1",60:"√3",90:"undefined"}
    if kind == "basic_val":
        angle=random.choice([0,30,45,60,90])
        func=random.choice(["sin","cos","tan"])
        if func=="sin": ans=sin_vals[angle]
        elif func=="cos": ans=cos_vals[angle]
        else: ans=tan_vals[angle]
        steps=[f"{func} {angle}° の値",f"単位円 or 特殊角の表より",f"= {ans}"]
        return f"\\( \\{func} {angle}^\\circ \\) を求めよ",ans,steps,"三角比"
    if kind == "identity":
        # sin²+cos²=1
        angle=random.choice([30,45,60])
        s={"30":"1/2","45":"√2/2","60":"√3/2"}[str(angle)]
        c={"30":"√3/2","45":"√2/2","60":"1/2"}[str(angle)]
        steps=[f"sin²{angle}° + cos²{angle}°",f"= ({s})² + ({c})²","= 1（恒等式）"]
        return f"\\( \\sin^2 {angle}^\\circ + \\cos^2 {angle}^\\circ \\) を計算せよ","1",steps,"三角比"
    if kind == "eq":
        angle=random.choice([30,45,60])
        s={"30":"1/2","45":"√2/2","60":"√3/2"}[str(angle)]
        steps=[f"sin x = {s}",f"x = {angle}° または x = {180-angle}°"]
        return f"\\( \\sin x = {s} \\) （0°≦x≦180°）を解け",f"{angle},{180-angle}",steps,"三角比"
    if kind == "law_cosines":
        a,b,C=_r(3,8),_r(3,8),60
        # c² = a² + b² - 2ab cosC
        import math as _m
        c2=a**2+b**2-2*a*b*_m.cos(_m.radians(C))
        c=round(_m.sqrt(c2),2)
        steps=[f"余弦定理: c² = a² + b² - 2ab cosC",f"= {a}² + {b}² - 2·{a}·{b}·cos60°",f"= {a**2} + {b**2} - {a*b}",f"c = √{int(c2)} ≒ {c}"]
        return f"a={a}, b={b}, C=60° の三角形の c を求めよ（小数第2位まで）",str(c),steps,"三角比"
    # law of sines
    r=_r(3,8); a=random.choice([30,45,60])
    side=round(2*r*math.sin(math.radians(a)),2)
    steps=[f"正弦定理: a/sinA = 2R",f"a = 2×{r}×sin{a}°",f"= {side}"]
    return f"外接円の半径 R={r}、角 A={a}° のとき対辺 a を求めよ（小数第2位まで）",str(side),steps,"三角比"

def gen_vector():
    kinds = ["add","scalar","dot","magnitude","angle"]
    kind = random.choice(kinds)
    ax,ay=_r(-5,5),_r(-5,5); bx,by=_r(-5,5),_r(-5,5)
    if kind == "add":
        steps=[f"a=({ax},{ay}), b=({bx},{by})",f"a+b = ({ax+bx},{ay+by})"]
        return f"ベクトル a=({ax},{ay}), b=({bx},{by}) のとき a+b を求めよ",f"({ax+bx},{ay+by})",steps,"ベクトル"
    if kind == "scalar":
        k=_r(2,4)
        steps=[f"k={k}, a=({ax},{ay})",f"ka = ({k*ax},{k*ay})"]
        return f"ベクトル a=({ax},{ay}) に対して {k}a を求めよ",f"({k*ax},{k*ay})",steps,"ベクトル"
    if kind == "dot":
        dot=ax*bx+ay*by
        steps=[f"a·b = ax·bx + ay·by",f"= {ax}×{bx} + {ay}×{by}",f"= {ax*bx} + {ay*by}",f"= {dot}"]
        return f"a=({ax},{ay}), b=({bx},{by}) の内積 a·b を求めよ",str(dot),steps,"ベクトル"
    if kind == "magnitude":
        import math as _m
        mag=_m.sqrt(ax**2+ay**2)
        steps=[f"|a| = √(ax²+ay²)",f"= √({ax}²+{ay}²)",f"= √{ax**2+ay**2}",f"≒ {mag:.2f}"]
        ans=f"√{ax**2+ay**2}"
        return f"ベクトル a=({ax},{ay}) の大きさ |a| を求めよ",ans,steps,"ベクトル"
    # angle - use simple cases
    ax,ay,bx,by=1,0,0,1
    steps=["a·b = 0","|a|=1, |b|=1","cosθ = 0 → θ = 90°"]
    return "a=(1,0), b=(0,1) のなす角 θ を求めよ（°で）","90",steps,"ベクトル"

def gen_sets():
    kinds = ["union","intersection","complement","de_morgan","count"]
    kind = random.choice(kinds)
    U=set(range(1,11))
    A=set(random.sample(list(U),_r(3,6)))
    B=set(random.sample(list(U),_r(3,6)))
    if kind == "union":
        ans=A|B
        steps=[f"A={sorted(A)}",f"B={sorted(B)}",f"A∪B = A と B の少なくとも一方に属する",f"= {sorted(ans)}"]
        return f"A={sorted(A)}, B={sorted(B)} のとき A∪B の要素数を求めよ",str(len(ans)),steps,"集合"
    if kind == "intersection":
        ans=A&B
        steps=[f"A={sorted(A)}",f"B={sorted(B)}",f"A∩B = 両方に属する",f"= {sorted(ans)}"]
        return f"A={sorted(A)}, B={sorted(B)} のとき A∩B の要素数を求めよ",str(len(ans)),steps,"集合"
    if kind == "complement":
        ans=U-A
        steps=[f"U={{1..10}}, A={sorted(A)}",f"Aᶜ = U - A",f"= {sorted(ans)}"]
        return f"全体集合 U={{1..10}}, A={sorted(A)} のとき Aᶜ の要素数を求めよ",str(len(ans)),steps,"集合"
    if kind == "de_morgan":
        # (A∪B)ᶜ = Aᶜ∩Bᶜ
        ans=(U-A)&(U-B)
        ans2=U-(A|B)
        steps=["ド・モルガンの法則","(A∪B)ᶜ = Aᶜ∩Bᶜ",f"= {sorted(ans2)}"]
        return f"A={sorted(A)}, B={sorted(B)} のとき (A∪B)ᶜ の要素数を求めよ（U={{1..10}}）",str(len(ans2)),steps,"集合"
    # inclusion-exclusion
    na=_r(5,15); nb=_r(5,15); nab=_r(1,min(na,nb))
    total=na+nb-nab
    steps=["|A∪B| = |A|+|B|-|A∩B|",f"= {na}+{nb}-{nab}",f"= {total}"]
    return f"|A|={na}, |B|={nb}, |A∩B|={nab} のとき |A∪B| を求めよ",str(total),steps,"集合"

def gen_inequality():
    kinds = ["linear","quadratic","abs","system"]
    kind = random.choice(kinds)
    if kind == "linear":
        a=_rc(); b=_rc(); c=a*_rc()+b+_r(1,5)
        # ax+b < c → ax < c-b
        rhs=c-b
        if a>0: ans=f"x < {rhs//a}" if rhs%a==0 else f"x < {Fraction(rhs,a)}"
        elif a<0: ans=f"x > {rhs//a}" if rhs%a==0 else f"x > {Fraction(rhs,a)}"
        else: return gen_inequality()
        steps=[f"{a}x + {b} < {c}",f"{a}x < {rhs}",f"a={'正' if a>0 else '負'}なので不等号の向き",f"{ans}"]
        return f"\\( {a}x + {b} < {c} \\) を解け",ans,steps,"不等式"
    if kind == "quadratic":
        p,q=sorted([_r(-5,5),_r(-5,5)])
        while p>=q: p,q=sorted([_r(-5,5),_r(-5,5)])
        # (x-p)(x-q)>0 → x<p or x>q
        steps=[f"(x-{p})(x-{q}) > 0",f"放物線は上に凸なので",f"x < {p} または x > {q}"]
        return f"\\( (x-{p})(x-{q}) > 0 \\) を解け",f"x<{p} または x>{q}",steps,"不等式"
    if kind == "abs":
        a=_r(1,5); b=_r(a+1,10)
        # |x-a| < b → a-b < x < a+b
        lo=a-b; hi=a+b
        steps=[f"|x - {a}| < {b}",f"-{b} < x-{a} < {b}",f"{lo} < x < {hi}"]
        return f"\\( |x-{a}| < {b} \\) を解け",f"{lo}<x<{hi}",steps,"不等式"
    # system
    a,b=_r(-5,5),_r(-5,5)
    lo=min(a,b); hi=max(a,b)
    steps=[f"x > {lo} かつ x < {hi}",f"= {lo} < x < {hi}"]
    return f"x > {lo} かつ x < {hi} を満たす整数 x の個数を求めよ",str(hi-lo-1),steps,"不等式"

def gen_number_theory():
    kinds = ["prime","mod","euclid","digit","factor_count"]
    kind = random.choice(kinds)
    if kind == "prime":
        primes=[p for p in range(2,50) if all(p%i!=0 for i in range(2,p))]
        n=_r(2,49)
        ans="素数" if n in primes else "素数でない"
        steps=[f"{n}の約数を確認",f"2〜√{n}≒{int(n**0.5)}までで割り切れるか",f"→ {ans}"]
        return f"{n} は素数かどうか（「素数」または「素数でない」で答えよ）",ans,steps,"整数の性質"
    if kind == "mod":
        a=_r(2,9); n=_r(3,99); r=n%a
        steps=[f"{n} ÷ {a}",f"= {n//a} 余り {r}",f"∴ {n} mod {a} = {r}"]
        return f"\\( {n} \\mod {a} \\) を求めよ",str(r),steps,"整数の性質"
    if kind == "euclid":
        import math as _m; a,b=_r(10,50),_r(10,50)
        g=_m.gcd(a,b)
        steps=[f"gcd({a},{b})",f"ユークリッドの互除法",f"{a} = {a//b}×{b}+{a%b}" if a>b else f"{b} = {b//a}×{a}+{b%a}",f"= {g}"]
        return f"ユークリッドの互除法で gcd({a},{b}) を求めよ",str(g),steps,"整数の性質"
    if kind == "digit":
        n=_r(100,999); s=sum(int(d) for d in str(n))
        steps=[f"{n}の各桁の和",f"= {' + '.join(list(str(n)))}",f"= {s}"]
        return f"{n} の各桁の和を求めよ",str(s),steps,"整数の性質"
    # factor_count
    n=_r(10,100)
    divs=[i for i in range(1,n+1) if n%i==0]
    import sympy as _s
    fact=_s.factorint(n)
    fact_str=' × '.join([f"{p}^{e}" if e>1 else str(p) for p,e in fact.items()])
    cnt=1
    for e in fact.values(): cnt*=(e+1)
    steps=[f"{n} = {fact_str}",f"約数の個数 = (指数+1)の積",f"= {cnt}"]
    return f"{n} の正の約数の個数を求めよ",str(cnt),steps,"整数の性質"

GENERATORS = {
    "arithmetic": gen_arithmetic,
    "linear_eq": gen_linear_eq,
    "simultaneous": gen_simultaneous,
    "quadratic": gen_quadratic,
    "factoring": gen_factoring,
    "sqrt": gen_sqrt,
    "expansion": gen_expansion,
    "proportion": gen_proportion,
    "linear_func": gen_linear_func,
    "quadratic_func": gen_quadratic_func,
    "probability": gen_probability,
    "sequence": gen_sequence,
    "exp_log": gen_exp_log,
    "trigonometry": gen_trigonometry,
    "vector": gen_vector,
    "sets": gen_sets,
    "inequality": gen_inequality,
    "number_theory": gen_number_theory,
}

def generate_problem(selected_topics):
    if not selected_topics:
        return None
    key = TOPICS[random.choice(selected_topics)]
    gen = GENERATORS.get(key, gen_arithmetic)
    try:
        q,a,s,cat = gen()
        return {"question":q,"answer":str(a),"steps":s,"category":cat}
    except:
        return generate_problem(selected_topics)

def normalize(s):
    return s.strip().replace(" ","").replace("　","").lower()

def check_answer(user_ans, correct_ans):
    u = normalize(user_ans)
    c = normalize(correct_ans)
    if u == c: return True
    # Try numeric comparison
    try:
        return abs(float(u) - float(c)) < 1e-4
    except:
        pass
    return False

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home",           # home | setup_battle | battle | result | practice
        "mode": None,               # "battle" | "practice"
        "ai_rank": "普通",
        "selected_topics": list(TOPICS.keys()),
        "total_questions": 10,
        "time_limit": 30,
        # battle
        "player_score": 0,
        "ai_score": 0,
        "q_num": 0,
        "current_problem": None,
        "start_time": None,
        "phase": "question",        # question | result
        "user_input": "",
        "result_msg": "",
        "result_correct": None,
        "history": [],
        # practice
        "p_solved": 0,
        "p_correct": 0,
        "p_current": None,
        "p_phase": "question",
        "p_result_msg": "",
        "p_result_correct": None,
        "answer_key": 0,            # trick to clear text input
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  AI RANK CONFIG
# ─────────────────────────────────────────────
AI_RANKS = {
    "🟢 初級": {"time": 45, "label":"初級","color":"var(--green)",  "desc":"ゆっくり考える時間あり。基礎を固めよう！"},
    "🔵 普通": {"time": 30, "label":"普通","color":"var(--accent1)","desc":"標準的な難易度。バランスよく戦おう！"},
    "🔴 上級": {"time": 15, "label":"上級","color":"var(--accent2)","desc":"超高速！一瞬の判断が勝敗を分ける！"},
}

# ─────────────────────────────────────────────
#  SCREENS
# ─────────────────────────────────────────────

def screen_home():
    st.markdown('<div class="main-title">⚔️ 数学バトル</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Math Battle ─ 中学〜高校2年 全範囲対応</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card card-accent">
        <div style="font-size:2rem;margin-bottom:.4rem">⚔️</div>
        <div style="font-weight:900;font-size:1.2rem;margin-bottom:.4rem">AIバトルモード</div>
        <div style="color:var(--muted);font-size:.9rem">AIと対戦！制限時間内に正解を目指せ。間違えるとAIにポイントが入る。</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚔️ バトル開始", use_container_width=True, key="btn_battle"):
            st.session_state.screen = "setup_battle"
            st.session_state.mode = "battle"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="card card-accent">
        <div style="font-size:2rem;margin-bottom:.4rem">📚</div>
        <div style="font-weight:900;font-size:1.2rem;margin-bottom:.4rem">練習モード</div>
        <div style="color:var(--muted);font-size:.9rem">制限時間なし、ポイントなし。ひたすら問題を解いて実力をつけよう。</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📚 練習開始", use_container_width=True, key="btn_practice"):
            st.session_state.screen = "setup_practice"
            st.session_state.mode = "practice"
            st.rerun()

def screen_setup_battle():
    st.markdown("## ⚙️ バトル設定")
    
    st.markdown("### 🤖 AIのランク")
    rank_choice = st.radio(
        "ランク",
        list(AI_RANKS.keys()),
        index=1,
        horizontal=True,
        label_visibility="collapsed"
    )
    cfg = AI_RANKS[rank_choice]
    st.markdown(f"""
    <div class="card" style="border-left:4px solid {cfg['color']}">
    ⏱️ 制限時間: <strong>{cfg['time']}秒</strong>　　{cfg['desc']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ❓ 問題数")
    n_q = st.slider("問題数", 5, 20, 10, key="setup_nq")
    
    st.markdown("### 📐 出題範囲")
    all_topics = list(TOPICS.keys())
    
    col1,col2 = st.columns(2)
    if col1.button("全選択", use_container_width=True):
        st.session_state["topic_sel"] = all_topics
    if col2.button("全解除", use_container_width=True):
        st.session_state["topic_sel"] = []
    
    default_sel = st.session_state.get("topic_sel", all_topics)
    selected = st.multiselect(
        "分野を選んでください",
        all_topics,
        default=default_sel,
        key="topic_multisel_battle"
    )
    
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("← ホームに戻る", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
    with col2:
        if st.button("🚀 バトル開始！", use_container_width=True):
            if not selected:
                st.error("分野を1つ以上選択してください。")
                return
            st.session_state.ai_rank = rank_choice
            st.session_state.time_limit = cfg["time"]
            st.session_state.selected_topics = selected
            st.session_state.total_questions = n_q
            st.session_state.player_score = 0
            st.session_state.ai_score = 0
            st.session_state.q_num = 0
            st.session_state.history = []
            st.session_state.phase = "question"
            st.session_state.current_problem = generate_problem(selected)
            st.session_state.start_time = time.time()
            st.session_state.answer_key += 1
            st.session_state.screen = "battle"
            st.rerun()

def screen_setup_practice():
    st.markdown("## ⚙️ 練習モード設定")
    
    st.markdown("### 📐 出題範囲")
    all_topics = list(TOPICS.keys())
    
    col1,col2 = st.columns(2)
    if col1.button("全選択", use_container_width=True, key="prac_all"):
        st.session_state["ptopic_sel"] = all_topics
    if col2.button("全解除", use_container_width=True, key="prac_none"):
        st.session_state["ptopic_sel"] = []
    
    default_sel = st.session_state.get("ptopic_sel", all_topics)
    selected = st.multiselect(
        "分野を選んでください",
        all_topics,
        default=default_sel,
        key="topic_multisel_practice"
    )
    
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("← ホームに戻る", use_container_width=True, key="prac_back"):
            st.session_state.screen = "home"
            st.rerun()
    with col2:
        if st.button("📚 練習開始！", use_container_width=True, key="prac_start"):
            if not selected:
                st.error("分野を1つ以上選択してください。")
                return
            st.session_state.selected_topics = selected
            st.session_state.p_solved = 0
            st.session_state.p_correct = 0
            st.session_state.p_current = generate_problem(selected)
            st.session_state.p_phase = "question"
            st.session_state.answer_key += 1
            st.session_state.screen = "practice"
            st.rerun()

def screen_battle():
    prob = st.session_state.current_problem
    if prob is None:
        st.error("問題を生成できませんでした。")
        return
    
    total = st.session_state.total_questions
    qn = st.session_state.q_num + 1
    ps = st.session_state.player_score
    ai = st.session_state.ai_score
    tl = st.session_state.time_limit
    
    # ── ヘッダー ──
    rank_cfg = AI_RANKS[st.session_state.ai_rank]
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem">
    <span class="badge badge-blue">⚔️ AIバトル</span>
    <span class="badge" style="background:rgba(255,215,0,.15);color:var(--gold);border:1px solid var(--gold)">
        AI: {rank_cfg['label']}
    </span>
    <span class="badge badge-red">Q {qn}/{total}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ── スコア ──
    st.markdown(f"""
    <div class="score-row">
    <div class="score-box">
        <div class="score-label">あなた</div>
        <div class="score-value score-player">{ps}</div>
    </div>
    <div class="score-box">
        <div class="score-label">進捗</div>
        <div class="score-value score-q">{qn}/{total}</div>
    </div>
    <div class="score-box">
        <div class="score-label">AI</div>
        <div class="score-value score-ai">{ai}</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.phase == "question":
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, tl - elapsed)
        pct = remaining / tl
        timer_cls = "timer-warn" if remaining < tl * 0.4 else "timer-ok"
        
        st.markdown(f'<div class="timer-box {timer_cls}">⏱ {remaining:.1f}s</div>', unsafe_allow_html=True)
        st.progress(pct)
        
        # ── 問題 ──
        st.markdown(f'<div class="question-box animate-in">{prob["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;margin:.3rem 0"><span class="badge badge-blue">📚 {prob["category"]}</span></div>', unsafe_allow_html=True)
        
        user_ans = st.text_input(
            "答えを入力（Enterで確定）",
            key=f"ans_input_{st.session_state.answer_key}",
            placeholder="答えをここに入力...",
        )
        
        col1,col2,col3 = st.columns([2,2,1])
        with col1:
            submit = st.button("✅ 答える", use_container_width=True, key="submit_btn")
        with col2:
            if st.button("⏭️ スキップ", use_container_width=True, key="skip_btn"):
                st.session_state.ai_score += 1
                st.session_state.result_msg = f"スキップ！正解は **{prob['answer']}**"
                st.session_state.result_correct = False
                st.session_state.phase = "result"
                st.rerun()
        with col3:
            if st.button("🚩 リタイア", use_container_width=True, key="retire_btn"):
                st.session_state.screen = "result"
                st.rerun()
        
        # 時間切れ
        if remaining <= 0:
            st.session_state.ai_score += 1
            st.session_state.result_msg = f"⏰ 時間切れ！正解は **{prob['answer']}**"
            st.session_state.result_correct = False
            st.session_state.phase = "result"
            st.rerun()
        
        if submit and user_ans.strip():
            if check_answer(user_ans, prob["answer"]):
                st.session_state.player_score += 1
                st.session_state.result_msg = "🎉 正解！"
                st.session_state.result_correct = True
            else:
                st.session_state.ai_score += 1
                st.session_state.result_msg = f"❌ 不正解。正解は **{prob['answer']}**"
                st.session_state.result_correct = False
            st.session_state.phase = "result"
            st.rerun()
        
        # 自動リフレッシュ
        time.sleep(0.5)
        st.rerun()
    
    else:  # result phase
        correct = st.session_state.result_correct
        msg = st.session_state.result_msg
        
        if correct:
            st.markdown(f'<div class="result-correct">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-wrong">{msg}</div>', unsafe_allow_html=True)
        
        # 解説
        st.markdown("""
        <div class="explanation">
        <div class="explanation-title">📖 解説・計算過程</div>
        """, unsafe_allow_html=True)
        for i, step in enumerate(prob["steps"]):
            st.markdown(f'<div class="step">Step {i+1}： {step}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 次の問題 or 終了
        st.session_state.history.append({
            "q": qn, "question": prob["question"],
            "answer": prob["answer"], "correct": correct,
            "category": prob["category"]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            if qn >= total:
                if st.button("🏆 結果を見る", use_container_width=True):
                    st.session_state.screen = "result"
                    st.rerun()
            else:
                if st.button("▶️ 次の問題", use_container_width=True):
                    st.session_state.q_num += 1
                    st.session_state.current_problem = generate_problem(st.session_state.selected_topics)
                    st.session_state.start_time = time.time()
                    st.session_state.phase = "question"
                    st.session_state.answer_key += 1
                    st.rerun()
        with col2:
            if st.button("🚩 リタイア", use_container_width=True, key="retire2"):
                st.session_state.screen = "result"
                st.rerun()

def screen_result():
    ps = st.session_state.player_score
    ai = st.session_state.ai_score
    
    if ps > ai:
        st.markdown('<div class="result-correct" style="font-size:1.8rem;padding:1.5rem">🏆 あなたの勝ち！</div>', unsafe_allow_html=True)
    elif ps < ai:
        st.markdown('<div class="result-wrong" style="font-size:1.8rem;padding:1.5rem">💀 AIの勝ち...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card card-gold" style="text-align:center;font-size:1.6rem;padding:1.5rem">🤝 引き分け！</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="score-row" style="margin-top:1rem">
    <div class="score-box"><div class="score-label">あなた</div><div class="score-value score-player">{ps}</div></div>
    <div class="score-box"><div class="score-label">AI</div><div class="score-value score-ai">{ai}</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        st.markdown("### 📋 問題履歴")
        for h in st.session_state.history:
            icon = "✅" if h["correct"] else "❌"
            color = "var(--green)" if h["correct"] else "var(--accent2)"
            st.markdown(f"""
            <div class="card" style="border-left:4px solid {color};padding:.7rem 1rem;margin-bottom:.4rem">
            <span style="font-size:.8rem;color:var(--muted)">Q{h['q']} [{h['category']}]</span>
            {icon} 正解: <code style="color:var(--gold)">{h['answer']}</code>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        for k in ["player_score","ai_score","q_num","current_problem","phase","history"]:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.screen = "home"
        init_state()
        st.rerun()

def screen_practice():
    prob = st.session_state.p_current
    if prob is None:
        prob = generate_problem(st.session_state.selected_topics)
        st.session_state.p_current = prob
    
    solved = st.session_state.p_solved
    correct = st.session_state.p_correct
    acc = int(correct/solved*100) if solved>0 else 0
    
    # ── ヘッダー ──
    st.markdown(f"""
    <div class="practice-header">
    <span style="font-size:1.8rem">📚</span>
    <div>
        <div style="font-weight:900;font-size:1.1rem">練習モード</div>
        <div style="color:var(--muted);font-size:.85rem">制限時間なし ─ 好きなだけ解こう</div>
    </div>
    <div style="margin-left:auto;text-align:right">
        <div style="font-size:.75rem;color:var(--muted)">正解率</div>
        <div style="font-size:1.5rem;font-weight:900;color:var(--green)">{acc}%</div>
        <div style="font-size:.75rem;color:var(--muted)">{correct}/{solved}</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.p_phase == "question":
        st.markdown(f'<div class="question-box animate-in">{prob["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;margin:.3rem 0"><span class="badge badge-blue">📚 {prob["category"]}</span></div>', unsafe_allow_html=True)
        
        user_ans = st.text_input(
            "答えを入力（Enterで確定）",
            key=f"pans_input_{st.session_state.answer_key}",
            placeholder="答えをここに入力...",
        )
        
        col1,col2,col3 = st.columns([2,2,1])
        with col1:
            submit = st.button("✅ 答える", use_container_width=True, key="p_submit")
        with col2:
            if st.button("⏭️ 解答を見る", use_container_width=True, key="p_skip"):
                st.session_state.p_solved += 1
                st.session_state.p_result_msg = f"答え: **{prob['answer']}**"
                st.session_state.p_result_correct = None
                st.session_state.p_phase = "result"
                st.rerun()
        with col3:
            if st.button("🏠 戻る", use_container_width=True, key="p_home"):
                st.session_state.screen = "home"
                st.rerun()
        
        if submit and user_ans.strip():
            st.session_state.p_solved += 1
            if check_answer(user_ans, prob["answer"]):
                st.session_state.p_correct += 1
                st.session_state.p_result_msg = "🎉 正解！"
                st.session_state.p_result_correct = True
            else:
                st.session_state.p_result_msg = f"❌ 不正解。正解は **{prob['answer']}**"
                st.session_state.p_result_correct = False
            st.session_state.p_phase = "result"
            st.rerun()
    
    else:  # result
        rc = st.session_state.p_result_correct
        msg = st.session_state.p_result_msg
        
        if rc is True:
            st.markdown(f'<div class="result-correct">{msg}</div>', unsafe_allow_html=True)
        elif rc is False:
            st.markdown(f'<div class="result-wrong">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="card card-gold">{msg}</div>', unsafe_allow_html=True)
        
        # 解説
        st.markdown("""
        <div class="explanation">
        <div class="explanation-title">📖 解説・計算過程</div>
        """, unsafe_allow_html=True)
        for i, step in enumerate(prob["steps"]):
            st.markdown(f'<div class="step">Step {i+1}： {step}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1,col2 = st.columns(2)
        with col1:
            if st.button("▶️ 次の問題", use_container_width=True, key="p_next"):
                st.session_state.p_current = generate_problem(st.session_state.selected_topics)
                st.session_state.p_phase = "question"
                st.session_state.answer_key += 1
                st.rerun()
        with col2:
            if st.button("🏠 ホームに戻る", use_container_width=True, key="p_home2"):
                st.session_state.screen = "home"
                st.rerun()

# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
screen = st.session_state.screen

if screen == "home":
    screen_home()
elif screen == "setup_battle":
    screen_setup_battle()
elif screen == "battle":
    screen_battle()
elif screen == "result":
    screen_result()
elif screen == "setup_practice":
    screen_setup_practice()
elif screen == "practice":
    screen_practice()