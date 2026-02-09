import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from config import BLOCKS
from prices import get_price
from calc import calc_pips

def fmt(value, decimals=2):
    if value is None:
        return "–"
    return f"{value:.{decimals}f}"

st.set_page_config(layout="wide")
st.title("FX – NORM + NORM")

st_autorefresh(interval=5 * 60 * 1000, key="auto")

if st.button("🔄 Refresh manuale"):
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=300)
def load_blocks():
    out = []
    for block in BLOCKS:
        rows = []
        for pair, direction, entry in block["pairs"]:
            att = get_price(pair)
            pips = calc_pips(direction, entry, att)

            rows.append({
                "pair": pair,
                "direction": direction,
                "entry": entry,
                "att": att,
                "pips": pips
            })
        gap = None
        if rows[0]["pips"] is not None and rows[1]["pips"] is not None:
            gap = round(rows[0]["pips"] + rows[1]["pips"], 1)
        out.append((block["name"], rows, gap))
    return out

blocks = load_blocks()

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
.buy  { color: #1f4ed8; font-weight: bold; }

.gap {
    text-align: center;
    font-weight: bold;
    padding: 6px;
    border-top: 1px solid #999;
}
</style>


<div class="container">
"""

for name, rows, gap in blocks:
    sell = rows[0] if rows[0]["direction"] == "SELL" else rows[1]
    buy  = rows[1] if sell == rows[0] else rows[0]

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
            <div class="cell value">{fmt(sell['pips'], 2)}</div>
            <div class="cell value">{fmt(buy['pips'], 2)}</div>
        </div>

        <div class="gap">
            GAP PIPS&nbsp;&nbsp;{fmt(gap, 2)}
        </div>
    </div>
    """

html += "</div>"

components.html(html, height=420, scrolling=False)
