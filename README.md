import streamlit as st
import random
import time

# ─── ページ設定 ───────────────────────────────────────────────
st.set_page_config(
    page_title="⚔️ 数学バトル",
    page_icon="⚔️",
    layout="centered",
)

# ─── スタイル ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Orbitron:wght@700;900&display=swap');

/* 全体 */
html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
    background-color: #0d0d1a;
    color: #f0f0ff;
}

/* メインコンテナ */
.block-container {
    padding-top: 2rem;
    max-width: 760px;
}

/* タイトル */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    font-size: 2.8rem !important;
    background: linear-gradient(135deg, #ff6ec7, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem !important;
}

/* HP バー */
.hp-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    margin: 1rem 0;
}
.hp-box {
    flex: 1;
    border-radius: 12px;
    padding: 12px 16px;
    background: #1a1a2e;
    border: 1px solid #2d2d4e;
}
.hp-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #a0a0c0;
    margin-bottom: 4px;
}
.hp-name {
    font-size: 1.1rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 6px;
}
.hp-bar-bg {
    height: 14px;
    border-radius: 7px;
    background: #2d2d4e;
    overflow: hidden;
}
.hp-bar-fill-player {
    height: 100%;
    border-radius: 7px;
    background: linear-gradient(90deg, #34d399, #10b981);
    transition: width 0.5s;
}
.hp-bar-fill-enemy {
    height: 100%;
    border-radius: 7px;
    background: linear-gradient(90deg, #f87171, #ef4444);
    transition: width 0.5s;
}
.hp-text {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-top: 4px;
    text-align: right;
}

/* 問題カード */
.question-card {
    background: linear-gradient(135deg, #1e1b4b, #1a1a2e);
    border: 2px solid #4f46e5;
    border-radius: 16px;
    padding: 28px 32px;
    margin: 1.2rem 0;
    box-shadow: 0 0 24px rgba(79, 70, 229, 0.3);
}
.question-level {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 10px;
}
.question-text {
    font-size: 1.55rem;
    font-weight: 700;
    color: #f8f9ff;
    line-height: 1.5;
}

/* 選択肢ボタン */
.stButton > button {
    width: 100%;
    background: #1e1b4b !important;
    color: #e2e8ff !important;
    border: 2px solid #4f46e5 !important;
    border-radius: 10px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 14px 20px !important;
    transition: all 0.2s ease !important;
    font-family: 'Noto Sans JP', sans-serif !important;
}
.stButton > button:hover {
    background: #312e81 !important;
    border-color: #818cf8 !important;
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(129, 140, 248, 0.4) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* 解説ボックス */
.explanation-box {
    border-radius: 14px;
    padding: 20px 24px;
    margin: 1rem 0;
    font-size: 1.0rem;
    line-height: 1.8;
    font-weight: 500;
}
.explanation-correct {
    background: #052e16;
    border: 2px solid #16a34a;
    color: #bbf7d0;
}
.explanation-wrong {
    background: #2d0a0a;
    border: 2px solid #dc2626;
    color: #fecaca;
}
.explanation-title {
    font-size: 1.1rem;
    font-weight: 900;
    margin-bottom: 10px;
}
.explanation-detail {
    background: rgba(0,0,0,0.25);
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 10px;
    color: #f0f0ff;
    font-size: 0.98rem;
    line-height: 1.9;
    font-weight: 400;
}

/* バトルログ */
.battle-log {
    background: #0f0f1e;
    border: 1px solid #2d2d4e;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.9rem;
    color: #c4c4e0;
    max-height: 140px;
    overflow-y: auto;
    line-height: 1.7;
    font-family: 'Noto Sans JP', monospace;
}

/* ステータスバッジ */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    margin: 2px;
}
.badge-round { background: #1e3a5f; color: #93c5fd; border: 1px solid #3b82f6; }
.badge-score { background: #1e1b4b; color: #a5b4fc; border: 1px solid #6366f1; }
.badge-combo { background: #2d1b0e; color: #fcd34d; border: 1px solid #f59e0b; }

/* セパレーター */
hr { border-color: #2d2d4e !important; }

/* 勝敗画面 */
.result-box {
    background: linear-gradient(135deg, #0f0a2e, #1e0a3e);
    border: 3px solid #7c3aed;
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    box-shadow: 0 0 40px rgba(124, 58, 237, 0.4);
}
.result-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    margin-bottom: 12px;
}
.result-win { color: #fbbf24; text-shadow: 0 0 20px rgba(251, 191, 36, 0.6); }
.result-lose { color: #f87171; text-shadow: 0 0 20px rgba(248, 113, 113, 0.6); }

/* モード選択 */
.mode-card {
    background: #1a1a2e;
    border: 2px solid #2d2d4e;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
    color: #e2e8f0;
}

/* Streamlit デフォルト要素の色を上書き */
label, .stMarkdown p, .stText {
    color: #e2e8f0 !important;
}
.stSelectbox label, .stSlider label {
    color: #c4c4e0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── 問題バンク ───────────────────────────────────────────────
QUESTION_BANK = {
    "かんたん": [
        {
            "q": "12 + 35 = ?",
            "choices": ["45", "47", "48", "50"],
            "answer": "47",
            "explanation": "12 に 35 を足します。\n一の位: 2 + 5 = 7\n十の位: 1 + 3 = 4\n→ 47",
        },
        {
            "q": "9 × 8 = ?",
            "choices": ["63", "72", "81", "64"],
            "answer": "72",
            "explanation": "九九の計算です。\n9 × 8 = 72\n（9 × 9 = 81 の一つ前）",
        },
        {
            "q": "100 − 37 = ?",
            "choices": ["53", "63", "73", "67"],
            "answer": "63",
            "explanation": "100 − 37 を計算します。\n100 − 40 = 60\n60 + 3 = 63（37 ではなく 40 引いたので 3 戻す）",
        },
        {
            "q": "56 ÷ 7 = ?",
            "choices": ["6", "7", "8", "9"],
            "answer": "8",
            "explanation": "56 ÷ 7 = ?\n7 × 8 = 56 なので、答えは 8 です。",
        },
        {
            "q": "3² = ?",
            "choices": ["6", "8", "9", "12"],
            "answer": "9",
            "explanation": "3² は「3 の 2 乗」= 3 × 3 = 9",
        },
        {
            "q": "√25 = ?",
            "choices": ["4", "5", "6", "7"],
            "answer": "5",
            "explanation": "√25 は「25 の平方根」\n5 × 5 = 25 なので √25 = 5",
        },
        {
            "q": "0.5 × 0.4 = ?",
            "choices": ["0.09", "0.2", "0.02", "2"],
            "answer": "0.2",
            "explanation": "小数の掛け算：\n0.5 × 0.4 = 5/10 × 4/10 = 20/100 = 0.2",
        },
        {
            "q": "2/3 + 1/6 = ?",
            "choices": ["3/9", "5/6", "1/2", "3/6"],
            "answer": "5/6",
            "explanation": "通分します（公倍数 = 6）：\n2/3 = 4/6\n4/6 + 1/6 = 5/6",
        },
    ],
    "ふつう": [
        {
            "q": "x² − 5x + 6 = 0 を解け",
            "choices": ["x=1,6", "x=2,3", "x=−2,−3", "x=3,4"],
            "answer": "x=2,3",
            "explanation": "因数分解を使います。\n(x − 2)(x − 3) = 0\n→ x = 2 または x = 3\n\n【確認】積が +6、和が −5 になる 2 数は −2, −3 ではなく 2, 3 です（符号に注意）。",
        },
        {
            "q": "2x + 3y = 12, x − y = 1 のとき x = ?",
            "choices": ["x=2", "x=3", "x=4", "x=5"],
            "answer": "x=3",
            "explanation": "連立方程式：\n② x = y + 1 を①に代入\n2(y+1) + 3y = 12\n5y = 10 → y = 2\nx = y + 1 = 3",
        },
        {
            "q": "log₂ 8 = ?",
            "choices": ["2", "3", "4", "8"],
            "answer": "3",
            "explanation": "log₂ 8 は「2 を何乗したら 8 になるか」\n2³ = 8 なので log₂ 8 = 3",
        },
        {
            "q": "sin(30°) = ?",
            "choices": ["√3/2", "1/√2", "1/2", "√3/3"],
            "answer": "1/2",
            "explanation": "三角比の基本値：\nsin(30°) = 1/2\ncos(30°) = √3/2\ntan(30°) = 1/√3\n\n30-60-90 の三角形で覚えましょう！",
        },
        {
            "q": "等差数列 3, 7, 11, … の第10項は？",
            "choices": ["39", "41", "43", "37"],
            "answer": "39",
            "explanation": "等差数列の一般項：aₙ = a₁ + (n−1)d\n初項 a₁ = 3、公差 d = 4\na₁₀ = 3 + 9 × 4 = 3 + 36 = 39",
        },
        {
            "q": "f(x) = 3x² の導関数 f'(x) は？",
            "choices": ["3x", "6x", "x²", "6x²"],
            "answer": "6x",
            "explanation": "べき乗の微分：d/dx[xⁿ] = n・xⁿ⁻¹\nf(x) = 3x²\nf'(x) = 3 × 2x¹ = 6x",
        },
        {
            "q": "nCr の計算：₅C₂ = ?",
            "choices": ["5", "10", "15", "20"],
            "answer": "10",
            "explanation": "₅C₂ = 5! / (2! × 3!)\n= (5 × 4) / (2 × 1)\n= 20 / 2 = 10\n\n「5 人から 2 人を選ぶ組み合わせ」と考えても OK！",
        },
        {
            "q": "∫₀² 2x dx = ?",
            "choices": ["2", "4", "6", "8"],
            "answer": "4",
            "explanation": "∫2x dx = x²+ C\n→ [x²]₀² = 2² − 0² = 4",
        },
    ],
    "むずかしい": [
        {
            "q": "lim(n→∞) (1 + 1/n)ⁿ = ?",
            "choices": ["1", "2", "e", "π"],
            "answer": "e",
            "explanation": "ネイピア数 e の定義そのものです。\ne ≈ 2.71828…\nこの極限は自然対数の底 e に収束します。\nオイラー数とも呼ばれ、自然対数・指数関数の基本です。",
        },
        {
            "q": "複素数 i⁴ = ?",
            "choices": ["i", "−1", "1", "−i"],
            "answer": "1",
            "explanation": "虚数単位 i の累乗：\ni¹ = i\ni² = −1\ni³ = −i\ni⁴ = (i²)² = (−1)² = 1\n4 の倍数乗は常に 1 になります。",
        },
        {
            "q": "ベクトル (1,2) と (3,4) の内積は？",
            "choices": ["5", "10", "11", "14"],
            "answer": "11",
            "explanation": "内積の公式：a⃗ · b⃗ = a₁b₁ + a₂b₂\n= 1×3 + 2×4\n= 3 + 8\n= 11",
        },
        {
            "q": "行列 [[1,2],[3,4]] の行列式は？",
            "choices": ["−2", "−1", "2", "10"],
            "answer": "−2",
            "explanation": "2×2 行列の行列式：det = ad − bc\n[[a,b],[c,d]] の場合\n= 1×4 − 2×3\n= 4 − 6\n= −2",
        },
        {
            "q": "∫₋∞^∞ e^(−x²) dx = ?",
            "choices": ["1", "√π", "π", "2"],
            "answer": "√π",
            "explanation": "ガウス積分の有名な結果です。\n∫₋∞^∞ e^(−x²) dx = √π\n極座標変換（x²+y²=r²）を使った 2 重積分で証明できます。\n確率・統計の正規分布でも本質的な役割を果たします。",
        },
        {
            "q": "フィボナッチ数列 1,1,2,3,5,… の第8項は？",
            "choices": ["13", "21", "34", "8"],
            "answer": "21",
            "explanation": "フィボナッチ数列：aₙ = aₙ₋₁ + aₙ₋₂\n1, 1, 2, 3, 5, 8, 13, 21\n数えてみると第8項は 21 です。",
        },
    ],
}

DIFFICULTIES = ["かんたん", "ふつう", "むずかしい"]
DAMAGE_MAP = {"かんたん": 15, "ふつう": 25, "むずかしい": 40}
ENEMY_DAMAGE_MAP = {"かんたん": 10, "ふつう": 18, "むずかしい": 28}

ENEMIES = [
    {"name": "スライム", "emoji": "🟢", "hp": 60},
    {"name": "ゴブリン", "emoji": "👺", "hp": 80},
    {"name": "ドラゴン", "emoji": "🐉", "hp": 120},
    {"name": "魔王", "emoji": "💀", "hp": 150},
]

# ─── セッション初期化 ─────────────────────────────────────────
def init_session():
    defaults = {
        "screen": "menu",         # menu / battle / result
        "difficulty": "ふつう",
        "player_hp": 100,
        "enemy_hp": 0,
        "enemy_max_hp": 0,
        "enemy": None,
        "score": 0,
        "round": 0,
        "max_rounds": 8,
        "combo": 0,
        "max_combo": 0,
        "question": None,
        "choices": [],
        "answered": False,
        "last_correct": None,
        "last_damage": 0,
        "battle_log": [],
        "wrong_review": [],     # 間違えた問題の記録
        "enemy_index": 0,
        "show_next_btn": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── ヘルパー ─────────────────────────────────────────────────
def add_log(msg: str):
    st.session_state.battle_log.insert(0, msg)
    if len(st.session_state.battle_log) > 8:
        st.session_state.battle_log.pop()

def pick_question():
    pool = QUESTION_BANK[st.session_state.difficulty]
    q = random.choice(pool)
    choices = q["choices"][:]
    random.shuffle(choices)
    st.session_state.question = q
    st.session_state.choices = choices
    st.session_state.answered = False
    st.session_state.last_correct = None
    st.session_state.show_next_btn = False

def start_battle():
    st.session_state.screen = "battle"
    st.session_state.player_hp = 100
    enemy = ENEMIES[st.session_state.enemy_index].copy()
    st.session_state.enemy = enemy
    st.session_state.enemy_hp = enemy["hp"]
    st.session_state.enemy_max_hp = enemy["hp"]
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.battle_log = []
    st.session_state.wrong_review = []
    pick_question()

def answer(choice: str):
    if st.session_state.answered:
        return
    st.session_state.answered = True
    q = st.session_state.question
    correct = (choice == q["answer"])
    st.session_state.last_correct = correct
    diff = st.session_state.difficulty

    if correct:
        st.session_state.combo += 1
        st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)
        dmg = DAMAGE_MAP[diff]
        combo_bonus = min(st.session_state.combo - 1, 3) * 5
        dmg += combo_bonus
        st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - dmg)
        st.session_state.score += (10 + combo_bonus)
        st.session_state.last_damage = dmg
        combo_str = f" ✨ {st.session_state.combo}連続コンボ！" if st.session_state.combo >= 2 else ""
        add_log(f"⚔️ 正解！ {dmg}ダメージ{combo_str}")
    else:
        st.session_state.combo = 0
        e_dmg = ENEMY_DAMAGE_MAP[diff]
        st.session_state.player_hp = max(0, st.session_state.player_hp - e_dmg)
        st.session_state.last_damage = e_dmg
        add_log(f"💥 不正解… {st.session_state.enemy['name']}に {e_dmg}ダメージ受けた")
        # 間違えた問題を記録
        st.session_state.wrong_review.append({
            "q": q["q"],
            "your": choice,
            "correct": q["answer"],
            "explanation": q["explanation"],
            "round": st.session_state.round + 1,
        })

    st.session_state.round += 1
    st.session_state.show_next_btn = True


# ─── 画面: メニュー ───────────────────────────────────────────
if st.session_state.screen == "menu":
    st.markdown("<h1>⚔️ 数学バトル</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#a0a0c0;font-size:1.0rem;'>問題を解いて敵を倒せ！間違えたら解説でしっかり学ぼう</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🗡 難易度**")
        diff = st.selectbox("", DIFFICULTIES, index=DIFFICULTIES.index(st.session_state.difficulty), label_visibility="collapsed")
        st.session_state.difficulty = diff

    with col2:
        st.markdown("**👾 対戦相手**")
        enemy_names = [f"{e['emoji']} {e['name']} (HP {e['hp']})" for e in ENEMIES]
        e_idx = st.selectbox("", enemy_names, index=st.session_state.enemy_index, label_visibility="collapsed")
        st.session_state.enemy_index = enemy_names.index(e_idx)

    st.markdown("")

    diff_info = {
        "かんたん": ("🟢 かんたん", "基本の四則演算・分数・平方根\nダメージ 15 / 被ダメージ 10"),
        "ふつう":   ("🟡 ふつう",   "方程式・対数・三角比・微積分\nダメージ 25 / 被ダメージ 18"),
        "むずかしい": ("🔴 むずかしい", "極限・複素数・行列・ガウス積分\nダメージ 40 / 被ダメージ 28"),
    }
    info = diff_info[st.session_state.difficulty]
    st.markdown(f"""
    <div style="background:#1a1a2e;border:1px solid #4f46e5;border-radius:12px;padding:16px 20px;margin-bottom:1.2rem;">
        <div style="font-weight:900;font-size:1.05rem;color:#a5b4fc;margin-bottom:6px;">{info[0]}</div>
        <div style="color:#c4c4e0;font-size:0.9rem;white-space:pre-line;">{info[1]}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 バトルスタート！", use_container_width=True):
        start_battle()
        st.rerun()

    st.markdown("""
    <div style="color:#606080;font-size:0.8rem;text-align:center;margin-top:0.5rem;">
    正解でコンボを繋げるとボーナスダメージ！間違えた問題は終了後に解説で確認できます。
    </div>
    """, unsafe_allow_html=True)


# ─── 画面: バトル ─────────────────────────────────────────────
elif st.session_state.screen == "battle":
    enemy = st.session_state.enemy
    p_hp = st.session_state.player_hp
    e_hp = st.session_state.enemy_hp
    e_max = st.session_state.enemy_max_hp

    # ゲームオーバー or クリア 判定
    if p_hp <= 0 or e_hp <= 0 or st.session_state.round >= st.session_state.max_rounds:
        st.session_state.screen = "result"
        st.rerun()

    # ── HP バー ──
    p_pct = max(0, p_hp / 100 * 100)
    e_pct = max(0, e_hp / e_max * 100)
    st.markdown(f"""
    <div class="hp-row">
      <div class="hp-box">
        <div class="hp-label">あなた</div>
        <div class="hp-name">🧙 勇者</div>
        <div class="hp-bar-bg"><div class="hp-bar-fill-player" style="width:{p_pct}%"></div></div>
        <div class="hp-text">{p_hp} / 100 HP</div>
      </div>
      <div style="font-size:1.8rem;color:#6366f1;font-weight:900;">VS</div>
      <div class="hp-box">
        <div class="hp-label">てき</div>
        <div class="hp-name">{enemy['emoji']} {enemy['name']}</div>
        <div class="hp-bar-bg"><div class="hp-bar-fill-enemy" style="width:{e_pct}%"></div></div>
        <div class="hp-text">{e_hp} / {e_max} HP</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ステータス ──
    combo_html = f'<span class="badge badge-combo">🔥 {st.session_state.combo}コンボ</span>' if st.session_state.combo >= 2 else ""
    st.markdown(f"""
    <div style="margin-bottom:0.6rem;">
        <span class="badge badge-round">第 {st.session_state.round + 1} / {st.session_state.max_rounds} 問</span>
        <span class="badge badge-score">⭐ {st.session_state.score} pt</span>
        {combo_html}
    </div>
    """, unsafe_allow_html=True)

    q = st.session_state.question

    # ── 問題カード ──
    diff_icon = {"かんたん": "🟢", "ふつう": "🟡", "むずかしい": "🔴"}
    st.markdown(f"""
    <div class="question-card">
        <div class="question-level">{diff_icon[st.session_state.difficulty]} {st.session_state.difficulty}</div>
        <div class="question-text">{q['q']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 解説表示（回答後） ──
    if st.session_state.answered:
        correct = st.session_state.last_correct
        if correct:
            st.markdown(f"""
            <div class="explanation-box explanation-correct">
                <div class="explanation-title">✅ 正解！ {st.session_state.last_damage}ダメージ！</div>
                <div class="explanation-detail">💡 解説：<br>{q['explanation'].replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="explanation-box explanation-wrong">
                <div class="explanation-title">❌ 不正解… 正解は「{q['answer']}」でした</div>
                <div class="explanation-detail">💡 解説：<br>{q['explanation'].replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── 選択肢 ──
    if not st.session_state.answered:
        cols = st.columns(2)
        for i, c in enumerate(st.session_state.choices):
            with cols[i % 2]:
                if st.button(c, key=f"choice_{i}", use_container_width=True):
                    answer(c)
                    st.rerun()
    else:
        if st.session_state.show_next_btn:
            if st.button("▶️ 次の問題へ", use_container_width=True):
                if st.session_state.player_hp <= 0 or st.session_state.enemy_hp <= 0 or st.session_state.round >= st.session_state.max_rounds:
                    st.session_state.screen = "result"
                else:
                    pick_question()
                st.rerun()

    # ── バトルログ ──
    if st.session_state.battle_log:
        st.markdown("---")
        log_html = "<br>".join(st.session_state.battle_log)
        st.markdown(f'<div class="battle-log">{log_html}</div>', unsafe_allow_html=True)

    # ── 降参ボタン ──
    st.markdown("")
    if st.button("🏳️ 降参してメニューに戻る", use_container_width=False):
        st.session_state.screen = "menu"
        st.rerun()


# ─── 画面: リザルト ───────────────────────────────────────────
elif st.session_state.screen == "result":
    p_hp = st.session_state.player_hp
    e_hp = st.session_state.enemy_hp
    enemy = st.session_state.enemy

    if p_hp <= 0:
        outcome = "lose"
        title = "💀 GAME OVER"
        sub = f"{enemy['emoji']} {enemy['name']} に倒された…"
    elif e_hp <= 0:
        outcome = "win"
        title = "🏆 VICTORY！"
        sub = f"{enemy['emoji']} {enemy['name']} を倒した！"
    else:
        outcome = "win" if st.session_state.score >= 50 else "lose"
        title = "⚔️ バトル終了" 
        sub = f"全 {st.session_state.max_rounds} 問終了"

    css_cls = "result-win" if outcome == "win" else "result-lose"
    st.markdown(f"""
    <div class="result-box">
        <div class="result-title {css_cls}">{title}</div>
        <div style="color:#c4c4e0;font-size:1.05rem;margin-bottom:16px;">{sub}</div>
        <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin-bottom:8px;">
            <div style="background:#1a1a2e;border-radius:10px;padding:12px 20px;">
                <div style="color:#818cf8;font-size:0.75rem;font-weight:700;text-transform:uppercase;">スコア</div>
                <div style="color:#f8f9ff;font-size:1.8rem;font-weight:900;">⭐ {st.session_state.score}</div>
            </div>
            <div style="background:#1a1a2e;border-radius:10px;padding:12px 20px;">
                <div style="color:#818cf8;font-size:0.75rem;font-weight:700;text-transform:uppercase;">最大コンボ</div>
                <div style="color:#fbbf24;font-size:1.8rem;font-weight:900;">🔥 {st.session_state.max_combo}</div>
            </div>
            <div style="background:#1a1a2e;border-radius:10px;padding:12px 20px;">
                <div style="color:#818cf8;font-size:0.75rem;font-weight:700;text-transform:uppercase;">残りHP</div>
                <div style="color:#34d399;font-size:1.8rem;font-weight:900;">❤️ {max(0, p_hp)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 間違えた問題の復習 ──
    wrongs = st.session_state.wrong_review
    if wrongs:
        st.markdown("")
        st.markdown(f"""
        <div style="background:#1a1a2e;border:2px solid #dc2626;border-radius:14px;padding:20px 24px;">
            <div style="font-size:1.15rem;font-weight:900;color:#fca5a5;margin-bottom:4px;">
                📚 間違えた問題の復習 ({len(wrongs)}問)
            </div>
            <div style="color:#a0a0c0;font-size:0.85rem;">しっかり確認してマスターしよう！</div>
        </div>
        """, unsafe_allow_html=True)

        for i, w in enumerate(wrongs):
            with st.expander(f"❌ 第{w['round']}問：{w['q']}", expanded=(i == 0)):
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <span style="background:#2d0a0a;color:#fca5a5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-weight:700;">
                        あなたの答え：{w['your']}
                    </span>
                    &nbsp;→&nbsp;
                    <span style="background:#052e16;color:#86efac;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-weight:700;">
                        正解：{w['correct']}
                    </span>
                </div>
                <div style="background:#0f0f1e;border-left:3px solid #6366f1;border-radius:0 8px 8px 0;padding:12px 16px;color:#d4d4f0;font-size:0.95rem;line-height:1.85;white-space:pre-wrap;">{w['explanation']}</div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#052e16;border:2px solid #16a34a;border-radius:14px;padding:16px 20px;margin-top:1rem;text-align:center;">
            <span style="color:#86efac;font-size:1.1rem;font-weight:700;">🎉 全問正解！完璧なバトルでした！</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 もう一度バトル！", use_container_width=True):
            start_battle()
            st.rerun()
    with c2:
        if st.button("🏠 メニューに戻る", use_container_width=True):
            st.session_state.screen = "menu"
            st.rerun()