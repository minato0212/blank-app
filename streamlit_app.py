import streamlit as st
import random
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Number Blast 15", page_icon="🔢", layout="centered")

# ============================================================
# 定数
# ============================================================
GRID_SIZE = 8
TARGET = 15
NUM_RANGE = list(range(1, 10))  # 1〜9

COLORS = {
    1: "#ef4444", 2: "#f97316", 3: "#eab308",
    4: "#22c55e", 5: "#06b6d4", 6: "#3b82f6",
    7: "#8b5cf6", 8: "#ec4899", 9: "#14b8a6",
}

# ============================================================
# セッション初期化
# ============================================================
def init():
    if "grid"        not in st.session_state: st.session_state.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    if "score"       not in st.session_state: st.session_state.score = 0
    if "sel_num"     not in st.session_state: st.session_state.sel_num = 1
    if "msg"         not in st.session_state: st.session_state.msg = "数字を選んでグリッドをクリック！"
    if "msg_type"    not in st.session_state: st.session_state.msg_type = "info"
    if "last_cleared" not in st.session_state: st.session_state.last_cleared = []
    if "game_over"   not in st.session_state: st.session_state.game_over = False
    if "moves"       not in st.session_state: st.session_state.moves = 0

# ============================================================
# ゲームロジック
# ============================================================
def find_clears(grid):
    """縦横で連続合計=TARGETのセルを返す"""
    to_clear = set()
    # 横
    for r in range(GRID_SIZE):
        cells = [(r, c) for c in range(GRID_SIZE) if grid[r][c] != 0]
        for s in range(len(cells)):
            total, group = 0, []
            for i in range(s, len(cells)):
                rr, cc = cells[i]
                if group and cc != group[-1][1] + 1:
                    break
                total += grid[rr][cc]
                group.append((rr, cc))
                if total == TARGET:
                    to_clear.update(group)
                elif total > TARGET:
                    break
    # 縦
    for c in range(GRID_SIZE):
        cells = [(r, c) for r in range(GRID_SIZE) if grid[r][c] != 0]
        for s in range(len(cells)):
            total, group = 0, []
            for i in range(s, len(cells)):
                rr, cc = cells[i]
                if group and rr != group[-1][0] + 1:
                    break
                total += grid[rr][cc]
                group.append((rr, cc))
                if total == TARGET:
                    to_clear.update(group)
                elif total > TARGET:
                    break
    return to_clear

def place_and_clear(r, c, num):
    grid = [row[:] for row in st.session_state.grid]
    if grid[r][c] != 0:
        st.session_state.msg = "❌ すでに埋まっています！"
        st.session_state.msg_type = "err"
        return
    grid[r][c] = num
    to_clear = find_clears(grid)
    cleared = len(to_clear)
    for cr, cc in to_clear:
        grid[cr][cc] = 0
    st.session_state.grid = grid
    st.session_state.moves += 1
    st.session_state.last_cleared = list(to_clear)
    if cleared > 0:
        pts = cleared * TARGET
        st.session_state.score += pts
        st.session_state.msg = f"🎉 {cleared}マス消去！ +{pts}点"
        st.session_state.msg_type = "good"
    else:
        st.session_state.msg = f"✔️ [{r+1},{c+1}] に {num} を配置"
        st.session_state.msg_type = "info"

# ============================================================
# URLパラメータ受信
# ============================================================
init()
params = st.query_params
if "r" in params and "c" in params and "n" in params:
    try:
        pr = int(params["r"])
        pc = int(params["c"])
        pn = int(params["n"])
        if 0 <= pr < GRID_SIZE and 0 <= pc < GRID_SIZE and pn in NUM_RANGE:
            place_and_clear(pr, pc, pn)
    except Exception:
        pass
    st.query_params.clear()
    st.rerun()

if "selnum" in params:
    try:
        sn = int(params["selnum"])
        if sn in NUM_RANGE:
            st.session_state.sel_num = sn
            st.session_state.msg = f"数字 {sn} を選択中 — グリッドをクリック！"
            st.session_state.msg_type = "info"
    except Exception:
        pass
    st.query_params.clear()
    st.rerun()

