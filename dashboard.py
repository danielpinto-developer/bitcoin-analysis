import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import subprocess
import time

OUTPUT_DIR = "charts_dip_alert"
DATA_PATH = os.path.join(OUTPUT_DIR, "dip_signals.csv")
IMG_PATH = os.path.join(OUTPUT_DIR, "top5_cumulative_returns.png")

st.set_page_config(page_title="Crypto Dashboard", layout="centered")
st.title("📉 Crypto Dashboard")

# CSV
if not os.path.exists(DATA_PATH):
    st.error("Dip signal data not found. Please run the analysis first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Trigger Scripts
st.markdown("---")
col1, col2 = st.columns([3, 1])  # Adjust layout

with col1:
    st.subheader("⚙️ Re-run Full Analysis")

with col2:
    if st.button("🚀 Run All Scripts"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.text("Preparing...")
            time.sleep(0.5)
            progress_bar.progress(10)

            status_text.text("Running dip_alert.py...")
            subprocess.run(["python", "dip_alert.py"], check=True)
            progress_bar.progress(35)

            status_text.text("Running bitcoin_analysis.py...")
            subprocess.run(["python", "bitcoin_analysis.py"], check=True)
            progress_bar.progress(65)

            status_text.text("Running top_crypto.py...")
            subprocess.run(["python", "top_crypto.py"], check=True)
            progress_bar.progress(90)

            time.sleep(0.5)
            progress_bar.progress(100)
            status_text.text("✅ All scripts completed successfully.")
            st.success("Done!")

        except subprocess.CalledProcessError as e:
            status_text.text("❌ Error during script execution.")
            st.error("Something went wrong.")
            st.code(str(e))

# Top 5
st.subheader("🔔 Top 5 Dip Signals")
top5 = df.head(5)
st.dataframe(top5, use_container_width=True)

# Full Table
with st.expander("📊 View All 30 Coins"):
    st.dataframe(df, use_container_width=True)

# Image
st.subheader("📈 Cumulative Returns (Top 5)")
if os.path.exists(IMG_PATH):
    st.image(IMG_PATH, caption="Cumulative performance of top 5 coins in last 180 days", use_container_width=True)
else:
    st.warning("Image file not found. Run analysis to generate it.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 16px;'>🚀 Built by Daniel Pinto — Powered by Python, Streamlit, and Real Crypto Data 💥</div>",
    unsafe_allow_html=True
)


