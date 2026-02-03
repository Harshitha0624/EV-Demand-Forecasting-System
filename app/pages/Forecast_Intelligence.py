import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px

# Sidebar Branding
with st.sidebar:
    st.markdown("## ⚡ EV Intelligence")
    st.markdown("---")

st.title("🔮 Forecast Intelligence")
st.markdown("<hr style='border:1px solid #2c2f36;'>", unsafe_allow_html=True)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(BASE_DIR, "data", "ev_charging_data.csv")
model_path = os.path.join(BASE_DIR, "models", "ev_demand_model.pkl")

# --------------------------------------------------
# Load Data & Model
# --------------------------------------------------
df = pd.read_csv(data_path)
model = joblib.load(model_path)

selected_station = st.session_state.get("selected_station", None)

if selected_station is None:
    st.warning("Select a station from main page first.")
    st.stop()

# --------------------------------------------------
# Filter Station
# --------------------------------------------------
df = df[df["station_id"] == selected_station].copy()

df["datetime"] = pd.to_datetime(df["date"]) + pd.to_timedelta(df["hour"], unit="h")
df = df.sort_values("datetime")

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------
df["lag_1"] = df["energy_kwh"].shift(1)
df["lag_24"] = df["energy_kwh"].shift(24)
df["rolling_mean_3"] = df["energy_kwh"].rolling(3).mean()
df["day_of_week"] = df["datetime"].dt.weekday
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

df = df.dropna()
df["station_id"] = selected_station

df_encoded = pd.get_dummies(df, columns=["station_id"], drop_first=True)

feature_cols = model.feature_names_in_

for col in feature_cols:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

df_encoded = df_encoded[feature_cols]

# --------------------------------------------------
# Forecast Controls
# --------------------------------------------------
st.subheader("⚙ Forecast Controls")

horizon = st.slider(
    "Forecast Duration (Hours)",
    min_value=6,
    max_value=72,
    value=24,
    step=6
)

growth_factor = st.slider(
    "Expected Demand Growth (%)",
    min_value=0,
    max_value=50,
    value=0,
    step=5
)

if horizon > 48:
    st.warning("Longer forecasts may accumulate prediction uncertainty.")

# --------------------------------------------------
# Recursive Forecast with Growth Adjustment
# --------------------------------------------------
latest_row = df_encoded.iloc[-1:].copy()

forecast_values = []
current_row = latest_row.copy()

for _ in range(horizon):
    pred = model.predict(current_row)[0]

    # Apply growth assumption
    adjusted_pred = pred * (1 + growth_factor / 100)

    forecast_values.append(adjusted_pred)

    current_row["lag_1"] = adjusted_pred
    current_row["hour"] = (current_row["hour"] + 1) % 24

forecast_df = pd.DataFrame({
    "Hour Ahead": range(1, horizon + 1),
    "Predicted Demand": forecast_values
})

# --------------------------------------------------
# Risk Classification
# --------------------------------------------------
historical_mean = df["energy_kwh"].mean()
historical_std = df["energy_kwh"].std()
historical_peak = df["energy_kwh"].max()

avg_forecast = np.mean(forecast_values)
peak_forecast = np.max(forecast_values)

if peak_forecast >= historical_peak:
    risk_level = "🔴 High Load Risk"
elif peak_forecast >= historical_mean + historical_std:
    risk_level = "🟡 Moderate Load Risk"
else:
    risk_level = "🟢 Low Load Risk"

st.subheader("⚠ Load Risk Assessment")

col1, col2, col3 = st.columns(3)
col1.metric("Average Forecast (kWh)", round(avg_forecast, 2))
col2.metric("Peak Forecast (kWh)", round(peak_forecast, 2))
col3.metric("Risk Level", risk_level)

# --------------------------------------------------
# Executive Insight
# --------------------------------------------------
st.subheader("🧠 Executive Insight")

if growth_factor > 0:
    st.info(f"Forecast adjusted assuming {growth_factor}% higher EV usage.")

if peak_forecast > historical_mean:
    insight = "Projected demand exceeds normal operating levels. Monitoring recommended."
else:
    insight = "Projected demand remains within typical operating range."

st.info(insight)

st.markdown("---")

# --------------------------------------------------
# Confidence Interval
# --------------------------------------------------
historical_preds = model.predict(df_encoded)
historical_actuals = df["energy_kwh"].values

residual_std = np.std(historical_actuals - historical_preds)

forecast_df["Upper Bound"] = forecast_df["Predicted Demand"] + residual_std
forecast_df["Lower Bound"] = forecast_df["Predicted Demand"] - residual_std

# --------------------------------------------------
# Plot Forecast
# --------------------------------------------------
fig = px.line(
    forecast_df,
    x="Hour Ahead",
    y="Predicted Demand",
    title=f"{horizon}-Hour Forecast with Confidence Band ({selected_station})"
)

fig.add_scatter(
    x=forecast_df["Hour Ahead"],
    y=forecast_df["Upper Bound"],
    mode="lines",
    name="Upper Bound",
    line=dict(dash="dash")
)

fig.add_scatter(
    x=forecast_df["Hour Ahead"],
    y=forecast_df["Lower Bound"],
    mode="lines",
    name="Lower Bound",
    line=dict(dash="dash")
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    title_font=dict(size=20)
)

fig.update_traces(line=dict(width=3))

st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------
# Load Station Metadata
# --------------------------------------------------
metadata_path = os.path.join(BASE_DIR, "data", "station_metadata.csv")
metadata = pd.read_csv(metadata_path)

station_info = metadata[metadata["station_id"] == selected_station].iloc[0]
capacity_kw = station_info["capacity_kw"]

# --------------------------------------------------
# Capacity Utilization
# --------------------------------------------------
utilization_pct = (peak_forecast / capacity_kw) * 100

if utilization_pct < 70:
    infra_risk = "🟢 Stable Infrastructure"
elif utilization_pct < 90:
    infra_risk = "🟡 Near Capacity"
else:
    infra_risk = "🔴 Overload Risk"

st.subheader("🏗 Infrastructure Utilization")

colA, colB = st.columns(2)
colA.metric("Station Capacity (kW)", capacity_kw)
colB.metric("Peak Utilization (%)", round(utilization_pct, 2))

st.metric("Infrastructure Status", infra_risk)

# --------------------------------------------------
# Peak Detection
# --------------------------------------------------
peak_hour = forecast_df["Predicted Demand"].idxmax() + 1
st.success(f"Predicted Peak within next {horizon} hours at Hour +{peak_hour}")
