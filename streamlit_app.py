import streamlit as st
import random
import time
import math
from math import gcd

# ─── ページ設定 ───────────────────────────────────────────────
st.set_page_config(
    page_title="数学バトル",
    page_icon="⚡",
    layout="wide",
)

# ─── カスタムCSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+JP:wght@300;400;700&display=swap');

:root {
    --neon-blue: #00f5ff;
    --neon-pink: #ff006e;
    --neon-yellow: #ffbe0b;
    --dark-bg: #0a0a1a;
    --card-bg: #0d0d2b;
    --border-glow: rgba(0,245,255,0.4);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark-bg) !important;
    color: #e0e0ff;
    font-family: 'Noto Sans JP', sans-serif;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: 
        radial-gradient(ellipse at 20% 20%, rgba(0,245,255,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(255,0,110,0.06) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
}

.title-main {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, var(--neon-blue), var(--neon-pink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    margin: 0;
    letter-spacing: 0.1em;
    animation: glow-title 2s ease-in-out infinite alternate;
}

@keyframes glow-title {
    from { filter: drop-shadow(0 0 8px rgba(0,245,255,0.5)); }
    to   { filter: drop-shadow(0 0 20px rgba(255,0,110,0.7)); }
}

.subtitle {
    text-align: center;
    color: rgba(224,224,255,0.5);
    font-size: 1rem;
    letter-spacing: 0.3em;
    margin-bottom: 2rem;
    font-family: 'Orbitron', monospace;
}

.score-panel {
    background: var(--card-bg);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.score-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
}

.score-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: rgba(224,224,255,0.5);
    margin-bottom: 0.5rem;
}

.score-value {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 900;
    line-height: 1;
}

.score-player { color: var(--neon-blue); }
.score-ai     { color: var(--neon-pink); }
.score-vs {
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--neon-yellow);
    text-align: center;
    padding-top: 1.5rem;
}

.question-box {
    background: linear-gradient(135deg, rgba(0,245,255,0.05), rgba(255,0,110,0.05));
    border: 2px solid rgba(0,245,255,0.3);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
    position: relative;
}

.question-box::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: linear-gradient(135deg, transparent 30%, rgba(0,245,255,0.03));
    pointer-events: none;
}

.question-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: var(--neon-blue);
    margin-bottom: 0.8rem;
}

.question-text {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.05em;
    font-family: 'Orbitron', monospace;
}

.timer-bar-container {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    margin: 1rem 0;
    overflow: hidden;
}

.timer-bar {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-pink));
    transition: width 0.5s linear;
}

.ai-thinking {
    background: rgba(255,0,110,0.08);
    border: 1px solid rgba(255,0,110,0.3);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    font-size: 0.85rem;
    color: var(--neon-pink);
    font-family: 'Orbitron', monospace;
    letter-spacing: 0.1em;
    text-align: center;
    animation: pulse-pink 1s ease-in-out infinite;
}

@keyframes pulse-pink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}

.result-correct {
    background: rgba(0,245,255,0.1);
    border: 1px solid var(--neon-blue);
    border-radius: 8px;
    padding: 0.8rem;
    color: var(--neon-blue);
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    text-align: center;
    letter-spacing: 0.1em;
}

.result-wrong {
    background: rgba(255,0,110,0.1);
    border: 1px solid var(--neon-pink);
    border-radius: 8px;
    padding: 0.8rem;
    color: var(--neon-pink);
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    text-align: center;
    letter-spacing: 0.1em;
}

.win-banner {
    background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(255,190,11,0.1));
    border: 2px solid var(--neon-blue);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    animation: victory-pulse 1.5s ease-in-out infinite alternate;
}

.lose-banner {
    background: linear-gradient(135deg, rgba(255,0,110,0.15), rgba(0,0,0,0.3));
    border: 2px solid var(--neon-pink);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
}

@keyframes victory-pulse {
    from { box-shadow: 0 0 20px rgba(0,245,255,0.3); }
    to   { box-shadow: 0 0 50px rgba(0,245,255,0.7), 0 0 80px rgba(255,190,11,0.3); }
}

.banner-title {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 1rem;
}

.difficulty-card {
    background: var(--card-bg);
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s;
    cursor: pointer;
}

.stButton button {
    width: 100%;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}

.stTextInput input {
    background: rgba(0,245,255,0.05) !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.2rem !important;
    text-align: center !important;
    letter-spacing: 0.1em !important;
}

.stTextInput input:focus {
    border-color: var(--neon-blue) !important;
    box-shadow: 0 0 12px rgba(0,245,255,0.3) !important;
}

.progress-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 0.5rem;
}

.dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: inline-block;
}

