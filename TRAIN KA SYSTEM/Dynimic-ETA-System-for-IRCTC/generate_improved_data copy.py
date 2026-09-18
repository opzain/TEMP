import pandas as pd
import numpy as np

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_FILE = "train_data.csv"
OUTPUT_FILE = "train_data_improved.csv"
N_SAMPLES = 50000

np.random.seed(42)

# --------------------------------------------------
# LOAD ORIGINAL TRAIN DATA
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)

# --------------------------------------------------
# REPEAT ORIGINAL TRAIN DATA
# --------------------------------------------------

# We need 50,000 records.
# Repeat the available trains until we reach 50,000 rows.

repeat_count = int(np.ceil(N_SAMPLES / len(df)))

expanded_df = pd.concat(
    [df] * repeat_count,
    ignore_index=True
).head(N_SAMPLES)

# --------------------------------------------------
# CREATE ML FEATURES
# --------------------------------------------------

# Distance
expanded_df["distance_km"] = pd.to_numeric(
    expanded_df["distance_km"],
    errors="coerce"
)

# Fill missing distance values
expanded_df["distance_km"] = expanded_df["distance_km"].fillna(
    expanded_df["distance_km"].median()
)

# --------------------------------------------------
# TIME FEATURES
# --------------------------------------------------

expanded_df["hour_of_day"] = np.random.randint(
    0, 24, N_SAMPLES
)

expanded_df["day_of_week"] = np.random.randint(
    0, 7, N_SAMPLES
)

expanded_df["is_weekend"] = (
    expanded_df["day_of_week"] >= 5
).astype(int)

# Peak hours:
# Morning: 07-10
# Evening: 17-21

expanded_df["is_peak_hour"] = (
    expanded_df["hour_of_day"].isin(
        [7, 8, 9, 10, 17, 18, 19, 20, 21]
    )
).astype(int)

# --------------------------------------------------
# CURRENT DELAY
# --------------------------------------------------

# Delay in minutes.
# Most trains have relatively small delays,
# while some have larger delays.

expanded_df["current_delay"] = np.random.gamma(
    shape=2.0,
    scale=5.0,
    size=N_SAMPLES
).round(1)

# Add some larger random delays
large_delay_mask = np.random.random(N_SAMPLES) < 0.08

expanded_df.loc[
    large_delay_mask,
    "current_delay"
] += np.random.uniform(
    10, 60, large_delay_mask.sum()
).round(1)

# --------------------------------------------------
# WEATHER
# --------------------------------------------------

weather_types = [
    "Clear",
    "Rain",
    "Fog",
    "Storm",
    "Heatwave"
]

expanded_df["weather"] = np.random.choice(
    weather_types,
    size=N_SAMPLES,
    p=[0.50, 0.20, 0.15, 0.05, 0.10]
)

weather_impact = {
    "Clear": 1.00,
    "Rain": 1.15,
    "Fog": 1.25,
    "Storm": 1.35,
    "Heatwave": 1.10
}

expanded_df["weather_factor"] = expanded_df[
    "weather"
].map(weather_impact)

# --------------------------------------------------
# CONGESTION
# --------------------------------------------------

congestion_levels = [
    "Low",
    "Medium",
    "High"
]

expanded_df["congestion"] = np.random.choice(
    congestion_levels,
    size=N_SAMPLES,
    p=[0.50, 0.35, 0.15]
)

congestion_impact = {
    "Low": 1.00,
    "Medium": 1.15,
    "High": 1.30
}

expanded_df["congestion_factor"] = expanded_df[
    "congestion"
].map(congestion_impact)

# --------------------------------------------------
# RAILWAY ZONE CODE
# --------------------------------------------------

zone_mapping = {
    "NR": 1,
    "WR": 2,
    "CR": 3,
    "SR": 4,
    "ER": 5,
    "SER": 6,
    "NCR": 7,
    "NER": 8,
    "NWR": 9,
    "SCR": 10,
    "SWR": 11,
    "ECR": 12,
    "ECoR": 13,
    "WCR": 14,
    "SECR": 15,
    "NFR": 16
}

expanded_df["zone_code"] = expanded_df[
    "zone"
].map(zone_mapping)

# Unknown zones get code 0
expanded_df["zone_code"] = expanded_df[
    "zone_code"
].fillna(0)

# --------------------------------------------------
# AVERAGE SPEED
# --------------------------------------------------

# Generate realistic average speeds.
# Longer-distance trains generally have
# somewhat higher average speeds.

base_speed = np.random.normal(
    loc=65,
    scale=10,
    size=N_SAMPLES
)

expanded_df["avg_speed_kmh"] = (
    base_speed
    / expanded_df["weather_factor"]
    / expanded_df["congestion_factor"]
)

expanded_df["avg_speed_kmh"] = (
    expanded_df["avg_speed_kmh"]
    .clip(25, 120)
    .round(1)
)

# --------------------------------------------------
# ACTUAL TRAVEL TIME
# --------------------------------------------------

# Base travel time = distance / speed

base_travel_time = (
    expanded_df["distance_km"]
    / expanded_df["avg_speed_kmh"]
    * 60
)

# Add delay and environmental effects

expanded_df["actual_travel_time_mins"] = (
    base_travel_time
    * expanded_df["weather_factor"]
    * expanded_df["congestion_factor"]
    + expanded_df["current_delay"]
)

# Add small natural variation
random_variation = np.random.normal(
    0,
    5,
    N_SAMPLES
)

expanded_df["actual_travel_time_mins"] += (
    random_variation
)

# Travel time cannot be negative
expanded_df["actual_travel_time_mins"] = (
    expanded_df["actual_travel_time_mins"]
    .clip(lower=5)
    .round(1)
)

# --------------------------------------------------
# SAVE DATASET
# --------------------------------------------------

expanded_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nImproved dataset created successfully!")
print("File:", OUTPUT_FILE)
print("Records:", len(expanded_df))
print("Columns:", len(expanded_df.columns))

print("\nML Features:")
print([
    "distance_km",
    "current_delay",
    "hour_of_day",
    "day_of_week",
    "is_weekend",
    "is_peak_hour",
    "weather_factor",
    "congestion_factor",
    "zone_code",
    "avg_speed_kmh",
    "actual_travel_time_mins"
])

print("\nFirst 5 rows:")
print(expanded_df.head())