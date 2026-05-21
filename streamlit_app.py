import streamlit as st
import random
import math

# ─────────────────────────────────────────────
#  ページ設定
# ─────────────────────────────────────────────
st.set_page_config(page_title="数学RPG ∑ Quest", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Cinzel+Decorative:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }

.title-font { font-family: 'Cinzel Decorative', serif; }

/* 背景 */
.stApp { background: linear-gradient(135deg, #0d0d1a 0%, #1a0d2e 50%, #0d1a0d 100%); }

/* ボタン */
.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white; border: none; border-radius: 12px;
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700; font-size: 1rem; padding: 0.6rem 1.4rem;
    transition: all 0.2s;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px #7c3aed88; }

/* テキスト入力 */
.stTextInput>div>div>input {
    background: #1e1e3a; color: #e2e8f0;
    border: 2px solid #4f46e5; border-radius: 10px;
    font-family: 'Noto Sans JP', sans-serif; font-size: 1.1rem;
}

/* カード */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px; padding: 1.4rem; margin-bottom: 1rem;
    backdrop-filter: blur(8px);
}
.enemy-card {
    background: linear-gradient(135deg, rgba(220,38,38,0.15), rgba(153,27,27,0.1));
    border: 2px solid #ef4444;
    border-radius: 18px; padding: 1.4rem; margin-bottom: 1rem;
}
.player-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.1));
    border: 2px solid #10b981;
    border-radius: 18px; padding: 1.4rem; margin-bottom: 1rem;
}
.question-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(79,70,229,0.1));
    border: 2px solid #6366f1;
    border-radius: 18px; padding: 1.6rem; margin-bottom: 1rem;
}
.explanation-card {
    background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(217,119,6,0.1));
    border: 2px solid #f59e0b;
    border-radius: 18px; padding: 1.4rem; margin-bottom: 1rem;
}

