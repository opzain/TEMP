from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random
import math
import os

app = Flask(__name__)
CORS(app)

# ============================================================
# 0. EMERGENCY OVERRIDE DATABASE
# ============================================================
OVERRIDE_DB = {}

# ============================================================
# 1. STATION DATABASE
# ============================================================
STATIONS = [
    {"code": "NDLS", "name": "New Delhi", "zone": "NR", "state": "Delhi"},
    {"code": "NZM", "name": "Hazrat Nizamuddin", "zone": "NR", "state": "Delhi"},
    {"code": "DLI", "name": "Delhi Junction", "zone": "NR", "state": "Delhi"},
    {"code": "DEE", "name": "Delhi Sarai Rohilla", "zone": "NR", "state": "Delhi"},
    {"code": "DEC", "name": "Delhi Cantt", "zone": "NR", "state": "Delhi"},
    {"code": "LKO", "name": "Lucknow Charbagh", "zone": "NR", "state": "Uttar Pradesh"},
    {"code": "CNB", "name": "Kanpur Central", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "ALD", "name": "Prayagraj Junction", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "VNS", "name": "Varanasi Junction", "zone": "NR", "state": "Uttar Pradesh"},
    {"code": "GKP", "name": "Gorakhpur Junction", "zone": "NER", "state": "Uttar Pradesh"},
    {"code": "MFP", "name": "Muzaffarpur Junction", "zone": "ECR", "state": "Bihar"},
    {"code": "SPJ", "name": "Samastipur Junction", "zone": "ECR", "state": "Bihar"},
    {"code": "BJU", "name": "Barauni Junction", "zone": "ECR", "state": "Bihar"},
    {"code": "PNBE", "name": "Patna Junction", "zone": "ECR", "state": "Bihar"},
    {"code": "GAYA", "name": "Gaya Junction", "zone": "ECR", "state": "Bihar"},
    {"code": "DDU", "name": "Pt. Deen Dayal Upadhyaya", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "MGS", "name": "Mughalsarai", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "ASR", "name": "Amritsar Junction", "zone": "NR", "state": "Punjab"},
    {"code": "JUC", "name": "Jalandhar City", "zone": "NR", "state": "Punjab"},
    {"code": "LDH", "name": "Ludhiana Junction", "zone": "NR", "state": "Punjab"},
    {"code": "CDG", "name": "Chandigarh", "zone": "NR", "state": "Punjab"},
    {"code": "UHL", "name": "Una Himachal", "zone": "NR", "state": "Himachal Pradesh"},
    {"code": "JAT", "name": "Jammu Tawi", "zone": "NR", "state": "Jammu & Kashmir"},
    {"code": "SVDK", "name": "Shri Mata Vaishno Devi Katra", "zone": "NR", "state": "Jammu & Kashmir"},
    {"code": "BCT", "name": "Mumbai Central", "zone": "WR", "state": "Maharashtra"},
    {"code": "BDTS", "name": "Mumbai Bandra Terminus", "zone": "WR", "state": "Maharashtra"},
    {"code": "CSMT", "name": "Mumbai CST", "zone": "CR", "state": "Maharashtra"},
    {"code": "LTT", "name": "Mumbai Lokmanya Tilak Terminus", "zone": "CR", "state": "Maharashtra"},
    {"code": "PNVL", "name": "Panvel Junction", "zone": "CR", "state": "Maharashtra"},
    {"code": "PUNE", "name": "Pune Junction", "zone": "CR", "state": "Maharashtra"},
    {"code": "SUR", "name": "Solapur", "zone": "CR", "state": "Maharashtra"},
    {"code": "KOP", "name": "Kolhapur", "zone": "CR", "state": "Maharashtra"},
    {"code": "SBC", "name": "Bangalore City", "zone": "SWR", "state": "Karnataka"},
    {"code": "MYS", "name": "Mysore Junction", "zone": "SWR", "state": "Karnataka"},
    {"code": "MAQ", "name": "Mangalore Central", "zone": "SR", "state": "Karnataka"},
    {"code": "UDU", "name": "Udupi", "zone": "SWR", "state": "Karnataka"},
    {"code": "KJM", "name": "Krishnarajapuram", "zone": "SWR", "state": "Karnataka"},
    {"code": "MAS", "name": "Chennai Central", "zone": "SR", "state": "Tamil Nadu"},
    {"code": "MS", "name": "Chennai Egmore", "zone": "SR", "state": "Tamil Nadu"},
    {"code": "CBE", "name": "Coimbatore Junction", "zone": "SR", "state": "Tamil Nadu"},
    {"code": "ERS", "name": "Ernakulam Junction", "zone": "SR", "state": "Kerala"},
    {"code": "TVC", "name": "Trivandrum Central", "zone": "SR", "state": "Kerala"},
    {"code": "KTYM", "name": "Kottayam", "zone": "SR", "state": "Kerala"},
    {"code": "KZH", "name": "Kozhikode", "zone": "SR", "state": "Kerala"},
    {"code": "HWH", "name": "Howrah Junction", "zone": "ER", "state": "West Bengal"},
    {"code": "SDAH", "name": "Sealdah", "zone": "ER", "state": "West Bengal"},
    {"code": "DGR", "name": "Durgapur", "zone": "ER", "state": "West Bengal"},
    {"code": "ASN", "name": "Asansol Junction", "zone": "ER", "state": "West Bengal"},
    {"code": "KGP", "name": "Kharagpur Junction", "zone": "SER", "state": "West Bengal"},
    {"code": "BBS", "name": "Bhubaneswar", "zone": "ECOR", "state": "Odisha"},
    {"code": "CTC", "name": "Cuttack", "zone": "ECOR", "state": "Odisha"},
    {"code": "VSKP", "name": "Visakhapatnam", "zone": "ECOR", "state": "Andhra Pradesh"},
    {"code": "BZA", "name": "Vijayawada Junction", "zone": "SCR", "state": "Andhra Pradesh"},
    {"code": "GNT", "name": "Guntur Junction", "zone": "SCR", "state": "Andhra Pradesh"},
    {"code": "TIR", "name": "Tirupati", "zone": "SCR", "state": "Andhra Pradesh"},
    {"code": "BPL", "name": "Bhopal Junction", "zone": "WCR", "state": "Madhya Pradesh"},
    {"code": "JHS", "name": "Jhansi Junction", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "AGC", "name": "Agra Cantt", "zone": "NCR", "state": "Uttar Pradesh"},
    {"code": "GWL", "name": "Gwalior", "zone": "NCR", "state": "Madhya Pradesh"},
    {"code": "KOTA", "name": "Kota Junction", "zone": "WCR", "state": "Rajasthan"},
    {"code": "RTM", "name": "Ratlam Junction", "zone": "WR", "state": "Madhya Pradesh"},
    {"code": "BRC", "name": "Vadodara Junction", "zone": "WR", "state": "Gujarat"},
    {"code": "ADI", "name": "Ahmedabad Junction", "zone": "WR", "state": "Gujarat"},
    {"code": "SURAT", "name": "Surat", "zone": "WR", "state": "Gujarat"},
    {"code": "HYB", "name": "Hyderabad Deccan", "zone": "SCR", "state": "Telangana"},
    {"code": "SC", "name": "Secunderabad Junction", "zone": "SCR", "state": "Telangana"},
    {"code": "GDR", "name": "Gudur Junction", "zone": "SCR", "state": "Andhra Pradesh"},
    {"code": "NLR", "name": "Nellore", "zone": "SCR", "state": "Andhra Pradesh"},
    {"code": "NJP", "name": "New Jalpaiguri", "zone": "NFR", "state": "West Bengal"},
    {"code": "GHY", "name": "Guwahati", "zone": "NFR", "state": "Assam"},
    {"code": "DBRG", "name": "Dibrugarh", "zone": "NFR", "state": "Assam"},
    {"code": "TZC", "name": "Tinsukia", "zone": "NFR", "state": "Assam"},
    {"code": "SLG", "name": "Silchar", "zone": "NFR", "state": "Assam"},
    {"code": "AGTL", "name": "Agartala", "zone": "NFR", "state": "Tripura"},
]
STATION_NAMES = {s["code"]: s["name"] for s in STATIONS}
CITY_TO_CODE = {s["name"].lower(): s["code"] for s in STATIONS}
STATION_STATES = {s["code"]: s["state"] for s in STATIONS}

