import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.set_page_config(page_title="Qatar Metro AI + GCC System", layout="wide")

st.title("🇶🇦 Qatar Metro + GCC AI Transport System")

st.markdown("Real metro network + Qatar + GCC cities + AI routing engine")

# -----------------------------
# 🌍 FULL GCC + QATAR NETWORK
# -----------------------------
locations = {

    # 🇶🇦 MAIN AREAS
    "Doha": (25.2854, 51.5310),
    "Lusail": (25.4207, 51.4905),
    "Al Wakra": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Hamad Airport": (25.2731, 51.6081),

    # 🇦🇪 UAE
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),

    # 🇸🇦 SAUDI
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),

    # 🚇 RED LINE
    "Lusail QNB": (25.4871, 51.4751),
    "Qatar University": (25.3743, 51.4876),
    "Legtaifiya": (25.3610, 51.4970),
    "Katara": (25.3548, 51.5247),
    "Al Qassar": (25.3540, 51.5360),
    "DECC": (25.3269, 51.5310),
    "West Bay Qatar Energy": (25.3210, 51.5230),
    "Corniche": (25.3000, 51.5400),
    "Al Bidda": (25.2865, 51.5200),
    "Msheireb": (25.2855, 51.5330),
    "Al Doha Al Jadeda": (25.2720, 51.5450),
    "Umm Ghuwailina": (25.2590, 51.5460),
    "Al Matar Al Qadeem": (25.2510, 51.5480),
    "Oqba Ibn Nafie": (25.2450, 51.5440),
    "Hamad Airport T1": (25.2731, 51.6081),
    "Free Zone": (25.2340, 51.5600),
    "Ras Bu Fontas": (25.2050, 51.5750),
    "Al Wakra": (25.1659, 51.5970),

    # 🟢 GREEN LINE
    "Al Mansoura": (25.2640, 51.5330),
    "The White Palace": (25.2900, 51.4900),
    "Hamad Hospital": (25.2800, 51.4800),
    "Al Messila": (25.2700, 51.4700),
    "Al Rayyan Al Qadeem": (25.2600, 51.4500),
    "Al Shaqab": (25.3169, 51.4421),
    "Qatar National Library": (25.3170, 51.4390),
    "Education City": (25.3139, 51.4382),
    "Al Riffa": (25.3100, 51.4200),

    # 🟡 GOLD LINE
    "Ras Bu Abboud": (25.2770, 51.5530),
    "National Museum": (25.2850, 51.5460),
    "Souq Waqif": (25.2860, 51.5336),
    "Bin Mahmoud": (25.2750, 51.5200),
    "Al Sadd": (25.2800, 51.5100),
    "Joaan": (25.2700, 51.5000),
    "Al Sudan": (25.2650, 51.4900),
    "Al Waab": (25.2600, 51.4800),
    "Sport City": (25.2550, 51.4700),
    "Al Aziziyah": (25.2420, 51.5390),
}

# -----------------------------
# REAL DISTANCE (HAVERSINE)
# -----------------------------
def haversine(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# -----------------------------
# METRO COST (REAL QATAR RANGE)
# -----------------------------
def metro_cost(dist):
    if dist < 10:
        return 2
    elif dist < 25:
        return 4
    return 6

# -----------------------------
# MODE AI
# -----------------------------
def ai_mode(dist):
    if dist < 8:
        return "🚇 Metro"
    elif dist < 150:
        return "🚗 Car"
    return "✈️ Air"

# -----------------------------
# UI
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    start = st.selectbox("Start", list(locations.keys()))

with col2:
    end = st.selectbox("End", list(locations.keys()))

mode = st.selectbox("Mode", ["🤖 AI Auto", "🚇 Metro", "🚗 Car", "✈️ Air"])

run = st.button("🚀 Generate Route")

# -----------------------------
# MAP
# -----------------------------
m = folium.Map(location=[25.3, 51.3], zoom_start=10)

for name, coord in locations.items():
    folium.CircleMarker(coord, radius=3, tooltip=name).add_to(m)

# -----------------------------
# ROUTE ENGINE
# -----------------------------
if run:

    a = locations[start]
    b = locations[end]

    dist = haversine(a, b)

    final_mode = ai_mode(dist) if mode == "🤖 AI Auto" else mode

    cost = metro_cost(dist) if final_mode == "🚇 Metro" else 0

    folium.PolyLine([a, b], color="purple", weight=5).add_to(m)

    st_folium(m, height=700, width=1100)

    st.subheader("📊 AI ROUTE REPORT")

    st.write(f"📍 From: {start}")
    st.write(f"📍 To: {end}")
    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"🚇 Mode: {final_mode}")

    if final_mode == "🚇 Metro":
        st.success(f"Metro Ticket Price: {cost} QAR")

    if dist > 500:
        st.warning("Long distance → Air recommended ✈️")

st.caption("Qatar Metro AI + GCC System 🚇🌍")
