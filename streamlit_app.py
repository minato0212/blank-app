import streamlit as st
import random

st.set_page_config(page_title="⚔️ 数学バトル", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500;700;900&family=Orbitron:wght@700;900&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stHeader"],
.main, section.main > div,
[data-testid="stMainBlockContainer"],
.block-container {
    background-color: #070714 !important;
}
.block-container { padding-top: 1.4rem !important; max-width: 800px !important; }

*, *::before, *::after {
    color: #f0f0ff !important;
    font-family: 'Noto Sans JP', sans-serif !important;
}

p, span, div, label, li, td, th, small,
.stMarkdown *, [data-testid="stMarkdownContainer"] *,
[class*="css-"] { color: #f0f0ff !important; }

h1 {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center !important;
    font-size: 2.5rem !important;
    background: linear-gradient(135deg, #ff6ec7 0%, #a78bfa 50%, #60a5fa 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: 2px !important;
    margin-bottom: 0.2rem !important;
}

[data-testid="stTextInput"] input,
.stTextInput input,
input[type="text"] {
    background: #12123a !important;
    border: 2.5px solid #6366f1 !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 1.55rem !important;
    font-weight: 900 !important;
    padding: 14px 22px !important;
    text-align: center !important;
    caret-color: #a78bfa !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.35) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #4040a0 !important; opacity: 1 !important; }
[data-testid="stTextInput"] label { color: #c0c0ff !important; font-size: 0.95rem !important; font-weight: 700 !important; }

[data-baseweb="select"] > div { background: #12123a !important; border-color: #4f46e5 !important; border-radius: 10px !important; }
[data-baseweb="select"] span, [data-baseweb="select"] div { color: #ffffff !important; }
[data-baseweb="popover"] div { background: #12123a !important; color: #ffffff !important; }
[data-testid="stSelectbox"] label { color: #c0c0ff !important; font-weight: 700 !important; }

.stButton > button {
    background: #141450 !important;
    color: #ffffff !important;
    border: 2px solid #4f46e5 !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    padding: 12px 18px !important;
    font-family: 'Noto Sans JP', sans-serif !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #3730a3 !important;
    border-color: #818cf8 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 22px rgba(129,140,248,0.55) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stExpander"] { background: #0c0c24 !important; border: 1.5px solid #2a2a50 !important; border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stExpander"] summary { background: #10103a !important; padding: 10px 16px !important; font-weight: 700 !important; }
[data-testid="stExpander"] > div > div { background: #0c0c24 !important; padding: 12px 16px !important; }

hr { border-color: #20204a !important; margin: 0.7rem 0 !important; }

.q-card {
    background: linear-gradient(135deg, #0f0e35, #0a0a1e);
    border: 2.5px solid #5b52e5;
    border-radius: 18px;
    padding: 24px 28px;
    margin: 0.7rem 0 0.3rem;
    box-shadow: 0 0 32px rgba(91,82,229,0.35);
}
.q-cat  { font-size: 0.7rem !important; font-weight: 800 !important; letter-spacing: 2.5px !important; text-transform: uppercase !important; color: #a78bfa !important; margin-bottom: 7px !important; }
.q-text { font-size: 1.55rem !important; font-weight: 900 !important; color: #ffffff !important; line-height: 1.55 !important; }
.q-hint { margin-top: 9px !important; font-size: 0.85rem !important; color: #8080c8 !important; }

.hp-row  { display: flex; align-items: center; gap: 10px; margin: 0.5rem 0; }
.hp-box  { flex: 1; background: #0b0b22; border: 1.5px solid #1e1e40; border-radius: 13px; padding: 9px 13px; }
.hp-name { font-size: 0.95rem !important; font-weight: 900 !important; color: #ffffff !important; margin-bottom: 5px !important; }
.hp-bg   { height: 12px; border-radius: 6px; background: #18183a; overflow: hidden; }
.hp-p    { height: 100%; border-radius: 6px; background: linear-gradient(90deg,#34d399,#10b981); transition: width .5s; }
.hp-e    { height: 100%; border-radius: 6px; background: linear-gradient(90deg,#f87171,#ef4444); transition: width .5s; }
.hp-num  { font-size: 0.82rem !important; font-weight: 700 !important; color: #d8d8ff !important; margin-top: 3px !important; text-align: right !important; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem !important; font-weight: 700 !important; margin: 2px; }
.b-rnd { background: #0c2040; color: #93c5fd !important; border: 1.5px solid #3b82f6; }
.b-scr { background: #18084a; color: #c4b5fd !important; border: 1.5px solid #7c3aed; }
.b-cmb { background: #2a1400; color: #fcd34d !important; border: 1.5px solid #d97706; }
.b-cat { background: #081e10; color: #6ee7b7 !important; border: 1.5px solid #059669; }

.exp-ok { background: #031208; border: 2px solid #16a34a; border-radius: 14px; padding: 15px 18px; margin: 0.5rem 0; }
.exp-ng { background: #150404; border: 2px solid #dc2626; border-radius: 14px; padding: 15px 18px; margin: 0.5rem 0; }
.exp-ok .exp-ttl { font-size: 1.05rem !important; font-weight: 900 !important; color: #4ade80 !important; margin-bottom: 7px !important; }
.exp-ng .exp-ttl { font-size: 1.05rem !important; font-weight: 900 !important; color: #f87171 !important; margin-bottom: 7px !important; }
.exp-body { background: rgba(0,0,0,0.45); border-radius: 8px; padding: 11px 15px; margin-top: 5px; color: #e8e8ff !important; font-size: 0.93rem !important; line-height: 1.9 !important; white-space: pre-wrap !important; }

.log-box { background: #06060e; border: 1.5px solid #18183a; border-radius: 10px; padding: 10px 14px; font-size: 0.84rem !important; color: #b0b0d8 !important; max-height: 105px; overflow-y: auto; line-height: 1.75 !important; }

.res-box { background: linear-gradient(135deg,#07051a,#130820); border: 3px solid #7c3aed; border-radius: 22px; padding: 28px; text-align: center; box-shadow: 0 0 50px rgba(124,58,237,0.45); }
.res-win  { font-family: 'Orbitron', sans-serif !important; font-size: 2.0rem !important; color: #fbbf24 !important; text-shadow: 0 0 24px rgba(251,191,36,0.65) !important; }
.res-lose { font-family: 'Orbitron', sans-serif !important; font-size: 2.0rem !important; color: #f87171 !important; text-shadow: 0 0 24px rgba(248,113,113,0.65) !important; }
.stat-box { background: #0d0d28; border-radius: 10px; padding: 10px 15px; display: inline-block; margin: 4px; }
.stat-lbl { font-size: 0.65rem !important; font-weight: 700 !important; color: #7070b8 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
.stat-val { font-size: 1.55rem !important; font-weight: 900 !important; color: #ffffff !important; }

.info-card { background: #0e0e2a; border: 2px solid #4f46e5; border-radius: 14px; padding: 13px 17px; margin: 0.8rem 0; }
.info-card .ic-ttl  { font-size: 0.97rem !important; font-weight: 900 !important; color: #c4b5fd !important; margin-bottom: 4px !important; }
.info-card .ic-cats { color: #d4d4ff !important; font-size: 0.86rem !important; margin-bottom: 3px !important; }
.info-card .ic-note { color: #8080b8 !important; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

QUESTION_BANK = {
    "四則演算": [
        {"q": "127 + 358 = ?", "answer": "485", "accept": ["485"], "hint": "整数",
         "explanation": "127 + 358\n= (120+350) + (7+8) = 470 + 15 = 485"},
        {"q": "1003 − 467 = ?", "answer": "536", "accept": ["536"], "hint": "整数",
         "explanation": "1000 − 467 = 533 → + 3 = 536"},
        {"q": "24 × 15 = ?", "answer": "360", "accept": ["360"], "hint": "整数",
         "explanation": "24×10 + 24×5 = 240 + 120 = 360"},
        {"q": "168 ÷ 14 = ?", "answer": "12", "accept": ["12"], "hint": "整数",
         "explanation": "14 × 12 = 168 → 168 ÷ 14 = 12"},
        {"q": "(-3) × (-7) = ?", "answer": "21", "accept": ["21"], "hint": "整数",
         "explanation": "負×負 = 正\n(-3) × (-7) = 21"},
        {"q": "48 ÷ 0.4 = ?", "answer": "120", "accept": ["120"], "hint": "整数",
         "explanation": "÷0.4 = ×2.5\n48 × 2.5 = 120"},
        {"q": "1.25 × 0.8 = ?", "answer": "1", "accept": ["1", "1.0"], "hint": "整数",
         "explanation": "125/100 × 8/10 = 1000/1000 = 1"},
        {"q": "√144 = ?", "answer": "12", "accept": ["12"], "hint": "整数",
         "explanation": "12 × 12 = 144 → √144 = 12"},
        {"q": "2³ × 5 = ?", "answer": "40", "accept": ["40"], "hint": "整数",
         "explanation": "2³ = 8, 8 × 5 = 40"},
        {"q": "3/4 + 5/6 = ?（分数）", "answer": "19/12", "accept": ["19/12"], "hint": "例: 19/12",
         "explanation": "公倍数12で通分\n9/12 + 10/12 = 19/12"},
        {"q": "7² − 4² = ?", "answer": "33", "accept": ["33"], "hint": "整数",
         "explanation": "49 − 16 = 33"},
        {"q": "15% を小数で答えよ", "answer": "0.15", "accept": ["0.15"], "hint": "例: 0.15",
         "explanation": "15 ÷ 100 = 0.15"},
    ],
    "整数・倍数・素数": [
        {"q": "12 と 18 の最大公約数は？", "answer": "6", "accept": ["6"], "hint": "整数",
         "explanation": "12=2²×3, 18=2×3²\nGCD = 2×3 = 6"},
        {"q": "4 と 6 の最小公倍数は？", "answer": "12", "accept": ["12"], "hint": "整数",
         "explanation": "4=2², 6=2×3\nLCM = 2²×3 = 12"},
        {"q": "30 以下の素数は何個？", "answer": "10", "accept": ["10"], "hint": "整数",
         "explanation": "2,3,5,7,11,13,17,19,23,29 → 10個"},
        {"q": "72 = 2ᵃ × 3ᵇ のとき a+b = ?", "answer": "5", "accept": ["5"], "hint": "整数",
         "explanation": "72=2³×3² → a=3, b=2 → 5"},
        {"q": "100 の約数は何個？", "answer": "9", "accept": ["9"], "hint": "整数",
         "explanation": "100=2²×5²\n(2+1)(2+1)=9個"},
        {"q": "2⁸ = ?", "answer": "256", "accept": ["256"], "hint": "整数",
         "explanation": "2^8 = 256"},
        {"q": "999 は 3 の倍数か？（はい/いいえ）", "answer": "はい", "accept": ["はい","1","yes"], "hint": "はい か いいえ",
         "explanation": "各桁の和: 9+9+9=27, 27÷3=9 → 3の倍数"},
    ],
    "分数・比・割合": [
        {"q": "2/3 × 3/4 = ?", "answer": "1/2", "accept": ["1/2", "0.5"], "hint": "例: 1/2",
         "explanation": "2/3 × 3/4 = 6/12 = 1/2"},
        {"q": "5/6 ÷ 5/3 = ?", "answer": "1/2", "accept": ["1/2", "0.5"], "hint": "例: 1/2",
         "explanation": "÷は逆数を掛ける\n5/6 × 3/5 = 1/2"},
        {"q": "3:5 = 24:x → x = ?", "answer": "40", "accept": ["40"], "hint": "整数",
         "explanation": "3x = 120 → x = 40"},
        {"q": "定価1200円の30%引きは？（円）", "answer": "840", "accept": ["840"], "hint": "整数",
         "explanation": "1200 × 0.70 = 840"},
        {"q": "60人の25%は何人？", "answer": "15", "accept": ["15"], "hint": "整数",
         "explanation": "60 × 0.25 = 15"},
        {"q": "元の値80→現在100 → 何%増？", "answer": "25", "accept": ["25","25%"], "hint": "整数",
         "explanation": "(100-80)/80 × 100 = 25%"},
    ],
    "方程式": [
        {"q": "3x − 7 = 14 → x = ?", "answer": "7", "accept": ["7"], "hint": "整数",
         "explanation": "3x = 21 → x = 7"},
        {"q": "2(x+5) = 18 → x = ?", "answer": "4", "accept": ["4"], "hint": "整数",
         "explanation": "x+5 = 9 → x = 4"},
        {"q": "5x+3 = 3x+11 → x = ?", "answer": "4", "accept": ["4"], "hint": "整数",
         "explanation": "2x = 8 → x = 4"},
        {"q": "連立: x+y=10, x-y=4 → x = ?", "answer": "7", "accept": ["7"], "hint": "整数",
         "explanation": "2x = 14 → x = 7"},
        {"q": "x²-7x+12=0 の小さい解は？", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "(x-3)(x-4)=0 → 小: 3"},
        {"q": "2x-3(x-1)=5 → x = ?", "answer": "-2", "accept": ["-2"], "hint": "例: -2",
         "explanation": "-x = 2 → x = -2"},
        {"q": "連立: 2x+3y=12, x-y=1 → y = ?", "answer": "2", "accept": ["2"], "hint": "整数",
         "explanation": "x=y+1 → 5y=10 → y=2"},
        {"q": "|2x-1|=5 の大きい解は？", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "2x-1=5→x=3, 2x-1=-5→x=-2\n大きい方: 3"},
    ],
    "数列・規則": [
        {"q": "等差: 2,5,8,11,… 第8項は？", "answer": "23", "accept": ["23"], "hint": "整数",
         "explanation": "初項2, 公差3\na₈ = 2+7×3 = 23"},
        {"q": "等比: 3,6,12,24,… 第6項は？", "answer": "96", "accept": ["96"], "hint": "整数",
         "explanation": "公比2: a₆=3×2⁵=96"},
        {"q": "1+2+3+…+20 = ?", "answer": "210", "accept": ["210"], "hint": "整数",
         "explanation": "n(n+1)/2 = 20×21/2 = 210"},
        {"q": "フィボナッチ 1,1,2,3,5,8,… 第9項は？", "answer": "34", "accept": ["34"], "hint": "整数",
         "explanation": "…13, 21, 34 → 第9項=34"},
        {"q": "Σ(k=1→5) k² = ?", "answer": "55", "accept": ["55"], "hint": "整数",
         "explanation": "1+4+9+16+25 = 55"},
        {"q": "1+3+5+…+19（奇数の和）= ?", "answer": "100", "accept": ["100"], "hint": "整数",
         "explanation": "n²乗 (n=10): 10²=100"},
        {"q": "2^10 = ?", "answer": "1024", "accept": ["1024"], "hint": "整数",
         "explanation": "2^10 = 1024"},
    ],
    "三角関数・図形": [
        {"q": "sin(30°) = ?（分数）", "answer": "1/2", "accept": ["1/2","0.5"], "hint": "例: 1/2",
         "explanation": "sin30°=1/2"},
        {"q": "cos(60°) = ?（分数）", "answer": "1/2", "accept": ["1/2","0.5"], "hint": "例: 1/2",
         "explanation": "cos60°=1/2"},
        {"q": "tan(45°) = ?", "answer": "1", "accept": ["1","1.0"], "hint": "整数",
         "explanation": "tan45°=1"},
        {"q": "底辺8, 高さ5 の三角形の面積は？", "answer": "20", "accept": ["20"], "hint": "整数",
         "explanation": "8×5÷2=20"},
        {"q": "直角三角形: 底3, 高4 → 斜辺は？", "answer": "5", "accept": ["5"], "hint": "整数",
         "explanation": "√(9+16)=5"},
        {"q": "正六角形の一内角は？（°）", "answer": "120", "accept": ["120"], "hint": "整数",
         "explanation": "(6-2)×180÷6=120"},
        {"q": "半径10の円の面積は？（π=3.14）", "answer": "314", "accept": ["314"], "hint": "整数",
         "explanation": "3.14×100=314"},
        {"q": "sin²x + cos²x = ?", "answer": "1", "accept": ["1"], "hint": "整数",
         "explanation": "三角関数の基本恒等式: 常に1"},
        {"q": "直方体: 縦3, 横4, 高さ5 → 体積は？", "answer": "60", "accept": ["60"], "hint": "整数",
         "explanation": "3×4×5=60"},
    ],
    "指数・対数": [
        {"q": "log₁₀ 1000 = ?", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "10³=1000 → 3"},
        {"q": "log₂ 32 = ?", "answer": "5", "accept": ["5"], "hint": "整数",
         "explanation": "2⁵=32 → 5"},
        {"q": "log₃ 81 = ?", "answer": "4", "accept": ["4"], "hint": "整数",
         "explanation": "3⁴=81 → 4"},
        {"q": "8^(2/3) = ?", "answer": "4", "accept": ["4"], "hint": "整数",
         "explanation": "8^(1/3)=2 → 2²=4"},
        {"q": "log₁₀100 + log₁₀10 = ?", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "2+1=3"},
        {"q": "log₂(1/8) = ?", "answer": "-3", "accept": ["-3"], "hint": "整数",
         "explanation": "2^(-3)=1/8 → -3"},
        {"q": "e⁰ = ?", "answer": "1", "accept": ["1"], "hint": "整数",
         "explanation": "a⁰=1 → e⁰=1"},
    ],
    "微分・積分": [
        {"q": "f(x) = x³ → f'(x) = ?", "answer": "3x^2", "accept": ["3x^2","3x²","3x2"], "hint": "例: 3x^2",
         "explanation": "d/dx[x³]=3x²"},
        {"q": "f(x) = 5x² → f'(x) = ?", "answer": "10x", "accept": ["10x"], "hint": "例: 10x",
         "explanation": "d/dx[5x²]=10x"},
        {"q": "∫₀¹ 3x² dx = ?", "answer": "1", "accept": ["1","1.0"], "hint": "整数",
         "explanation": "[x³]₀¹=1"},
        {"q": "∫₀² x dx = ?", "answer": "2", "accept": ["2","2.0"], "hint": "整数",
         "explanation": "[x²/2]₀²=2"},
        {"q": "f(x)=sin(x) → f'(x) = ?", "answer": "cos(x)", "accept": ["cos(x)","cosx","cos x"], "hint": "例: cos(x)",
         "explanation": "d/dx[sinx]=cosx"},
        {"q": "f(x)=eˣ → f'(x) = ?", "answer": "e^x", "accept": ["e^x","eˣ","ex"], "hint": "例: e^x",
         "explanation": "d/dx[eˣ]=eˣ"},
        {"q": "f(x)=ln(x) → f'(x) = ?", "answer": "1/x", "accept": ["1/x"], "hint": "例: 1/x",
         "explanation": "d/dx[lnx]=1/x"},
    ],
    "確率・統計": [
        {"q": "コイン2枚, 両面表の確率は？", "answer": "1/4", "accept": ["1/4","0.25"], "hint": "例: 1/4",
         "explanation": "全4通り中1通り=1/4"},
        {"q": "サイコロで3の倍数の確率は？", "answer": "1/3", "accept": ["1/3"], "hint": "例: 1/3",
         "explanation": "3,6→2通り/6通り=1/3"},
        {"q": "₅C₂ = ?", "answer": "10", "accept": ["10"], "hint": "整数",
         "explanation": "5!/(2!3!)=10"},
        {"q": "₄P₂ = ?", "answer": "12", "accept": ["12"], "hint": "整数",
         "explanation": "4×3=12"},
        {"q": "2,4,6,8,10 の平均は？", "answer": "6", "accept": ["6"], "hint": "整数",
         "explanation": "30÷5=6"},
        {"q": "3,7,7,9,4 の中央値は？", "answer": "7", "accept": ["7"], "hint": "整数",
         "explanation": "並び替え: 3,4,7,7,9 → 中央=7"},
        {"q": "₆C₃ = ?", "answer": "20", "accept": ["20"], "hint": "整数",
         "explanation": "6!/(3!3!)=20"},
    ],
    "複素数・行列": [
        {"q": "i² = ?", "answer": "-1", "accept": ["-1"], "hint": "整数",
         "explanation": "虚数単位の定義: i²=-1"},
        {"q": "i³ = ?", "answer": "-i", "accept": ["-i"], "hint": "例: -i",
         "explanation": "i³=i²×i=-i"},
        {"q": "i⁴ = ?", "answer": "1", "accept": ["1"], "hint": "整数",
         "explanation": "i⁴=(i²)²=1"},
        {"q": "|3+4i| = ?", "answer": "5", "accept": ["5"], "hint": "整数",
         "explanation": "√(9+16)=5"},
        {"q": "det[[2,1],[3,4]] = ?", "answer": "5", "accept": ["5"], "hint": "整数",
         "explanation": "2×4-1×3=5"},
        {"q": "(1+i)² = ?", "answer": "2i", "accept": ["2i"], "hint": "例: 2i",
         "explanation": "1+2i+i²=2i"},
        {"q": "lim(n→∞)(1+1/n)ⁿ = ?", "answer": "e", "accept": ["e"], "hint": "英字 e",
         "explanation": "ネイピア数 e の定義\ne≈2.71828…"},
    ],
    "速さ・仕事・単位換算": [
        {"q": "時速60kmで3時間走った距離は？（km）", "answer": "180", "accept": ["180"], "hint": "整数",
         "explanation": "60×3=180"},
        {"q": "200kmを4時間で → 時速は？（km/h）", "answer": "50", "accept": ["50"], "hint": "整数",
         "explanation": "200÷4=50"},
        {"q": "1時間36分 = 何分？", "answer": "96", "accept": ["96"], "hint": "整数",
         "explanation": "60+36=96分"},
        {"q": "3km = 何m？", "answer": "3000", "accept": ["3000"], "hint": "整数",
         "explanation": "3×1000=3000"},
        {"q": "A=8日, B=12日でできる仕事。2人でやると何日？", "answer": "4.8", "accept": ["4.8","24/5"], "hint": "小数",
         "explanation": "1日量: 1/8+1/12=5/24\n1÷(5/24)=24/5=4.8日"},
        {"q": "池の水900Lを毎分10L排出 → 何分？", "answer": "90", "accept": ["90"], "hint": "整数",
         "explanation": "900÷10=90分"},
    ],
    "文字式・因数分解": [
        {"q": "(a+b)² = a²+?ab+b²", "answer": "2", "accept": ["2"], "hint": "整数",
         "explanation": "(a+b)²=a²+2ab+b²"},
        {"q": "(a+3)(a-3) = a² - ?", "answer": "9", "accept": ["9"], "hint": "整数",
         "explanation": "(a+b)(a-b)=a²-b², b=3→9"},
        {"q": "x²+5x+6 = (x+2)(x+?)", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "積6, 和5 → 2と3"},
        {"q": "4x²-9 = (2x+3)(2x-?)", "answer": "3", "accept": ["3"], "hint": "整数",
         "explanation": "(2x)²-3²=(2x+3)(2x-3)"},
        {"q": "2x(x+1) = 2x²+?x", "answer": "2", "accept": ["2"], "hint": "整数",
         "explanation": "2x×1=2x → 2x²+2x"},
        {"q": "x³-1 = (x-1)(x²+x+?)", "answer": "1", "accept": ["1"], "hint": "整数",
         "explanation": "x³-1=(x-1)(x²+x+1)"},
    ],
}

DIFF_CATS = {
    "かんたん":   ["四則演算","整数・倍数・素数","分数・比・割合","速さ・仕事・単位換算"],
    "ふつう":     ["方程式","数列・規則","三角関数・図形","指数・対数","確率・統計","文字式・因数分解"],
    "むずかしい": ["微分・積分","確率・統計","複素数・行列"],
}
DMG   = {"かんたん": 14, "ふつう": 22, "むずかしい": 35}
E_DMG = {"かんたん":  8, "ふつう": 15, "むずかしい": 26}

ENEMIES = [
    {"name":"スライム","emoji":"🟢","hp":60},
    {"name":"ゴブリン","emoji":"👺","hp":90},
    {"name":"ドラゴン","emoji":"🐉","hp":130},
    {"name":"魔王","emoji":"💀","hp":170},
]
CAT_ICON = {
    "四則演算":"🔢","整数・倍数・素数":"🔬","分数・比・割合":"📊",
    "方程式":"🧮","数列・規則":"📐","三角関数・図形":"📏",
    "指数・対数":"📈","微分・積分":"∫","確率・統計":"🎲",
    "複素数・行列":"🔭","速さ・仕事・単位換算":"⏱","文字式・因数分解":"✏️",
}

def _init():
    d = dict(screen="menu",difficulty="ふつう",
             player_hp=100,enemy_hp=0,enemy_max_hp=0,enemy=None,
             score=0,round=0,max_rounds=10,
             combo=0,max_combo=0,question=None,
             answered=False,last_correct=None,last_damage=0,
             battle_log=[],wrong_review=[],
             enemy_index=0,input_key=0)
    for k,v in d.items():
        if k not in st.session_state:
            st.session_state[k]=v
_init()

def add_log(msg):
    st.session_state.battle_log.insert(0,msg)
    if len(st.session_state.battle_log)>8:
        st.session_state.battle_log.pop()

def pick_question():
    cat=random.choice(DIFF_CATS[st.session_state.difficulty])
    q=random.choice(QUESTION_BANK[cat])
    st.session_state.question={**q,"category":cat}
    st.session_state.answered=False
    st.session_state.last_correct=None
    st.session_state.input_key+=1

def start_battle():
    st.session_state.screen="battle"
    st.session_state.player_hp=100
    e=ENEMIES[st.session_state.enemy_index].copy()
    st.session_state.enemy=e
    st.session_state.enemy_hp=e["hp"]
    st.session_state.enemy_max_hp=e["hp"]
    st.session_state.round=0
    st.session_state.score=0
    st.session_state.combo=0
    st.session_state.max_combo=0
    st.session_state.battle_log=[]
    st.session_state.wrong_review=[]
    pick_question()

def norm(s): return s.strip().replace(" ","").replace("\u3000","").lower()

def submit(user_input):
    if st.session_state.answered or not user_input.strip():
        return
    st.session_state.answered=True
    q=st.session_state.question
    correct=norm(user_input) in [norm(a) for a in q["accept"]]
    st.session_state.last_correct=correct
    diff=st.session_state.difficulty
    if correct:
        st.session_state.combo+=1
        st.session_state.max_combo=max(st.session_state.max_combo,st.session_state.combo)
        dmg=DMG[diff]+min(st.session_state.combo-1,4)*5
        st.session_state.enemy_hp=max(0,st.session_state.enemy_hp-dmg)
        st.session_state.score+=10+(st.session_state.combo-1)*3
        st.session_state.last_damage=dmg
        c=f" \u2728 {st.session_state.combo}\u30b3\u30f3\u30dc\uff01" if st.session_state.combo>=2 else ""
        add_log(f"\u2694\ufe0f \u6b63\u89e3\uff01{dmg}\u30c0\u30e1\u30fc\u30b8{c}")
    else:
        st.session_state.combo=0
        ed=E_DMG[diff]
        st.session_state.player_hp=max(0,st.session_state.player_hp-ed)
        st.session_state.last_damage=ed
        add_log(f"\U0001f4a5 \u4e0d\u6b63\u89e3\u2026 {st.session_state.enemy['name']}\u304b\u3089{ed}\u30c0\u30e1\u30fc\u30b8")
        st.session_state.wrong_review.append({
            "q":q["q"],"cat":q["category"],
            "your":user_input,"correct":q["answer"],
            "explanation":q["explanation"],
            "round":st.session_state.round+1,
        })
    st.session_state.round+=1

# ── メニュー ──────────────────────────────────────────────────
if st.session_state.screen=="menu":
    st.markdown("<h1>⚔️ 数学バトル</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:0.97rem;margin-bottom:1rem;color:#a0a0d8 !important;'>答えを自分で入力して敵を倒せ！間違えた問題は解説で振り返ろう 📚</p>",unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        st.markdown("<p style='font-weight:800;font-size:0.95rem;color:#c0c0ff !important;margin-bottom:2px;'>🗡 難易度</p>",unsafe_allow_html=True)
        DIFFS=["かんたん","ふつう","むずかしい"]
        diff=st.selectbox("難易度",DIFFS,index=DIFFS.index(st.session_state.difficulty),label_visibility="collapsed")
        st.session_state.difficulty=diff
    with c2:
        st.markdown("<p style='font-weight:800;font-size:0.95rem;color:#c0c0ff !important;margin-bottom:2px;'>👾 対戦相手</p>",unsafe_allow_html=True)
        enames=[f"{e['emoji']} {e['name']} (HP {e['hp']})" for e in ENEMIES]
        esel=st.selectbox("敵",enames,index=st.session_state.enemy_index,label_visibility="collapsed")
        st.session_state.enemy_index=enames.index(esel)

    info={"かんたん":("🟢","四則演算・素数・分数・単位換算","ダメージ14 / 被ダメ8"),
          "ふつう":("🟡","方程式・数列・三角・対数・確率・因数","ダメージ22 / 被ダメ15"),
          "むずかしい":("🔴","微積分・確率・複素数・行列","ダメージ35 / 被ダメ26")}[st.session_state.difficulty]
    cats="　".join(f"{CAT_ICON.get(c,'')} {c}" for c in DIFF_CATS[st.session_state.difficulty])
    st.markdown(f"""
    <div class="info-card">
        <div class="ic-ttl">{info[0]} {st.session_state.difficulty} — {info[1]}</div>
        <div class="ic-cats">📚 出題カテゴリ: {cats}</div>
        <div class="ic-note">{info[2]}　｜　全{st.session_state.max_rounds}問</div>
    </div>""",unsafe_allow_html=True)

    all_cats=sorted(QUESTION_BANK.keys())
    cat_html="".join(f'<span style="display:inline-block;background:#0c0c2a;border:1.5px solid #3a3a60;border-radius:8px;padding:3px 10px;margin:3px;font-size:0.78rem;color:#b0b0ff !important;font-weight:700;">{CAT_ICON.get(c,"")} {c}</span>' for c in all_cats)
    st.markdown(f'<div style="margin:0.8rem 0 1rem;"><div style="font-size:0.82rem;font-weight:700;color:#7070b8 !important;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;">全12カテゴリ</div>{cat_html}</div>',unsafe_allow_html=True)

    if st.button("🚀 バトルスタート！",use_container_width=True):
        start_battle(); st.rerun()

    st.markdown("<p style='color:#505070 !important;font-size:0.76rem;text-align:center;margin-top:0.3rem;'>答えを入力してEnterキー or「回答する」で送信 | コンボでボーナスダメージ！</p>",unsafe_allow_html=True)

# ── バトル ────────────────────────────────────────────────────
elif st.session_state.screen=="battle":
    e=st.session_state.enemy
    p_hp=st.session_state.player_hp
    e_hp=st.session_state.enemy_hp
    e_max=st.session_state.enemy_max_hp

    if p_hp<=0 or e_hp<=0 or st.session_state.round>=st.session_state.max_rounds:
        st.session_state.screen="result"; st.rerun()

    pp=max(0,p_hp)
    ep=max(0,round(e_hp/e_max*100,1))
    st.markdown(f"""
    <div class="hp-row">
      <div class="hp-box">
        <div class="hp-name">🧙 勇者</div>
        <div class="hp-bg"><div class="hp-p" style="width:{pp}%"></div></div>
        <div class="hp-num">{p_hp} / 100 HP</div>
      </div>
      <div style="font-size:1.3rem;color:#7060e0 !important;font-weight:900;padding:0 4px;">VS</div>
      <div class="hp-box">
        <div class="hp-name">{e['emoji']} {e['name']}</div>
        <div class="hp-bg"><div class="hp-e" style="width:{ep}%"></div></div>
        <div class="hp-num">{e_hp} / {e_max} HP</div>
      </div>
    </div>""",unsafe_allow_html=True)

    q=st.session_state.question
    combo_b=f'<span class="badge b-cmb">🔥 {st.session_state.combo}コンボ</span>' if st.session_state.combo>=2 else ""
    ci=CAT_ICON.get(q["category"],"📝")
    st.markdown(f'<div style="margin-bottom:0.4rem;"><span class="badge b-rnd">第 {st.session_state.round+1} / {st.session_state.max_rounds} 問</span><span class="badge b-scr">⭐ {st.session_state.score} pt</span><span class="badge b-cat">{ci} {q["category"]}</span>{combo_b}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="q-card"><div class="q-cat">{ci} {q["category"]}</div><div class="q-text">{q["q"]}</div><div class="q-hint">💬 入力形式：{q["hint"]}</div></div>',unsafe_allow_html=True)

    if not st.session_state.answered:
        user_in=st.text_input("✏️ 答えを入力してEnter",key=f"ans_{st.session_state.input_key}",placeholder=q["hint"])
        ca,cb=st.columns([3,1])
        with ca:
            if st.button("⚔️ 回答する！",use_container_width=True):
                if user_in.strip(): submit(user_in); st.rerun()
        with cb:
            if st.button("🏳️ 降参",use_container_width=True):
                st.session_state.screen="menu"; st.rerun()
    else:
        ok=st.session_state.last_correct
        if ok:
            st.markdown(f'<div class="exp-ok"><div class="exp-ttl">✅ 正解！ {st.session_state.last_damage}ダメージを与えた！</div><div class="exp-body">{q["explanation"]}</div></div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="exp-ng"><div class="exp-ttl">❌ 不正解… 正解は「{q["answer"]}」</div><div class="exp-body">{q["explanation"]}</div></div>',unsafe_allow_html=True)
        ca,cb=st.columns([3,1])
        with ca:
            end=st.session_state.round>=st.session_state.max_rounds or p_hp<=0 or e_hp<=0
            lbl="🏁 結果を見る" if end else "▶️ 次の問題へ"
            if st.button(lbl,use_container_width=True):
                if st.session_state.player_hp<=0 or st.session_state.enemy_hp<=0 or st.session_state.round>=st.session_state.max_rounds:
                    st.session_state.screen="result"
                else:
                    pick_question()
                st.rerun()
        with cb:
            if st.button("🏳️ 降参",use_container_width=True):
                st.session_state.screen="menu"; st.rerun()

    if st.session_state.battle_log:
        st.markdown("---")
        st.markdown(f'<div class="log-box">{"<br>".join(st.session_state.battle_log)}</div>',unsafe_allow_html=True)

# ── リザルト ──────────────────────────────────────────────────
elif st.session_state.screen=="result":
    p_hp=st.session_state.player_hp
    e_hp=st.session_state.enemy_hp
    en=st.session_state.enemy

    if p_hp<=0:   cls,title,sub="res-lose","💀 GAME OVER",f"{en['emoji']} {en['name']} に倒された…"
    elif e_hp<=0: cls,title,sub="res-win","🏆 VICTORY！",f"{en['emoji']} {en['name']} を撃破！"
    else:
        cls="res-win" if st.session_state.score>=60 else "res-lose"
        title,sub="⚔️ バトル終了",f"全{st.session_state.max_rounds}問終了"

    correct_count=st.session_state.round-len(st.session_state.wrong_review)
    st.markdown(f"""
    <div class="res-box">
        <div class="{cls}">{title}</div>
        <div style="font-size:0.96rem;margin:7px 0 14px;color:#b0b0d8 !important;">{sub}</div>
        <div>
            <div class="stat-box"><div class="stat-lbl">スコア</div><div class="stat-val">⭐ {st.session_state.score}</div></div>
            <div class="stat-box"><div class="stat-lbl">最大コンボ</div><div class="stat-val">🔥 {st.session_state.max_combo}</div></div>
            <div class="stat-box"><div class="stat-lbl">残りHP</div><div class="stat-val">❤️ {max(0,p_hp)}</div></div>
            <div class="stat-box"><div class="stat-lbl">正解数</div><div class="stat-val">✅ {correct_count}/{st.session_state.round}</div></div>
        </div>
    </div>""",unsafe_allow_html=True)

    wrongs=st.session_state.wrong_review
    st.markdown("")
    if wrongs:
        st.markdown(f'<div style="background:#100418;border:2px solid #dc2626;border-radius:14px;padding:13px 18px;margin-bottom:0.7rem;"><div style="font-size:1.04rem;font-weight:900;color:#f87171 !important;">📚 間違えた問題の復習 ({len(wrongs)}問)</div><div style="font-size:0.83rem;color:#906890 !important;">解説を読んでしっかりマスターしよう！</div></div>',unsafe_allow_html=True)
        for i,w in enumerate(wrongs):
            ic=CAT_ICON.get(w["cat"],"📝")
            with st.expander(f"{ic} 第{w['round']}問 [{w['cat']}]　{w['q']}",expanded=(i==0)):
                st.markdown(f"""
                <div style="margin-bottom:10px;line-height:2.2;">
                    <span style="background:#280808;color:#fca5a5 !important;border-radius:6px;padding:4px 11px;font-size:0.87rem;font-weight:700;">あなた: {w['your']}</span>
                    &nbsp;→&nbsp;
                    <span style="background:#031408;color:#6ee7b7 !important;border-radius:6px;padding:4px 11px;font-size:0.87rem;font-weight:700;">正解: {w['correct']}</span>
                </div>
                <div style="background:#05050f;border-left:3px solid #6366f1;border-radius:0 8px 8px 0;padding:13px 17px;color:#e0e0ff !important;font-size:0.93rem;line-height:1.9;white-space:pre-wrap;font-weight:500;">{w['explanation']}</div>
                """,unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#021408;border:2px solid #16a34a;border-radius:14px;padding:13px 18px;text-align:center;"><span style="color:#4ade80 !important;font-size:1.04rem;font-weight:800;">🎉 全問正解！完璧なバトルでした！</span></div>',unsafe_allow_html=True)

    st.markdown("")
    c1,c2=st.columns(2)
    with c1:
        if st.button("🔄 もう一度バトル！",use_container_width=True):
            start_battle(); st.rerun()
    with c2:
        if st.button("🏠 メニューへ戻る",use_container_width=True):
            st.session_state.screen="menu"; st.rerun()