# ============================================================
# 2. WEATHER DATABASE
# ============================================================
WEATHER_DB = {}
weather_conditions = [
    {"condition": "Clear", "speed_multiplier": 1.0, "icon": "fa-sun", "color": "#00e676"},
    {"condition": "Fog", "speed_multiplier": 0.6, "icon": "fa-smog", "color": "#b0b0b0"},
    {"condition": "Rain", "speed_multiplier": 0.8, "icon": "fa-cloud-rain", "color": "#4fc3f7"},
    {"condition": "Storm", "speed_multiplier": 0.5, "icon": "fa-cloud-bolt", "color": "#ff6b6b"},
    {"condition": "Heatwave", "speed_multiplier": 0.9, "icon": "fa-temperature-high", "color": "#ff9800"},
]

for station in STATIONS:
    code = station["code"]
    state = station["state"]
    if state in ["Delhi", "Uttar Pradesh", "Bihar", "Punjab"]:
        WEATHER_DB[code] = {"condition": "Fog" if random.random() < 0.3 else "Clear", "speed_multiplier": 0.6 if random.random() < 0.3 else 1.0, "icon": "fa-smog" if random.random() < 0.3 else "fa-sun", "color": "#b0b0b0" if random.random() < 0.3 else "#00e676"}
    elif state in ["Maharashtra", "Gujarat"]:
        WEATHER_DB[code] = {"condition": "Heatwave" if random.random() < 0.25 else "Clear", "speed_multiplier": 0.9 if random.random() < 0.25 else 1.0, "icon": "fa-temperature-high" if random.random() < 0.25 else "fa-sun", "color": "#ff9800" if random.random() < 0.25 else "#00e676"}
    elif state in ["Kerala", "Tamil Nadu", "Karnataka"]:
        WEATHER_DB[code] = {"condition": "Rain" if random.random() < 0.35 else "Clear", "speed_multiplier": 0.8 if random.random() < 0.35 else 1.0, "icon": "fa-cloud-rain" if random.random() < 0.35 else "fa-sun", "color": "#4fc3f7" if random.random() < 0.35 else "#00e676"}
    elif state in ["West Bengal", "Odisha", "Assam"]:
        WEATHER_DB[code] = {"condition": "Rain" if random.random() < 0.3 else "Clear", "speed_multiplier": 0.8 if random.random() < 0.3 else 1.0, "icon": "fa-cloud-rain" if random.random() < 0.3 else "fa-sun", "color": "#4fc3f7" if random.random() < 0.3 else "#00e676"}
    else:
        WEATHER_DB[code] = {"condition": "Clear", "speed_multiplier": 1.0, "icon": "fa-sun", "color": "#00e676"}

