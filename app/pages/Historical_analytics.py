import streamlit as st
import pandas as pd
import os
import plotly.express as px
with st.sidebar:
    st.markdown("## ⚡ EV Intelligence")
    st.markdown("---")

# Only spacing styling (no light metric override)
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📈 Historical Demand Insights")
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(BASE_DIR, "data", "ev_charging_data.csv")

df = pd.read_csv(data_path)

selected_station = st.session_state.get("selected_station", None)

if selected_station is None:
    st.warning("Select a station from main page.")
    st.stop()

df = df[df["station_id"] == selected_station].copy()

df["datetime"] = pd.to_datetime(df["date"]) + pd.to_timedelta(df["hour"], unit="h")
df["day_of_week"] = pd.to_datetime(df["date"]).dt.day_name()

# --------------------------------------------------
# 1️⃣ Daily Trend
# --------------------------------------------------
st.subheader("📊 Daily Energy Trend")

daily_total = df.groupby("date")["energy_kwh"].sum().reset_index()

fig1 = px.line(
    daily_total,
    x="date",
    y="energy_kwh",
    markers=True,
    title="Total Daily Energy Consumption"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# 2️⃣ Hour vs Day Heatmap
# --------------------------------------------------
st.subheader("🔥 Hourly Demand Heatmap")

heatmap_data = df.pivot_table(
    values="energy_kwh",
    index="hour",
    columns="date",
    aggfunc="mean"
)

fig2 = px.imshow(
    heatmap_data,
    aspect="auto",
    color_continuous_scale="Blues"
)

fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# 3️⃣ Day-of-Week Comparison
# --------------------------------------------------
st.subheader("📅 Day-of-Week Comparison")

dow_avg = df.groupby("day_of_week")["energy_kwh"].mean().reset_index()

fig3 = px.bar(
    dow_avg,
    x="day_of_week",
    y="energy_kwh",
    title="Average Demand by Day of Week"
)

fig3.update_layout(template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# 4️⃣ Demand Distribution
# --------------------------------------------------
st.subheader("📉 Demand Distribution")

fig4 = px.histogram(
    df,
    x="energy_kwh",
    nbins=30,
    title="Demand Distribution"
)

fig4.update_layout(template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# 5️⃣ Volatility Metric (Clean Dark Version)
# --------------------------------------------------
st.subheader("📌 Volatility Insight")

# Dark metric styling only here
st.markdown(
    """
    <style>
        div[data-testid="metric-container"] {
            background-color: #1e2430 !important;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="metric-container"] label {
            color: #9aa4b2 !important;
        }

        div[data-testid="metric-container"] div {
            color: #ffffff !important;
            font-size: 24px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)

volatility = df["energy_kwh"].std()
st.metric("Demand Volatility (Std Dev)", round(volatility, 2))
mean_demand = df["energy_kwh"].mean()

if volatility < mean_demand * 0.2:
    st.success("Low variability — station demand is highly stable.")
elif volatility < mean_demand * 0.4:
    st.warning("Moderate variability — occasional demand spikes observed.")
else:
    st.error("High variability — station shows significant fluctuation.")

