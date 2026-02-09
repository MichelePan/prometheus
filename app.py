import streamlit as st
from streamlit_autorefresh import st_autorefresh
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
    result = []
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
        result.append((block["name"], rows, gap))
    return result

blocks = load_blocks()

# ===== CSS stile Excel =====
st.markdown("""
<style>
.block {
    border: 1px solid #999;
    padding: 6px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
.block-title {
    text-align: center;
    font-weight: bold;
    border-bottom: 1px solid #999;
    padding-bottom: 4px;
    margin-bottom: 6px;
}
.row {
    border-bottom: 1px solid #ddd;
    padding: 4px 0;
}
.pair {
    font-weight: bold;
}
.cell {
    display: flex;
    justify-content: space-between;
}
.label {
    color: #555;
}
.value {
    font-weight: bold;
}
.pos {
    color: green;
}
.neg {
    color: red;
}
.gap {
    text-align: center;
    font-weight: bold;
    margin-top: 6px;
    padding-top: 4px;
    border-top: 1px solid #999;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(4)

for col, (name, rows, gap) in zip(cols, blocks):
    with col:
        html = f"""
        <div class="block">
            <div class="block-title">{name}</div>
        """

        for r in rows:
            color = "pos" if r["pips"] and r["pips"] > 0 else "neg"
            html += f"""
            <div class="row">
                <div class="pair">{r['pair']}</div>
                <div class="cell"><span class="label">INGR</span><span class="value">{r['entry']}</span></div>
                <div class="cell"><span class="label">ATT</span><span class="value">{r['att']}</span></div>
                <div class="cell"><span class="label">MOV</span><span class="value {color}">{r['pips']}</span></div>
            </div>
            """

        gap_color = "pos" if gap and gap > 0 else "neg"
        html += f"""
            <div class="gap {gap_color}">
                GAP PIPS&nbsp;&nbsp;{gap}
            </div>
        </div>
        """

        st.markdown(html, unsafe_allow_html=True)
