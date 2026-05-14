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
        _q_arithmetic,
        _q_linear_eq,
        _q_ratio,
        _q_percentage,
        _q_power,
        _q_factoring_basic,
    ]
    high_school = [
        _q_quadratic,
        _q_factoring_hs,
        _q_sqrt_simplify,
        _q_log,
        _q_trig,
        _q_arithmetic_seq,
        _q_geometric_seq,
        _q_fraction_eq,
    ]

    if level == "中学":
        pool = middle_school
    elif level == "高校":
        pool = high_school
    else:  # 混合
        pool = middle_school + high_school

    fn = random.choice(pool)
    return fn()


# --- 中学レベル問題 ---

def _q_arithmetic():
    ops = ['+', '-', '*']
    op = random.choice(ops)
    if op == '+':
        a, b = random.randint(10, 999), random.randint(10, 999)
        return {"q": f"{a} + {b} = ?", "a": a + b, "hint": "足し算"}
    elif op == '-':
        a, b = random.randint(100, 999), random.randint(10, 99)
        return {"q": f"{a} - {b} = ?", "a": a - b, "hint": "引き算"}
    else:
        a, b = random.randint(2, 99), random.randint(2, 99)
        return {"q": f"{a} × {b} = ?", "a": a * b, "hint": "掛け算"}


def _q_linear_eq():
    """ax + b = c 形式の一次方程式。"""
    a = random.randint(2, 9)
    x = random.randint(-10, 10)
    b = random.randint(-20, 20)
    c = a * x + b
    sign = '+' if b >= 0 else '-'
    abs_b = abs(b)
    q_str = f"{a}x {sign} {abs_b} = {c}　のとき x = ?"
    return {"q": q_str, "a": x, "hint": "一次方程式"}


def _q_ratio():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    total = random.randint(10, 100) * (a + b)
    part = total * a // (a + b)
    return {"q": f"{total} を {a}:{b} に分けたとき、大きい方は？", "a": max(part, total - part), "hint": "比"}


def _q_percentage():
    base = random.choice([100, 200, 500, 1000, 2000])
    pct  = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80])
    ans  = base * pct // 100
    return {"q": f"{base} の {pct}% は？", "a": ans, "hint": "百分率"}


def _q_power():
    base = random.randint(2, 9)
    exp  = random.randint(2, 4)
    return {"q": f"{base}^{exp} = ?", "a": base ** exp, "hint": "累乗"}


def _q_factoring_basic():
    """x^2 + (a+b)x + ab 形式。"""
    a = random.randint(-9, 9)
    b = random.randint(-9, 9)
    s = a + b
    p = a * b
    sign_s = '+' if s >= 0 else '-'
    sign_p = '+' if p >= 0 else '-'
    q = f"x² {sign_s} {abs(s)}x {sign_p} {abs(p)} を因数分解すると (x + □)(x + □)。□ の積は？"
    return {"q": q, "a": p, "hint": "因数分解（積）"}


# --- 高校レベル問題 ---

def _q_quadratic():
    """解の公式不要な二次方程式 ax^2 = b 形式。"""
    n = random.randint(1, 12)
    a = random.randint(1, 5)
    b = a * n * n
    return {"q": f"{a}x² = {b}　のとき x > 0 での x = ?", "a": n, "hint": "二次方程式"}


def _q_factoring_hs():
    """ax^2 + bx + c = 0 の整数解。"""
    r1 = random.randint(-6, 6)
    r2 = random.randint(-6, 6)
    a = random.randint(1, 3)
    b = -a * (r1 + r2)
    c = a * r1 * r2
    sign_b = '+' if b >= 0 else '-'
    sign_c = '+' if c >= 0 else '-'
    larger = max(r1, r2)
    return {
        "q": f"{a}x² {sign_b} {abs(b)}x {sign_c} {abs(c)} = 0 の大きい方の解は？",
        "a": larger,
        "hint": "二次方程式の解"
    }


def _q_sqrt_simplify():
    """√(n²m) = n√m 形式。"""
    n = random.randint(2, 9)
    m = random.choice([2, 3, 5, 6, 7])
    val = n * n * m
    return {"q": f"√{val} を簡略化すると a√{m}。a = ?", "a": n, "hint": "平方根"}


def _q_log():
    """log_a(a^n) = n 形式。"""
    base = random.choice([2, 3, 5, 10])
    exp  = random.randint(1, 5)
    val  = base ** exp
    return {"q": f"log_{base}({val}) = ?", "a": exp, "hint": "対数"}


def _q_trig():
    """sin/cos/tan の主要角度。"""
    angle_map = {
        "sin(0°)": 0, "sin(30°)": "1/2", "sin(45°)": "1",
        "sin(60°)": "1", "sin(90°)": 1,
        "cos(0°)": 1, "cos(60°)": "1/2", "cos(90°)": 0,
        "tan(0°)": 0, "tan(45°)": 1,
    }
    choice = random.choice(list(angle_map.items()))
    q_str  = f"{choice[0]} の値（分数は分子のみ答えよ。√2/2 なら 1）= ?"
    return {"q": q_str, "a": choice[1], "hint": "三角関数"}


def _q_arithmetic_seq():
    """等差数列の第n項。"""
    a1   = random.randint(1, 20)
    d    = random.randint(1, 10)
    n    = random.randint(5, 15)
    an   = a1 + (n - 1) * d
    return {"q": f"初項 {a1}、公差 {d} の等差数列の第 {n} 項は？", "a": an, "hint": "等差数列"}


def _q_geometric_seq():
    """等比数列の第n項。"""
    a1 = random.randint(1, 5)
    r  = random.randint(2, 4)
    n  = random.randint(2, 5)
    an = a1 * (r ** (n - 1))
    return {"q": f"初項 {a1}、公比 {r} の等比数列の第 {n} 項は？", "a": an, "hint": "等比数列"}


def _q_fraction_eq():
    """分数の足し算（同分母）。"""
    denom = random.randint(2, 12)
    a     = random.randint(1, denom - 1)
    b     = random.randint(1, denom - 1)
    num   = a + b
    g     = gcd(num, denom)
    r_num = num // g
    r_den = denom // g
    if r_den == 1:
        q   = f"{a}/{denom} + {b}/{denom} = ?"
        ans = str(r_num)
    else:
        q   = f"{a}/{denom} + {b}/{denom} = ? （既約分数で答えよ。例: 3/4）"
        ans = f"{r_num}/{r_den}"
    return {"q": q, "a": ans, "hint": "分数計算"}


# ─── AI の回答速度計算 ────────────────────────────────────────

AI_SPEED = {
    "よわい":  (8.0, 15.0),
    "ふつう":  (4.0,  8.0),
    "つよい":  (1.5,  4.0),
    "さいきょう": (0.3, 1.5),
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
            "よわい":     "🐢 AIが答えるまで 8〜15 秒",
            "ふつう":     "🐇 AIが答えるまで 4〜8 秒",
            "つよい":     "🦅 AIが答えるまで 1.5〜4 秒",
            "さいきょう": "⚡ AIが答えるまで 0.3〜1.5 秒",
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