import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.set_page_config(page_title="GCC AI Logistics System", layout="wide")

st.title("🌍 GCC AI Logistics AI System (Qatar + UAE + Saudi)")

st.markdown("Interactive map + real distance + metro pricing + smart routing")

# -----------------------------
# 🌍 FULL REGIONAL DATA
# -----------------------------
locations = {
    # 🇶🇦 QATAR
    "Doha": (25.2854, 51.5310),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Lusail": (25.4207, 51.4905),
    "Mesaieed": (24.9923, 51.5519),
    "Ras Laffan": (25.8904, 51.5489),
    "Dukhan": (25.4242, 50.7827),
    "Hamad Airport": (25.2731, 51.6081),
    "The Pearl": (25.3694, 51.5486),
    "Industrial Area": (25.1390, 51.5370),

    # 🚇 DOHA METRO
    "Msheireb Metro": (25.2855, 51.5330),
    "DECC Metro": (25.3269, 51.5310),
    "West Bay Metro": (25.3239, 51.5273),
    "Qatar University Metro": (25.3743, 51.4876),
    "Education City Metro": (25.3139, 51.4382),

    # 🇦🇪 UAE
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),
    "Sharjah": (25.3463, 55.4209),

    # 🇸🇦 SAUDI ARABIA
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
    "Dammam": (26.4207, 50.0888),
    "Mecca": (21.3891, 39.8579),
}

# -----------------------------
# REAL DISTANCE (HAVERSINE)
# -----------------------------
def distance(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# -----------------------------
# METRO PRICE (REALISTIC QATAR STYLE)
# -----------------------------
def metro_price(dist):
    if dist <= 10:
        return 2
    elif dist <= 25:
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
# UI (INTERACTIVE FEEL)
# -----------------------------
st.sidebar.header("🧭 Smart Controls")

start = st.sidebar.selectbox("Start Location", list(locations.keys()))
end = st.sidebar.selectbox("End Location", list(locations.keys()))

mode = st.sidebar.selectbox(
    "Transport Mode",
    ["🤖 Auto AI", "🚗 Car", "🚇 Metro", "✈️ Air"]
)

run = st.button("🚀 Generate Smart Route")

# -----------------------------
# MAP (NO SESSION STATE = NO BUGS)
# -----------------------------
m = folium.Map(location=[25.2, 51.3], zoom_start=6)

# Add markers
for name, coord in locations.items():
    folium.Marker(coord, tooltip=name).add_to(m)

# -----------------------------
# MAIN ENGINE
# -----------------------------
if run:

    a = locations[start]
    b = locations[end]

    dist = distance(a, b)

    # AI MODE SELECT
    if mode == "🤖 Auto AI":
        if dist < 8:
            mode = "🚇 Metro"
        elif dist < 80:
            mode = "🚗 Car"
        else:
            mode = "✈️ Air"

    time = travel_time(dist, mode)
    price = metro_price(dist) if mode == "🚇 Metro" else 0

    # route line
    folium.PolyLine([a, b], color="blue", weight=5).add_to(m)

    # show map
    st_folium(m, height=700, width=1100)

    # -----------------------------
    # CALCULATIONS PANEL (VISIBLE ALWAYS)
    # -----------------------------
    st.subheader("📊 AI LOGISTICS CALCULATION PANEL")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Distance (km)", f"{dist:.2f}")

    with col2:
        st.metric("Mode", mode)

    with col3:
        st.metric("Time (hrs)", f"{time:.2f}")

    st.write("### 💰 Cost System")
    if mode == "🚇 Metro":
        st.success(f"Metro Ticket Price: {price} QAR")
    elif mode == "🚗 Car":
        st.info("Fuel cost estimated: 10–25 QAR (simulation)")
    else:
        st.info("Air cost: High (simulation)")

    st.write("### 🌍 AI Insight")

    if dist > 500:
        st.warning("Very long distance → Air recommended ✈️")

    if mode == "🚇 Metro" and dist > 30:
        st.warning("Metro not efficient for long distance")

else:
    st_folium(m, height=700, width=1100)