# ============================================================
# CSS (Streamlit側)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=M+PLUS+Rounded+1c:wght@700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'M PLUS Rounded 1c', sans-serif;
    background: #0a0f1e;
    color: #e2e8f0;
}
.block-container { padding-top: 0.8rem !important; }
.stButton > button {
    font-family: 'M PLUS Rounded 1c', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    background: #1e293b !important;
    color: #94a3b8 !important;
    border: 1px solid #334155 !important;
    font-size: 0.8rem !important;
}
.stButton > button:hover {
    border-color: #f59e0b !important;
    color: #f59e0b !important;
    background: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# インタラクティブHTML
# ============================================================
grid = st.session_state.grid
sel  = st.session_state.sel_num
score = st.session_state.score
msg  = st.session_state.msg
msg_type = st.session_state.msg_type
moves = st.session_state.moves

# グリッドJSON
grid_js = str(grid).replace("True","true").replace("False","false").replace("'",'"')

# 色マップJS
colors_js = "{" + ",".join(f"{k}:'{v}'" for k,v in COLORS.items()) + "}"

msg_color = {"good": "#4ade80", "err": "#f87171", "info": "#94a3b8"}[msg_type]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=M+PLUS+Rounded+1c:wght@700;900&display=swap');
*{{ box-sizing:border-box; margin:0; padding:0; }}
body {{
  background: transparent;
  font-family: 'M PLUS Rounded 1c', sans-serif;
  color: #e2e8f0;
  padding: 6px 4px 10px;
}}

/* ---- タイトル ---- */
.title {{
  font-family: 'Orbitron', monospace;
  font-size: 1.9rem;
  font-weight: 900;
  text-align: center;
  letter-spacing: 0.12em;
  background: linear-gradient(90deg,#f97316,#eab308,#22c55e,#06b6d4,#8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
}}
.subtitle {{
  text-align: center;
  font-size: 0.75rem;
  color: #475569;
  margin-bottom: 10px;
  letter-spacing: 0.05em;
}}

/* ---- スコア ---- */
.hud {{
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}}
.hud-pill {{
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 40px;
  padding: 6px 22px;
  text-align: center;
}}
.hud-pill .lbl {{ font-size:0.6rem; color:#475569; letter-spacing:0.08em; text-transform:uppercase; }}
.hud-pill .val {{ font-family:'Orbitron',monospace; font-size:1.4rem; font-weight:900; color:#f59e0b; }}
.hud-pill .val.mv {{ color:#38bdf8; }}

/* ---- メッセージ ---- */
.msg {{
  text-align: center;
  font-size: 0.85rem;
  font-weight: 700;
  min-height: 1.3rem;
  margin-bottom: 10px;
  color: {msg_color};
  letter-spacing: 0.02em;
}}

/* ---- 数字パレット ---- */
.palette-wrap {{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}}
.palette-label {{
  font-size: 0.68rem;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-right: 4px;
}}
.num-btn {{
  width: 48px;
  height: 48px;
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
  font-family: 'Orbitron', monospace;
  font-size: 1.1rem;
  font-weight: 900;
  color: rgba(255,255,255,0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.12s, box-shadow 0.12s, border-color 0.12s;
  text-shadow: 0 1px 3px rgba(0,0,0,0.5);
}}
.num-btn:hover {{
  transform: translateY(-3px) scale(1.08);
  box-shadow: 0 6px 18px rgba(0,0,0,0.45);
}}
.num-btn.selected {{
  border-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.35), 0 6px 20px rgba(0,0,0,0.5);
  transform: scale(1.12);
}}

/* ---- グリッド ---- */
.grid-outer {{
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat({GRID_SIZE}, 50px);
  grid-template-rows: repeat({GRID_SIZE}, 50px);
  gap: 3px;
  background: #0f172a;
  padding: 6px;
  border-radius: 14px;
  border: 1px solid #1e293b;
}}
.cell {{
  width: 50px; height: 50px;
  border-radius: 8px;
  background: #0c1524;
  border: 1px solid #1e293b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', monospace;
  font-size: 1.05rem;
  font-weight: 900;
  color: rgba(255,255,255,0.88);
  text-shadow: 0 1px 3px rgba(0,0,0,0.5);
  transition: transform 0.1s, filter 0.1s;
  position: relative;
  user-select: none;
}}
.cell.empty {{
  color: transparent;
}}
.cell.empty:hover {{
  background: rgba(255,255,255,0.07);
  border-color: rgba(255,255,255,0.2);
  transform: scale(1.06);
}}
.cell.filled:hover {{
  filter: brightness(1.25);
  transform: scale(1.04);
}}
.cell.preview-ok {{
  border-color: rgba(255,255,255,0.6) !important;
  filter: brightness(1.3);
  transform: scale(1.07);
}}
.cell.preview-ng {{
  border-color: #ef4444 !important;
}}
@keyframes clearPop {{
  0%   {{ transform: scale(1.4); filter: brightness(2.5); opacity:1; }}
  60%  {{ transform: scale(0.7); filter: brightness(1.5); }}
  100% {{ transform: scale(0); opacity: 0; }}
}}
.cell.popping {{
  animation: clearPop 0.42s ease forwards;
  pointer-events: none;
}}

/* ---- 行・列の合計ヒント ---- */
.sum-row {{
  display: grid;
  grid-template-columns: repeat({GRID_SIZE}, 50px);
  gap: 3px;
  padding: 0 6px;
  margin-bottom: 4px;
}}
.sum-col-wrap {{
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 6px 0;
}}
.sum-cell {{
  width: 50px; height: 20px;
  border-radius: 4px;
  display: flex; align-items:center; justify-content:center;
  font-size: 0.62rem;
  font-family: 'Orbitron', monospace;
  font-weight: 700;
  color: #334155;
  background: transparent;
}}
.sum-cell.hot {{ color: #f59e0b; }}
.sum-cell.over {{ color: #ef4444; }}

.row-sums {{
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 6px 0;
  margin-left: 4px;
}}
.row-sum-cell {{
  height: 50px;
  display: flex; align-items:center; justify-content:center;
  font-size: 0.62rem;
  font-family: 'Orbitron', monospace;
  font-weight: 700;
  color: #334155;
  min-width: 22px;
}}
.row-sum-cell.hot  {{ color: #f59e0b; }}
.row-sum-cell.over {{ color: #ef4444; }}

.grid-with-sums {{
  display: flex;
  justify-content: center;
  align-items: flex-start;
}}
.grid-block {{
  display: flex;
  flex-direction: column;
}}
</style>
</head>
<body>

<div class="title">NUMBER BLAST</div>
<div class="subtitle">縦か横に連続した合計が <b style="color:#f59e0b">{TARGET}</b> になったら消える！</div>

<div class="hud">
  <div class="hud-pill">
    <div class="lbl">スコア</div>
    <div class="val" id="score-val">{score}</div>
  </div>
  <div class="hud-pill">
    <div class="lbl">手数</div>
    <div class="val mv" id="moves-val">{moves}</div>
  </div>
</div>

<div class="msg" id="msg">{msg}</div>

<!-- 数字パレット -->
<div class="palette-wrap">
  <span class="palette-label">数字を選ぶ▶</span>
"""

for n in NUM_RANGE:
    sel_cls = " selected" if n == sel else ""
    html_code += f'  <div class="num-btn{sel_cls}" id="nbtn-{n}" style="background:{COLORS[n]};" onclick="selectNum({n})">{n}</div>\n'

html_code += f"""
</div>

<!-- グリッド + 合計 -->
<div class="grid-with-sums">
  <div class="grid-block">
    <!-- 列合計(上) -->
    <div class="sum-row" id="col-sums"></div>
    <!-- グリッド本体 -->
    <div class="grid-outer">
      <div class="grid" id="grid"></div>
    </div>
  </div>
  <!-- 行合計(右) -->
  <div class="row-sums" id="row-sums" style="margin-top:20px;"></div>
</div>

<script>
const GRID_SIZE = {GRID_SIZE};
const TARGET    = {TARGET};
const COLORS    = {colors_js};
let   grid      = {grid_js};
let   selNum    = {sel};

// ============ 合計ヒント計算 ============
function rowMaxConsec(r) {{
  let cells = [];
  for (let c=0; c<GRID_SIZE; c++) if (grid[r][c]!==0) cells.push([r,c]);
  let maxSum = 0;
  for (let s=0; s<cells.length; s++) {{
    let total=0;
    for (let i=s; i<cells.length; i++) {{
      let [rr,cc]=cells[i];
      if (i>s && cc !== cells[i-1][1]+1) break;
      total += grid[rr][cc];
      if (total > maxSum) maxSum = total;
      if (total >= TARGET) break;
    }}
  }}
  // 行全体の合計も
  let rowTotal = 0;
  for (let c=0; c<GRID_SIZE; c++) rowTotal += grid[r][c];
  return rowTotal;
}}
function colTotal(c) {{
  let t=0;
  for (let r=0; r<GRID_SIZE; r++) t+=grid[r][c];
  return t;
}}

// ============ レンダリング ============
function render() {{
  renderGrid();
  renderSums();
}}

function renderGrid() {{
  const container = document.getElementById('grid');
  container.innerHTML = '';
  for (let r=0; r<GRID_SIZE; r++) {{
    for (let c=0; c<GRID_SIZE; c++) {{
      let div = document.createElement('div');
      div.className = 'cell';
      div.dataset.r = r; div.dataset.c = c;
      let val = grid[r][c];
      if (val !== 0) {{
        div.classList.add('filled');
        div.style.background = COLORS[val];
        div.style.boxShadow  = `0 0 10px ${{COLORS[val]}}55 inset, 0 2px 8px rgba(0,0,0,0.5)`;
        div.textContent = val;
      }} else {{
        div.classList.add('empty');
      }}
      div.addEventListener('mouseenter', onEnter);
      div.addEventListener('mouseleave', onLeave);
      div.addEventListener('click', onClickCell);
      container.appendChild(div);
    }}
  }}
}}

function renderSums() {{
  // 列合計
  const colWrap = document.getElementById('col-sums');
  colWrap.innerHTML = '';
  for (let c=0; c<GRID_SIZE; c++) {{
    let t = colTotal(c);
    let div = document.createElement('div');
    div.className = 'sum-cell' + (t===TARGET?' hot':(t>TARGET?' over':''));
    div.textContent = t > 0 ? t : '';
    colWrap.appendChild(div);
  }}
  // 行合計
  const rowWrap = document.getElementById('row-sums');
  rowWrap.innerHTML = '';
  for (let r=0; r<GRID_SIZE; r++) {{
    let t = rowMaxConsec(r);
    let div = document.createElement('div');
    div.className = 'row-sum-cell' + (t===TARGET?' hot':(t>TARGET?' over':''));
    div.textContent = t > 0 ? t : '';
    rowWrap.appendChild(div);
  }}
}}

// ============ ホバープレビュー ============
function onEnter(e) {{
  let r = +e.currentTarget.dataset.r;
  let c = +e.currentTarget.dataset.c;
  let cell = e.currentTarget;
  if (grid[r][c] !== 0) {{ cell.classList.add('preview-ng'); return; }}
  cell.classList.add('preview-ok');
  // プレビュー数字表示
  cell.style.background = COLORS[selNum] + '88';
  cell.style.color = 'rgba(255,255,255,0.75)';
  cell.textContent = selNum;
}}
function onLeave(e) {{
  let r = +e.currentTarget.dataset.r;
  let c = +e.currentTarget.dataset.c;
  let cell = e.currentTarget;
  cell.classList.remove('preview-ok','preview-ng');
  // 元に戻す
  let val = grid[r][c];
  if (val !== 0) {{
    cell.style.background = COLORS[val];
    cell.style.color = 'rgba(255,255,255,0.88)';
    cell.textContent = val;
  }} else {{
    cell.style.background = '';
    cell.style.color = 'transparent';
    cell.textContent = '';
  }}
}}

// ============ クリックで配置 ============
function onClickCell(e) {{
  let r = +e.currentTarget.dataset.r;
  let c = +e.currentTarget.dataset.c;
  // Streamlitにパラメータ送信してページ更新
  const url = new URL(window.parent.location.href);
  url.searchParams.set('r', r);
  url.searchParams.set('c', c);
  url.searchParams.set('n', selNum);
  window.parent.location.href = url.toString();
}}

// ============ 数字選択 ============
function selectNum(n) {{
  selNum = n;
  document.querySelectorAll('.num-btn').forEach(btn => btn.classList.remove('selected'));
  document.getElementById('nbtn-' + n).classList.add('selected');
  document.getElementById('msg').textContent = '数字 ' + n + ' を選択中 — グリッドをクリック！';
  document.getElementById('msg').style.color = '#94a3b8';
  // Streamlitに選択を通知
  const url = new URL(window.parent.location.href);
  url.searchParams.set('selnum', n);
  window.parent.location.href = url.toString();
}}

// ============ 初期描画 ============
render();
</script>
</body>
</html>
"""

# Streamlitタイトル非表示（HTML内で表示）
st_html(html_code, height=680, scrolling=False)

# リセットボタン
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 リセット", use_container_width=True):
        for k in ["grid","score","sel_num","msg","msg_type","last_cleared","game_over","moves"]:
            st.session_state.pop(k, None)
        st.rerun()

with st.expander("📖 遊び方"):
    st.markdown(f"""
    1. **カラーボタンで数字を選ぶ**（1〜9）
    2. **グリッドにカーソルを乗せる** → 置く数字がプレビュー表示
    3. **クリックで配置！**
    4. 縦か横に連続したマスの合計が **{TARGET}** になったら自動消去 🎉
    5. 消去 1マスにつき **{TARGET}点**
    6. 右と上に各行・列の合計ヒントが表示される

    **戦略のコツ**: 合計ヒントを見て、あと何を足せば{TARGET}になるか考えよう！
    """)