.dot-filled-blue  { background: var(--neon-blue);  box-shadow: 0 0 6px var(--neon-blue); }
.dot-filled-pink  { background: var(--neon-pink);  box-shadow: 0 0 6px var(--neon-pink); }

.history-item {
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    margin: 3px 0;
    font-size: 0.78rem;
    font-family: 'Orbitron', monospace;
    letter-spacing: 0.05em;
}

.hist-player { background: rgba(0,245,255,0.08); color: var(--neon-blue); border-left: 3px solid var(--neon-blue); }
.hist-ai     { background: rgba(255,0,110,0.08); color: var(--neon-pink); border-left: 3px solid var(--neon-pink); }
</style>
""", unsafe_allow_html=True)


# ─── 問題生成 ─────────────────────────────────────────────────

def generate_question(level: str) -> dict:
    """ランダムに数学の問題を生成して返す。"""

    middle_school = [
        _q_add, _q_sub, _q_mul, _q_div_integer,
        _q_linear_eq, _q_linear_eq2,
        _q_ratio, _q_percentage, _q_percentage_change,
        _q_power, _q_negative_calc,
        _q_factoring_basic, _q_expand_basic,
        _q_lcm, _q_gcd_q,
        _q_area_rect, _q_area_triangle, _q_volume_box,
        _q_pythagorean,
        _q_fraction_add, _q_fraction_mul,
        _q_proportion,
        _q_speed_distance_time,
        _q_number_pattern,
    ]
    high_school = [
        _q_quadratic, _q_factoring_hs,
        _q_sqrt_simplify, _q_sqrt_calc,
        _q_log, _q_log_product,
        _q_trig, _q_trig_identity,
        _q_arithmetic_seq, _q_arithmetic_seq_sum,
        _q_geometric_seq,
        _q_fraction_eq,
        _q_abs_value,
        _q_inequality,
        _q_vertex_form,
        _q_combination, _q_permutation,
        _q_probability_basic,
        _q_vector_dot,
        _q_complex_add,
        _q_remainder,
    ]

    if level == "中学":
        pool = middle_school
    elif level == "高校":
        pool = high_school
    else:  # 混合
        pool = middle_school + high_school

    fn = random.choice(pool)
    return fn()


# ═══════════════════════════════════════════
#  中学レベル問題  (23種)
# ═══════════════════════════════════════════

def _q_add():
    a, b = random.randint(10, 500), random.randint(10, 500)
    return {"q": f"{a} + {b} = ?", "a": a + b, "hint": "足し算"}

def _q_sub():
    b = random.randint(10, 400)
    a = b + random.randint(10, 400)
    return {"q": f"{a} - {b} = ?", "a": a - b, "hint": "引き算"}

def _q_mul():
    a, b = random.randint(2, 50), random.randint(2, 50)
    return {"q": f"{a} × {b} = ?", "a": a * b, "hint": "掛け算"}

def _q_div_integer():
    b   = random.randint(2, 12)
    ans = random.randint(2, 30)
    a   = b * ans
    return {"q": f"{a} ÷ {b} = ?", "a": ans, "hint": "割り算"}

def _q_negative_calc():
    a = random.randint(-20, 20)
    b = random.randint(-20, 20)
    op = random.choice(['+', '-', '×'])
    if op == '+':
        return {"q": f"({a}) + ({b}) = ?", "a": a + b, "hint": "負の数の計算"}
    elif op == '-':
        return {"q": f"({a}) - ({b}) = ?", "a": a - b, "hint": "負の数の計算"}
    else:
        return {"q": f"({a}) × ({b}) = ?", "a": a * b, "hint": "負の数の計算"}

def _q_linear_eq():
    """ax + b = c"""
    a = random.randint(2, 9)
    x = random.randint(-10, 10)
    b = random.randint(-15, 15)
    c = a * x + b
    sign = '+' if b >= 0 else '-'
    return {"q": f"{a}x {sign} {abs(b)} = {c}  のとき x = ?", "a": x, "hint": "一次方程式"}

def _q_linear_eq2():
    """ax = b + cx 形式"""
    x   = random.randint(1, 10)
    a   = random.randint(3, 9)
    c   = random.randint(1, a - 1)
    b   = (a - c) * x
    return {"q": f"{a}x = {b} + {c}x  のとき x = ?", "a": x, "hint": "一次方程式"}

def _q_ratio():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    total = (a + b) * random.randint(3, 20)
    part  = total * a // (a + b)
    return {"q": f"{total} を {a}:{b} に分けたとき、大きい方は？", "a": max(part, total - part), "hint": "比"}

def _q_proportion():
    """x/a = b/c → x = ?"""
    b   = random.randint(2, 9)
    c   = random.randint(2, 9)
    x   = random.randint(2, 9)
    a   = x * c // b if x * c % b == 0 else b
    x   = a * b // c if a * b % c == 0 else a
    # 整数になるよう再設定
    c   = random.randint(2, 9)
    b   = random.randint(2, 9)
    x   = random.randint(1, 9)
    a   = x * c // gcd(b, c) * (b // gcd(b, c))
    # シンプルに: x/b = a/c => x = a*b/c  (整数保証)
    c2  = random.randint(2, 6)
    b2  = c2 * random.randint(1, 4)
    a2  = random.randint(1, 8)
    x2  = a2 * b2 // c2
    return {"q": f"x / {b2} = {a2} / {c2}  のとき x = ?", "a": x2, "hint": "比例式"}

def _q_percentage():
    base = random.choice([100, 200, 400, 500, 800, 1000])
    pct  = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
    ans  = base * pct // 100
    return {"q": f"{base} の {pct}% は？", "a": ans, "hint": "百分率"}

def _q_percentage_change():
    base = random.choice([100, 200, 500, 1000])
    pct  = random.choice([10, 20, 25, 30, 50])
    kind = random.choice(['増', '減'])
    if kind == '増':
        ans = base * (100 + pct) // 100
    else:
        ans = base * (100 - pct) // 100
    return {"q": f"{base} を {pct}% {kind}やすと？", "a": ans, "hint": "割合の変化"}

def _q_power():
    base = random.randint(2, 9)
    exp  = random.randint(2, 4)
    return {"q": f"{base}² = ?" if exp == 2 else f"{base}^{exp} = ?", "a": base ** exp, "hint": "累乗"}

def _q_lcm():
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    from math import lcm
    return {"q": f"{a} と {b} の最小公倍数は？", "a": lcm(a, b), "hint": "最小公倍数"}

def _q_gcd_q():
    g = random.randint(2, 9)
    a = g * random.randint(2, 8)
    b = g * random.randint(2, 8)
    return {"q": f"{a} と {b} の最大公約数は？", "a": gcd(a, b), "hint": "最大公約数"}

def _q_factoring_basic():
    """x² + (a+b)x + ab = (x+a)(x+b)。積を答える。"""
    a = random.randint(1, 8)
    b = random.randint(1, 8)
    s, p = a + b, a * b
    return {"q": f"x² + {s}x + {p} = (x+□)(x+□)。□ の積は？", "a": p, "hint": "因数分解"}

def _q_expand_basic():
    """(x+a)(x+b) を展開したときの定数項。"""
    a = random.randint(-8, 8)
    b = random.randint(-8, 8)
    c = a * b
    sign_a = '+' if a >= 0 else '-'
    sign_b = '+' if b >= 0 else '-'
    return {"q": f"(x {sign_a} {abs(a)})(x {sign_b} {abs(b)}) の定数項は？", "a": c, "hint": "展開"}

def _q_area_rect():
    w, h = random.randint(3, 30), random.randint(3, 30)
    return {"q": f"縦 {h}cm × 横 {w}cm の長方形の面積は？", "a": w * h, "hint": "面積"}

def _q_area_triangle():
    base = random.randint(3, 20)
    h    = random.randint(2, 20) * 2  # 偶数で答えが整数に
    ans  = base * h // 2
    return {"q": f"底辺 {base}cm、高さ {h}cm の三角形の面積は？", "a": ans, "hint": "三角形の面積"}

def _q_volume_box():
    a, b, c = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
    return {"q": f"{a}cm × {b}cm × {c}cm の直方体の体積は？", "a": a * b * c, "hint": "体積"}

def _q_pythagorean():
    """ピタゴラス数。"""
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15),(5,12,13)]
    a, b, c = random.choice(triples)
    kind = random.choice(['hyp', 'leg'])
    if kind == 'hyp':
        return {"q": f"直角三角形で 2 辺が {a}cm と {b}cm。斜辺は？", "a": c, "hint": "三平方の定理"}
    else:
        return {"q": f"直角三角形で斜辺 {c}cm、1辺 {a}cm。もう1辺は？", "a": b, "hint": "三平方の定理"}

def _q_fraction_add():
    """異分母の分数の足し算。"""
    a_n, a_d = random.randint(1, 5), random.randint(2, 8)
    b_n, b_d = random.randint(1, 5), random.randint(2, 8)
    from math import lcm as _lcm
    L   = _lcm(a_d, b_d)
    num = a_n * (L // a_d) + b_n * (L // b_d)
    g   = gcd(num, L)
    rn, rd = num // g, L // g
    ans = str(rn) if rd == 1 else f"{rn}/{rd}"
    return {"q": f"{a_n}/{a_d} + {b_n}/{b_d} = ?  （既約分数で。整数なら整数で）", "a": ans, "hint": "分数の足し算"}

def _q_fraction_mul():
    a_n, a_d = random.randint(1, 6), random.randint(2, 8)
    b_n, b_d = random.randint(1, 6), random.randint(2, 8)
    num = a_n * b_n
    den = a_d * b_d
    g   = gcd(num, den)
    rn, rd = num // g, den // g
    ans = str(rn) if rd == 1 else f"{rn}/{rd}"
    return {"q": f"{a_n}/{a_d} × {b_n}/{b_d} = ?  （既約分数で）", "a": ans, "hint": "分数の掛け算"}

def _q_speed_distance_time():
    """距離・速さ・時間。"""
    kind = random.choice(['dist', 'time', 'speed'])
    if kind == 'dist':
        v = random.randint(2, 10) * 10
        t = random.randint(1, 5)
        return {"q": f"時速 {v}km で {t} 時間進んだ距離は？（km）", "a": v * t, "hint": "速さ・距離・時間"}
    elif kind == 'time':
        v   = random.randint(2, 8) * 10
        d   = v * random.randint(1, 5)
        return {"q": f"時速 {v}km で {d}km 進むのにかかる時間は？（時間）", "a": d // v, "hint": "速さ・距離・時間"}
    else:
        t = random.randint(2, 5)
        d = random.randint(2, 10) * t * 10
        return {"q": f"{d}km を {t} 時間で走った時速は？（km/h）", "a": d // t, "hint": "速さ・距離・時間"}

def _q_number_pattern():
    """等差数列の次の数。"""
    start = random.randint(1, 20)
    d     = random.randint(2, 8)
    n     = 4
    seq   = [start + d * i for i in range(n)]
    return {"q": f"数列 {', '.join(map(str,seq))}, □ の □ は？", "a": seq[-1] + d, "hint": "数の規則"}


# ═══════════════════════════════════════════
#  高校レベル問題  (20種)
# ═══════════════════════════════════════════

def _q_quadratic():
    n = random.randint(1, 10)
    a = random.randint(1, 4)
    b = a * n * n
    return {"q": f"{a}x² = {b}  x > 0 のとき x = ?", "a": n, "hint": "二次方程式"}

def _q_vertex_form():
    """y = (x-p)² + q の頂点 x 座標。"""
    p = random.randint(-8, 8)
    q = random.randint(-10, 10)
    sign_p = '-' if p >= 0 else '+'
    return {"q": f"y = (x {sign_p} {abs(p)})² + {q} の頂点の x 座標は？", "a": p, "hint": "二次関数の頂点"}

def _q_factoring_hs():
    r1 = random.randint(-5, 5)
    r2 = random.randint(-5, 5)
    b  = -(r1 + r2)
    c  = r1 * r2
    sign_b = '+' if b >= 0 else '-'
    sign_c = '+' if c >= 0 else '-'
    larger = max(r1, r2)
    return {"q": f"x² {sign_b} {abs(b)}x {sign_c} {abs(c)} = 0 の大きい方の解は？", "a": larger, "hint": "二次方程式の解"}

def _q_sqrt_simplify():
    n = random.randint(2, 8)
    m = random.choice([2, 3, 5, 6, 7])
    val = n * n * m
    return {"q": f"√{val} = a√{m} のとき a = ?", "a": n, "hint": "平方根の簡略化"}

def _q_sqrt_calc():
    """√a × √b = √(ab)。"""
    a = random.choice([2, 3, 5, 6, 7])
    b = random.choice([2, 3, 5, 6, 7])
    val = a * b
    # 簡略化
    g_sq = 1
    for k in range(int(val**0.5), 0, -1):
        if val % (k*k) == 0:
            g_sq = k
            break
    coeff = g_sq
    rem   = val // (g_sq * g_sq)
    if rem == 1:
        ans = str(coeff)
        q   = f"√{a} × √{b} = ?  （整数で答えよ）"
    else:
        ans = str(coeff) if coeff > 1 else ""
        q   = f"√{a} × √{b} = {coeff}√□ の □ は？"
        ans = str(rem)
    return {"q": q, "a": ans, "hint": "平方根の計算"}

def _q_log():
    base = random.choice([2, 3, 5, 10])
    exp  = random.randint(1, 4)
    val  = base ** exp
    return {"q": f"log_{base}({val}) = ?", "a": exp, "hint": "対数"}

def _q_log_product():
    """log_a(b) + log_a(c) = log_a(bc)。"""
    base = random.choice([2, 3, 10])
    b    = random.randint(2, 6)
    c    = random.randint(2, 6)
    val  = b * c
    exp  = 0
    tmp  = val
    while tmp % base == 0:
        tmp //= base
        exp += 1
    if tmp == 1:
        ans_val = exp
        return {"q": f"log_{base}({b}) + log_{base}({c}) = ?", "a": ans_val, "hint": "対数の性質"}
    # 整数にならない場合は別の問題を返す
    b2, exp2 = base, random.randint(2, 4)
    return {"q": f"log_{base}({base**exp2}) + log_{base}(1) = ?", "a": exp2, "hint": "対数の性質"}

def _q_trig():
    tbl = [
        ("sin(30°)", "1/2"), ("sin(45°)", "√2/2"), ("sin(60°)", "√3/2"), ("sin(90°)", "1"),
        ("cos(0°)", "1"),    ("cos(60°)", "1/2"),   ("cos(90°)", "0"),
        ("tan(45°)", "1"),   ("tan(30°)", "√3/3"),  ("tan(60°)", "√3"),
        ("sin(0°)", "0"),    ("cos(30°)", "√3/2"),  ("cos(45°)", "√2/2"),
    ]
    fn, ans = random.choice(tbl)
    return {"q": f"{fn} = ?  （√を含む場合はそのまま入力。例: √3/2）", "a": ans, "hint": "三角関数"}

def _q_trig_identity():
    """sin²θ + cos²θ = 1 の応用。"""
    # sin θ = a/b のとき cos²θ = ?
    triples = [(3,5),(4,5),(5,13),(12,13),(8,17)]
    s, h = random.choice(triples)
    c    = int((h*h - s*s)**0.5)
    return {"q": f"sin θ = {s}/{h} (0<θ<90°) のとき cos θ = ?  （分数で）", "a": f"{c}/{h}", "hint": "三角関数の相互関係"}

def _q_arithmetic_seq():
    a1 = random.randint(1, 15)
    d  = random.randint(1, 8)
    n  = random.randint(4, 12)
    an = a1 + (n - 1) * d
    return {"q": f"初項 {a1}、公差 {d} の等差数列の第 {n} 項は？", "a": an, "hint": "等差数列"}

def _q_arithmetic_seq_sum():
    """等差数列の和。"""
    a1 = random.randint(1, 10)
    d  = random.randint(1, 5)
    n  = random.randint(4, 10)
    s  = n * (2 * a1 + (n - 1) * d) // 2
    return {"q": f"初項 {a1}、公差 {d} の等差数列の初項から第 {n} 項までの和は？", "a": s, "hint": "等差数列の和"}

def _q_geometric_seq():
    a1 = random.randint(1, 4)
    r  = random.randint(2, 3)
    n  = random.randint(2, 5)
    an = a1 * (r ** (n - 1))
    return {"q": f"初項 {a1}、公比 {r} の等比数列の第 {n} 項は？", "a": an, "hint": "等比数列"}

def _q_fraction_eq():
    """同分母の分数の足し算（既約）。"""
    denom = random.randint(3, 12)
    a     = random.randint(1, denom - 1)
    b     = random.randint(1, denom - 1)
    num   = a + b
    g     = gcd(num, denom)
    rn, rd = num // g, denom // g
    ans   = str(rn) if rd == 1 else f"{rn}/{rd}"
    return {"q": f"{a}/{denom} + {b}/{denom} = ?  （既約分数で）", "a": ans, "hint": "分数計算"}

def _q_abs_value():
    a = random.randint(-15, 15)
    return {"q": f"|{a}| = ?", "a": abs(a), "hint": "絶対値"}

def _q_inequality():
    """ax + b > c の解（整数 x の最小値）。"""
    a = random.randint(2, 6)
    b = random.randint(-10, 10)
    c = random.randint(-10, 20)
    # ax > c - b → x > (c-b)/a
    import math as _math
    thresh = (c - b) / a
    min_x  = _math.floor(thresh) + 1
    sign_b = '+' if b >= 0 else '-'
    return {"q": f"{a}x {sign_b} {abs(b)} > {c} を満たす最小の整数 x は？", "a": min_x, "hint": "一次不等式"}

def _q_combination():
    n = random.randint(4, 8)
    r = random.randint(2, min(n-1, 4))
    from math import comb
    return {"q": f"C({n},{r}) = ?  （{n}個から{r}個選ぶ組合せ）", "a": comb(n, r), "hint": "組み合わせ"}

def _q_permutation():
    n = random.randint(4, 7)
    r = random.randint(2, min(n, 3))
    from math import perm
    return {"q": f"P({n},{r}) = ?  （{n}個から{r}個並べる順列）", "a": perm(n, r), "hint": "順列"}

def _q_probability_basic():
    """サイコロ・コインの基本確率（分数）。"""
    kind = random.choice(['dice_even','dice_ge','coin'])
    if kind == 'dice_even':
        return {"q": "サイコロを1回投げて偶数が出る確率は？（分数で）", "a": "1/2", "hint": "確率"}
    elif kind == 'dice_ge':
        k = random.randint(2, 5)
        cnt = 6 - k + 1
        g = gcd(cnt, 6)
        ans = f"{cnt//g}/{6//g}"
        return {"q": f"サイコロで {k} 以上が出る確率は？（既約分数で）", "a": ans, "hint": "確率"}
    else:
        return {"q": "コインを2回投げて両方表が出る確率は？（分数で）", "a": "1/4", "hint": "確率"}

def _q_vector_dot():
    """2次元ベクトルの内積。"""
    a1, a2 = random.randint(-4, 4), random.randint(-4, 4)
    b1, b2 = random.randint(-4, 4), random.randint(-4, 4)
    dot = a1*b1 + a2*b2
    return {"q": f"ベクトル ({a1},{a2})・({b1},{b2}) の内積は？", "a": dot, "hint": "ベクトルの内積"}

def _q_complex_add():
    """複素数の和の実部。"""
    a, b = random.randint(-5, 5), random.randint(-5, 5)
    c, d = random.randint(-5, 5), random.randint(-5, 5)
    sign_b = '+' if b >= 0 else '-'
    sign_d = '+' if d >= 0 else '-'
    return {"q": f"({a} {sign_b} {abs(b)}i) + ({c} {sign_d} {abs(d)}i) の実部は？", "a": a + c, "hint": "複素数"}

def _q_remainder():
    """整式の余りの定理。p(a) を答える。"""
    a    = random.randint(-4, 4)
    c2   = random.randint(-3, 3)
    c1   = random.randint(-5, 5)
    c0   = random.randint(-5, 5)
    val  = c2 * a * a + c1 * a + c0
    sign1 = '+' if c1 >= 0 else '-'
    sign0 = '+' if c0 >= 0 else '-'
    return {
        "q": f"p(x) = {c2}x² {sign1} {abs(c1)}x {sign0} {abs(c0)} を (x-({a})) で割った余りは？",
        "a": val,
        "hint": "余りの定理"
    }


# ─── AI の回答速度計算 ────────────────────────────────────────

AI_SPEED = {
    "よわい":     (15.0, 30.0),
    "ふつう":     ( 8.0, 18.0),
    "つよい":     ( 3.0,  8.0),
    "さいきょう": ( 0.8,  3.0),
}


def ai_answer_time(difficulty: str) -> float:
    lo, hi = AI_SPEED[difficulty]
    return random.uniform(lo, hi)


# ─── セッション初期化 ─────────────────────────────────────────

def init_state():
    defaults = {
        "phase": "menu",       # menu | playing | result
        "player_score": 0,
        "ai_score": 0,
        "current_q": None,
        "q_start": None,
        "ai_answer_at": None,
        "answered": False,
        "last_result": None,   # "player" | "ai" | "wrong"
        "history": [],
        "difficulty": "ふつう",
        "level": "混合",
        "round_num": 0,
        "answer_input_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── ヘルパー ─────────────────────────────────────────────────

def start_game():
    st.session_state.phase         = "playing"
    st.session_state.player_score  = 0
    st.session_state.ai_score      = 0
    st.session_state.history       = []
    st.session_state.round_num     = 0
    next_question()


def next_question():
    q = generate_question(st.session_state.level)
    st.session_state.current_q      = q
    st.session_state.q_start        = time.time()
    st.session_state.ai_answer_at   = time.time() + ai_answer_time(st.session_state.difficulty)
    st.session_state.answered       = False
    st.session_state.last_result    = None
    st.session_state.round_num     += 1
    st.session_state.answer_input_key += 1


def check_answer(user_input: str):
    if st.session_state.answered:
        return
    now = time.time()
    correct_val = st.session_state.current_q["a"]

    # 正規化
    def normalize(v):
        try:
            return float(str(v).strip())
        except Exception:
            return str(v).strip()

    user_norm    = normalize(user_input)
    correct_norm = normalize(correct_val)

    if user_norm == correct_norm or (
        isinstance(user_norm, float) and isinstance(correct_norm, float)
        and abs(user_norm - correct_norm) < 0.01
    ):
        st.session_state.player_score += 1
        st.session_state.last_result   = "player"
        st.session_state.history.append(
            f"Q{st.session_state.round_num}: あなたが先取！ 答え={correct_val}"
        )
    else:
        st.session_state.last_result = "wrong"
        st.session_state.history.append(
            f"Q{st.session_state.round_num}: 不正解… 正解={correct_val}"
        )

    st.session_state.answered = True


def tick_ai():
    """AIの回答時刻が来たら AI が正解を取る。"""
    if st.session_state.answered:
        return
    if time.time() >= st.session_state.ai_answer_at:
        st.session_state.ai_score    += 1
        st.session_state.last_result  = "ai"
        correct_val = st.session_state.current_q["a"]
        st.session_state.history.append(
            f"Q{st.session_state.round_num}: AIが先取… 答え={correct_val}"
        )
        st.session_state.answered = True


def dots_html(score, color_class):
    dots = ""
    for i in range(10):
        if i < score:
            dots += f'<span class="dot {color_class}"></span>'
        else:
            dots += '<span class="dot"></span>'
    return f'<div class="progress-dots">{dots}</div>'


# ─── 画面描画 ─────────────────────────────────────────────────

# === メニュー画面 ===
if st.session_state.phase == "menu":
    st.markdown('<p class="title-main">MATH BATTLE</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">⚡ AI vs HUMAN ⚡</p>', unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("### 難易度を選択")
        difficulty = st.radio(
            "AI の強さ",
            ["よわい", "ふつう", "つよい", "さいきょう"],
            index=["よわい", "ふつう", "つよい", "さいきょう"].index(
                st.session_state.difficulty
            ),
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state.difficulty = difficulty

        speed_desc = {
            "よわい":     "🐢 AIが答えるまで 15〜30 秒",
            "ふつう":     "🐇 AIが答えるまで 8〜18 秒",
            "つよい":     "🦅 AIが答えるまで 3〜8 秒",
            "さいきょう": "⚡ AIが答えるまで 0.8〜3 秒",
        }
        st.caption(speed_desc[difficulty])

        st.markdown("---")
        st.markdown("### 問題レベル")
        level = st.radio(
            "レベル",
            ["中学", "高校", "混合"],
            index=["中学", "高校", "混合"].index(st.session_state.level),
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state.level = level

        st.markdown("---")
        st.markdown("""
        <div style='background:rgba(0,245,255,0.05); border:1px solid rgba(0,245,255,0.2);
             border-radius:10px; padding:1rem; font-size:0.85rem; color:rgba(224,224,255,0.7); margin-bottom:1rem;'>
        🎮 ルール<br>
        ・ランダムに式が出題されます<br>
        ・先に正解した方に 1 ポイント<br>
        ・先に <strong>10 点</strong> 取った方が勝ち！<br>
        ・不正解でもペナルティなし
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ ゲームスタート", use_container_width=True, type="primary"):
            start_game()
            st.rerun()


