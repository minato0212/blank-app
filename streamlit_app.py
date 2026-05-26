import streamlit as st
import random
import time
import math

# ─────────────────────────────────────────
# ページ設定
# ─────────────────────────────────────────
st.set_page_config(
    page_title="数学バトル ⚔️",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# カスタムCSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}

/* 全体背景 */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* メインコンテナ */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}

/* タイトル */
h1 {
    font-size: 3rem !important;
    font-weight: 900 !important;
    text-align: center;
    background: linear-gradient(90deg, #f093fb, #f5576c, #fda085);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    color: #e0e0ff !important;
    font-weight: 700 !important;
}

/* スコアボード */
.score-board {
    display: flex;
    justify-content: space-around;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 20px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
}
.score-item {
    text-align: center;
}
.score-label {
    font-size: 0.85rem;
    color: #aaa;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.score-value {
    font-size: 2.8rem;
    font-weight: 900;
    font-family: 'Share Tech Mono', monospace;
}
.score-player { color: #43e97b; }
.score-ai     { color: #f5576c; }
.score-vs     { color: #aaa; font-size: 1.5rem; padding-top: 12px; }

/* タイマー */
.timer-bar-wrap {
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    height: 12px;
    margin: 10px 0 4px;
    overflow: hidden;
}
.timer-bar {
    height: 100%;
    border-radius: 99px;
    transition: width 1s linear;
}
.timer-ok   { background: linear-gradient(90deg,#43e97b,#38f9d7); }
.timer-warn { background: linear-gradient(90deg,#fda085,#f6d365); }
.timer-low  { background: linear-gradient(90deg,#f5576c,#f093fb); }

/* 問題カード */
.question-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 32px;
    margin: 20px 0;
    text-align: center;
    backdrop-filter: blur(12px);
}
.question-level {
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: #f093fb;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.question-text {
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.5;
}

/* 解説カード */
.explain-card {
    background: rgba(67,233,123,0.08);
    border: 1px solid rgba(67,233,123,0.3);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    color: #d0ffd0;
    font-size: 1rem;
    line-height: 1.8;
}
.explain-card.wrong {
    background: rgba(245,87,108,0.08);
    border-color: rgba(245,87,108,0.3);
    color: #ffd0d0;
}

/* 結果バナー */
.result-banner {
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 12px 0;
}
.result-correct {
    background: rgba(67,233,123,0.15);
    border: 1px solid #43e97b;
    color: #43e97b;
}
.result-wrong {
    background: rgba(245,87,108,0.15);
    border: 1px solid #f5576c;
    color: #f5576c;
}
.result-timeout {
    background: rgba(253,160,133,0.15);
    border: 1px solid #fda085;
    color: #fda085;
}

/* ボタン上書き */
div.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 12px 28px !important;
    width: 100%;
    transition: opacity 0.2s;
    font-family: 'Noto Sans JP', sans-serif !important;
}
div.stButton > button:hover {
    opacity: 0.85 !important;
}

/* テキスト入力 */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    font-size: 1.3rem !important;
    text-align: center;
    font-family: 'Share Tech Mono', monospace !important;
    padding: 12px !important;
}

/* ラジオ */
div[data-testid="stRadio"] label {
    color: #e0e0ff !important;
    font-size: 1.1rem !important;
}

/* 難易度カード */
.diff-card {
    border-radius: 16px;
    padding: 18px 16px;
    text-align: center;
    cursor: pointer;
    border: 2px solid transparent;
    margin: 4px;
    transition: all 0.2s;
}
.diff-easy   { background: rgba(67,233,123,0.1);  border-color: rgba(67,233,123,0.4); }
.diff-normal { background: rgba(102,126,234,0.1); border-color: rgba(102,126,234,0.4); }
.diff-hard   { background: rgba(245,87,108,0.1);  border-color: rgba(245,87,108,0.4); }
.diff-title  { font-size: 1.2rem; font-weight: 700; color: #fff; }
.diff-sub    { font-size: 0.82rem; color: #aaa; margin-top: 4px; }

/* Win/Lose */
.win-screen  { text-align:center; padding:40px 0; }
.win-emoji   { font-size: 5rem; }
.win-title   { font-size: 2.5rem; font-weight:900; margin:12px 0; }
.win-player  { color: #43e97b; }
.win-ai      { color: #f5576c; }

/* paragraph */
p { color: #c8c8e8 !important; font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 問題データベース
# ─────────────────────────────────────────
def make_problems(difficulty):
    """指定難易度の問題リストを生成"""
    easy = [
        # 中学1年：計算
        lambda: _linear1(),
        lambda: _proportion(),
        lambda: _abs_value(),
        lambda: _area_basic(),
        lambda: _linear1(),
        lambda: _proportion(),
    ]
    normal = [
        lambda: _quadratic_factor(),
        lambda: _simultaneous(),
        lambda: _pythagorean(),
        lambda: _percent_calc(),
        lambda: _ratio_problem(),
        lambda: _geometry_angle(),
        lambda: _sequence_arithmetic(),
    ]
    hard = [
        lambda: _quadratic_formula(),
        lambda: _sin_cos_basic(),
        lambda: _log_basic(),
        lambda: _inequality(),
        lambda: _function_graph(),
        lambda: _probability(),
        lambda: _sequence_geometric(),
    ]
    pool = {"easy": easy, "normal": normal, "hard": hard}[difficulty]
    return pool

# ── 問題生成関数 ──────────────────────────

def _linear1():
    a = random.randint(2, 9)
    b = random.randint(1, 20)
    x = random.randint(-10, 10)
    c = a * x + b
    sign = "+" if b > 0 else "-"
    abs_b = abs(b)
    return {
        "level": "中学1年",
        "q": f"{a}x {'+' if b>=0 else '-'} {abs_b} = {c}　のとき、x の値は？",
        "answer": str(x),
        "explanation": (
            f"**解き方**\n\n"
            f"{a}x {'+' if b>=0 else '-'} {abs_b} = {c}\n\n"
            f"両辺から {'+' if b>=0 else '-'}{abs_b} を引く：\n\n"
            f"{a}x = {c} {'-' if b>=0 else '+'} {abs_b} = {c-b}\n\n"
            f"両辺を {a} で割る：\n\n"
            f"x = {c-b} ÷ {a} = **{x}**"
        ),
    }

def _proportion():
    a = random.choice([2, 3, 4, 5, 6, 8, 10])
    x = random.randint(1, 10)
    y = a * x
    return {
        "level": "中学1年",
        "q": f"y は x に比例し、x=1 のとき y={a}。\nx={x} のとき y は？",
        "answer": str(y),
        "explanation": (
            f"**解き方**\n\n"
            f"比例の式は y = ax\n\n"
            f"x=1, y={a} を代入すると a={a}\n\n"
            f"よって y = {a}x\n\n"
            f"x={x} を代入: y = {a} × {x} = **{y}**"
        ),
    }

def _abs_value():
    x = random.randint(-15, 15)
    return {
        "level": "中学1年",
        "q": f"|{x}| の値は？",
        "answer": str(abs(x)),
        "explanation": (
            f"**解き方**\n\n"
            f"絶対値は数直線上の原点からの距離です。\n\n"
            f"|{x}| = **{abs(x)}**"
        ),
    }

def _area_basic():
    r = random.randint(2, 10)
    area = r * r
    return {
        "level": "中学1年",
        "q": f"一辺が {r} cm の正方形の面積は何 cm²？",
        "answer": str(area),
        "explanation": (
            f"**解き方**\n\n"
            f"正方形の面積 = 一辺 × 一辺\n\n"
            f"= {r} × {r} = **{area}** cm²"
        ),
    }

def _quadratic_factor():
    r1 = random.randint(-5, 5)
    r2 = random.randint(-5, 5)
    b = -(r1 + r2)
    c = r1 * r2
    sign_b = "+" if b >= 0 else "-"
    sign_c = "+" if c >= 0 else "-"
    roots = sorted([r1, r2])
    return {
        "level": "中学3年",
        "q": (
            f"x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c} = 0 の解を\n"
            f"小さい順に「a,b」の形で答えよ（例: -3,2）"
        ),
        "answer": f"{roots[0]},{roots[1]}",
        "explanation": (
            f"**解き方（因数分解）**\n\n"
            f"x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c}\n\n"
            f"= (x {'+' if -r1>=0 else ''}{-r1})(x {'+' if -r2>=0 else ''}{-r2})\n\n"
            f"各因数 = 0 とおくと\n\n"
            f"x = **{roots[0]}**, **{roots[1]}**"
        ),
    }

def _simultaneous():
    x = random.randint(1, 5)
    y = random.randint(1, 5)
    a1 = random.randint(1, 3)
    b1 = random.randint(1, 3)
    a2 = random.randint(1, 3)
    b2 = random.randint(1, 3)
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    return {
        "level": "中学2年",
        "q": (
            f"連立方程式を解いて x の値を答えよ\n\n"
            f"{a1}x + {b1}y = {c1}\n"
            f"{a2}x + {b2}y = {c2}"
        ),
        "answer": str(x),
        "explanation": (
            f"**解き方（代入法/加減法）**\n\n"
            f"①: {a1}x + {b1}y = {c1}\n"
            f"②: {a2}x + {b2}y = {c2}\n\n"
            f"この連立方程式の解は\n\n"
            f"x = **{x}**, y = {y}\n\n"
            f"（ガウス消去法や代入法で解けます）"
        ),
    }

def _pythagorean():
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25)]
    a,b,c = random.choice(triples)
    k = random.randint(1,3)
    return {
        "level": "中学2年",
        "q": f"直角三角形の2辺が {a*k} と {b*k} のとき、斜辺の長さは？",
        "answer": str(c*k),
        "explanation": (
            f"**解き方（三平方の定理）**\n\n"
            f"斜辺² = {a*k}² + {b*k}²\n\n"
            f"= {(a*k)**2} + {(b*k)**2} = {(c*k)**2}\n\n"
            f"斜辺 = √{(c*k)**2} = **{c*k}**"
        ),
    }

def _percent_calc():
    orig = random.choice([100, 200, 500, 1000, 2000])
    pct = random.choice([10, 15, 20, 25, 30])
    result = orig * pct // 100
    return {
        "level": "中学2年",
        "q": f"{orig} 円の {pct}% はいくら？（整数で答えよ）",
        "answer": str(result),
        "explanation": (
            f"**解き方**\n\n"
            f"{orig} × {pct}/100 = {orig} × {pct/100} = **{result}** 円"
        ),
    }

def _ratio_problem():
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    total = (a + b) * random.randint(3, 8)
    partA = total * a // (a + b)
    return {
        "level": "中学2年",
        "q": f"{total} を {a}:{b} に分けると、大きい方はいくつ？",
        "answer": str(max(partA, total - partA)),
        "explanation": (
            f"**解き方**\n\n"
            f"1の単位 = {total} ÷ ({a}+{b}) = {total}//{a+b} = {total//(a+b)}\n\n"
            f"大きい方 ({max(a,b)}) = {total//(a+b)} × {max(a,b)} = **{max(partA, total-partA)}**"
        ),
    }

def _geometry_angle():
    a = random.randint(30, 80)
    b = random.randint(30, 80)
    c = 180 - a - b
    return {
        "level": "中学2年",
        "q": f"三角形の2つの内角が {a}°, {b}° のとき、残りの内角は何度？",
        "answer": str(c),
        "explanation": (
            f"**解き方**\n\n"
            f"三角形の内角の和 = 180°\n\n"
            f"残り = 180° - {a}° - {b}° = **{c}°**"
        ),
    }

def _sequence_arithmetic():
    a1 = random.randint(1, 10)
    d = random.randint(2, 7)
    n = random.randint(5, 12)
    an = a1 + (n - 1) * d
    return {
        "level": "高1",
        "q": f"初項 {a1}、公差 {d} の等差数列の第 {n} 項は？",
        "answer": str(an),
        "explanation": (
            f"**解き方**\n\n"
            f"等差数列の一般項: aₙ = a₁ + (n-1)d\n\n"
            f"a_{n} = {a1} + ({n}-1) × {d}\n\n"
            f"= {a1} + {(n-1)*d} = **{an}**"
        ),
    }

def _quadratic_formula():
    # ax²+bx+c=0 with integer solutions
    r1 = random.randint(-4, 4)
    r2 = random.randint(-4, 4)
    b = -(r1 + r2)
    c = r1 * r2
    roots = sorted([r1, r2])
    return {
        "level": "中学3年",
        "q": (
            f"解の公式を使って解け\n\n"
            f"x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c} = 0\n\n"
            f"解を小さい順に「a,b」の形で答えよ（例: -2,3）"
        ),
        "answer": f"{roots[0]},{roots[1]}",
        "explanation": (
            f"**解き方（解の公式）**\n\n"
            f"x = (-b ± √(b²-4ac)) / 2a\n\n"
            f"a=1, b={b}, c={c}\n\n"
            f"判別式 D = {b}² - 4×{c} = {b**2 - 4*c}\n\n"
            f"√D = {int(math.sqrt(b**2 - 4*c))}\n\n"
            f"x = ({-b} ± {int(math.sqrt(b**2 - 4*c))}) / 2\n\n"
            f"= **{roots[0]}** または **{roots[1]}**"
        ),
    }

def _sin_cos_basic():
    angles = {30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"), 60: ("√3/2", "1/2")}
    angle = random.choice([30, 45, 60])
    func = random.choice(["sin", "cos"])
    val = angles[angle][0] if func == "sin" else angles[angle][1]
    return {
        "level": "高1",
        "q": f"{func} {angle}° の値は？（例: √3/2）",
        "answer": val,
        "explanation": (
            f"**三角比の表**\n\n"
            f"| 角度 | sin | cos |\n"
            f"|------|-----|-----|\n"
            f"| 30° | 1/2 | √3/2 |\n"
            f"| 45° | √2/2 | √2/2 |\n"
            f"| 60° | √3/2 | 1/2 |\n\n"
            f"{func} {angle}° = **{val}**"
        ),
    }

def _log_basic():
    base = random.choice([2, 3, 10])
    exp = random.randint(2, 4)
    val = base ** exp
    return {
        "level": "高2",
        "q": f"log_{base}({val}) の値は？（整数で答えよ）",
        "answer": str(exp),
        "explanation": (
            f"**解き方**\n\n"
            f"log_{base}({val}) = x とおくと\n\n"
            f"{base}^x = {val} = {base}^{exp}\n\n"
            f"よって x = **{exp}**"
        ),
    }

def _inequality():
    a = random.randint(2, 5)
    b = random.randint(1, 10)
    x_thresh = (b + a) // a  # rough
    # 2x - 3 > 5  →  x > 4
    lhs_b = random.randint(-8, -1)
    rhs = random.randint(1, 12)
    x_val = math.ceil((rhs - lhs_b) / a) if (rhs - lhs_b) % a != 0 else (rhs - lhs_b) // a
    return {
        "level": "高1",
        "q": (
            f"{a}x {'+' if lhs_b>=0 else ''}{lhs_b} > {rhs} を解け\n\n"
            f"x > □ の □ に入る整数は？"
        ),
        "answer": str(x_val),
        "explanation": (
            f"**解き方**\n\n"
            f"{a}x {'+' if lhs_b>=0 else ''}{lhs_b} > {rhs}\n\n"
            f"{a}x > {rhs} - ({lhs_b}) = {rhs - lhs_b}\n\n"
            f"x > {rhs - lhs_b} ÷ {a} = **{x_val}**"
        ),
    }

def _function_graph():
    a = random.choice([-2, -1, 1, 2, 3])
    b = random.randint(-5, 5)
    x = random.randint(-3, 3)
    y = a * x + b
    return {
        "level": "高1",
        "q": f"一次関数 y = {a}x {'+' if b>=0 else ''}{b} で\nx = {x} のときの y の値は？",
        "answer": str(y),
        "explanation": (
            f"**解き方**\n\n"
            f"y = {a}x {'+' if b>=0 else ''}{b} に x={x} を代入\n\n"
            f"y = {a} × {x} {'+' if b>=0 else ''}{b}\n\n"
            f"= {a*x} {'+' if b>=0 else ''}{b} = **{y}**"
        ),
    }

def _probability():
    n = random.randint(3, 6)
    k = random.randint(1, n - 1)
    # P(X=k) from n cards numbered 1..n, drawing 1
    return {
        "level": "高1",
        "q": (
            f"1 から {n} までの番号が書かれたカードが {n} 枚あります。\n"
            f"1 枚引いたとき、{k} 以下になる確率を分数で答えよ（例: 2/5）"
        ),
        "answer": f"{k}/{n}",
        "explanation": (
            f"**解き方**\n\n"
            f"全事象の数 = {n}\n\n"
            f"{k} 以下になる場合 = {k} 通り（1, 2, ..., {k}）\n\n"
            f"確率 = {k}/{n}"
            + (f" = {k//math.gcd(k,n)}/{n//math.gcd(k,n)}" if math.gcd(k,n) > 1 else "")
        ),
    }

def _sequence_geometric():
    a1 = random.randint(1, 5)
    r = random.choice([2, 3, -2])
    n = random.randint(3, 6)
    an = a1 * (r ** (n - 1))
    return {
        "level": "高2",
        "q": f"初項 {a1}、公比 {r} の等比数列の第 {n} 項は？",
        "answer": str(an),
        "explanation": (
            f"**解き方**\n\n"
            f"等比数列の一般項: aₙ = a₁ × r^(n-1)\n\n"
            f"a_{n} = {a1} × {r}^({n}-1)\n\n"
            f"= {a1} × {r}^{n-1} = {a1} × {r**(n-1)} = **{an}**"
        ),
    }

# ─────────────────────────────────────────
# セッション状態初期化
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "title",          # title | select | game | result
        "difficulty": "normal",
        "player_score": 0,
        "ai_score": 0,
        "current_q": None,
        "q_start_time": None,
        "time_limit": 30,
        "answer_submitted": False,
        "last_result": None,        # "correct" | "wrong" | "timeout"
        "show_explanation": False,
        "total_questions": 0,
        "player_correct": 0,
        "history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
ss = st.session_state

# ─────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────
DIFFICULTY_CONFIG = {
    "easy":   {"label": "かんたん", "limit": 40, "ai_rate": 0.3, "color": "#43e97b"},
    "normal": {"label": "ふつう",   "limit": 30, "ai_rate": 0.55,"color": "#667eea"},
    "hard":   {"label": "むずかしい","limit": 20, "ai_rate": 0.75,"color": "#f5576c"},
}

def new_question():
    pool = make_problems(ss["difficulty"])
    fn = random.choice(pool)
    ss["current_q"] = fn()
    ss["q_start_time"] = time.time()
    ss["answer_submitted"] = False
    ss["last_result"] = None
    ss["show_explanation"] = False
    ss["total_questions"] += 1

def ai_answer():
    cfg = DIFFICULTY_CONFIG[ss["difficulty"]]
    return random.random() < cfg["ai_rate"]

def timer_fraction():
    limit = DIFFICULTY_CONFIG[ss["difficulty"]]["limit"]
    elapsed = time.time() - ss["q_start_time"]
    return max(0, 1 - elapsed / limit)

def timer_class(frac):
    if frac > 0.5:  return "timer-ok"
    if frac > 0.25: return "timer-warn"
    return "timer-low"

def remaining_sec():
    limit = DIFFICULTY_CONFIG[ss["difficulty"]]["limit"]
    elapsed = time.time() - ss["q_start_time"]
    return max(0, int(limit - elapsed))

# ─────────────────────────────────────────
# 画面: タイトル
# ─────────────────────────────────────────
def screen_title():
    st.markdown("<h1>🧮 数学バトル</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;font-size:1.1rem;color:#aaa;margin-bottom:32px;'>"
        "AIと数学の問題を解いて戦おう！先に10ポイント取った方が勝ち⚔️</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 ゲームスタート"):
            ss["screen"] = "select"
            st.rerun()

    st.markdown("---")
    st.markdown("""
<div style='color:#888;font-size:0.9rem;text-align:center;line-height:2;'>
📚 問題範囲：中学1年〜高校2年<br>
⏱ 制限時間内に答えよう<br>
🤖 AIも同時に解いている<br>
🏆 先に10ポイント取れば勝ち！
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 画面: 難易度選択
# ─────────────────────────────────────────
def screen_select():
    st.markdown("<h2 style='text-align:center;'>難易度を選んでね</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
<div class='diff-card diff-easy'>
  <div class='diff-title' style='color:#43e97b;'>🟢 かんたん</div>
  <div class='diff-sub'>中学1〜2年<br>制限時間 40秒<br>AIは30%の確率で正解</div>
</div>""", unsafe_allow_html=True)
        if st.button("かんたんで始める"):
            _start_game("easy")

    with col2:
        st.markdown("""
<div class='diff-card diff-normal'>
  <div class='diff-title' style='color:#667eea;'>🔵 ふつう</div>
  <div class='diff-sub'>中学2〜3年<br>制限時間 30秒<br>AIは55%の確率で正解</div>
</div>""", unsafe_allow_html=True)
        if st.button("ふつうで始める"):
            _start_game("normal")

    with col3:
        st.markdown("""
<div class='diff-card diff-hard'>
  <div class='diff-title' style='color:#f5576c;'>🔴 むずかしい</div>
  <div class='diff-sub'>中学3年〜高2<br>制限時間 20秒<br>AIは75%の確率で正解</div>
</div>""", unsafe_allow_html=True)
        if st.button("むずかしいで始める"):
            _start_game("hard")

def _start_game(diff):
    ss["difficulty"] = diff
    ss["player_score"] = 0
    ss["ai_score"] = 0
    ss["total_questions"] = 0
    ss["player_correct"] = 0
    ss["history"] = []
    ss["screen"] = "game"
    new_question()
    st.rerun()

# ─────────────────────────────────────────
# 画面: ゲーム
# ─────────────────────────────────────────
def screen_game():
    cfg = DIFFICULTY_CONFIG[ss["difficulty"]]

    # スコアボード
    st.markdown(f"""
<div class='score-board'>
  <div class='score-item'>
    <div class='score-label'>👤 あなた</div>
    <div class='score-value score-player'>{ss['player_score']}</div>
  </div>
  <div class='score-item score-vs'>VS</div>
  <div class='score-item'>
    <div class='score-label'>🤖 AI</div>
    <div class='score-value score-ai'>{ss['ai_score']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    q = ss["current_q"]

    if not ss["answer_submitted"]:
        # タイマー表示
        frac = timer_fraction()
        rem = remaining_sec()
        cls = timer_class(frac)

        if frac <= 0:
            # タイムアウト処理
            ss["answer_submitted"] = True
            ss["last_result"] = "timeout"
            ss["show_explanation"] = True
            ss["ai_score"] += 1  # タイムアウトはAIポイント
            ss["history"].append({"q": q["q"], "result": "timeout", "answer": q["answer"]})
            _check_win()
            st.rerun()

        st.markdown(f"""
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
  <span style='color:#aaa;font-size:0.85rem;'>残り時間</span>
  <span style='color:white;font-family:"Share Tech Mono",monospace;font-size:1.1rem;font-weight:700;'>{rem}秒</span>
</div>
<div class='timer-bar-wrap'><div class='timer-bar {cls}' style='width:{int(frac*100)}%;'></div></div>
""", unsafe_allow_html=True)

        # 問題カード
        st.markdown(f"""
<div class='question-card'>
  <div class='question-level'>📚 {q['level']}</div>
  <div class='question-text'>{q['q'].replace(chr(10), '<br>')}</div>
</div>
""", unsafe_allow_html=True)

        # 回答入力
        answer_input = st.text_input(
            "答えを入力してください",
            key=f"ans_{ss['total_questions']}",
            placeholder="ここに入力...",
            label_visibility="visible"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ 答えを送信", key="submit_btn"):
                if answer_input.strip():
                    _submit_answer(answer_input.strip(), q)
                    st.rerun()
        with col_b:
            if st.button("⏩ スキップ（AI +1）", key="skip_btn"):
                ss["answer_submitted"] = True
                ss["last_result"] = "timeout"
                ss["show_explanation"] = True
                ss["ai_score"] += 1
                ss["history"].append({"q": q["q"], "result": "skip", "answer": q["answer"]})
                _check_win()
                st.rerun()

        # 自動リロード（タイマー更新）
        time.sleep(1)
        st.rerun()

    else:
        # 結果表示
        result = ss["last_result"]
        if result == "correct":
            st.markdown("<div class='result-banner result-correct'>🎉 正解！ +1ポイント</div>", unsafe_allow_html=True)
        elif result == "wrong":
            st.markdown(f"<div class='result-banner result-wrong'>❌ 不正解… AIが +1ポイント<br><small>正解: {q['answer']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-banner result-timeout'>⏰ 時間切れ！AIが +1ポイント<br><small>正解: {q['answer']}</small></div>", unsafe_allow_html=True)

        # 解説
        if ss["show_explanation"]:
            cls = "explain-card" if result == "correct" else "explain-card wrong"
            st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
            st.markdown("**📖 解説**")
            st.markdown(q["explanation"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➡ 次の問題へ"):
            new_question()
            st.rerun()

def _submit_answer(user_ans, q):
    correct = user_ans.replace(" ", "").lower() == q["answer"].replace(" ", "").lower()
    ss["answer_submitted"] = True
    ss["show_explanation"] = True

    if correct:
        ss["last_result"] = "correct"
        ss["player_score"] += 1
        ss["player_correct"] += 1
        ss["history"].append({"q": q["q"], "result": "correct", "answer": q["answer"]})
    else:
        ss["last_result"] = "wrong"
        # AIが正解するか判定
        if ai_answer():
            ss["ai_score"] += 1
        ss["history"].append({"q": q["q"], "result": "wrong", "answer": q["answer"]})

    _check_win()

def _check_win():
    if ss["player_score"] >= 10:
        ss["screen"] = "result"
        ss["winner"] = "player"
    elif ss["ai_score"] >= 10:
        ss["screen"] = "result"
        ss["winner"] = "ai"

# ─────────────────────────────────────────
# 画面: 結果
# ─────────────────────────────────────────
def screen_result():
    winner = ss.get("winner", "player")
    acc = ss["player_correct"] / max(ss["total_questions"], 1) * 100

    if winner == "player":
        st.markdown("""
<div class='win-screen'>
  <div class='win-emoji'>🏆</div>
  <div class='win-title win-player'>あなたの勝ち！</div>
  <p style='color:#43e97b;font-size:1.1rem;'>おめでとう！AIに勝ちました！</p>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class='win-screen'>
  <div class='win-emoji'>🤖</div>
  <div class='win-title win-ai'>AIの勝ち…</div>
  <p style='color:#f5576c;font-size:1.1rem;'>次は勝てるはず！もう一度挑戦しよう！</p>
</div>
""", unsafe_allow_html=True)

    # スタッツ
    st.markdown(f"""
<div class='score-board'>
  <div class='score-item'>
    <div class='score-label'>あなた</div>
    <div class='score-value score-player'>{ss['player_score']}</div>
  </div>
  <div class='score-item'>
    <div class='score-label'>正解率</div>
    <div class='score-value' style='color:#f6d365;'>{acc:.0f}%</div>
  </div>
  <div class='score-item'>
    <div class='score-label'>AI</div>
    <div class='score-value score-ai'>{ss['ai_score']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 もう一度遊ぶ"):
            ss["screen"] = "select"
            ss["history"] = []
            st.rerun()
    with col2:
        if st.button("🏠 タイトルへ"):
            ss["screen"] = "title"
            st.rerun()

    # 問題履歴
    if ss["history"]:
        with st.expander("📋 問題履歴を見る"):
            for i, h in enumerate(ss["history"], 1):
                icon = "✅" if h["result"] == "correct" else ("⏰" if h["result"] in ["timeout","skip"] else "❌")
                st.markdown(f"**Q{i}** {icon}  正解: `{h['answer']}`")

# ─────────────────────────────────────────
# ルーティング
# ─────────────────────────────────────────
screen = ss["screen"]
if screen == "title":
    screen_title()
elif screen == "select":
    screen_select()
elif screen == "game":
    screen_game()
elif screen == "result":
    screen_result()