/* HPバー */
.hp-bar-bg { background: #1e1e3a; border-radius: 999px; height: 22px; margin: 4px 0; overflow: hidden; }
.hp-bar-player { background: linear-gradient(90deg, #10b981, #6ee7b7); height: 100%; border-radius: 999px; transition: width 0.5s; }
.hp-bar-enemy { background: linear-gradient(90deg, #ef4444, #fca5a5); height: 100%; border-radius: 999px; transition: width 0.5s; }

/* テキスト */
h1,h2,h3 { color: #e2e8f0 !important; }
p, .stMarkdown { color: #cbd5e1; }
.big-emoji { font-size: 3.5rem; text-align: center; display: block; }
.rank-badge { display: inline-block; padding: 2px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 700; }
.rank-d { background: #4ade80; color: #052e16; }
.rank-b { background: #facc15; color: #1c1917; }
.rank-s { background: linear-gradient(90deg, #f97316, #ef4444); color: white; }
.damage-text { color: #ef4444; font-weight: 900; font-size: 1.3rem; }
.heal-text { color: #10b981; font-weight: 900; font-size: 1.3rem; }
.correct-text { color: #6ee7b7; font-weight: 900; font-size: 1.3rem; }
.wrong-text { color: #fca5a5; font-weight: 900; font-size: 1.3rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  敵キャラクター定義（オリジナル）
# ─────────────────────────────────────────────
ENEMIES = {
    "D": [  # ランクD（中1〜中2）
        {
            "name": "ルート・ゴブリン",
            "emoji": "👺",
            "description": "√を食べて育った地下の小悪魔。計算ミスを狙っている。",
            "hp": 60, "attack": 15,
            "rank": "D",
        },
        {
            "name": "カズ・スライム",
            "emoji": "🟢",
            "description": "数字を吸収して形を変える謎のスライム。",
            "hp": 50, "attack": 12,
            "rank": "D",
        },
        {
            "name": "ヒレイ・バット",
            "emoji": "🦇",
            "description": "比例・反比例の洞窟に潜む夜行性の魔物。",
            "hp": 55, "attack": 14,
            "rank": "D",
        },
    ],
    "B": [  # ランクB（中3〜高1）
        {
            "name": "二次方程式の魔女",
            "emoji": "🧙‍♀️",
            "description": "判別式を操り、解なしの呪いをかける恐ろしい魔女。",
            "hp": 90, "attack": 22,
            "rank": "B",
        },
        {
            "name": "ベクトル・ゴーレム",
            "emoji": "🗿",
            "description": "大きさと向きを持つ石の巨人。内積で心を読む。",
            "hp": 100, "attack": 25,
            "rank": "B",
        },
        {
            "name": "因数分解の番人",
            "emoji": "🔐",
            "description": "式を解体されることを何より嫌う古代の守護者。",
            "hp": 85, "attack": 20,
            "rank": "B",
        },
    ],
    "S": [  # ランクS（高2）
        {
            "name": "∫積分の魔王 ∑igma",
            "emoji": "👿",
            "description": "全ての数学を支配する闇の王。彼を倒せれば数学マスターだ。",
            "hp": 150, "attack": 35,
            "rank": "S",
        },
        {
            "name": "微分女帝 d/dx",
            "emoji": "🔱",
            "description": "変化率を操り時間を加速させる古代の女帝。",
            "hp": 130, "attack": 32,
            "rank": "S",
        },
        {
            "name": "対数の賢者 log∞",
            "emoji": "🌑",
            "description": "底の変換を自在に操り、真数条件の落とし穴を作る。",
            "hp": 140, "attack": 30,
            "rank": "S",
        },
    ]
}

# ─────────────────────────────────────────────
#  問題生成
# ─────────────────────────────────────────────
def generate_question(rank):
    """rankに応じた問題を返す (question_text, answer, explanation, category)"""

    if rank == "D":
        pool = [
            _q_linear_equation,
            _q_proportion,
            _q_square_root,
            _q_polynomial_mult,
            _q_ratio,
        ]
    elif rank == "B":
        pool = [
            _q_quadratic_formula,
            _q_factoring,
            _q_simultaneous,
            _q_sine_rule_basic,
            _q_vector_basic,
            _q_probability,
        ]
    else:  # S
        pool = [
            _q_differential,
            _q_integral,
            _q_log,
            _q_trig_equation,
            _q_quadratic_inequality,
        ]

    fn = random.choice(pool)
    return fn()


def _q_linear_equation():
    a = random.randint(2, 9)
    b = random.randint(1, 20)
    ans = random.randint(-10, 10)
    c = a * ans + b
    return (
        f"次の方程式を解け：{a}x + {b} = {c}",
        str(ans),
        f"{a}x = {c} - {b} = {c - b}　なので　x = {c - b} ÷ {a} = **{ans}**",
        "一次方程式"
    )


def _q_proportion():
    k = random.randint(2, 8)
    x = random.randint(1, 10)
    y = k * x
    ask_x = random.randint(1, 10)
    ans = k * ask_x
    return (
        f"y は x に比例し、x = {x} のとき y = {y} である。x = {ask_x} のとき y は？",
        str(ans),
        f"比例定数 k = y/x = {y}/{x} = {k}。よって y = {k}x に x = {ask_x} を代入 → y = **{ans}**",
        "比例"
    )


def _q_square_root():
    n = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
    return (
        f"√{n} = ?（整数で答えよ）",
        str(int(math.sqrt(n))),
        f"√{n} = **{int(math.sqrt(n))}** （{int(math.sqrt(n))}² = {n}）",
        "平方根"
    )


def _q_polynomial_mult():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    c = random.randint(1, 5)
    d = random.randint(1, 5)
    # (ax+b)(cx+d) の展開
    coef_x2 = a * c
    coef_x = a * d + b * c
    const = b * d
    def fmt(c2, c1, c0):
        parts = []
        if c2 != 0:
            parts.append(f"{c2}x²" if c2 != 1 else "x²")
        if c1 > 0: parts.append(f"+{c1}x" if c1 != 1 else "+x")
        elif c1 < 0: parts.append(f"{c1}x" if c1 != -1 else "-x")
        if c0 > 0: parts.append(f"+{c0}")
        elif c0 < 0: parts.append(str(c0))
        return "".join(parts).lstrip("+")
    ans_str = fmt(coef_x2, coef_x, const)
    return (
        f"展開せよ：({a}x + {b})({c}x + {d})",
        ans_str,
        f"FOIL法：{a}x×{c}x + {a}x×{d} + {b}×{c}x + {b}×{d} = {coef_x2}x² + {a*d}x + {b*c}x + {const} = **{ans_str}**",
        "式の展開"
    )


def _q_ratio():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    total = random.randint(20, 100)
    part_a = round(total * a / (a + b))
    return (
        f"{a} : {b} の比で {total} を分けるとき、大きい方の値は？（整数で答えよ）",
        str(max(part_a, total - part_a)),
        f"合計を (a+b) = {a+b} で割り、a 分を掛ける。{total} × {max(a,b)}/{a+b} ≈ **{max(part_a, total-part_a)}**",
        "比の計算"
    )


def _q_quadratic_formula():
    # 解が整数になるケース: x²+bx+c=0, 解 p,q
    p = random.randint(-5, 5)
    q = random.randint(-5, 5)
    b = -(p + q)
    c = p * q
    b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    c_str = f"+ {c}" if c >= 0 else f"- {abs(c)}"
    ans = f"x={p}, x={q}" if p != q else f"x={p}"
    return (
        f"次の方程式を解け：x² {b_str}x {c_str} = 0",
        ans,
        f"因数分解 → (x - {p})(x - {q}) = 0 → **x = {p}, x = {q}**",
        "二次方程式"
    )


def _q_factoring():
    a = random.randint(1, 4)
    b = random.randint(1, 6)
    expr = f"{a**2}x² - {b**2}" if a != 1 else f"x² - {b**2}"
    ans = f"({a}x+{b})({a}x-{b})" if a != 1 else f"(x+{b})(x-{b})"
    return (
        f"因数分解せよ：{expr}",
        ans,
        f"差の平方の公式 a²-b² = (a+b)(a-b) を使う → **{ans}**",
        "因数分解"
    )


def _q_simultaneous():
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    a1 = random.randint(1, 4)
    b1 = random.randint(1, 4)
    a2 = random.randint(1, 4)
    b2 = random.randint(1, 4)
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    return (
        f"連立方程式を解け：{a1}x + {b1}y = {c1}　/ {a2}x + {b2}y = {c2}",
        f"x={x}, y={y}",
        f"加減法または代入法で解く → **x = {x}, y = {y}**",
        "連立方程式"
    )


def _q_vector_basic():
    ax, ay = random.randint(1, 5), random.randint(1, 5)
    bx, by = random.randint(1, 5), random.randint(1, 5)
    inner = ax * bx + ay * by
    return (
        f"ベクトル a = ({ax}, {ay})、b = ({bx}, {by}) の内積 a·b を求めよ。",
        str(inner),
        f"a·b = {ax}×{bx} + {ay}×{by} = {ax*bx} + {ay*by} = **{inner}**",
        "ベクトル"
    )


def _q_sine_rule_basic():
    # 簡単な三角比: sin30, cos60等
    choices = [
        ("sin 30°", "1/2", "sin 30° = 1/2 は基本値として暗記。"),
        ("cos 60°", "1/2", "cos 60° = 1/2 は基本値として暗記。"),
        ("tan 45°", "1", "tan 45° = sin45/cos45 = (√2/2)/(√2/2) = 1"),
        ("sin 90°", "1", "sin 90° = 1（単位円の最上点）"),
        ("cos 0°", "1", "cos 0° = 1（単位円の始点）"),
        ("sin 45°", "√2/2", "sin 45° = √2/2 ≈ 0.707"),
        ("cos 30°", "√3/2", "cos 30° = √3/2 ≈ 0.866"),
        ("tan 60°", "√3", "tan 60° = sin60/cos60 = (√3/2)/(1/2) = √3"),
    ]
    q, a, expl = random.choice(choices)
    return (f"{q} の値を求めよ。", a, f"**{q} = {a}**。{expl}", "三角比")


def _q_probability():
    n = random.randint(4, 8)
    r = random.randint(1, 3)
    from math import comb
    total = comb(n, r)
    return (
        f"{n} 個の異なるものから {r} 個を選ぶ組み合わせの数は？（ₙCᵣ）",
        str(total),
        f"C({n},{r}) = {n}! / ({r}! × {n-r}!) = **{total}**",
        "確率・組み合わせ"
    )


def _q_differential():
    n = random.randint(2, 6)
    a = random.randint(1, 5)
    # f(x) = ax^n を微分
    ans = f"{a*n}x^{n-1}" if n - 1 > 1 else (f"{a*n}x" if n - 1 == 1 else str(a * n))
    return (
        f"f(x) = {a}x^{n} を微分せよ。（f'(x) = ?）",
        ans,
        f"べき乗の微分：(axⁿ)' = n·axⁿ⁻¹ → f'(x) = **{ans}**",
        "微分"
    )


def _q_integral():
    n = random.randint(1, 4)
    a = random.randint(1, 4)
    # ∫ax^n dx (不定積分の係数と指数)
    new_coef = a
    new_pow = n + 1
    from math import gcd
    g = gcd(new_coef, new_pow)
    if new_pow // g == 1:
        ans = f"{new_coef // g}x + C"
    else:
        ans = f"{new_coef // g}/{new_pow // g}x^{new_pow} + C" if new_coef // g != 1 else f"1/{new_pow // g}x^{new_pow} + C"
    return (
        f"∫{a}x^{n} dx を求めよ。（積分定数 C を含む）",
        ans,
        f"べき乗の積分：∫axⁿdx = a/(n+1)·xⁿ⁺¹ + C = **{ans}**",
        "積分"
    )


def _q_log():
    base = random.choice([2, 3, 10])
    exp = random.randint(1, 4)
    val = base ** exp
    return (
        f"log_{base} {val} = ?",
        str(exp),
        f"log_{base} {val} = x とすると {base}^x = {val} = {base}^{exp} → x = **{exp}**",
        "対数"
    )


def _q_trig_equation():
    choices = [
        ("0 ≤ x < 2π のとき sin x = 0 の解をすべて答えよ（カンマ区切り）",
         "x=0, x=π",
         "sin x = 0 → x = 0, π（0 ≤ x < 2π の範囲）"),
        ("0 ≤ x < 2π のとき cos x = 1 の解を答えよ",
         "x=0",
         "cos x = 1 → x = 0（単位円上で x 座標が 1 の点）"),
        ("0 ≤ x < 2π のとき sin x = 1 の解を答えよ",
         "x=π/2",
         "sin x = 1 → x = π/2（単位円最上点）"),
    ]
    q, a, expl = random.choice(choices)
    return (q, a, f"**解：{a}**。{expl}", "三角方程式")


def _q_quadratic_inequality():
    p = random.randint(-3, 0)
    q = random.randint(1, 4)
    b = -(p + q)
    c = p * q
    b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    c_str = f"+ {c}" if c >= 0 else f"- {abs(c)}"
    return (
        f"二次不等式を解け：x² {b_str}x {c_str} > 0（p={p}, q={q}）",
        f"x<{p}, x>{q}",
        f"(x - {p})(x - {q}) > 0 → 放物線が x 軸より上 → **x < {p} または x > {q}**",
        "二次不等式"
    )


# ─────────────────────────────────────────────
#  セッション初期化
# ─────────────────────────────────────────────
def init_state():
    if "game_phase" not in st.session_state:
        st.session_state.game_phase = "title"  # title / battle / result
    if "player_hp" not in st.session_state:
        st.session_state.player_hp = 100
    if "player_max_hp" not in st.session_state:
        st.session_state.player_max_hp = 100
    if "enemy" not in st.session_state:
        st.session_state.enemy = None
    if "enemy_hp" not in st.session_state:
        st.session_state.enemy_hp = 0
    if "question" not in st.session_state:
        st.session_state.question = None
    if "answer" not in st.session_state:
        st.session_state.answer = None
    if "explanation" not in st.session_state:
        st.session_state.explanation = None
    if "category" not in st.session_state:
        st.session_state.category = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None  # "correct" / "wrong" / None
    if "battle_log" not in st.session_state:
        st.session_state.battle_log = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "battles_won" not in st.session_state:
        st.session_state.battles_won = 0
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    if "awaiting_next" not in st.session_state:
        st.session_state.awaiting_next = False
    if "selected_rank" not in st.session_state:
        st.session_state.selected_rank = None

init_state()


# ─────────────────────────────────────────────
#  ヘルパー
# ─────────────────────────────────────────────
def hp_bar(current, maximum, player=True):
    pct = max(0, min(100, int(current / maximum * 100)))
    bar_class = "hp-bar-player" if player else "hp-bar-enemy"
    color = "#10b981" if player else "#ef4444"
    return f"""
    <div class="hp-bar-bg">
        <div class="{bar_class}" style="width:{pct}%"></div>
    </div>
    <p style="color:{color}; font-weight:700; margin:2px 0;">{current} / {maximum} HP</p>
    """

def pick_enemy(rank):
    return random.choice(ENEMIES[rank]).copy()

def new_question(rank):
    q, a, expl, cat = generate_question(rank)
    st.session_state.question = q
    st.session_state.answer = a
    st.session_state.explanation = expl
    st.session_state.category = cat
    st.session_state.last_result = None
    st.session_state.awaiting_next = False
    st.session_state.input_key += 1

def start_battle(rank):
    enemy = pick_enemy(rank)
    st.session_state.enemy = enemy
    st.session_state.enemy_hp = enemy["hp"]
    st.session_state.selected_rank = rank
    st.session_state.game_phase = "battle"
    st.session_state.battle_log = []
    st.session_state.last_result = None
    new_question(rank)

def normalize_answer(s):
    return s.replace(" ", "").replace("　", "").lower()


# ─────────────────────────────────────────────
#  タイトル画面
# ─────────────────────────────────────────────
if st.session_state.game_phase == "title":
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem;'>
        <p style='font-size:3rem; margin:0;'>⚔️</p>
        <h1 style='font-family:"Cinzel Decorative", serif; font-size:2.2rem; color:#a78bfa !important;
                   text-shadow: 0 0 30px #7c3aed88; letter-spacing:0.05em;'>
            ∑ Quest
        </h1>
        <p style='color:#94a3b8; font-size:1rem;'>〜 数学の魔物を倒して知識の王者になれ 〜</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎮 ゲームの流れ")
    st.markdown("""
- 数学の問題を解くと **敵にダメージ** を与えられる ⚔️
- 間違えると **自分がダメージ** を受ける 💥
- HPが0になる前に敵を倒せ！
- 各問題に **解説** あり 📖
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### ⚔️ 難易度を選んでバトル開始！")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='card' style='text-align:center;'>
            <span class='rank-badge rank-d'>RANK D</span>
            <p style='font-size:2rem;'>👺</p>
            <p style='font-weight:700; color:#4ade80;'>中1〜中2レベル</p>
            <p style='font-size:0.85rem; color:#94a3b8;'>一次方程式・比例・平方根</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Dランクで戦う", key="d_rank", use_container_width=True):
            start_battle("D")
            st.rerun()

    with col2:
        st.markdown("""
        <div class='card' style='text-align:center;'>
            <span class='rank-badge rank-b'>RANK B</span>
            <p style='font-size:2rem;'>🧙‍♀️</p>
            <p style='font-weight:700; color:#facc15;'>中3〜高1レベル</p>
            <p style='font-size:0.85rem; color:#94a3b8;'>二次方程式・ベクトル・確率</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Bランクで戦う", key="b_rank", use_container_width=True):
            start_battle("B")
            st.rerun()

    with col3:
        st.markdown("""
        <div class='card' style='text-align:center;'>
            <span class='rank-badge rank-s'>RANK S</span>
            <p style='font-size:2rem;'>👿</p>
            <p style='font-weight:700; color:#f97316;'>高2レベル</p>
            <p style='font-size:0.85rem; color:#94a3b8;'>微分・積分・対数</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sランクで戦う", key="s_rank", use_container_width=True):
            start_battle("S")
            st.rerun()

    if st.session_state.battles_won > 0 or st.session_state.score > 0:
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <p style='color:#a78bfa; font-size:1.1rem; font-weight:700;'>
                🏆 これまでの成績：撃破数 {st.session_state.battles_won} 体 ／ スコア {st.session_state.score} 点
            </p>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  バトル画面
# ─────────────────────────────────────────────
elif st.session_state.game_phase == "battle":
    enemy = st.session_state.enemy
    rank = st.session_state.selected_rank
    rank_labels = {"D": "D", "B": "B", "S": "S"}
    rank_class = {"D": "rank-d", "B": "rank-b", "S": "rank-s"}

    # ── ヘッダー
    st.markdown(f"""
    <div style='text-align:center; padding-bottom:0.5rem;'>
        <h2 style='color:#a78bfa !important; font-size:1.6rem;'>⚔️ BATTLE ⚔️</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── 敵ステータス
    enemy_pct = max(0, int(st.session_state.enemy_hp / enemy["hp"] * 100))
    st.markdown(f"""
    <div class='enemy-card'>
        <div style='display:flex; align-items:center; gap:1rem;'>
            <span style='font-size:3rem;'>{enemy['emoji']}</span>
            <div style='flex:1;'>
                <div style='display:flex; align-items:center; gap:0.5rem;'>
                    <span class='rank-badge {rank_class[rank]}'>RANK {rank}</span>
                    <span style='color:#f1f5f9; font-weight:900; font-size:1.2rem;'>{enemy['name']}</span>
                </div>
                <p style='color:#94a3b8; font-size:0.85rem; margin:4px 0;'>{enemy['description']}</p>
                {hp_bar(st.session_state.enemy_hp, enemy['hp'], player=False)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── プレイヤーステータス
    st.markdown(f"""
    <div class='player-card'>
        <div style='display:flex; align-items:center; gap:1rem;'>
            <span style='font-size:2.5rem;'>🧑‍🎓</span>
            <div style='flex:1;'>
                <span style='color:#f1f5f9; font-weight:900; font-size:1.1rem;'>あなた</span>
                {hp_bar(st.session_state.player_hp, st.session_state.player_max_hp, player=True)}
            </div>
            <div style='text-align:right;'>
                <p style='color:#a78bfa; font-weight:700;'>🏆 {st.session_state.score} pts</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 直前の結果 + 解説
    if st.session_state.last_result == "correct":
        st.markdown(f"""
        <div class='explanation-card'>
            <p class='correct-text'>✅ 正解！ 敵に 20 ダメージ！</p>
            <p style='color:#94a3b8; font-size:0.85rem; margin:2px 0;'>
                カテゴリ：{st.session_state.category}
            </p>
            <p style='color:#fcd34d; margin:6px 0 0;'>📖 解説：{st.session_state.explanation}</p>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.last_result == "wrong":
        st.markdown(f"""
        <div class='explanation-card'>
            <p class='wrong-text'>❌ 不正解… {enemy['attack']} ダメージを受けた！</p>
            <p style='color:#94a3b8; font-size:0.85rem; margin:2px 0;'>
                正解：<strong style='color:#fca5a5;'>{st.session_state.answer}</strong>　カテゴリ：{st.session_state.category}
            </p>
            <p style='color:#fcd34d; margin:6px 0 0;'>📖 解説：{st.session_state.explanation}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── 問題
    st.markdown(f"""
    <div class='question-card'>
        <p style='color:#94a3b8; font-size:0.8rem; margin:0 0 6px;'>📚 {st.session_state.category}</p>
        <p style='color:#e2e8f0; font-size:1.2rem; font-weight:700; margin:0;'>{st.session_state.question}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 回答欄（結果表示中は非表示）
    if not st.session_state.awaiting_next:
        user_input = st.text_input(
            "答えを入力してください（例：5、x=3, x=-2 など）",
            key=f"ans_{st.session_state.input_key}",
            placeholder="ここに答えを入力..."
        )

        col_a, col_b = st.columns([2, 1])
        with col_a:
            if st.button("⚔️ 答えを送信", use_container_width=True, key="submit_btn"):
                if user_input.strip():
                    correct_ans = normalize_answer(st.session_state.answer)
                    user_ans = normalize_answer(user_input)
                    if user_ans == correct_ans:
                        dmg = 20
                        st.session_state.enemy_hp -= dmg
                        st.session_state.score += 10
                        st.session_state.last_result = "correct"
                    else:
                        st.session_state.player_hp -= enemy["attack"]
                        st.session_state.last_result = "wrong"
                    st.session_state.awaiting_next = True
                    st.rerun()
        with col_b:
            if st.button("🚪 やめる", use_container_width=True, key="quit_btn"):
                st.session_state.game_phase = "result"
                st.session_state.result_reason = "quit"
                st.rerun()
    else:
        # 結果確認後、次へ進む
        col_a, col_b = st.columns([2, 1])
        with col_a:
            # 勝利/敗北チェック
            if st.session_state.enemy_hp <= 0:
                if st.button("🎉 敵を倒した！次へ", use_container_width=True, key="next_enemy"):
                    st.session_state.battles_won += 1
                    new_enemy = pick_enemy(rank)
                    st.session_state.enemy = new_enemy
                    st.session_state.enemy_hp = new_enemy["hp"]
                    new_question(rank)
                    st.rerun()
            elif st.session_state.player_hp <= 0:
                st.button("💀 ゲームオーバー", use_container_width=True, key="go_btn",
                          on_click=lambda: st.session_state.update({"game_phase": "result", "result_reason": "dead"}))
            else:
                if st.button("➡️ 次の問題へ", use_container_width=True, key="next_q"):
                    new_question(rank)
                    st.rerun()
        with col_b:
            if st.button("🚪 やめる", use_container_width=True, key="quit_btn2"):
                st.session_state.game_phase = "result"
                st.session_state.result_reason = "quit"
                st.rerun()

    # ── バトルログ（最新3件）
    if st.session_state.battle_log:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**📜 バトルログ**")
        for log in st.session_state.battle_log[-3:]:
            st.markdown(f"<p style='color:#94a3b8; font-size:0.85rem; margin:2px 0;'>{log}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  リザルト画面
# ─────────────────────────────────────────────
elif st.session_state.game_phase == "result":
    reason = getattr(st.session_state, "result_reason", "quit")

    if reason == "dead":
        st.markdown("""
        <div style='text-align:center; padding:2rem 0;'>
            <p style='font-size:4rem;'>💀</p>
            <h2 style='color:#ef4444 !important; font-size:2rem;'>GAME OVER</h2>
            <p style='color:#94a3b8;'>HPが尽きてしまった…また挑戦しよう！</p>
        </div>
        """, unsafe_allow_html=True)
    elif reason == "win":
        st.markdown("""
        <div style='text-align:center; padding:2rem 0;'>
            <p style='font-size:4rem;'>🏆</p>
            <h2 style='color:#fbbf24 !important; font-size:2rem;'>VICTORY!</h2>
            <p style='color:#94a3b8;'>見事な勝利！数学の力を見せつけた！</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center; padding:2rem 0;'>
            <p style='font-size:4rem;'>🚪</p>
            <h2 style='color:#a78bfa !important; font-size:2rem;'>退却</h2>
            <p style='color:#94a3b8;'>冒険を中断した。いつでも再挑戦できる！</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='text-align:center;'>
        <p style='color:#e2e8f0; font-size:1.3rem; font-weight:700;'>最終スコア</p>
        <p style='color:#a78bfa; font-size:3rem; font-weight:900;'>{st.session_state.score} pts</p>
        <p style='color:#94a3b8;'>撃破数：{st.session_state.battles_won} 体</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 タイトルに戻る", use_container_width=True):
        # スコアと撃破数は保持、それ以外リセット
        kept_score = st.session_state.score
        kept_won = st.session_state.battles_won
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.score = kept_score
        st.session_state.battles_won = kept_won
        st.session_state.game_phase = "title"
        init_state()
        st.rerun()

    if st.button("🆕 スコアリセットして最初から", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()