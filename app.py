import streamlit as st
import folium
from streamlit_folium import st_folium
import math
import json
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="GCC AI Logistics PRO MAX",
    layout="wide"
)

st.title("🌍 GCC AI Logistics PRO MAX SYSTEM")
st.markdown("Real routing engine + AI decision system + interactive map")

# =========================================================
# SESSION STATE INIT
# =========================================================
if "start" not in st.session_state:
    st.session_state.start = None

if "end" not in st.session_state:
    st.session_state.end = None

if "history" not in st.session_state:
    st.session_state.history = []

# =========================================================
# FULL LOCATION DATABASE
# =========================================================
locations = {
    # ---------------- QATAR ----------------
    "Doha": (25.2854, 51.5310),
    "Lusail": (25.4207, 51.4905),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Mesaieed": (24.9923, 51.5519),
    "Ras Laffan": (25.8904, 51.5489),
    "Hamad Airport": (25.2731, 51.6081),

    # ---------------- DOHA METRO RED ----------------
    "Msheireb": (25.2855, 51.5330),
    "DECC": (25.3269, 51.5310),
    "West Bay": (25.3239, 51.5273),
    "Katara": (25.3548, 51.5247),
    "Qatar University": (25.3743, 51.4876),
    "Legtaifiya": (25.3610, 51.4970),
    "Al Wakra Metro": (25.1659, 51.5970),
    "Free Zone": (25.2340, 51.5600),

    # ---------------- GREEN LINE ----------------
    "Education City": (25.3139, 51.4382),
    "Hamad Hospital": (25.2800, 51.4800),
    "Al Rayyan": (25.2600, 51.4500),
    "Al Shaqab": (25.3169, 51.4421),

    # ---------------- GOLD LINE ----------------
    "Souq Waqif": (25.2860, 51.5336),
    "National Museum": (25.2850, 51.5460),
    "Al Sadd": (25.2800, 51.5100),

    # ---------------- UAE ----------------
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),
    "Sharjah": (25.3463, 55.4209),

    # ---------------- SAUDI ----------------
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
    "Dammam": (26.4207, 50.0888),
    "Mecca": (21.3891, 39.8579),
}

# =========================================================
# DISTANCE FUNCTION (REAL EARTH MATH)
# =========================================================
def haversine(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# =========================================================
# AI ENGINE (REAL SCORING SYSTEM)
# =========================================================
def ai_engine(distance):
    car = (distance / 90) * 1.0
    metro = (distance / 60) * 0.8 + 0.3
    air = (distance / 850) * 1.2

    scores = {
        "Car": car,
        "Metro": metro,
        "Air": air
    }

    best = min(scores, key=scores.get)
    return best, scores

# =========================================================
# METRO COST SYSTEM
# =========================================================
def metro_cost(distance):
    if distance < 10:
        return 2
    elif distance < 25:
        return 4
    return 6

# =========================================================
# UI PANEL
# =========================================================
st.sidebar.header("🧭 Controls")

start = st.sidebar.selectbox("Start Location", list(locations.keys()))
end = st.sidebar.selectbox("End Location", list(locations.keys()))

mode = st.sidebar.selectbox(
    "Mode",
    ["🤖 AI AUTO", "🚗 Car", "🚇 Metro", "✈️ Air"]
)

run = st.sidebar.button("🚀 RUN AI ROUTE")

reset = st.sidebar.button("🔄 RESET")

if reset:
    st.session_state.start = None
    st.session_state.end = None
    st.experimental_rerun()

# =========================================================
# MAP BASE (ALWAYS STABLE)
# =========================================================
base_map = folium.Map(location=[25.3, 51.3], zoom_start=6)

for name, coord in locations.items():
    folium.CircleMarker(
        location=coord,
        radius=3,
        tooltip=name
    ).add_to(base_map)

map_data = st_folium(base_map, height=600, width=1100)

# =========================================================
# CLICK LOGIC (OPTIONAL FUTURE UPGRADE READY)
# =========================================================
clicked = map_data.get("last_clicked")

if clicked:
    point = (clicked["lat"], clicked["lng"])

# =========================================================
# RUN ENGINE
# =========================================================
if run:

    a = locations[start]
    b = locations[end]

    dist = haversine(a, b)

    best_mode, scores = ai_engine(dist)

    final_mode = best_mode if mode == "🤖 AI AUTO" else mode

    cost = metro_cost(dist) if final_mode == "Metro" else 0

    # ROUTE MAP
    route_map = folium.Map(location=[(a[0]+b[0])/2, (a[1]+b[1])/2], zoom_start=6)

    folium.Marker(a, tooltip="START").add_to(route_map)
    folium.Marker(b, tooltip="END").add_to(route_map)

    folium.PolyLine([a, b], color="purple", weight=5).add_to(route_map)

    folium.Marker(
        [(a[0]+b[0])/2, (a[1]+b[1])/2],
        icon=folium.DivIcon(html=f"""
        <div style="background:purple;color:white;padding:5px;border-radius:8px">
        {dist:.2f} km
        </div>
        """)
    ).add_to(route_map)

    st_folium(route_map, height=600, width=1100)

    # =====================================================
    # AI OUTPUT PANEL
    # =====================================================
    st.subheader("🤖 AI ROUTE ENGINE OUTPUT")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Distance (km)", f"{dist:.2f}")

    with col2:
        st.metric("Mode", final_mode)

    with col3:
        st.metric("Cost (Metro)", f"{cost} QAR")

    st.write("### 🧠 AI Decision Scores")
    st.json(scores)

    # =====================================================
    # HISTORY SYSTEM
    # =====================================================
    st.session_state.history.append({
        "time": str(datetime.now()),
        "start": start,
        "end": end,
        "distance": dist,
        "mode": final_mode
    })

    st.write("### 📜 Route History")

    for h in st.session_state.history[-5:]:
        st.write(h)

    # =====================================================
    # WARNINGS
    # =====================================================
    if dist > 500:
        st.warning("Long distance → Air recommended ✈️")

else:
    st.info("Select route and press RUN AI ROUTE")

# =========================================================
# FOOTER
# =========================================================
st.caption("GCC AI Logistics PRO MAX SYSTEM 🚀")
