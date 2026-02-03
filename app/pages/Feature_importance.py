import streamlit as st
import joblib
import os
import pandas as pd
import plotly.express as px
with st.sidebar:
    st.markdown("## ⚡ EV Intelligence")
    st.markdown("---")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stMetric {
            background-color: #f5f7fa;
            padding: 15px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧠 Model Explainability")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(BASE_DIR, "models", "ev_demand_model.pkl")

model = joblib.load(model_path)

if not hasattr(model, "feature_importances_"):
    st.warning("Current model does not support feature importance.")
    st.stop()

feature_names = model.feature_names_in_
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values("Importance", ascending=False)

st.subheader("Top Influencing Features")

fig = px.bar(
    importance_df.head(10),
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top 10 Feature Importances"
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    title_font=dict(size=20)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("""
### Interpretation

- **Lag_24 dominance** indicates strong daily seasonality.
- **Rolling mean influence** shows short-term trend smoothing.
- Station features contribute to localized baseline differences.

Model behavior aligns with realistic EV demand patterns.
""")
