import streamlit as st
import folium
from streamlit_folium import st_folium
import math
import random

st.set_page_config(page_title="Qatar AI Logistics System", layout="wide")

st.title("🇶🇦 Qatar Smart AI Logistics System (Metro + Roads + Air)")

# -----------------------------
# 🇶🇦 QATAR + METRO SYSTEM
# -----------------------------
cities = {
    # 🌆 Main cities
    "Doha": (25.2854, 51.5310),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Lusail": (25.4207, 51.4905),
    "Mesaieed": (24.9923, 51.5519),
    "Ras Laffan": (25.8904, 51.5489),
    "Hamad Airport": (25.2731, 51.6081),

    # 🚇 RED LINE METRO
    "Qatar University Station": (25.3743, 51.4876),
    "West Bay QIC Station": (25.3239, 51.5273),
    "DECC Station": (25.3269, 51.5310),
    "Msheireb Station": (25.2855, 51.5330),
    "Hamad Airport Metro": (25.2654, 51.6089),

    # 🚇 GREEN LINE METRO
    "Education City Station": (25.3139, 51.4382),
    "Al Shaqab Station": (25.3169, 51.4421),
    "Al Rayyan Station": (25.3292, 51.4511),

    # 🚇 GOLD LINE METRO
    "Souq Waqif Station": (25.2860, 51.5336),
    "Al Aziziyah Station": (25.2420, 51.5390),
    "Sport City Station": (25.2810, 51.4480),
}

# -----------------------------
# DISTANCE FUNCTION
# -----------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) * 111

# -----------------------------
# TRAFFIC SIMULATION
# -----------------------------
def traffic():
    return random.uniform(0.7, 2.0)

# -----------------------------
# WEATHER SIMULATION
# -----------------------------
def weather():
    options = [
        ("Clear ☀️", 1.0),
        ("Hot 🔥", 1.1),
        ("Windy 🌬️", 1.2),
        ("Sandstorm 🌪️", 1.6),
        ("Rain 🌧️", 1.3),
    ]
    return random.choice(options)

# -----------------------------
# TRAVEL TIME ENGINE
# -----------------------------
def travel_time(dist, mode, t, w):
    if mode == "🚗 Land":
        speed = 90
    elif mode == "✈️ Air":
        speed = 850
    elif mode == "🚇 Metro":
        speed = 60
    else:
        speed = 40

    return (dist / speed) * t * w

# -----------------------------
# UI
# -----------------------------
st.sidebar.header("🧭 Controls")

start = st.sidebar.selectbox("Start Location", list(cities.keys()))
end = st.sidebar.selectbox("End Location", list(cities.keys()))
mode = st.sidebar.selectbox("Transport Mode", ["🚗 Land", "✈️ Air", "🚢 Sea", "🚇 Metro"])

# -----------------------------
# MAP
# -----------------------------
m = folium.Map(location=[25.3, 51.3], zoom_start=10)

for city, coord in cities.items():
    folium.Marker(coord, tooltip=city).add_to(m)

# -----------------------------
# ROUTE ENGINE
# -----------------------------
if st.button("🚀 Generate Smart Route"):

    start_coord = cities[start]
    end_coord = cities[end]

    dist = distance(start_coord, end_coord)

    t_factor = traffic()
    weather_name, w_factor = weather()

    time = travel_time(dist, mode, t_factor, w_factor)

    folium.PolyLine([start_coord, end_coord], color="blue", weight=4).add_to(m)

    st_folium(m, height=650, width=1000)

    st.subheader("📊 AI LOGISTICS REPORT")

    st.write(f"📍 Start: {start}")
    st.write(f"📍 End: {end}")
    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"🚦 Traffic Factor: {t_factor:.2f}")
    st.write(f"🌦 Weather: {weather_name}")
    st.write(f"⏱ Estimated Time: {time:.2f} hours")
    st.write(f"🚛 Mode: {mode}")

    # SMART WARNINGS
    if mode == "🚇 Metro" and "Airport" in start and "Airport" in end:
        st.warning("Metro may require transfer at Msheireb hub!")

    if t_factor > 1.5:
        st.error("Heavy traffic detected!")

    if w_factor > 1.3:
        st.warning("Weather delay expected!")

st.caption("Built for Qatar Smart Logistics AI System 🇶🇦")
