import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.title("🌍 GCC AI Logistics System (Interactive Map)")

# -------------------------
# CITY DATA
# -------------------------
cities = {
    "Doha (Qatar)": (25.2854, 51.5310),
    "Dubai (UAE)": (25.2048, 55.2708),
    "Abu Dhabi (UAE)": (24.4539, 54.3773),
    "Riyadh (Saudi Arabia)": (24.7136, 46.6753),
    "Jeddah (Saudi Arabia)": (21.4858, 39.1925),
}

# -------------------------
# DISTANCE (KM approx)
# -------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) * 111

# -------------------------
# TRAVEL TIME
# -------------------------
def travel_time(dist, mode):
    if mode == "🚗 Land":
        return dist / 90
    elif mode == "✈️ Air":
        return dist / 850
    elif mode == "🚢 Sea":
        return dist / 45

# -------------------------
# UI
# -------------------------
start = st.selectbox("Start City", list(cities.keys()))
end = st.selectbox("End City", list(cities.keys()))
mode = st.selectbox("Transport Mode", ["🚗 Land", "✈️ Air", "🚢 Sea"])

# -------------------------
# MAP BASE
# -------------------------
m = folium.Map(location=[24.8, 53], zoom_start=5)

# Add markers
for city, coord in cities.items():
    folium.Marker(coord, tooltip=city).add_to(m)

# -------------------------
# ROUTE
# -------------------------
if st.button("Generate Route"):
    start_coord = cities[start]
    end_coord = cities[end]

    dist = distance(start_coord, end_coord)
    time = travel_time(dist, mode)

    # Draw line
    folium.PolyLine([start_coord, end_coord], color="blue", weight=4).add_to(m)

    st_folium(m, height=600, width=700)

    st.success(f"📏 Distance: {dist:.1f} km")
    st.success(f"⏱️ Time: {time:.2f} hours")

    # SMART RULES
    if mode == "🚢 Sea" and ("Riyadh" in start or "Riyadh" in end):
        st.warning("Sea route not valid for inland cities!")
    if mode == "✈️ Air" and dist < 300:
        st.warning("Air travel not needed for short distances!")