# ============================================================
# 3. TRAIN DATABASE GENERATOR
# ============================================================
def generate_trains():
    trains = []
    train_types = ["Rajdhani", "Shatabdi", "Duronto", "Superfast", "Express", "Jan Shatabdi", "Garib Rath", "Humsafar"]
    routes = [
        ["NDLS", "KOTA", "RTM", "BRC", "BCT"],
        ["BCT", "BRC", "RTM", "KOTA", "NDLS"],
        ["NDLS", "JHS", "BPL", "SUR", "HYB", "MAS"],
        ["MAS", "HYB", "SUR", "BPL", "JHS", "NDLS"],
        ["NDLS", "LKO", "CNB", "ALD", "PNBE", "HWH"],
        ["HWH", "PNBE", "ALD", "CNB", "LKO", "NDLS"],
        ["SDAH", "DGR", "ASN", "GAYA", "NDLS"],
        ["NDLS", "GAYA", "ASN", "DGR", "SDAH"],
        ["HWH", "DGR", "ASN", "GAYA", "PNBE", "MFP", "SPJ", "BJU"],
        ["BCT", "SUR", "PUNE", "MYS", "SBC"],
        ["SBC", "MYS", "PUNE", "SUR", "BCT"],
        ["NDLS", "LKO", "GKP", "MFP", "SPJ", "BJU", "NJP", "GHY"],
        ["NDLS", "CNB", "VNS", "DDU", "GAYA", "PNBE"],
        ["PNBE", "MFP", "SPJ", "BJU", "NJP", "GHY"],
        ["SBC", "KJM", "MYS", "MAQ", "PUNE", "BCT"],
        ["MAS", "CBE", "ERS", "TVC"],
        ["TVC", "ERS", "CBE", "MAS"],
        ["HYB", "BZA", "VSKP", "BBS", "CTC", "KGP", "HWH"],
        ["MAS", "GDR", "NLR", "BZA", "VSKP"],
        ["BCT", "BRC", "ADI", "SURAT"],
        ["ADI", "BRC", "RTM", "KOTA", "NDLS"],
        ["PUNE", "SUR", "HYB", "BZA", "MAS"],
        ["NDLS", "CDG", "LDH", "JUC", "ASR"],
        ["NDLS", "JHS", "AGC", "GWL", "BPL"],
        ["ASR", "JUC", "LDH", "CDG", "NDLS"],
        ["BPL", "JHS", "AGC", "NDLS"],
        ["NDLS", "AGC", "JHS", "BPL"],
        ["BCT", "PUNE", "SUR", "HYB"],
        ["HWH", "KGP", "BBS", "CTC", "VSKP"],
        ["VSKP", "BZA", "HYB", "SUR", "PUNE", "BCT"],
    ]
    
    expanded_routes = []
    for route in routes:
        expanded_routes.append(route)
        if len(route) > 4:
            variant = [route[0]]
            for i in range(2, len(route), 2):
                if i < len(route):
                    variant.append(route[i])
            if route[-1] not in variant:
                variant.append(route[-1])
            expanded_routes.append(variant)
        if len(route) < 6:
            variant = route.copy()
            all_stations = [s["code"] for s in STATIONS]
            for _ in range(2):
                random_station = random.choice(all_stations)
                if random_station not in variant:
                    pos = random.randint(1, len(variant)-1)
                    variant.insert(pos, random_station)
            expanded_routes.append(variant)
    
    train_number = 12000
    used_names = set()
    generated_count = 0
    
    for route in expanded_routes:
        if generated_count >= 500:
            break
        for direction in range(2):
            if generated_count >= 500:
                break
            route_copy = route.copy()
            if direction == 1:
                route_copy = route_copy[::-1]
            if len(route_copy) < 3:
                continue
            train_type = random.choice(train_types)
            start_city = STATION_NAMES.get(route_copy[0], route_copy[0])
            end_city = STATION_NAMES.get(route_copy[-1], route_copy[-1])
            start_name = start_city.split(" ")[0] if " " in start_city else start_city
            end_name = end_city.split(" ")[0] if " " in end_city else end_city
            
            name_candidates = []
            if train_type == "Rajdhani":
                name_candidates.append(f"{start_name} {end_name} Rajdhani Express")
            elif train_type == "Shatabdi":
                name_candidates.append(f"{start_name} {end_name} Shatabdi Express")
            elif train_type == "Duronto":
                name_candidates.append(f"{start_name} {end_name} Duronto Express")
            elif train_type == "Superfast":
                name_candidates.append(f"{start_name} {end_name} Superfast Express")
            else:
                name_candidates.append(f"{start_name} {end_name} Express")
            
            train_name = None
            for candidate in name_candidates:
                if candidate not in used_names:
                    train_name = candidate
                    used_names.add(candidate)
                    break
            if not train_name:
                continue
            
            delay = random.choice([0, 5, 10, 15, 20, 25, 30, 45, 60])
            current_idx = random.randint(0, max(0, len(route_copy) - 2))
            segment_distances = {}
            for i in range(len(route_copy) - 1):
                segment_distances[route_copy[i]] = random.randint(80, 350)
            
            schedule = {}
            current_time = datetime.time(6, 0)
            for i, station in enumerate(route_copy):
                if i == 0:
                    schedule[station] = f"{current_time.hour:02d}:{current_time.minute:02d}"
                else:
                    prev_station = route_copy[i-1]
                    dist = segment_distances.get(prev_station, 100)
                    speed = random.randint(40, 65)
                    minutes_to_add = int((dist / speed) * 60) + random.randint(0, 10)
                    total_minutes = current_time.hour * 60 + current_time.minute + minutes_to_add
                    if total_minutes >= 24 * 60:
                        total_minutes -= 24 * 60
                    new_hour = total_minutes // 60
                    new_minute = total_minutes % 60
                    current_time = datetime.time(new_hour, new_minute)
                    schedule[station] = f"{new_hour:02d}:{new_minute:02d}"
            
            trains.append({
                "number": str(train_number),
                "name": train_name,
                "type": train_type,
                "route": route_copy,
                "segment_distances": segment_distances,
                "current_station_index": current_idx,
                "delay": delay,
                "schedule": schedule
            })
            train_number += 1
            generated_count += 1
    
    print(f"✅ Generated {len(trains)} trains")
    return trains