# === ゲームプレイ画面 ===
elif st.session_state.phase == "playing":

    # AI タイマーチェック
    tick_ai()

    # 勝利判定
    if st.session_state.player_score >= 10:
        st.session_state.phase = "result"
        st.session_state.winner = "player"
        st.rerun()
    if st.session_state.ai_score >= 10:
        st.session_state.phase = "result"
        st.session_state.winner = "ai"
        st.rerun()

    # ── スコアボード ──
    c1, c2, c3 = st.columns([5, 2, 5])
    with c1:
        st.markdown(f"""
        <div class="score-panel">
            <div class="score-label">👤 PLAYER</div>
            <div class="score-value score-player">{st.session_state.player_score}</div>
            {dots_html(st.session_state.player_score, "dot-filled-blue")}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="score-vs">VS</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="score-panel">
            <div class="score-label">🤖 AI [{st.session_state.difficulty}]</div>
            <div class="score-value score-ai">{st.session_state.ai_score}</div>
            {dots_html(st.session_state.ai_score, "dot-filled-pink")}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── 問題表示 ──
    q = st.session_state.current_q
    if q:
        elapsed = time.time() - st.session_state.q_start
        ai_remaining = max(0.0, st.session_state.ai_answer_at - time.time())
        bar_pct = max(0.0, min(100.0, (ai_remaining / (st.session_state.ai_answer_at - st.session_state.q_start)) * 100))

        st.markdown(f"""
        <div class="question-box">
            <div class="question-label">Q {st.session_state.round_num} ／ {q['hint']}</div>
            <div class="question-text">{q['q']}</div>
        </div>
        """, unsafe_allow_html=True)

        # タイマーバー（AIが答えるまでの時間）
        if not st.session_state.answered:
            st.markdown(f"""
            <div style='font-size:0.75rem; color:rgba(224,224,255,0.4); font-family:Orbitron,monospace;
                 letter-spacing:0.2em; margin-bottom:4px;'>AI が答えるまで {ai_remaining:.1f}s</div>
            <div class="timer-bar-container">
                <div class="timer-bar" style="width:{bar_pct}%"></div>
            </div>
            """, unsafe_allow_html=True)

    # ── 入力エリア ──
    left_col, right_col = st.columns([3, 1])

    if not st.session_state.answered:
        with left_col:
            answer = st.text_input(
                "答えを入力",
                key=f"ans_{st.session_state.answer_input_key}",
                placeholder="数値を入力して Enter",
                label_visibility="collapsed",
            )
        with right_col:
            if st.button("✅ 答える", use_container_width=True, type="primary"):
                if answer.strip():
                    check_answer(answer.strip())
                    st.rerun()

        if answer and answer.strip():
            check_answer(answer.strip())
            if st.session_state.answered:
                st.rerun()

    # ── 結果表示 ──
    if st.session_state.answered and st.session_state.last_result is not None:
        result = st.session_state.last_result
        if result == "player":
            st.markdown('<div class="result-correct">⚡ 正解！ あなたが先取しました！ +1</div>', unsafe_allow_html=True)
        elif result == "ai":
            st.markdown(f'<div class="result-wrong">🤖 AIが先取… 正解は {q["a"]} でした</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-wrong">❌ 不正解… 正解は {q["a"]} でした（AIが得点）</div>', unsafe_allow_html=True)
            # 不正解の場合もAIポイント付与
            if result == "wrong" and not any("AIが得点" in h for h in st.session_state.history[-1:]):
                pass  # すでに履歴に記録済み

        st.markdown("")
        if st.button("▶ 次の問題へ", use_container_width=True):
            next_question()
            st.rerun()

    # ── 履歴サイドバー ──
    with st.expander("📋 回答履歴", expanded=False):
        for h in reversed(st.session_state.history[-20:]):
            if "あなた" in h:
                st.markdown(f'<div class="history-item hist-player">{h}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="history-item hist-ai">{h}</div>', unsafe_allow_html=True)

    # 自動リロード（AIタイマー用）
    if not st.session_state.answered:
        time.sleep(0.3)
        st.rerun()


# === リザルト画面 ===
elif st.session_state.phase == "result":
    winner = st.session_state.get("winner", "unknown")

    st.markdown('<p class="title-main">MATH BATTLE</p>', unsafe_allow_html=True)
    st.markdown("")

    col_l, col_c, col_r = st.columns([1, 3, 1])
    with col_c:
        if winner == "player":
            st.markdown(f"""
            <div class="win-banner">
                <div class="banner-title" style="color:var(--neon-blue);">🏆 WIN!</div>
                <div style="font-family:Orbitron,monospace; font-size:1.2rem; color:var(--neon-yellow); margin:0.5rem 0;">
                    おめでとうございます！
                </div>
                <div style="font-size:4rem; margin:1rem 0;">
                    <span style="color:var(--neon-blue);">{st.session_state.player_score}</span>
                    <span style="color:rgba(255,255,255,0.3); font-size:2rem;"> — </span>
                    <span style="color:var(--neon-pink);">{st.session_state.ai_score}</span>
                </div>
                <div style="font-family:Orbitron,monospace; font-size:0.7rem; letter-spacing:0.2em; 
                     color:rgba(224,224,255,0.5);">PLAYER vs AI [{st.session_state.difficulty}]</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="lose-banner">
                <div class="banner-title" style="color:var(--neon-pink);">💀 LOSE...</div>
                <div style="font-family:Orbitron,monospace; font-size:1.2rem; color:rgba(224,224,255,0.6); margin:0.5rem 0;">
                    AIの勝利です。また挑戦しよう！
                </div>
                <div style="font-size:4rem; margin:1rem 0;">
                    <span style="color:var(--neon-blue);">{st.session_state.player_score}</span>
                    <span style="color:rgba(255,255,255,0.3); font-size:2rem;"> — </span>
                    <span style="color:var(--neon-pink);">{st.session_state.ai_score}</span>
                </div>
                <div style="font-family:Orbitron,monospace; font-size:0.7rem; letter-spacing:0.2em; 
                     color:rgba(224,224,255,0.5);">PLAYER vs AI [{st.session_state.difficulty}]</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # 履歴
        with st.expander("📋 全問答履歴", expanded=True):
            for h in st.session_state.history:
                if "あなた" in h:
                    st.markdown(f'<div class="history-item hist-player">{h}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="history-item hist-ai">{h}</div>', unsafe_allow_html=True)

        st.markdown("")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔄 もう一度", use_container_width=True, type="primary"):
                # ゲーム状態だけリセット
                for key in ["phase", "player_score", "ai_score", "current_q",
                            "q_start", "ai_answer_at", "answered", "last_result",
                            "history", "round_num", "answer_input_key", "winner"]:
                    if key in st.session_state:
                        del st.session_state[key]
                init_state()
                start_game()
                st.rerun()
        with b2:
            if st.button("🏠 メニューへ", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_state()
                st.rerun()