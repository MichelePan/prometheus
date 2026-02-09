import streamlit as st
import pandas as pd
from config import FX_NORM_NORM
from prices import get_current_price
from calc import calc_pips
import time

st.set_page_config(
    page_title="FX Dashboard – NORM + NORM",
    layout="centered"
)

st.title("💱 FX Dashboard – NORM + NORM")

# Refresh manuale
if st.button("🔄 Refresh manuale"):
    st.experimental_rerun()

# Refresh automatico ogni 5 minuti
st.caption("⏱ Refresh automatico ogni 5 minuti")
time.sleep(0)  # placeholder

rows = []

for fx in FX_NORM_NORM:
    current = get_current_price(fx["pair"])
    pips = calc_pips(fx["pair"], fx["entry"], current)

    rows.append({
        "Coppia": fx["pair"],
        "INGR": fx["entry"],
        "ATT": current,
        "MOV PIPS": pips
    })

df = pd.DataFrame(rows)

def color_pips(val):
    if val is None:
        return ""
    return "color: green" if val > 0 else "color: red"

st.dataframe(
    df.style.applymap(color_pips, subset=["MOV PIPS"]),
    use_container_width=True
)

# Auto refresh
st.experimental_autorefresh(interval=5 * 60 * 1000)