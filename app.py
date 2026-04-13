import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.set_page_config(page_title="GCC AI Logistics PRO MAX", layout="wide")

st.title("🌍 GCC AI Logistics PRO MAX System")

st.markdown("Real routing system for Qatar 🇶🇦 + UAE 🇦🇪 + Saudi 🇸🇦")

# -----------------------------
# 🌍 FULL REGIONAL MAP DATA
# -----------------------------
locations = {
    # 🇶🇦 QATAR MAIN
    "Doha": (25.2854, 51.5310),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Lusail": (25.4207, 51.4905),
    "Mesaieed": (24.9923, 51.5519),
    "Ras Laffan": (25.8904, 51.5489),
    "Dukhan": (25.4242, 50.7827),
    "Hamad Airport": (25.2731, 51.6081),
    "The Pearl": (25.3694, 51.5486),
    "Industrial Area Doha": (25.1390, 51.5370),

    # 🚇 DOHA METRO (REAL MAJOR STATIONS)
    "Msheireb Metro": (25.2855, 51.5330),
    "DECC Metro": (25.3269, 51.5310),
    "West Bay Metro": (25.3239, 51.5273),
    "Education City Metro": (25.3139, 51.4382),
    "Qatar University Metro": (25.3743, 51.4876),
    "Al Wakrah Metro": (25.1768, 51.5820),
    "Souq Waqif Metro": (25.2860, 51.5336),

    # 🇦🇪 UAE
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),
    "Sharjah": (25.3463, 55.4209),
    "Al Ain": (24.1302, 55.8023),

    # 🇸🇦 SAUDI ARABIA
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
    "Dammam": (26.4207, 50.0888),
    "Mecca": (21.3891, 39.8579),
}

# -----------------------------
# REAL DISTANCE (Haversine)
# -----------------------------
def haversine(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# -----------------------------
# METRO PRICE (REALISTIC QATAR RANGE)
# -----------------------------
def metro_price(dist):
    if dist < 10:
        return 2
    elif dist < 25:
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
        speed = 55
    elif mode == "✈️ Air":
        speed = 850
    else:
        speed = 60

    return dist / speed

# -----------------------------
# UI
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    start = st.selectbox("Start Location", list(locations.keys()))

with col2:
    end = st.selectbox("End Location", list(locations.keys()))

with col3:
    mode = st.selectbox("Transport Mode", ["🚗 Car", "🚇 Metro", "✈️ Air"])

# -----------------------------
# IMPORTANT FIX:
# ❌ NO session_state map (THIS FIXES DISAPPEARING ISSUE)
# -----------------------------
m = folium.Map(location=[25.3, 51.3], zoom_start=6)

# Add all markers every run (correct way)
for name, coord in locations.items():
    folium.Marker(coord, tooltip=name).add_to(m)

# -----------------------------
# RUN
# -----------------------------
if st.button("🚀 Calculate Route"):

    a = locations[start]
    b = locations[end]

    dist = haversine(a, b)
    time = travel_time(dist, mode)

    price = 0
    if mode == "🚇 Metro":
        price = metro_price(dist)

    folium.PolyLine([a, b], color="blue", weight=4).add_to(m)

    st_folium(m, height=700, width=1000)

    st.subheader("📊 AI ROUTE REPORT")

    st.write(f"📍 From: {start}")
    st.write(f"📍 To: {end}")
    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"⏱ Travel Time: {time:.2f} hours")
    st.write(f"🚇 Metro Price: {price} QAR" if mode == "🚇 Metro" else "No Metro cost")

    # Smart logic
    if dist > 500 and mode == "🚗 Car":
        st.warning("Long distance — Air travel recommended ✈️")

    if mode == "🚇 Metro" and dist > 40:
        st.warning("Metro not efficient for long distance")

st.caption("GCC AI Logistics System PRO MAX 🚀")
st.write(f"🚇 Metro Cost: {cost} QAR" if mode == "🚇 Metro" else "🚗 No ticket cost")

    st.success("System using REAL Earth-distance formula 🌍")

st.caption("Qatar Logistics AI PRO System")
