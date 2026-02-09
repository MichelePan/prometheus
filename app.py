import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from config import BLOCKS
from prices import get_price
from calc import calc_pips

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
        for pair, entry in block["pairs"]:
            att = get_price(pair)
            pips = calc_pips(pair, entry, att)
            rows.append({
                "pair": pair,
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
    gap: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
.block {
    border: 1px solid #999;
    padding: 6px;
}
.title {
    text-align: center;
    font-weight: bold;
    border-bottom: 1px solid #999;
    margin-bottom: 6px;
}
.row {
    border-bottom: 1px solid #ddd;
    padding: 4px 0;
}
.pair {
    font-weight: bold;
}
.line {
    display: flex;
    justify-content: space-between;
}
.pos { color: green; }
.neg { color: red; }
.gap {
    text-align: center;
    font-weight: bold;
    border-top: 1px solid #999;
    margin-top: 6px;
    padding-top: 4px;
}
</style>

<div class="container">
"""

for name, rows, gap in blocks:
    html += f"""
    <div class="block">
        <div class="title">{name}</div>
    """
    for r in rows:
        cls = "pos" if r["pips"] and r["pips"] > 0 else "neg"
        html += f"""
        <div class="row">
            <div class="pair">{r['pair']}</div>
            <div class="line"><span>INGR</span><span>{r['entry']}</span></div>
            <div class="line"><span>ATT</span><span>{r['att']}</span></div>
            <div class="line"><span>MOV</span><span class="{cls}">{r['pips']}</span></div>
        </div>
        """
    gap_cls = "pos" if gap and gap > 0 else "neg"
    html += f"""
        <div class="gap {gap_cls}">
            GAP PIPS&nbsp;&nbsp;{gap}
        </div>
    </div>
    """

html += "</div>"

components.html(html, height=420, scrolling=False)
