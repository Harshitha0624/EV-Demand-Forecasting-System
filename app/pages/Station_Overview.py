import streamlit as st
import pandas as pd
import os
import plotly.express as px
with st.sidebar:
    st.markdown("## ⚡ EV Intelligence")
    st.markdown("---")


st.title("📊 Station Overview")
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --------------------------------------------------
# Dark Metric Styling (Correct Contrast)
# --------------------------------------------------
st.markdown(
    """
    <style>
        div[data-testid="metric-container"] {
            background-color: #1e2430;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="metric-container"] label {
            color: #9aa4b2 !important;
            font-size: 14px;
        }

        div[data-testid="metric-container"] div {
            color: #ffffff !important;
            font-size: 26px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(BASE_DIR, "data", "ev_charging_data.csv")

df = pd.read_csv(data_path)

selected_station = st.session_state.get("selected_station", None)

if selected_station is None:
    st.warning("Please select a station from main page.")
    st.stop()

df = df[df["station_id"] == selected_station].copy()

# --------------------------------------------------
# Core KPIs
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Avg Demand (kWh)", round(df["energy_kwh"].mean(), 2))
col3.metric("Peak Demand (kWh)", round(df["energy_kwh"].max(), 2))

st.markdown("---")

# --------------------------------------------------
# NEW FEATURE 1: Demand Stability Score
# --------------------------------------------------
st.subheader("📊 Demand Stability Analysis")

volatility = df["energy_kwh"].std()
mean_demand = df["energy_kwh"].mean()

stability_score = 100 - (volatility / mean_demand) * 100

col1, col2 = st.columns(2)

col1.metric("Volatility (Std Dev)", round(volatility, 2))
col2.metric("Stability Score", f"{round(stability_score,1)}%")

if stability_score > 80:
    st.success("Station demand is highly stable.")
elif stability_score > 60:
    st.warning("Station shows moderate variability.")
else:
    st.error("Station demand is highly volatile.")

st.markdown("---")

# --------------------------------------------------
# NEW FEATURE 2: Hourly Performance Radar Insight
# --------------------------------------------------
st.subheader("⏱ Peak Hour Pattern")

hourly_avg = df.groupby("hour")["energy_kwh"].mean().reset_index()

peak_hour = hourly_avg.loc[hourly_avg["energy_kwh"].idxmax(), "hour"]

fig = px.line(
    hourly_avg,
    x="hour",
    y="energy_kwh",
    title=f"Average Hourly Demand Pattern ({selected_station})"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white")
)

fig.update_traces(line=dict(color="#00c2ff", width=3))

st.plotly_chart(fig, use_container_width=True)

st.info(f"Station typically experiences highest demand around hour {int(peak_hour)}.")
