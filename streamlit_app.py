import streamlit as st
import random
import json

st.set_page_config(page_title="Number Blast", page_icon="🔢", layout="centered")

# ============================================================
# 定数
# ============================================================
GRID_SIZE = 8
COLORS = {
    1: "#FF6B6B", 2: "#FF8E53", 3: "#FFC300",
    4: "#6BCB77", 5: "#4D96FF", 6: "#C77DFF",
    7: "#FF6EC7", 8: "#00C9A7", 9: "#F9844A",
}

# ============================================================
# ブロックピース定義（形状リスト）
# ============================================================
PIECES = [
    [[1]],                              # 1×1
    [[1, 1]],                           # 1×2 横
    [[1], [1]],                         # 2×1 縦
    [[1, 1, 1]],                        # 1×3 横
    [[1], [1], [1]],                    # 3×1 縦
    [[1, 1], [1, 1]],                   # 2×2
    [[1, 1, 0], [0, 1, 1]],            # S字
    [[0, 1, 1], [1, 1, 0]],            # Z字
    [[1, 0], [1, 1]],                  # L字小
    [[1, 1], [1, 0]],                  # J字小
]

# ============================================================
# セッション初期化
# ============================================================
def init_state():
    if "grid" not in st.session_state:
        st.session_state.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "pieces" not in st.session_state:
        st.session_state.pieces = generate_pieces()
    if "selected_piece" not in st.session_state:
        st.session_state.selected_piece = 0
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "cleared_lines" not in st.session_state:
        st.session_state.cleared_lines = []

def generate_pieces():
    pieces = []
    for _ in range(3):
        shape = random.choice(PIECES)
        number = random.randint(1, 9)
        pieces.append({"shape": shape, "number": number})
    return pieces

# ============================================================
# ゲームロジック
# ============================================================
def can_place(grid, shape, row, col):
    for r, rowdata in enumerate(shape):
        for c, cell in enumerate(rowdata):
            if cell:
                nr, nc = row + r, col + c
                if nr < 0 or nr >= GRID_SIZE or nc < 0 or nc >= GRID_SIZE:
                    return False
                if grid[nr][nc] != 0:
                    return False
    return True

def place_piece(grid, shape, number, row, col):
    new_grid = [row_[:] for row_ in grid]
    for r, rowdata in enumerate(shape):
        for c, cell in enumerate(rowdata):
            if cell:
                new_grid[row + r][col + c] = number
    return new_grid

def check_and_clear(grid):
    """縦か横で合計10になるセルを消す"""
    to_clear = set()

    # 横チェック
    for r in range(GRID_SIZE):
        vals = [grid[r][c] for c in range(GRID_SIZE) if grid[r][c] != 0]
        # 連続する部分列で合計10を探す
        row_cells = [(r, c) for c in range(GRID_SIZE) if grid[r][c] != 0]
        for start in range(len(row_cells)):
            total = 0
            group = []
            for idx in range(start, len(row_cells)):
                _, c0 = row_cells[idx]
                # 連続しているか（列が隣接）
                if group and c0 != group[-1][1] + 1:
                    break
                total += grid[row_cells[idx][0]][c0]
                group.append(row_cells[idx])
                if total == 10:
                    for cell in group:
                        to_clear.add(cell)
                elif total > 10:
                    break

    # 縦チェック
    for c in range(GRID_SIZE):
        col_cells = [(r, c) for r in range(GRID_SIZE) if grid[r][c] != 0]
        for start in range(len(col_cells)):
            total = 0
            group = []
            for idx in range(start, len(col_cells)):
                r0, _ = col_cells[idx]
                if group and r0 != group[-1][0] + 1:
                    break
                total += grid[r0][col_cells[idx][1]]
                group.append(col_cells[idx])
                if total == 10:
                    for cell in group:
                        to_clear.add(cell)
                elif total > 10:
                    break

    return to_clear

def apply_clear(grid, to_clear):
    new_grid = [row[:] for row in grid]
    for r, c in to_clear:
        new_grid[r][c] = 0
    return new_grid

def check_game_over(grid, pieces):
    for pi, p in enumerate(pieces):
        if p is None:
            continue
        shape = p["shape"]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if can_place(grid, shape, r, c):
                    return False
    return True

