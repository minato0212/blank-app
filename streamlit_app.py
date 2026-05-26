ｃ"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}
.block-container { padding-top: 2rem; max-width: 820px; }

h1 {
    font-size: 3rem !important; font-weight: 900 !important; text-align: center;
    background: linear-gradient(90deg, #f093fb, #f5576c, #fda085);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: none; margin-bottom: 0.5rem !important;
}
h2, h3 { color: #e0e0ff !important; font-weight: 700 !important; }

.score-board {
    display: flex; justify-content: space-around;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px; padding: 20px; margin: 16px 0; backdrop-filter: blur(10px);
}
.score-item { text-align: center; }
.score-label { font-size: 0.85rem; color: #aaa; letter-spacing: 2px; text-transform: uppercase; }
.score-value { font-size: 2.8rem; font-weight: 900; font-family: 'Share Tech Mono', monospace; }
.score-player { color: #43e97b; }
.score-ai     { color: #f5576c; }
.score-vs     { color: #aaa; font-size: 1.5rem; padding-top: 12px; }

.timer-bar-wrap {
    background: rgba(255,255,255,0.1); border-radius: 99px;
    height: 12px; margin: 10px 0 4px; overflow: hidden;
}
.timer-bar { height: 100%; border-radius: 99px; transition: width 1s linear; }
.timer-ok   { background: linear-gradient(90deg,#43e97b,#38f9d7); }
.timer-warn { background: linear-gradient(90deg,#fda085,#f6d365); }
.timer-low  { background: linear-gradient(90deg,#f5576c,#f093fb); }

.question-card {
    background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px; padding: 32px; margin: 20px 0; text-align: center;
    backdrop-filter: blur(12px);
}
.question-level { font-size: 0.75rem; letter-spacing: 3px; color: #f093fb; text-transform: uppercase; margin-bottom: 8px; }
.question-text  { font-size: 1.7rem; font-weight: 700; color: #fff; line-height: 1.6; }

.explain-card {
    background: rgba(67,233,123,0.08); border: 1px solid rgba(67,233,123,0.3);
    border-radius: 16px; padding: 24px; margin: 12px 0; color: #d0ffd0;
    font-size: 1rem; line-height: 1.8;
}
.explain-card.wrong {
    background: rgba(245,87,108,0.08); border-color: rgba(245,87,108,0.3); color: #ffd0d0;
}

.result-banner {
    border-radius: 16px; padding: 20px; text-align: center;
    font-size: 1.4rem; font-weight: 700; margin: 12px 0;
}
.result-correct { background: rgba(67,233,123,0.15); border: 1px solid #43e97b; color: #43e97b; }
.result-wrong   { background: rgba(245,87,108,0.15); border: 1px solid #f5576c; color: #f5576c; }
.result-timeout { background: rgba(253,160,133,0.15); border: 1px solid #fda085; color: #fda085; }

/* ボタン */
div.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-size: 1.05rem !important; font-weight: 700 !important; padding: 12px 28px !important;
    width: 100%; transition: opacity 0.2s; font-family: 'Noto Sans JP', sans-serif !important;
}
div.stButton > button:hover { opacity: 0.85 !important; }

/* ★修正: テキスト入力を見やすく（白背景＋黒文字） */
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    color: #111111 !important;
    border: 2px solid #667eea !important;
    border-radius: 12px !important;
    font-size: 1.4rem !important;
    text-align: center;
    font-family: 'Share Tech Mono', monospace !important;
    padding: 14px !important;
    font-weight: 700 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #999 !important; }
div[data-testid="stTextInput"] label {
    color: #e0e0ff !important; font-size: 1rem !important; font-weight: 700 !important;
}

/* チェックボックス */
div[data-testid="stCheckbox"] label { color: #e0e0ff !important; font-size: 1rem !important; }
div[data-testid="stCheckbox"] { margin: 4px 0; }

.diff-card {
    border-radius: 16px; padding: 18px 16px; text-align: center;
    border: 2px solid transparent; margin: 4px; transition: all 0.2s;
}
.diff-easy   { background: rgba(67,233,123,0.1);  border-color: rgba(67,233,123,0.4); }
.diff-normal { background: rgba(102,126,234,0.1); border-color: rgba(102,126,234,0.4); }
.diff-hard   { background: rgba(245,87,108,0.1);  border-color: rgba(245,87,108,0.4); }
.diff-title  { font-size: 1.2rem; font-weight: 700; }
.diff-sub    { font-size: 0.82rem; color: #aaa; margin-top: 4px; }

/* 単元タグ */
.unit-tag {
    display: inline-block; background: rgba(102,126,234,0.2);
    border: 1px solid rgba(102,126,234,0.5); border-radius: 8px;
    padding: 4px 10px; font-size: 0.8rem; color: #aac; margin: 2px;
}

.win-screen  { text-align:center; padding:40px 0; }
.win-emoji   { font-size: 5rem; }
.win-title   { font-size: 2.5rem; font-weight:900; margin:12px 0; }
.win-player  { color: #43e97b; }
.win-ai      { color: #f5576c; }

p { color: #c8c8e8 !important; font-size: 1rem !important; }

/* セクション区切り */
.section-header {
    color: #f093fb; font-size: 0.8rem; letter-spacing: 3px;
    text-transform: uppercase; margin: 20px 0 8px; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 問題定義（単元ごと）
# ─────────────────────────────────────────

ALL_UNITS = {
    # ─ 中学 ─
    "一次方程式":       {"grade": "中学1年", "diff": "easy"},
    "比例・反比例":     {"grade": "中学1年", "diff": "easy"},
    "絶対値":           {"grade": "中学1年", "diff": "easy"},
    "面積・図形基礎":   {"grade": "中学1年", "diff": "easy"},
    "連立方程式":       {"grade": "中学2年", "diff": "normal"},
    "一次関数":         {"grade": "中学2年", "diff": "normal"},
    "角度・図形":       {"grade": "中学2年", "diff": "normal"},
    "割合・比":         {"grade": "中学2年", "diff": "normal"},
    "三平方の定理":     {"grade": "中学3年", "diff": "normal"},
    "因数分解":         {"grade": "中学3年", "diff": "normal"},
    "二次方程式":       {"grade": "中学3年", "diff": "hard"},
    "確率":             {"grade": "中学3年", "diff": "normal"},
    # ─ 高校 ─
    "等差数列":         {"grade": "高校1年", "diff": "normal"},
    "等比数列":         {"grade": "高校2年", "diff": "hard"},
    "一次不等式":       {"grade": "高校1年", "diff": "hard"},
    "三角比":           {"grade": "高校1年", "diff": "hard"},
    "対数":             {"grade": "高校2年", "diff": "hard"},
}

def _linear1():
    a = random.randint(2, 9); b = random.randint(1, 20)
    x = random.randint(-10, 10); c = a * x + b
    return {
        "unit": "一次方程式", "level": "中学1年",
        "q": f"{a}x {'+' if b>=0 else '-'} {abs(b)} = {c}　→ x = ?",
        "answer": str(x),
        "explanation": (
            f"**解き方**\n\n{a}x {'+' if b>=0 else '-'} {abs(b)} = {c}\n\n"
            f"両辺から {'+' if b>=0 else '-'}{abs(b)} を移項：\n\n"
            f"{a}x = {c-b}\n\nx = {c-b} ÷ {a} = **{x}**"
        ),
    }

def _proportion():
    a = random.choice([2,3,4,5,6,8,10]); x = random.randint(1,10); y = a*x
    return {
        "unit": "比例・反比例", "level": "中学1年",
        "q": f"y は x に比例し、x=1 のとき y={a}。\nx={x} のとき y = ?",
        "answer": str(y),
        "explanation": f"**解き方**\n\ny = ax → a={a}\n\ny = {a} × {x} = **{y}**",
    }

def _abs_value():
    x = random.randint(-15,15)
    return {
        "unit": "絶対値", "level": "中学1年",
        "q": f"|{x}| の値は？",
        "answer": str(abs(x)),
        "explanation": f"**解き方**\n\n絶対値は原点からの距離。|{x}| = **{abs(x)}**",
    }

def _area_basic():
    r = random.randint(2,10); area = r*r
    return {
        "unit": "面積・図形基礎", "level": "中学1年",
        "q": f"一辺が {r} cm の正方形の面積は何 cm²？",
        "answer": str(area),
        "explanation": f"**解き方**\n\n面積 = 一辺 × 一辺 = {r} × {r} = **{area}** cm²",
    }

def _simultaneous():
    x = random.randint(1,5); y = random.randint(1,5)
    a1,b1 = random.randint(1,3), random.randint(1,3)
    a2,b2 = random.randint(1,3), random.randint(1,3)
    c1 = a1*x + b1*y; c2 = a2*x + b2*y
    return {
        "unit": "連立方程式", "level": "中学2年",
        "q": f"連立方程式の x の値は？\n{a1}x + {b1}y = {c1}\n{a2}x + {b2}y = {c2}",
        "answer": str(x),
        "explanation": (
            f"**解き方**\n\n①: {a1}x + {b1}y = {c1}\n②: {a2}x + {b2}y = {c2}\n\n"
            f"解: x = **{x}**, y = {y}"
        ),
    }

def _linear_func():
    a = random.choice([-3,-2,-1,1,2,3,4]); b = random.randint(-8,8)
    x = random.randint(-4,4); y = a*x+b
    return {
        "unit": "一次関数", "level": "中学2年",
        "q": f"y = {a}x {'+' if b>=0 else ''}{b} で x={x} のとき y = ?",
        "answer": str(y),
        "explanation": f"**解き方**\n\ny = {a}×{x} {'+' if b>=0 else ''}{b} = {a*x} {'+' if b>=0 else ''}{b} = **{y}**",
    }

def _geometry_angle():
    a = random.randint(30,80); b = random.randint(30,80); c = 180-a-b
    return {
        "unit": "角度・図形", "level": "中学2年",
        "q": f"三角形の2つの内角が {a}°, {b}°\n残りの内角は何度？",
        "answer": str(c),
        "explanation": f"**解き方**\n\n内角の和 = 180°\n\n残り = 180 - {a} - {b} = **{c}°**",
    }

def _percent_calc():
    orig = random.choice([100,200,500,1000,2000])
    pct = random.choice([10,15,20,25,30]); result = orig*pct//100
    return {
        "unit": "割合・比", "level": "中学2年",
        "q": f"{orig} 円の {pct}% はいくら？",
        "answer": str(result),
        "explanation": f"**解き方**\n\n{orig} × {pct}/100 = **{result}** 円",
    }

def _pythagorean():
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25)]
    a,b,c = random.choice(triples); k = random.randint(1,3)
    return {
        "unit": "三平方の定理", "level": "中学3年",
        "q": f"2辺が {a*k}, {b*k} の直角三角形の斜辺は？",
        "answer": str(c*k),
        "explanation": (
            f"**三平方の定理**\n\n斜辺² = {a*k}² + {b*k}²\n\n"
            f"= {(a*k)**2} + {(b*k)**2} = {(c*k)**2}\n\n斜辺 = **{c*k}**"
        ),
    }

def _quadratic_factor():
    r1 = random.randint(-5,5); r2 = random.randint(-5,5)
    b = -(r1+r2); c = r1*r2; roots = sorted([r1,r2])
    return {
        "unit": "因数分解", "level": "中学3年",
        "q": (
            f"因数分解して解け（小さい順 例: -3,2）\n\n"
            f"x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c} = 0"
        ),
        "answer": f"{roots[0]},{roots[1]}",
        "explanation": (
            f"**解き方**\n\n= (x{'+' if -r1>=0 else ''}{-r1})(x{'+' if -r2>=0 else ''}{-r2}) = 0\n\n"
            f"x = **{roots[0]}**, **{roots[1]}**"
        ),
    }

def _quadratic_formula():
    r1 = random.randint(-4,4); r2 = random.randint(-4,4)
    b = -(r1+r2); c = r1*r2; roots = sorted([r1,r2])
    D = b*b - 4*c; sqrtD = int(math.sqrt(D)) if D >= 0 else 0
    return {
        "unit": "二次方程式", "level": "中学3年",
        "q": (
            f"解の公式で解け（小さい順 例: -2,3）\n\n"
            f"x² {'+' if b>=0 else ''}{b}x {'+' if c>=0 else ''}{c} = 0"
        ),
        "answer": f"{roots[0]},{roots[1]}",
        "explanation": (
            f"**解の公式**: x = (-b ± √(b²-4ac)) / 2a\n\n"
            f"D = {b}² - 4×{c} = {D}, √D = {sqrtD}\n\n"
            f"x = ({-b} ± {sqrtD}) / 2 = **{roots[0]}**, **{roots[1]}**"
        ),
    }

def _probability():
    n = random.randint(3,6); k = random.randint(1,n-1)
    g = math.gcd(k,n)
    ans = f"{k//g}/{n//g}" if g > 1 else f"{k}/{n}"
    return {
        "unit": "確率", "level": "中学3年",
        "q": (
            f"1〜{n} の番号カード {n} 枚から1枚引く。\n"
            f"{k} 以下の確率は？（例: 2/5）"
        ),
        "answer": ans,
        "explanation": (
            f"**解き方**\n\n全事象={n}通り, {k}以下={k}通り\n\n"
            f"確率 = {k}/{n}" + (f" = **{ans}**" if g>1 else "")
        ),
    }

def _sequence_arithmetic():
    a1 = random.randint(1,10); d = random.randint(2,7); n = random.randint(5,12)
    an = a1+(n-1)*d
    return {
        "unit": "等差数列", "level": "高校1年",
        "q": f"初項 {a1}、公差 {d} の等差数列の第 {n} 項は？",
        "answer": str(an),
        "explanation": (
            f"**等差数列の一般項**\n\naₙ = a₁ + (n-1)d\n\n"
            f"a_{n} = {a1} + ({n}-1)×{d} = {a1}+{(n-1)*d} = **{an}**"
        ),
    }

def _sequence_geometric():
    a1 = random.randint(1,5); r = random.choice([2,3,-2]); n = random.randint(3,6)
    an = a1*(r**(n-1))
    return {
        "unit": "等比数列", "level": "高校2年",
        "q": f"初項 {a1}、公比 {r} の等比数列の第 {n} 項は？",
        "answer": str(an),
        "explanation": (
            f"**等比数列の一般項**\n\naₙ = a₁ × r^(n-1)\n\n"
            f"a_{n} = {a1} × {r}^{n-1} = {a1}×{r**(n-1)} = **{an}**"
        ),
    }

def _inequality():
    a = random.randint(2,5); lhs_b = random.randint(-8,-1); rhs = random.randint(1,12)
    num = rhs - lhs_b
    x_val = math.ceil(num/a) if num % a != 0 else num//a
    return {
        "unit": "一次不等式", "level": "高校1年",
        "q": f"{a}x {'+' if lhs_b>=0 else ''}{lhs_b} > {rhs}\n\nx > □ の □ は？（整数）",
        "answer": str(x_val),
        "explanation": (
            f"**解き方**\n\n{a}x > {rhs}-({lhs_b}) = {num}\n\n"
            f"x > {num}/{a} → x > **{x_val}**"
        ),
    }

def _sin_cos_basic():
    angles = {30: ("1/2","√3/2"), 45: ("√2/2","√2/2"), 60: ("√3/2","1/2")}
    angle = random.choice([30,45,60]); func = random.choice(["sin","cos"])
    val = angles[angle][0] if func=="sin" else angles[angle][1]
    return {
        "unit": "三角比", "level": "高校1年",
        "q": f"{func} {angle}° の値は？\n（例: √3/2）",
        "answer": val,
        "explanation": (
            f"**三角比の表**\n\n| 角 | sin | cos |\n|---|---|---|\n"
            f"| 30° | 1/2 | √3/2 |\n| 45° | √2/2 | √2/2 |\n| 60° | √3/2 | 1/2 |\n\n"
            f"{func} {angle}° = **{val}**"
        ),
    }

def _log_basic():
    base = random.choice([2,3,10]); exp = random.randint(2,4); val = base**exp
    return {
        "unit": "対数", "level": "高校2年",
        "q": f"log_{base}({val}) = ?（整数で）",
        "answer": str(exp),
        "explanation": (
            f"**解き方**\n\nlog_{base}({val}) = x とおくと\n\n"
            f"{base}^x = {val} = {base}^{exp}\n\nx = **{exp}**"
        ),
    }

# 単元 → 生成関数のマッピング
UNIT_GENERATORS = {
    "一次方程式":    _linear1,
    "比例・反比例":  _proportion,
    "絶対値":        _abs_value,
    "面積・図形基礎":_area_basic,
    "連立方程式":    _simultaneous,
    "一次関数":      _linear_func,
    "角度・図形":    _geometry_angle,
    "割合・比":      _percent_calc,
    "三平方の定理":  _pythagorean,
    "因数分解":      _quadratic_factor,
    "二次方程式":    _quadratic_formula,
    "確率":          _probability,
    "等差数列":      _sequence_arithmetic,
    "等比数列":      _sequence_geometric,
    "一次不等式":    _inequality,
    "三角比":        _sin_cos_basic,
    "対数":          _log_basic,
}

# 学年グループ
GRADE_GROUPS = {
    "中学1年": ["一次方程式","比例・反比例","絶対値","面積・図形基礎"],
    "中学2年": ["連立方程式","一次関数","角度・図形","割合・比"],
    "中学3年": ["三平方の定理","因数分解","二次方程式","確率"],
    "高校1年": ["等差数列","一次不等式","三角比"],
    "高校2年": ["等比数列","対数"],
}

# ─────────────────────────────────────────
# セッション初期化
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "title",
        "difficulty": "normal",
        "selected_units": list(UNIT_GENERATORS.keys()),
        "player_score": 0,
        "ai_score": 0,
        "current_q": None,
        "q_start_time": None,
        "answer_submitted": False,
        "last_result": None,
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

DIFFICULTY_CONFIG = {
    "easy":   {"label": "かんたん",  "limit": 40, "color": "#43e97b"},
    "normal": {"label": "ふつう",    "limit": 30, "color": "#667eea"},
    "hard":   {"label": "むずかしい","limit": 20, "color": "#f5576c"},
}

# ─────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────
def new_question():
    units = ss["selected_units"] if ss["selected_units"] else list(UNIT_GENERATORS.keys())
    unit = random.choice(units)
    ss["current_q"] = UNIT_GENERATORS[unit]()
    ss["q_start_time"] = time.time()
    ss["answer_submitted"] = False
    ss["last_result"] = None
    ss["show_explanation"] = False
    ss["total_questions"] += 1

def timer_fraction():
    limit = DIFFICULTY_CONFIG[ss["difficulty"]]["limit"]
    return max(0, 1 - (time.time() - ss["q_start_time"]) / limit)

def timer_class(frac):
    if frac > 0.5:  return "timer-ok"
    if frac > 0.25: return "timer-warn"
    return "timer-low"

def remaining_sec():
    limit = DIFFICULTY_CONFIG[ss["difficulty"]]["limit"]
    return max(0, int(limit - (time.time() - ss["q_start_time"])))

def _check_win():
    if ss["player_score"] >= 10:
        ss["screen"] = "result"; ss["winner"] = "player"
    elif ss["ai_score"] >= 10:
        ss["screen"] = "result"; ss["winner"] = "ai"

# ─────────────────────────────────────────
# ★修正: 間違い→必ずAI +1
# ─────────────────────────────────────────
def _submit_answer(user_ans, q):
    correct = user_ans.replace(" ","").lower() == q["answer"].replace(" ","").lower()
    ss["answer_submitted"] = True
    ss["show_explanation"] = True
    if correct:
        ss["last_result"] = "correct"
        ss["player_score"] += 1
        ss["player_correct"] += 1
        ss["history"].append({"q": q["q"], "result": "correct", "answer": q["answer"]})
    else:
        ss["last_result"] = "wrong"
        ss["ai_score"] += 1          # ★ ランダムをやめて必ず +1
        ss["history"].append({"q": q["q"], "result": "wrong", "answer": q["answer"]})
    _check_win()

# ─────────────────────────────────────────
# タイトル画面
# ─────────────────────────────────────────
def screen_title():
    st.markdown("<h1>🧮 数学バトル</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;font-size:1.1rem;color:#aaa;margin-bottom:32px;'>"
        "AIと数学の問題を解いて戦おう！先に10ポイント取った方が勝ち⚔️</p>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎮 ゲームスタート"):
            ss["screen"] = "select"; st.rerun()
    st.markdown("""
<div style='color:#888;font-size:0.9rem;text-align:center;line-height:2.2;margin-top:24px;'>
📚 問題範囲：中学1年〜高校2年　|　単元を自由に選択可能<br>
⏱ 制限時間あり　|　間違えたらAI +1ポイント<br>
🏆 先に10ポイント取れば勝ち！
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 難易度＋単元選択画面
# ─────────────────────────────────────────
def screen_select():
    st.markdown("<h2 style='text-align:center;'>設定</h2>", unsafe_allow_html=True)

    # 難易度
    st.markdown("<div class='section-header'>① 難易度を選ぶ</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='diff-card diff-easy'><div class='diff-title' style='color:#43e97b;'>🟢 かんたん</div><div class='diff-sub'>制限時間 40秒</div></div>", unsafe_allow_html=True)
        if st.button("かんたん"):
            ss["difficulty"] = "easy"
    with col2:
        st.markdown("<div class='diff-card diff-normal'><div class='diff-title' style='color:#667eea;'>🔵 ふつう</div><div class='diff-sub'>制限時間 30秒</div></div>", unsafe_allow_html=True)
        if st.button("ふつう"):
            ss["difficulty"] = "normal"
    with col3:
        st.markdown("<div class='diff-card diff-hard'><div class='diff-title' style='color:#f5576c;'>🔴 むずかしい</div><div class='diff-sub'>制限時間 20秒</div></div>", unsafe_allow_html=True)
        if st.button("むずかしい"):
            ss["difficulty"] = "hard"

    cfg = DIFFICULTY_CONFIG[ss["difficulty"]]
    st.markdown(
        f"<div style='text-align:center;color:{cfg['color']};font-weight:700;margin:8px 0 20px;'>"
        f"現在: {cfg['label']}（制限時間 {cfg['limit']}秒）</div>",
        unsafe_allow_html=True,
    )

    # 単元選択
    st.markdown("<div class='section-header'>② 出題する単元を選ぶ</div>", unsafe_allow_html=True)

    col_all, col_none = st.columns(2)
    with col_all:
        if st.button("✅ すべて選択"):
            ss["selected_units"] = list(UNIT_GENERATORS.keys()); st.rerun()
    with col_none:
        if st.button("⬜ すべて解除"):
            ss["selected_units"] = []; st.rerun()

    for grade, units in GRADE_GROUPS.items():
        st.markdown(f"<p style='color:#f093fb;font-weight:700;margin:14px 0 4px;'>📘 {grade}</p>", unsafe_allow_html=True)
        cols = st.columns(len(units))
        for i, unit in enumerate(units):
            with cols[i]:
                checked = unit in ss["selected_units"]
                if st.checkbox(unit, value=checked, key=f"unit_{unit}"):
                    if unit not in ss["selected_units"]:
                        ss["selected_units"].append(unit)
                else:
                    if unit in ss["selected_units"]:
                        ss["selected_units"].remove(unit)

    # 選択中の表示
    n_selected = len(ss["selected_units"])
    if n_selected == 0:
        st.warning("⚠️ 単元を1つ以上選んでください")
    else:
        tags = "".join(f"<span class='unit-tag'>{u}</span>" for u in ss["selected_units"])
        st.markdown(
            f"<div style='margin:12px 0;'><span style='color:#aaa;font-size:0.85rem;'>選択中 {n_selected}単元：</span>{tags}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_start, _ = st.columns([1,1])
    with col_start:
        if st.button("⚔️ バトル開始！", disabled=(n_selected == 0)):
            _start_game(); st.rerun()

def _start_game():
    ss["player_score"] = 0; ss["ai_score"] = 0
    ss["total_questions"] = 0; ss["player_correct"] = 0
    ss["history"] = []; ss["screen"] = "game"
    new_question()

# ─────────────────────────────────────────
# ゲーム画面
# ─────────────────────────────────────────
def screen_game():
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
</div>""", unsafe_allow_html=True)

    q = ss["current_q"]

    if not ss["answer_submitted"]:
        frac = timer_fraction(); rem = remaining_sec()

        if frac <= 0:
            ss["answer_submitted"] = True; ss["last_result"] = "timeout"
            ss["show_explanation"] = True; ss["ai_score"] += 1
            ss["history"].append({"q": q["q"], "result": "timeout", "answer": q["answer"]})
            _check_win(); st.rerun()

        cls = timer_class(frac)
        st.markdown(f"""
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
  <span style='color:#aaa;font-size:0.85rem;'>残り時間</span>
  <span style='color:white;font-family:"Share Tech Mono",monospace;font-size:1.1rem;font-weight:700;'>{rem}秒</span>
</div>
<div class='timer-bar-wrap'><div class='timer-bar {cls}' style='width:{int(frac*100)}%;'></div></div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class='question-card'>
  <div class='question-level'>📚 {q['level']}｜{q['unit']}</div>
  <div class='question-text'>{q['q'].replace(chr(10), '<br>')}</div>
</div>""", unsafe_allow_html=True)

        answer_input = st.text_input(
            "✏️ 答えを入力してください",
            key=f"ans_{ss['total_questions']}",
            placeholder="ここに入力...",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ 答えを送信", key="submit_btn"):
                if answer_input.strip():
                    _submit_answer(answer_input.strip(), q); st.rerun()
        with col_b:
            if st.button("⏩ スキップ（AI +1）", key="skip_btn"):
                ss["answer_submitted"] = True; ss["last_result"] = "timeout"
                ss["show_explanation"] = True; ss["ai_score"] += 1
                ss["history"].append({"q": q["q"], "result": "skip", "answer": q["answer"]})
                _check_win(); st.rerun()

        time.sleep(1); st.rerun()

    else:
        result = ss["last_result"]
        if result == "correct":
            st.markdown("<div class='result-banner result-correct'>🎉 正解！ あなた +1ポイント</div>", unsafe_allow_html=True)
        elif result == "wrong":
            st.markdown(f"<div class='result-banner result-wrong'>❌ 不正解… AI +1ポイント<br><small>正解: {q['answer']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-banner result-timeout'>⏰ 時間切れ！AI +1ポイント<br><small>正解: {q['answer']}</small></div>", unsafe_allow_html=True)

        if ss["show_explanation"]:
            exp_cls = "explain-card" if result == "correct" else "explain-card wrong"
            st.markdown(f"<div class='{exp_cls}'>", unsafe_allow_html=True)
            st.markdown("**📖 解説**")
            st.markdown(q["explanation"])
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("➡ 次の問題へ"):
            new_question(); st.rerun()

# ─────────────────────────────────────────
# 結果画面
# ─────────────────────────────────────────
def screen_result():
    winner = ss.get("winner","player")
    acc = ss["player_correct"] / max(ss["total_questions"],1) * 100

    if winner == "player":
        st.markdown("<div class='win-screen'><div class='win-emoji'>🏆</div><div class='win-title win-player'>あなたの勝ち！</div><p style='color:#43e97b;'>おめでとう！AIに勝ちました！</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='win-screen'><div class='win-emoji'>🤖</div><div class='win-title win-ai'>AIの勝ち…</div><p style='color:#f5576c;'>次は勝てるはず！もう一度挑戦しよう！</p></div>", unsafe_allow_html=True)

    st.markdown(f"""
<div class='score-board'>
  <div class='score-item'><div class='score-label'>あなた</div><div class='score-value score-player'>{ss['player_score']}</div></div>
  <div class='score-item'><div class='score-label'>正解率</div><div class='score-value' style='color:#f6d365;'>{acc:.0f}%</div></div>
  <div class='score-item'><div class='score-label'>AI</div><div class='score-value score-ai'>{ss['ai_score']}</div></div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 もう一度遊ぶ"):
            ss["screen"] = "select"; ss["history"] = []; st.rerun()
    with col2:
        if st.button("🏠 タイトルへ"):
            ss["screen"] = "title"; st.rerun()

    if ss["history"]:
        with st.expander("📋 問題履歴を見る"):
            for i, h in enumerate(ss["history"], 1):
                icon = "✅" if h["result"]=="correct" else ("⏰" if h["result"] in ["timeout","skip"] else "❌")
                st.markdown(f"**Q{i}** {icon}　正解: `{h['answer']}`")

# ─────────────────────────────────────────
# ルーティング
# ─────────────────────────────────────────
screen = ss["screen"]
if screen == "title":   screen_title()
elif screen == "select": screen_select()
elif screen == "game":   screen_game()
elif screen == "result": screen_result()