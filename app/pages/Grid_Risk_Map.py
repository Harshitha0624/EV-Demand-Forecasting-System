import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px

# --------------------------------------------------
# Sidebar Branding
# --------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ EV Intelligence")
    st.markdown("---")

st.title("🗺 Grid Risk Map")
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(BASE_DIR, "data", "ev_charging_data.csv")
metadata_path = os.path.join(BASE_DIR, "data", "station_metadata.csv")
model_path = os.path.join(BASE_DIR, "models", "ev_demand_model.pkl")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = pd.read_csv(data_path)
metadata = pd.read_csv(metadata_path)
model = joblib.load(model_path)

results = []

# --------------------------------------------------
# Forecast For All Stations (24h Peak)
# --------------------------------------------------
for station in df["station_id"].unique():

    station_df = df[df["station_id"] == station].copy()

    station_df["datetime"] = pd.to_datetime(station_df["date"]) + pd.to_timedelta(station_df["hour"], unit="h")
    station_df = station_df.sort_values("datetime")

    # Feature Engineering
    station_df["lag_1"] = station_df["energy_kwh"].shift(1)
    station_df["lag_24"] = station_df["energy_kwh"].shift(24)
    station_df["rolling_mean_3"] = station_df["energy_kwh"].rolling(3).mean()
    station_df["day_of_week"] = station_df["datetime"].dt.weekday
    station_df["is_weekend"] = (station_df["day_of_week"] >= 5).astype(int)

    station_df = station_df.dropna()

    station_df["station_id"] = station

    encoded = pd.get_dummies(station_df, columns=["station_id"], drop_first=True)

    feature_cols = model.feature_names_in_

    for col in feature_cols:
        if col not in encoded.columns:
            encoded[col] = 0

    encoded = encoded[feature_cols]

    latest_row = encoded.iloc[-1:].copy()

    forecast_values = []
    current_row = latest_row.copy()

    # Fixed 24-hour forecast
    for _ in range(24):
        pred = model.predict(current_row)[0]
        forecast_values.append(pred)
        current_row["lag_1"] = pred
        current_row["hour"] = (current_row["hour"] + 1) % 24

    peak_forecast = max(forecast_values)

    # Get Metadata
    station_info = metadata[metadata["station_id"] == station].iloc[0]
    capacity = station_info["capacity_kw"]

    utilization = (peak_forecast / capacity) * 100

    if utilization < 70:
        risk = "Low"
    elif utilization < 90:
        risk = "Moderate"
    else:
        risk = "High"

    results.append({
        "station_id": station,
        "area": station_info["area"],
        "zone": station_info["zone"],
        "latitude": station_info["latitude"],
        "longitude": station_info["longitude"],
        "peak_forecast": round(peak_forecast, 2),
        "capacity_kw": capacity,
        "utilization_pct": round(utilization, 2),
        "risk": risk
    })

map_df = pd.DataFrame(results)

# --------------------------------------------------
# Map Visualization
# --------------------------------------------------
fig = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    size="peak_forecast",
    color="risk",
    color_discrete_map={
        "Low": "#2ECC71",
        "Moderate": "#F1C40F",
        "High": "#E74C3C"
    },
    zoom=10,
    height=600,
    mapbox_style="carto-darkmatter"
)

fig.update_traces(
    marker=dict(sizemode="area", opacity=0.85),
    hovertemplate=
    "<b>%{customdata[0]}</b><br>"
    "Zone: %{customdata[1]}<br>"
    "Station ID: %{customdata[2]}<br>"
    "<br>"
    "Forecast Peak: %{customdata[3]} kWh<br>"
    "Capacity: %{customdata[4]} kW<br>"
    "Utilization: %{customdata[5]}%<br>"
    "<extra></extra>",
    customdata=map_df[[
        "area",
        "zone",
        "station_id",
        "peak_forecast",
        "capacity_kw",
        "utilization_pct"
    ]]
)

fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    title="Real-Time Infrastructure Load Risk Overview",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)
