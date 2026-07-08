import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from streamlit_extras.let_it_rain import rain

# ---------------- PAGE ---------------- #
st.set_page_config(
    page_title="🎯 Decision Spinner",
    page_icon="🎯",
    layout="centered"
)

# ---------------- CSS ---------------- #
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

h1,h2,h3,p,label{
    color:white !important;
}

.result{
    font-size:55px;
    text-align:center;
    font-weight:bold;
    color:#FFD700;
    padding:20px;
    border-radius:15px;
    background:#111827;
}

.spinbox{
    font-size:40px;
    text-align:center;
    color:#00E5FF;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HISTORY ---------------- #
history_file = "history.csv"

try:
    history = pd.read_csv(history_file)
except:
    history = pd.DataFrame(columns=["Time","Winner"])

# ---------------- TITLE ---------------- #
st.title("🎯 Decision Spinner")
st.caption("Can't decide? Let fate choose!")

# ---------------- INPUT ---------------- #
options_text = st.text_area(
    "Enter one option per line",
    height=180,
    placeholder="Pizza\nBurger\nDosa\nBiryani"
)

col1, col2 = st.columns(2)

with col1:
    spin_speed = st.slider("Spin Speed", 20, 100, 50)


# ---------------- SPIN ---------------- #
if st.button("🎉 SPIN", use_container_width=True):

    options = [x.strip() for x in options_text.split("\n") if x.strip()]

    if len(options) < 2:
        st.warning("Enter at least 2 options.")
        st.stop()

    display = st.empty()

    for _ in range(spin_speed):
        display.markdown(
            f"""
            <div class='spinbox'>
            🎲 {random.choice(options)}
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.05)

    winner = random.choice(options)

    display.markdown(
        f"""
        <div class='result'>
        🏆 {winner}
        </div>
        """,
        unsafe_allow_html=True,
    )

    rain(
        emoji="❤️",
        font_size=40,
        falling_speed=5,
        animation_length="5"
    )

    st.success(f"🎉 Winner: **{winner}**")


    new = pd.DataFrame({
        "Time":[datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
        "Winner":[winner]
    })

    history = pd.concat([history,new],ignore_index=True)
    history.to_csv(history_file,index=False)

# ---------------- HISTORY ---------------- #
st.divider()

st.subheader("📜 Spin History")

if len(history)==0:
    st.info("No spins yet.")
else:
    st.dataframe(
        history.iloc[::-1],
        use_container_width=True,
        hide_index=True
    )


# ---------------- CLEAR ---------------- #
st.divider()

if st.button("🗑 Clear History"):

    history = pd.DataFrame(columns=["Time","Winner"])
    history.to_csv(history_file,index=False)

    st.success("History Cleared!")
    st.rerun()