TRAINS = generate_trains()

# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================
def get_full_station_name(code):
    return STATION_NAMES.get(code, code)

def get_city_code(city_name):
    city_name = city_name.strip().lower()
    if city_name.upper() in STATION_NAMES:
        return city_name.upper()
    if city_name in CITY_TO_CODE:
        return CITY_TO_CODE[city_name]
    for name, code in CITY_TO_CODE.items():
        if city_name in name or name in city_name:
            return code
    return None

def generate_historical_data(train, station_code):
    if station_code not in train["schedule"]:
        return []
    scheduled_time_str = train["schedule"][station_code]
    try:
        scheduled_hour = int(scheduled_time_str.split(":")[0])
        scheduled_min = int(scheduled_time_str.split(":")[1])
    except:
        return []
    historical = []
    base_delay = train["delay"]
    for day_offset in range(7, 0, -1):
        date = datetime.datetime.now() - datetime.timedelta(days=day_offset)
        random_factor = random.choice([
            random.uniform(-0.3, 0.3),
            random.uniform(0.5, 1.2),
            random.uniform(-0.2, 0.1),
        ])
        is_weekend = date.weekday() >= 5
        weekend_boost = 1.1 if is_weekend else 1.0
        actual_delay = base_delay * (1 + random_factor) * weekend_boost
        actual_delay = max(-15, min(90, actual_delay))
        total_minutes = scheduled_hour * 60 + scheduled_min + actual_delay
        if total_minutes >= 24 * 60:
            total_minutes -= 24 * 60
        elif total_minutes < 0:
            total_minutes += 24 * 60
        actual_hour = int(total_minutes // 60)
        actual_min = int(total_minutes % 60)
        actual_time_str = f"{actual_hour:02d}:{actual_min:02d}"
        historical.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%a"),
            "actual_time": actual_time_str,
            "delay_minutes": round(actual_delay, 1)
        })
    return historical

