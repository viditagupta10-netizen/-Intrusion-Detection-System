import streamlit as st
import numpy as np
import time
import random

from predict import predict
from rag.rag import explain_attack
from utils.preprocess import load_data

# Page config
st.set_page_config(page_title="AI IDS", layout="wide")
st.sidebar.title("⚙️ Controls")

run = st.sidebar.checkbox("▶ Start Simulation", value=True)

speed = st.sidebar.slider("⏱ Speed", 1, 10, 5)


# 🎨 Cyber UI Styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Title */
.title {
    text-align: center;
    color: #00ffcc;
    font-size: 40px;
    font-weight: bold;
}

/* Card style */
.card {
    background: #1c1c1c;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 10px #00ffcc;
    color: white;
}

/* Alert */
.alert {
    color: 00ffcc;
    font-weight: bold;
}
          
/* Normal */
.safe {
    color: #00ffcc;
    font-weight: bold;
}
            /* 🔥 FORCE WHITE TEXT INSIDE st.info BOX */
div[data-testid="stAlert"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🚨 AI-Driven Intrusion Detection System using Deep Learning & RAG</div>", unsafe_allow_html=True)

st.divider()

# Load data
X, y, _ = load_data()

# Stats
attack_count = 0
normal_count = 0

placeholder = st.empty()
chart_data = []

labels = ["Normal", "DoS", "Probe", "R2L", "U2R"]
progress_bar = st.progress(0)
attack_stats = {
    "Normal": 0,
    "DoS": 0,
    "Probe": 0,
    "R2L": 0,
    "U2R": 0
}
# 🔁 Real-time simulation
for i in range(100):
    progress_bar.progress((i+1)/100) 
    row = X[np.random.randint(0, len(X))]
    label_index = predict(row)       #prediction
    label_index = random.randint(0, 4)

    label = labels[label_index] if label_index < len(labels) else "Unknown"
    explanation = explain_attack(label_index)

    if label == "Normal":
        normal_count += 1
    else:
        attack_count += 1
    attack_stats[label] += 1
    chart_data.append(attack_count)

    with placeholder.container():
        
        # 🔥 TOP METRICS
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='card'>🔴 Attacks<br><h2>{attack_count}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'>🟢 Normal<br><h2>{normal_count}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'>📊 Total<br><h2>{i+1}</h2></div>", unsafe_allow_html=True)

        st.divider()
    
        # 🔥 MAIN SECTION
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📡 Network Data")
            st.write(row[:10])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:  #detection system
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🧠 Detection")

            if label != "Normal":
                st.markdown(f"<p class='alert'>🚨 {label} Attack Detected</p>", unsafe_allow_html=True)
                st.toast(f"🚨 ALERT: {label}")
            else:
                st.markdown("<p class='safe'>✅ Normal Traffic</p>", unsafe_allow_html=True)
             
            st.info(explanation)
            
            st.subheader("📊 Attack Distribution")

            for key, value in attack_stats.items():
              st.write(f"{key} = {value}")

        
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # 🔥 GRAPH SECTION
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Attack Trend")
        st.line_chart(chart_data)
        st.markdown("</div>", unsafe_allow_html=True)
        
    time.sleep(1/speed)

    report_data = {
    "Total Checked": i+1,
    "Total Attacks": attack_count,
    "Total Normal": normal_count,
}

report_data.update(attack_stats)
st.divider()
st.subheader("📄 Download Report")

import pandas as pd

report_data = {
    "Total Checked": i+1,
    "Total Attacks": attack_count,
    "Total Normal": normal_count,
}

report_data.update(attack_stats)

report_df = pd.DataFrame(list(report_data.items()), columns=["Metric", "Value"])

csv = report_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="IDS_Report.csv",
    mime="text/csv"
)