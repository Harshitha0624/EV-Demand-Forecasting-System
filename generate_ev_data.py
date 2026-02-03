import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_DAYS = 180
NUM_STATIONS = 5
START_DATE = datetime(2025, 1, 1)

# -----------------------------
# CREATE DATA FOLDER IF NOT EXISTS
# -----------------------------
os.makedirs("data", exist_ok=True)

records = []

# -----------------------------
# DATA GENERATION
# -----------------------------
for day in range(NUM_DAYS):
    current_date = START_DATE + timedelta(days=day)
    for hour in range(24):
        for station in range(1, NUM_STATIONS + 1):

            base = np.random.uniform(5, 15)

            # Peak hours: morning & evening
            if 7 <= hour <= 10 or 17 <= hour <= 21:
                energy = base + np.random.uniform(10, 25)
            else:
                energy = base + np.random.uniform(0, 5)

            records.append([
                current_date.strftime("%Y-%m-%d"),
                hour,
                f"Station_{station}",
                round(energy, 2)
            ])

# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame(
    records,
    columns=["date", "hour", "station_id", "energy_kwh"]
)

# -----------------------------
# SAVE CSV
# -----------------------------
output_path = os.path.join("data", "ev_charging_data.csv")
df.to_csv(output_path, index=False)

print("✅ EV charging dataset created successfully!")
print(f"📁 Saved at: {output_path}")
print(df.head())
