import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from datetime import datetime

from config import BLOCKS
from prices import get_price, clear_price_cache
from calc import calc_pips

# ===============================
# Utility
# ===============================

def fmt(value, decimals=2):
 if value is None:
 return "–"
 return f"{value:.{decimals}f}"

def cls_gap(value):
 if value is None:
 return ""
 return "pos" if value > 0 else "neg"

def cls_pips(value):
 if value is None:
 return ""
 return "pos" if value > 0 else "neg"

# ===============================
# Config pagina
# ===============================

st.set_page_config(layout="wide")
st.title("PROMETHEUS")

# auto refresh ogni 5 minuti
st_autorefresh(interval=5 * 60 * 1000, key="auto")

# ===============================
# Stato sessione
# ===============================

if "refresh_key" not in st.session_state:
 st.session_state.refresh_key = 0

# ===============================
# Load dati
# ===============================

@st.cache_data(ttl=300)
def load_blocks(_refresh_key):
 out = []
 any_missing = False
 source_mode = "CACHE"

 for block in BLOCKS:
 rows = []

 for pair, direction, entry in block["pairs"]:
 att, source = get_price(pair)

 if source == "LIVE":
 source_mode = "LIVE"

 if att is None:
 any_missing = True

 pips = calc_pips(direction, entry, att) if att else None

 rows.append({
 "pair": pair,
 "direction": direction,
 "entry": entry,
 "att": att,
 "pips": pips
 })

 gap = None
 if rows[0]["pips"] is not None and rows[1]["pips"] is not None:
 gap = round(rows[0]["pips"] + rows[1]["pips"], 2)

 out.append((block["name"], rows, gap))

 ts = datetime.now()

 return out, ts, any_missing, source_mode

# ===============================
# LOAD
# ===============================

blocks, last_update_dt, any_missing, source_mode = load_blocks(st.session_state.refresh_key)
last_update = last_update_dt.strftime("%d/%m/%Y %H:%M:%S")

# ===============================
# UI: header
# ===============================

col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

# 🔄 Refresh
with col1:
 if st.button("🔄 Refresh"):
 clear_price_cache()
 st.session_state.refresh_key += 1
 st.rerun()

# 🕒 Timestamp
with col2:
 st.caption(f"Ultimo aggiornamento: {last_update}")

# 📡 Fonte dati (LIVE / CACHE)
with col3:
 if source_mode == "LIVE":
 label = "LIVE DATA 🔄"
 color = "green"
 else:
 label = "CACHE 📦"
 color = "gray"

 st.markdown(
 f"<b style='color:{color}; font-size:16px'>Fonte: {label}</b>",
 unsafe_allow_html=True
 )

# 🚦 Stato qualità dati
with col4:
 now = datetime.now()
 age_sec = (now - last_update_dt).total_seconds()

 if any_missing:
 status = "STALE ⚠️"
 color = "red"
 elif age_sec < 120:
 status = "LIVE ✅"
 color = "green"
 elif age_sec < 300:
 status = "OK 🟡"
 color = "orange"
 else:
 status = "STALE ⛔"
 color = "red"

 st.markdown(
 f"<b style='color:{color}; font-size:16px'>Stato: {status}</b>",
 unsafe_allow_html=True
 )

# ===============================
# HTML + CSS
# ===============================

html = """
<style>
.container {
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 12px;
 font-family: Arial, sans-serif;
 font-size: 14px;
}

.block {
 border: 1px solid #999;
}

.title {
 text-align: center;
 font-weight: bold;
 padding: 6px;
 border-bottom: 1px solid #999;
 background: #f2f2f2;
}

.grid {
 display: grid;
 grid-template-columns: 80px 1fr 1fr;
}

.cell {
 padding: 6px;
 border-bottom: 1px solid #ddd;
}

.header {
 text-align: center;
 font-weight: bold;
 border-bottom: 1px solid #999;
}

.label {
 color: #666;
}

.value {
 text-align: right;
 font-family: monospace;
}

.sell { color: #c00000; font-weight: bold; }
.buy { color: #1f4ed8; font-weight: bold; }

.pos { color: green; }
.neg { color: red; }

.gap {
 text-align: center;
 font-weight: bold;
 padding: 6px;
 border-top: 1px solid #999;
}

@media (max-width: 768px) {
 .container {
 grid-template-columns: 1fr;
 }
}
</style>

<div class="container">
"""

# ===============================
# Rendering blocchi
# ===============================

for name, rows, gap in blocks:
 sell = rows[0] if rows[0]["direction"] == "SELL" else rows[1]
 buy = rows[1] if sell == rows[0] else rows[0]

 html += f"""
 <div class="block">
 <div class="title">{name}</div>

 <div class="grid">
 <div class="cell"></div>
 <div class="cell header sell">{sell['pair']} (SELL)</div>
 <div class="cell header buy">{buy['pair']} (BUY)</div>

 <div class="cell label">INGR</div>
 <div class="cell value">{fmt(sell['entry'], 5)}</div>
 <div class="cell value">{fmt(buy['entry'], 5)}</div>

 <div class="cell label">ATT</div>
 <div class="cell value">{fmt(sell['att'], 5)}</div>
 <div class="cell value">{fmt(buy['att'], 5)}</div>

 <div class="cell label">MOV</div>
 <div class="cell value {cls_pips(sell['pips'])}">
 {fmt(sell['pips'], 2)}
 </div>
 <div class="cell value {cls_pips(buy['pips'])}">
 {fmt(buy['pips'], 2)}
 </div>
 </div>

 <div class="gap {cls_gap(gap)}">
 GAP PIPS&nbsp;&nbsp;{fmt(gap, 2)}
 </div>
 </div>
 """

html += "</div>"

# ===============================
# Render
# ===============================

components.html(html, height=900, scrolling=True)
