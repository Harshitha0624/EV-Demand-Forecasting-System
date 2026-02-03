import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Page Config (MUST BE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="EV Demand Intelligence Platform",
    page_icon="⚡",
    layout="wide"
)

# --------------------------------------------------
# Minimal Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        div[data-testid="metric-container"] {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .feature-card {
            background-color: #161b22;
            padding: 28px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.06);
            height: 100%;
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            border: 1px solid rgba(0,194,255,0.6);
            transform: translateY(-6px);
            box-shadow: 0px 8px 30px rgba(0,194,255,0.15);
        }

        .feature-title {
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .feature-desc {
            font-size: 14px;
            color: #9aa4b2;
            line-height: 1.6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "ev_charging_data.csv")
df = pd.read_csv(data_path)

stations = sorted(df["station_id"].unique())

# --------------------------------------------------
# Sidebar (Minimal – Only What’s Needed)
# --------------------------------------------------
with st.sidebar:

    st.markdown("## ⚡ EV Intelligence")
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    st.markdown("### 🎯 Station Selection")

    selected_station = st.selectbox(
        "Choose Charging Station",
        stations
    )

    st.session_state["selected_station"] = selected_station

    st.markdown("---")

    st.markdown("### 📌 Quick Info")

    st.markdown("""
    - Forecast next 24 hours  
    - Load risk classification  
    - Historical trend analysis  
    - Model explainability  
    """)

    st.markdown("---")

    st.caption("EV Demand Intelligence Platform v1.0")

# --------------------------------------------------
# Page Header
# --------------------------------------------------
st.title("⚡ EV Demand Intelligence Platform")
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --------------------------------------------------
# Platform Overview
# --------------------------------------------------
st.markdown("## 🚀 Platform Overview")

st.markdown("""
The EV Demand Intelligence Platform is an AI-powered analytical system 
designed to forecast short-term EV charging demand and evaluate potential 
grid stress across multiple charging stations.

It integrates time-series machine learning, dynamic forecasting controls, 
risk classification, and explainable analytics to support infrastructure planning.
""")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Core Capabilities (3 Column Layout)
# --------------------------------------------------
st.markdown("## 🔍 Core Capabilities")

# First Row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">📊 Multi-step Forecasting</div>
            <div class="feature-desc">
            Recursive 6–72 hour prediction engine with built-in uncertainty estimation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">⚠ Load Risk Assessment</div>
            <div class="feature-desc">
            Automated classification of Low, Moderate, and High load conditions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">📈 Historical Analytics</div>
            <div class="feature-desc">
            Trend analysis, volatility insights, and demand distribution patterns.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Second Row
col4, col5 = st.columns(2)

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🧠 Model Explainability</div>
            <div class="feature-desc">
            Feature importance analysis to interpret demand drivers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🔬 Growth Scenario Evaluation</div>
            <div class="feature-desc">
            Interactive demand growth adjustment for infrastructure stress testing.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )