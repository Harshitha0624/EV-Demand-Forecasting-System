# EV Demand Intelligence Platform

A geo-aware, capacity-driven forecasting system for EV charging infrastructure.

This platform predicts short-term charging demand, evaluates infrastructure utilization, and visualizes station-level grid risk using a structured multi-layer architecture.


## Overview

The EV Demand Intelligence Platform is designed to support proactive EV infrastructure planning through:

* Multi-step demand forecasting
* Capacity-aware load assessment
* Spatial risk visualization
* Scenario-based demand simulation

The system transforms historical charging behavior into forward-looking operational intelligence.


## Key Capabilities

### Multi-Step Forecasting

Recursive time-series forecasting (6–72 hours ahead) using engineered temporal features.

### Infrastructure Risk Assessment

Capacity-based utilization modeling:

* Forecast peak vs station capacity
* Utilization percentage calculation
* Risk classification (Low / Moderate / High)

### Grid Risk Map

Geo-spatial visualization of charging stations:

* Bubble size represents forecast peak demand
* Color indicates infrastructure stress
* Hover displays station metadata and utilization

### Scenario Simulation

Interactive demand growth modeling to simulate EV adoption impact.

### Model Explainability

Feature importance analysis to interpret key demand drivers.

---

## System Architecture

**Data Layer**

* Historical charging dataset
* Station metadata (area, zone, capacity, coordinates)

**Feature Engineering**

* Lag features (t-1, t-24)
* Rolling averages
* Day-of-week encoding
* Weekend indicator

**Modeling**

* Random Forest Regressor
* Recursive multi-step prediction
* Residual-based confidence estimation

**Application Layer**

* Multi-page Streamlit dashboard
* Forecast intelligence module
* Historical analytics module
* Infrastructure visualization module


## Tech Stack

* Python
* Pandas / NumPy
* Scikit-learn
* Plotly
* Streamlit


## Model Performance

| Model         | MAE   | RMSE  |
| ------------- | ----- | ----- |
| Random Forest | ~2.35 | ~2.97 |

Engineered temporal features provide strong short-term predictive stability while maintaining interpretability.

---

## Project Structure

```
EV_demand_forecasting/
│
├── app.py
├── data/
│   ├── ev_charging_data.csv
│   ├── station_metadata.csv
│
├── models/
│   └── ev_demand_model.pkl
│
└── pages/
    ├── Station_Overview.py
    ├── Forecast_Intelligence.py
    ├── Historical_Analytics.py
    ├── Model_Diagnostics.py
    ├── Feature_Importance.py
    └── Grid_Risk_Map.py

## Real-World Application

This system can support:

* EV charging network operators
* Utility infrastructure planners
* Smart city energy teams

By shifting from reactive monitoring to predictive infrastructure management.

## Deployment

Live Demo: (Add deployed link here)

---

Author: Harshitha Vasanth
Computer Science Engineering

