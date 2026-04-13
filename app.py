import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.set_page_config(page_title="Qatar AI Logistics PRO", layout="wide")

st.title("🇶🇦 Qatar AI Logistics System PRO (Real Engine)")

st.markdown("Real distance + Metro pricing + stable interactive map")

# -----------------------------
# 🇶🇦 LOCATIONS
# -----------------------------
locations = {
    "Doha": (25.2854, 51.5310),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Lusail": (25.4207, 51.4905),
    "Mesaieed": (24.9923, 51.5519),
    "Ras Laffan": (25.8904, 51.5489),
    "Hamad Airport": (25.2731, 51.6081),
    "West Bay Metro": (25.3239, 51.5273),
    "Msheireb Metro": (25.2855, 51.5330),
    "Education City Metro": (25.3139, 51.4382),
    "Qatar University Metro": (25.3743, 51.4876),
}

# -----------------------------
# REAL DISTANCE (HAVERSINE)
# -----------------------------
def haversine(coord1, coord2):
    R = 6371  # Earth radius km
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

# -----------------------------
# METRO PRICING (REAL QATAR METRO)
# -----------------------------
def metro_price(distance):
    if distance <= 10:
        return 2  # QAR
    elif distance <= 20:
        return 4
    else:
        return 6

# -----------------------------
# SPEED MODEL
# -----------------------------
def travel_time(dist, mode):
    if mode == "🚗 Car":
        speed = 90
    elif mode == "🚇 Metro":
        speed = 60
    elif mode == "✈️ Air":
        speed = 850
    else:
        speed = 50

    return dist / speed

# -----------------------------
# MAP (PERSISTENT FIX)
# -----------------------------
if "map" not in st.session_state:
    st.session_state.map = folium.Map(location=[25.3, 51.3], zoom_start=10)

m = st.session_state.map

# -----------------------------
# UI
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    start = st.selectbox("Start", list(locations.keys()))

with col2:
    end = st.selectbox("End", list(locations.keys()))

with col3:
    mode = st.selectbox("Transport", ["🚗 Car", "🚇 Metro", "✈️ Air"])

# -----------------------------
# RUN SYSTEM
# -----------------------------
if st.button("🚀 Calculate Route"):

    a = locations[start]
    b = locations[end]

    dist = haversine(a, b)
    time = travel_time(dist, mode)

    if mode == "🚇 Metro":
        cost = metro_price(dist)
    else:
        cost = 0

    folium.Marker(a, tooltip=start).add_to(m)
    folium.Marker(b, tooltip=end).add_to(m)

    folium.PolyLine([a, b], color="blue", weight=4).add_to(m)

    st_folium(m, height=650, width=1000)

    st.subheader("📊 REAL AI LOGISTICS OUTPUT")

    st.write(f"📍 From: {start}")
    st.write(f"📍 To: {end}")
    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"⏱ Time: {time:.2f} hours")
    st.write(f"🚇 Metro Cost: {cost} QAR" if mode == "🚇 Metro" else "🚗 No ticket cost")

    st.success("System using REAL Earth-distance formula 🌍")

st.caption("Qatar Logistics AI PRO System")
