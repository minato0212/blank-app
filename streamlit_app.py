import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="✊ じゃんけんゲーム",
    page_icon="✊",
    layout="centered"
)

# カスタムCSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Zen Maru Gothic', sans-serif;
}

.main {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #e94560, #f5a623, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #8892b0;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.score-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.2rem 2rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

.score-label {
    font-size: 0.8rem;
    color: #8892b0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.score-number {
    font-size: 2.5rem;
    font-weight: 900;
}

.win { color: #4ecdc4; }
.lose { color: #e94560; }
.draw { color: #f5a623; }

.hand-display {
    text-align: center;
    font-size: 6rem;
    padding: 1rem;
    animation: pop 0.3s ease;
}

@keyframes pop {
    0% { transform: scale(0.5); opacity: 0; }
    70% { transform: scale(1.15); }
    100% { transform: scale(1); opacity: 1; }
}

.result-banner {
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.result-win {
    background: rgba(78,205,196,0.15);
    color: #4ecdc4;
    border: 2px solid #4ecdc4;
}

.result-lose {
    background: rgba(233,69,96,0.15);
    color: #e94560;
    border: 2px solid #e94560;
}

.result-draw {
    background: rgba(245,166,35,0.15);
    color: #f5a623;
    border: 2px solid #f5a623;
}

.vs-text {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 900;
    color: #8892b0;
    padding: 1rem 0;
}

.history-item {
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    margin: 0.2rem 0;
    font-size: 0.9rem;
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #8892b0;
}

.stButton > button {
    width: 100%;
    font-family: 'Zen Maru Gothic', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    padding: 1rem !important;
    border-radius: 16px !important;
    border: 2px solid rgba(255,255,255,0.1) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.3) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stHorizontalBlock"] {
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "player_hand" not in st.session_state:
    st.session_state.player_hand = None
if "cpu_hand" not in st.session_state:
    st.session_state.cpu_hand = None

# 定数
HANDS = {
    "グー": "✊",
    "チョキ": "✌️",
    "パー": "🖐️"
}

WINS = {
    "グー": "チョキ",
    "チョキ": "パー",
    "パー": "グー"
}

RESULT_EMOJI = {
    "win": "🎉",
    "lose": "😢",
    "draw": "🤝"
}

def judge(player, cpu):
    if player == cpu:
        return "draw"
    elif WINS[player] == cpu:
        return "win"
    else:
        return "lose"

def play(player_choice):
    cpu_choice = random.choice(list(HANDS.keys()))
    result = judge(player_choice, cpu_choice)
    
    st.session_state.player_hand = player_choice
    st.session_state.cpu_hand = cpu_choice
    st.session_state.last_result = result
    
    if result == "win":
        st.session_state.wins += 1
    elif result == "lose":
        st.session_state.losses += 1
    else:
        st.session_state.draws += 1
    
    result_text = {"win": "あなたの勝ち", "lose": "あなたの負け", "draw": "引き分け"}[result]
    emoji = RESULT_EMOJI[result]
    st.session_state.history.insert(0, f"{emoji} {HANDS[player_choice]} vs {HANDS[cpu_choice]} → {result_text}")
    if len(st.session_state.history) > 10:
        st.session_state.history.pop()

# ===== UI =====

st.markdown("<h1>✊ じゃんけん</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>コンピューターと対戦しよう！</p>", unsafe_allow_html=True)

# スコア表示
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='score-card'>
        <div class='score-label'>勝ち</div>
        <div class='score-number win'>{st.session_state.wins}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='score-card'>
        <div class='score-label'>引き分け</div>
        <div class='score-number draw'>{st.session_state.draws}</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='score-card'>
        <div class='score-label'>負け</div>
        <div class='score-number lose'>{st.session_state.losses}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 対戦結果表示
if st.session_state.last_result:
    player = st.session_state.player_hand
    cpu = st.session_state.cpu_hand
    result = st.session_state.last_result
    
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        st.markdown(f"<div class='hand-display'>{HANDS[player]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#ccd6f6;font-weight:700;'>あなた<br>{player}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-text' style='margin-top:2rem'>VS</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='hand-display'>{HANDS[cpu]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#ccd6f6;font-weight:700;'>CPU<br>{cpu}</p>", unsafe_allow_html=True)
    
    result_labels = {
        "win": ("🎉 あなたの勝ち！", "result-win"),
        "lose": ("😢 あなたの負け...", "result-lose"),
        "draw": ("🤝 引き分け！", "result-draw"),
    }
    label, cls = result_labels[result]
    st.markdown(f"<div class='result-banner {cls}'>{label}</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align:center; padding: 2rem; color:#8892b0; font-size:1.2rem;'>
        👇 下のボタンを押して勝負しよう！
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 手を選ぶボタン
st.markdown("#### 手を選んでね")
col_g, col_c, col_p = st.columns(3)
with col_g:
    if st.button("✊\nグー", key="guu"):
        play("グー")
        st.rerun()
with col_c:
    if st.button("✌️\nチョキ", key="choki"):
        play("チョキ")
        st.rerun()
with col_p:
    if st.button("🖐️\nパー", key="paa"):
        play("パー")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 履歴とリセット
col_h, col_r = st.columns([3, 1])
with col_h:
    if st.session_state.history:
        with st.expander("📋 対戦履歴", expanded=False):
            for item in st.session_state.history:
                st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

with col_r:
    if st.button("🔄 リセット"):
        for key in ["wins", "losses", "draws", "history", "last_result", "player_hand", "cpu_hand"]:
            del st.session_state[key]
        st.rerun()