# ============================================================
# CSS
# ============================================================
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+JP:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
        background-color: #0d0d1a;
        color: #e0e0ff;
    }
    .main { background: #0d0d1a; }

    h1.title {
        font-family: 'Orbitron', monospace;
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: 0.15em;
        background: linear-gradient(90deg, #FF6B6B, #FFC300, #6BCB77, #4D96FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0;
    }

    .score-area {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 0.5rem 0 1rem 0;
    }

    .score-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        text-align: center;
        min-width: 100px;
    }

    .score-label { font-size: 0.7rem; color: #8888aa; letter-spacing:0.1em; text-transform: uppercase; }
    .score-value { font-family: 'Orbitron', monospace; font-size: 2rem; font-weight: 900; color: #FFC300; }

    .rule-hint {
        text-align: center;
        color: #8888aa;
        font-size: 0.82rem;
        margin-bottom: 0.8rem;
    }

    .grid-table {
        border-collapse: separate;
        border-spacing: 3px;
        margin: 0 auto;
    }

    .grid-cell {
        width: 52px;
        height: 52px;
        border-radius: 8px;
        text-align: center;
        vertical-align: middle;
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        font-weight: 900;
        cursor: pointer;
        transition: transform 0.1s, filter 0.1s;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .grid-cell.empty {
        background: rgba(255,255,255,0.04);
        color: transparent;
    }

    .grid-cell.filled {
        box-shadow: 0 0 8px rgba(255,255,255,0.15) inset, 0 2px 6px rgba(0,0,0,0.4);
        color: rgba(255,255,255,0.9);
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    .grid-cell.cleared {
        animation: pop 0.4s ease forwards;
    }

    @keyframes pop {
        0%   { transform: scale(1.3); filter: brightness(2); }
        100% { transform: scale(0); opacity: 0; }
    }

    .pieces-area {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.2rem 0;
        flex-wrap: wrap;
    }

    .piece-card {
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        cursor: pointer;
        transition: border-color 0.2s, background 0.2s;
        min-width: 90px;
        text-align: center;
    }

    .piece-card.selected {
        border-color: #FFC300;
        background: rgba(255,195,0,0.10);
        box-shadow: 0 0 16px rgba(255,195,0,0.25);
    }

    .piece-label {
        font-size: 0.7rem;
        color: #8888aa;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .piece-mini-table {
        border-collapse: separate;
        border-spacing: 2px;
        margin: 0 auto;
    }

    .piece-mini-cell {
        width: 22px;
        height: 22px;
        border-radius: 4px;
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        font-weight: 900;
        text-align: center;
        vertical-align: middle;
        color: rgba(255,255,255,0.9);
    }

    .piece-mini-empty {
        width: 22px;
        height: 22px;
        border-radius: 4px;
        background: transparent;
    }

    .place-btn { margin-top: 0.4rem; }

    .msg-box {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #6BCB77;
        min-height: 1.8rem;
        margin: 0.3rem 0;
    }

    .msg-box.error { color: #FF6B6B; }

    .gameover-overlay {
        background: rgba(13,13,26,0.95);
        border: 2px solid #FF6B6B;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem auto;
        max-width: 400px;
    }

    .gameover-title {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        color: #FF6B6B;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }

    .stButton > button {
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        background: rgba(255,255,255,0.06) !important;
        color: #e0e0ff !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: rgba(255,195,0,0.15) !important;
        border-color: #FFC300 !important;
        color: #FFC300 !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ============================================================
# グリッドをHTMLで描画
# ============================================================
def render_grid(grid):
    html = "<table class='grid-table'>"
    for r in range(GRID_SIZE):
        html += "<tr>"
        for c in range(GRID_SIZE):
            val = grid[r][c]
            if val == 0:
                html += f"<td class='grid-cell empty' data-r='{r}' data-c='{c}'>&nbsp;</td>"
            else:
                color = COLORS.get(val, "#aaaaaa")
                html += (
                    f"<td class='grid-cell filled' "
                    f"style='background:{color};' "
                    f"data-r='{r}' data-c='{c}'>{val}</td>"
                )
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# ピースをHTMLで描画
# ============================================================
def render_piece_card(piece, index, selected):
    shape = piece["shape"]
    num = piece["number"]
    color = COLORS.get(num, "#aaaaaa")
    sel_class = "selected" if selected == index else ""
    label = f"ピース {index + 1}"

    rows_html = ""
    for row in shape:
        rows_html += "<tr>"
        for cell in row:
            if cell:
                rows_html += f"<td class='piece-mini-cell' style='background:{color};'>{num}</td>"
            else:
                rows_html += "<td class='piece-mini-empty'></td>"
        rows_html += "</tr>"

    html = f"""
    <div class='piece-card {sel_class}' id='piece-{index}'>
        <div class='piece-label'>{label}</div>
        <table class='piece-mini-table'>{rows_html}</table>
    </div>
    """
    return html

# ============================================================
# メイン
# ============================================================
init_state()
inject_css()

st.markdown("<h1 class='title'>NUMBER BLAST</h1>", unsafe_allow_html=True)

# スコア
total_games = st.session_state.score
st.markdown(f"""
<div class='score-area'>
    <div class='score-box'>
        <div class='score-label'>スコア</div>
        <div class='score-value'>{st.session_state.score}</div>
    </div>
</div>
<p class='rule-hint'>縦か横に並んだ数字の合計が <b>10</b> になったら消える！</p>
""", unsafe_allow_html=True)

# ゲームオーバー
if st.session_state.game_over:
    st.markdown(f"""
    <div class='gameover-overlay'>
        <div class='gameover-title'>GAME OVER</div>
        <p style='font-size:1.3rem; color:#FFC300;'>スコア: {st.session_state.score}</p>
        <p style='color:#8888aa;'>置けるピースがなくなりました</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 もう一度プレイ", use_container_width=True):
        for key in ["grid", "score", "pieces", "selected_piece", "message", "game_over", "cleared_lines"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.stop()

# グリッド描画
render_grid(st.session_state.grid)

# メッセージ
msg_class = "error" if "置けません" in st.session_state.message else ""
st.markdown(f"<div class='msg-box {msg_class}'>{st.session_state.message or '&nbsp;'}</div>", unsafe_allow_html=True)

# ピース選択エリア
st.markdown("<div style='text-align:center;color:#8888aa;font-size:0.85rem;margin-bottom:0.3rem;'>▼ ピースを選んで置く場所を指定</div>", unsafe_allow_html=True)

pieces_html = "<div class='pieces-area'>"
for i, p in enumerate(st.session_state.pieces):
    if p is not None:
        pieces_html += render_piece_card(p, i, st.session_state.selected_piece)
    else:
        pieces_html += f"<div class='piece-card' style='opacity:0.2;min-width:90px;'><div class='piece-label'>使用済</div></div>"
pieces_html += "</div>"
st.markdown(pieces_html, unsafe_allow_html=True)

# ピース選択ボタン
col1, col2, col3 = st.columns(3)
for i, (col, label) in enumerate(zip([col1, col2, col3], ["ピース1", "ピース2", "ピース3"])):
    with col:
        if st.session_state.pieces[i] is not None:
            btn_style = "🟡 " if st.session_state.selected_piece == i else ""
            if st.button(f"{btn_style}{label}を選択", key=f"sel_{i}", use_container_width=True):
                st.session_state.selected_piece = i
                st.session_state.message = f"ピース{i+1}を選択中。行・列を指定して置こう！"
                st.rerun()

st.markdown("---")

# 置く場所の指定
st.markdown("#### 📍 置く場所を指定")

pc1, pc2, pc3 = st.columns([2, 2, 1])
with pc1:
    row_input = st.number_input("行 (1〜8)", min_value=1, max_value=GRID_SIZE, value=1, step=1) - 1
with pc2:
    col_input = st.number_input("列 (1〜8)", min_value=1, max_value=GRID_SIZE, value=1, step=1) - 1
with pc3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    place_btn = st.button("✅ 置く", use_container_width=True)

if place_btn:
    sel = st.session_state.selected_piece
    piece = st.session_state.pieces[sel]
    if piece is None:
        st.session_state.message = "⚠️ そのピースはもう使用済みです！"
    else:
        shape = piece["shape"]
        number = piece["number"]
        grid = st.session_state.grid
        if can_place(grid, shape, row_input, col_input):
            # 配置
            new_grid = place_piece(grid, shape, number, row_input, col_input)
            # 消去チェック
            to_clear = check_and_clear(new_grid)
            cleared_count = len(to_clear)
            new_grid = apply_clear(new_grid, to_clear)
            st.session_state.grid = new_grid
            st.session_state.score += cleared_count * 10
            st.session_state.pieces[sel] = None

            if cleared_count > 0:
                st.session_state.message = f"🎉 {cleared_count}マス消去！ +{cleared_count * 10}点"
            else:
                st.session_state.message = f"✔️ ピース{sel+1}を ({row_input+1}, {col_input+1}) に配置！"

            # 全ピース使い切ったら補充
            if all(p is None for p in st.session_state.pieces):
                st.session_state.pieces = generate_pieces()
                st.session_state.message += " 　新しいピースが来た！"

            # 次の選択
            for i, p in enumerate(st.session_state.pieces):
                if p is not None:
                    st.session_state.selected_piece = i
                    break

            # ゲームオーバー判定
            if check_game_over(st.session_state.grid, st.session_state.pieces):
                st.session_state.game_over = True

            st.rerun()
        else:
            st.session_state.message = f"❌ そこには置けません！はみ出るか重なっています。"
            st.rerun()

# リセット
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 ゲームリセット", use_container_width=False):
    for key in ["grid", "score", "pieces", "selected_piece", "message", "game_over", "cleared_lines"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# 操作ガイド
with st.expander("📖 遊び方"):
    st.markdown("""
    1. **ピースを選ぶ** → 下のボタンで選択（黄色ハイライト）
    2. **行・列を指定** → グリッドの上から何行目、左から何列目かを入力（1〜8）
    3. **「✅ 置く」ボタン** → ピースを配置！
    4. **縦または横に連続するマスの数字の合計が10**になると消えてポイントゲット！
    5. 3枚全部使うと新しいピースが3枚補充される
    6. どのピースも置けなくなったらゲームオーバー
    
    **ポイント**: 消去1マスにつき10点。連鎖を狙って高得点を目指そう！
    """)