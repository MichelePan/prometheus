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

cols = st.columns(4)

for col, (name, rows, gap) in zip(cols, blocks):
    with col:
        st.markdown(f"### {name}")

        for r in rows:
            color = "green" if r["pips"] and r["pips"] > 0 else "red"
            st.markdown(
                f"""
                **{r['pair']}**
                INGR: {r['entry']}
                ATT: {r['att']}
                <span style="color:{color}">MOV PIPS: {r['pips']}</span>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown(
            f"**GAP PIPS:** <span style='color:blue'>{gap}</span>",
            unsafe_allow_html=True
        )