def get_average_delay(train, station_code):
    historical = generate_historical_data(train, station_code)
    if not historical:
        return 0, "N/A"
    delays = [h["delay_minutes"] for h in historical]
    avg_delay = sum(delays) / len(delays)
    scheduled_time_str = train["schedule"].get(station_code, "00:00")
    try:
        scheduled_hour = int(scheduled_time_str.split(":")[0])
        scheduled_min = int(scheduled_time_str.split(":")[1])
        avg_time_total = scheduled_hour * 60 + scheduled_min + avg_delay
        if avg_time_total >= 24 * 60:
            avg_time_total -= 24 * 60
        elif avg_time_total < 0:
            avg_time_total += 24 * 60
        avg_hour = int(avg_time_total // 60)
        avg_min = int(avg_time_total % 60)
        avg_time_str = f"{avg_hour:02d}:{avg_min:02d}"
    except:
        avg_time_str = "N/A"
    return round(avg_delay, 1), avg_time_str

def calculate_eta_with_weather(train, source, destination):
    route = train["route"]
    source_idx = route.index(source)
    dest_idx = route.index(destination)
    current_idx = train["current_station_index"]
    start_idx = max(current_idx, source_idx)
    
    now = datetime.datetime.now()
    day_of_week = now.weekday()
    is_weekend = day_of_week >= 5
    base_speed = 55 if is_weekend else 48
    
    total_time = 0
    distance_total = 0
    weather_alerts = []
    full_route_info = []
    station_etas = []
    current_time = now
    
    for i in range(start_idx, dest_idx):
        current_station = route[i]
        next_station = route[i+1]
        segment_km = train["segment_distances"].get(current_station, 100)
        distance_total += segment_km
        
        weather = WEATHER_DB.get(next_station, {"condition": "Clear", "speed_multiplier": 1.0, "icon": "fa-sun", "color": "#00e676"})
        speed_mult = weather["speed_multiplier"]
        effective_speed = base_speed * speed_mult
        time_for_segment = (segment_km / effective_speed) * 60
        total_time += time_for_segment
        
        predicted_dt = current_time + datetime.timedelta(minutes=time_for_segment)
        predicted_time_str = predicted_dt.strftime("%H:%M")
        scheduled_time = train["schedule"].get(next_station, "N/A")
        
        extra_delay = 0
        if speed_mult < 0.9:
            extra_delay = (segment_km / base_speed) * (1 - speed_mult) * 60
        
        if extra_delay > 5:
            weather_alerts.append({
                "station": next_station,
                "station_name": get_full_station_name(next_station),
                "condition": weather["condition"],
                "extra_delay_mins": round(extra_delay, 1),
                "icon": weather["icon"],
                "color": weather["color"]
            })
        
        station_etas.append({
            "station_code": next_station,
            "station_name": get_full_station_name(next_station),
            "scheduled_time": scheduled_time,
            "predicted_time": predicted_time_str,
            "delay_mins": round(time_for_segment - ((segment_km / base_speed) * 60), 1)
        })
        
        full_route_info.append({
            "station_code": next_station,
            "station_name": get_full_station_name(next_station),
            "distance_km": segment_km,
            "weather": weather["condition"],
            "weather_icon": weather["icon"],
            "weather_color": weather["color"],
            "speed_multiplier": speed_mult,
            "time_mins": round(time_for_segment, 1),
            "extra_delay": round(extra_delay, 1),
            "scheduled_time": scheduled_time,
            "predicted_time": predicted_time_str
        })
        current_time = predicted_dt
    
    train_number = train["number"]
    if train_number in OVERRIDE_DB:
        override_mins = OVERRIDE_DB[train_number]
        total_time += override_mins
    else:
        override_mins = 0
    
    total_time += train["delay"] * 1.2
    total_time += 5
    
    delay_causes = []
    if train["delay"] > 20:
        delay_causes.append(f"Current operational delay of {train['delay']} minutes")
    if weather_alerts:
        for alert in weather_alerts:
            if alert["extra_delay_mins"] > 10:
                delay_causes.append(f"{alert['condition']} at {alert['station_name']}")
    if is_weekend and train["type"] in ["Rajdhani", "Duronto"]:
        delay_causes.append("Weekend operational adjustments")
    if override_mins > 0:
        delay_causes.append(f"⚠️ Emergency Override: +{override_mins} minutes")
    if not delay_causes:
        delay_causes.append("Normal running conditions")
    
    return {
        "total_minutes": round(total_time, 1),
        "distance_km": distance_total,
        "weather_alerts": weather_alerts,
        "full_route": full_route_info,
        "delay_causes": delay_causes,
        "current_location": route[current_idx],
        "current_location_name": get_full_station_name(route[current_idx]),
        "station_etas": station_etas,
        "is_weekend": is_weekend,
        "override_applied": override_mins
    }

# --- NEW: Next station helper ---
def get_next_station_info(train, eta_data):
    route = train["route"]
    current_idx = train["current_station_index"]
    
    if current_idx >= len(route) - 1:
        return None
    
    next_station = route[current_idx + 1]
    next_station_name = get_full_station_name(next_station)
    scheduled_time = train["schedule"].get(next_station, "N/A")
    
    predicted_time = "N/A"
    time_to_next = 0
    distance_to_next = 0
    
    for segment in eta_data.get("full_route", []):
        if segment["station_code"] == next_station:
            predicted_time = segment["predicted_time"]
            time_to_next = segment["time_mins"]
            distance_to_next = segment["distance_km"]
            break
    
    if predicted_time == "N/A":
        for station in eta_data.get("station_etas", []):
            if station["station_code"] == next_station:
                predicted_time = station["predicted_time"]
                break
    
    # Calculate static schedule time to next station
    static_time = (distance_to_next / 50) * 60 if distance_to_next > 0 else 0
    
    return {
        "station_code": next_station,
        "station_name": next_station_name,
        "scheduled_time": scheduled_time,
        "predicted_time": predicted_time,
        "time_to_next_mins": round(time_to_next, 1),
        "distance_to_next_km": distance_to_next,
        "static_schedule_mins": round(static_time, 1)
    }

# ============================================================
# 5. API ENDPOINTS
# ============================================================

@app.route('/search_trains', methods=['POST'])
def search_trains():
    try:
        data = request.get_json()
        source = data.get('source', '').strip()
        destination = data.get('destination', '').strip()
        date = data.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        if not source or not destination:
            return jsonify({"status": "error", "message": "Please provide source and destination"}), 400
        source_code = get_city_code(source) or source
        dest_code = get_city_code(destination) or destination
        
        results = []
        for train in TRAINS:
            route = train["route"]
            try:
                source_idx = route.index(source_code)
                dest_idx = route.index(dest_code)
                if source_idx < dest_idx:
                    upcoming_stops = route[source_idx+1:dest_idx+1]
                    train_copy = train.copy()
                    train_copy["source"] = source_code
                    train_copy["destination"] = dest_code
                    train_copy["upcoming_stops"] = upcoming_stops
                    train_copy["source_idx"] = source_idx
                    train_copy["dest_idx"] = dest_idx
                    results.append(train_copy)
            except ValueError:
                continue
        
        result_trains = []
        for train in results:
            eta_data = calculate_eta_with_weather(train, source_code, dest_code)
            result_trains.append({
                "number": train["number"],
                "name": train["name"],
                "type": train["type"],
                "source": source_code,
                "source_name": get_full_station_name(source_code),
                "destination": dest_code,
                "destination_name": get_full_station_name(dest_code),
                "upcoming_stops": [{"code": s, "name": get_full_station_name(s)} for s in train["upcoming_stops"]],
                "current_location": train["route"][train["current_station_index"]],
                "current_location_name": get_full_station_name(train["route"][train["current_station_index"]]),
                "delay": train["delay"],
                "minutes_remaining": eta_data["total_minutes"],
                "distance_remaining": eta_data["distance_km"]
            })
        
        return jsonify({
            "status": "success",
            "source": source_code,
            "source_name": get_full_station_name(source_code),
            "destination": dest_code,
            "destination_name": get_full_station_name(dest_code),
            "date": date,
            "count": len(result_trains),
            "trains": result_trains
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/train_detail', methods=['POST'])
def train_detail():
    try:
        data = request.get_json()
        train_number = data.get('train_number')
        source = data.get('source', '').strip().upper()
        destination = data.get('destination', '').strip().upper()
        if not train_number:
            return jsonify({"status": "error", "message": "Train number required"}), 400
        
        if source and source not in STATION_NAMES:
            source_code = get_city_code(source)
            if source_code:
                source = source_code
        if destination and destination not in STATION_NAMES:
            dest_code = get_city_code(destination)
            if dest_code:
                destination = dest_code
        
        train = None
        for t in TRAINS:
            if t["number"] == train_number:
                train = t
                break
        if not train:
            return jsonify({"status": "error", "message": "Train not found"}), 404
        
        if not source or not destination:
            source = train["route"][0]
            destination = train["route"][-1]
        
        eta_data = calculate_eta_with_weather(train, source, destination)
        
        now = datetime.datetime.now()
        eta_time = now + datetime.timedelta(minutes=eta_data["total_minutes"])
        eta_formatted = eta_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if train["delay"] > 20:
            status = "Significantly Delayed"
            status_color = "#ff6b6b"
        elif train["delay"] > 5:
            status = "Slightly Delayed"
            status_color = "#ffc107"
        else:
            status = "On Time"
            status_color = "#00e676"
        
        # Get next station info
        next_station_info = get_next_station_info(train, eta_data)
        
        # Build full route with weather
        route_weather = []
        for i, station in enumerate(train["route"]):
            weather = WEATHER_DB.get(station, {"condition": "Clear", "icon": "fa-sun", "color": "#00e676", "speed_multiplier": 1.0})
            is_current = (i == train["current_station_index"])
            route_weather.append({
                "code": station,
                "name": get_full_station_name(station),
                "position": i,
                "is_current": is_current,
                "weather": weather["condition"],
                "icon": weather["icon"],
                "color": weather["color"],
                "speed_multiplier": weather["speed_multiplier"],
                "scheduled_time": train["schedule"].get(station, "N/A")
            })
        
        # Station ETAs with history
        station_etas_with_history = []
        for station_eta in eta_data.get("station_etas", []):
            station_code = station_eta["station_code"]
            historical = generate_historical_data(train, station_code)
            avg_delay, avg_time = get_average_delay(train, station_code)
            try:
                sh, sm = map(int, station_eta["scheduled_time"].split(':'))
                ph, pm = map(int, station_eta["predicted_time"].split(':'))
                s_min = sh * 60 + sm
                p_min = ph * 60 + pm
                diff = p_min - s_min
                if diff > 0:
                    diff_text = f"{diff}m late"
                elif diff < 0:
                    diff_text = f"{abs(diff)}m early"
                else:
                    diff_text = "On Time"
            except:
                diff_text = "N/A"
            
            station_etas_with_history.append({
                "station_code": station_code,
                "station_name": station_eta["station_name"],
                "scheduled_time": station_eta["scheduled_time"],
                "predicted_time": station_eta["predicted_time"],
                "delay_mins": station_eta["delay_mins"],
                "historical_data": historical,
                "average_delay": avg_delay,
                "average_time": avg_time,
                "comparison_text": diff_text
            })
        
        # Calculate savings
        savings = 0
        if eta_data["total_minutes"] > 0:
            static_est = eta_data["distance_km"] / 50 * 60
            savings = max(0, static_est - eta_data["total_minutes"])
        
        response = {
            "status": "success",
            "train_number": train["number"],
            "train_name": train["name"],
            "train_type": train["type"],
            "source": source,
            "source_name": get_full_station_name(source),
            "destination": destination,
            "destination_name": get_full_station_name(destination),
            "current_location": train["route"][train["current_station_index"]],
            "current_location_name": get_full_station_name(train["route"][train["current_station_index"]]),
            "current_delay": train["delay"],
            "delay_status": status,
            "delay_status_color": status_color,
            "minutes_remaining": eta_data["total_minutes"],
            "distance_remaining": eta_data["distance_km"],
            "predicted_arrival": eta_formatted,
            "confidence_score": 0.92,
            "full_route": route_weather,
            "weather_alerts": eta_data["weather_alerts"],
            "delay_causes": eta_data["delay_causes"],
            "full_route_weather": eta_data["full_route"],
            "station_etas": station_etas_with_history,
            "is_weekend": eta_data["is_weekend"],
            "override_applied": eta_data["override_applied"],
            "savings_minutes": round(savings, 1),
            "next_station": next_station_info  # NEW
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/train_by_number', methods=['POST'])
def train_by_number():
    try:
        data = request.get_json()
        train_number = data.get('train_number', '').strip()
        if not train_number:
            return jsonify({"status": "error", "message": "Train number required"}), 400
        train = None
        for t in TRAINS:
            if t["number"] == train_number:
                train = t
                break
        if not train:
            return jsonify({"status": "error", "message": f"Train {train_number} not found"}), 404
        return jsonify({
            "status": "success",
            "train_number": train["number"],
            "train_name": train["name"],
            "train_type": train["type"],
            "route": [{"code": s, "name": get_full_station_name(s)} for s in train["route"]],
            "current_location": train["route"][train["current_station_index"]],
            "current_location_name": get_full_station_name(train["route"][train["current_station_index"]]),
            "delay": train["delay"],
            "schedule": train["schedule"]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/predict_eta', methods=['POST'])
def predict_eta():
    try:
        data = request.get_json()
        train_id = data.get('train_id')
        train = None
        for t in TRAINS:
            if t["number"] == train_id or t["name"].lower() == str(train_id).lower():
                train = t
                break
        if not train:
            return jsonify({"status": "error", "message": "Train not found"}), 404
        destination = train["route"][-1]
        source = train["route"][0]
        eta_data = calculate_eta_with_weather(train, source, destination)
        now = datetime.datetime.now()
        eta_time = now + datetime.timedelta(minutes=eta_data["total_minutes"])
        eta_formatted = eta_time.strftime("%Y-%m-%d %H:%M:%S")
        
        next_station_info = get_next_station_info(train, eta_data)
        
        response = {
            "status": "success",
            "train_id": train["number"],
            "train_name": train["name"],
            "destination": destination,
            "destination_name": get_full_station_name(destination),
            "current_location": train["route"][train["current_station_index"]],
            "current_location_name": get_full_station_name(train["route"][train["current_station_index"]]),
            "predicted_arrival_time": eta_formatted,
            "minutes_remaining": eta_data["total_minutes"],
            "distance_remaining_km": eta_data["distance_km"],
            "current_delay_mins": train["delay"],
            "confidence_score": 0.92,
            "weather_alerts": eta_data["weather_alerts"],
            "route_upcoming": [s for s in train["route"][train["current_station_index"]+1:] if s != destination],
            "delay_causes": eta_data["delay_causes"],
            "station_etas": eta_data["station_etas"],
            "next_station": next_station_info
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ============================================================
# 6. EMERGENCY OVERRIDE
# ============================================================
@app.route('/override_delay', methods=['POST'])
def override_delay():
    try:
        data = request.get_json()
        train_number = data.get('train_number')
        extra_minutes = data.get('extra_minutes', 0)
        if not train_number:
            return jsonify({"status": "error", "message": "Train number required"}), 400
        train_exists = any(t["number"] == train_number for t in TRAINS)
        if not train_exists:
            return jsonify({"status": "error", "message": "Train not found"}), 404
        
        if extra_minutes <= 0:
            if train_number in OVERRIDE_DB:
                del OVERRIDE_DB[train_number]
            return jsonify({"status": "success", "message": "Override cleared", "override": 0}), 200
        
        OVERRIDE_DB[train_number] = extra_minutes
        return jsonify({
            "status": "success", 
            "message": f"Added {extra_minutes} minutes emergency delay",
            "override": extra_minutes
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ============================================================
# 7. HEALTH CHECK
# ============================================================
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "trains_loaded": len(TRAINS)}), 200

# ============================================================
# 8. RUN THE SERVER
# ============================================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'True') == 'True'
    print(f"🚀 Dynamic Train Forecast System API is starting...")
    print(f"📊 {len(TRAINS)} trains loaded")
    print(f"📍 Server running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)