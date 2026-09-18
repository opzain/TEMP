import json
import pandas as pd
import requests

url = "https://raw.githubusercontent.com/datameet/railways/master/trains.json"
print("Fetching and parsing dataset...")

response = requests.get(url)
data = response.json()

# Extract properties from GeoJSON features array
if "features" in data:
    records = [feature["properties"] for feature in data["features"]]
else:
    records = data

df = pd.DataFrame(records)

# Parse duration string (e.g., "28:30" or "08:15") into hours and minutes
if "duration" in df.columns:

    def parse_h(val):
        try:
            return int(str(val).split(":")[0])
        except:
            return 0

    def parse_m(val):
        try:
            return int(str(val).split(":")[1])
        except:
            return 0

    df["duration_h"] = df["duration"].apply(parse_h)
    df["duration_m"] = df["duration"].apply(parse_m)

# Map and standardize required headers
mapping = {
    "number": "train_number",
    "name": "train_name",
    "from_station_code": "from_station_code",
    "from_station_name": "from_station_name",
    "to_station_code": "to_station_code",
    "to_station_name": "to_station_name",
    "departure": "departure",
    "arrival": "arrival",
    "duration_h": "duration_h",
    "duration_m": "duration_m",
    "distance": "distance_km",
    "classes": "classes",
    "zone": "zone",
}

# Ensure missing keys exist
for col in mapping.keys():
    if col not in df.columns:
        df[col] = ""

df_final = df[list(mapping.keys())].rename(columns=mapping)

# Save to CSV
df_final.to_csv("train_data.csv", index=False)
print("SUCCESS! 'train_data.csv' updated with populated fields.")