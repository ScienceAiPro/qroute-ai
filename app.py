import streamlit as st
import folium
from streamlit_folium import st_folium
import math
from datetime import datetime

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(page_title="AI Logistics Map PRO", layout="wide")

st.title("🌍 AI Logistics Map PRO (Interactive + Smart Routing)")
st.markdown("Click START → Click END → AI generates route")

# =====================================================
# SESSION STATE
# =====================================================
if "start" not in st.session_state:
    st.session_state.start = None

if "end" not in st.session_state:
    st.session_state.end = None

if "route_ready" not in st.session_state:
    st.session_state.route_ready = False

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# LOCATIONS (QATAR + GCC + METRO + CITIES)
# =====================================================
locations = {
    # Qatar main
    "Doha": (25.2854, 51.5310),
    "Lusail": (25.4207, 51.4905),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Hamad Airport": (25.2731, 51.6081),

    # Metro stations (sample expanded)
    "Msheireb": (25.2855, 51.5330),
    "West Bay": (25.3239, 51.5273),
    "Katara": (25.3548, 51.5247),
    "Qatar University": (25.3743, 51.4876),
    "Education City": (25.3139, 51.4382),
    "Souq Waqif": (25.2860, 51.5336),

    # UAE
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),

    # Saudi
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
}

# =====================================================
# DISTANCE FUNCTION (REAL EARTH MATH)
# =====================================================
def distance_km(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# =====================================================
# AI ENGINE (SMART LOGIC)
# =====================================================
def ai_engine(d):
    car = d / 90
    metro = (d / 60) + 0.2
    air = d / 850

    scores = {
        "🚗 Car": car,
        "🚇 Metro": metro,
        "✈️ Air": air
    }

    best = min(scores, key=scores.get)
    return best, scores

# =====================================================
# METRO COST
# =====================================================
def metro_cost(d):
    if d < 10:
        return 2
    elif d < 25:
        return 4
    return 6

# =====================================================
# RESET
# =====================================================
if st.button("🔄 Reset"):
    st.session_state.start = None
    st.session_state.end = None
    st.session_state.route_ready = False
    st.rerun()

# =====================================================
# SIDEBAR CONTROLS
# =====================================================
st.sidebar.header("Controls")

start = st.sidebar.selectbox("Start", list(locations.keys()))
end = st.sidebar.selectbox("End", list(locations.keys()))

if st.sidebar.button("📍 Set Route"):
    st.session_state.start = start
    st.session_state.end = end
    st.session_state.route_ready = True

# =====================================================
# MAP STYLE (THIS FIXES YOUR “BORING MAP” ISSUE)
# =====================================================
base_map = folium.Map(
    location=[25.3, 51.3],
    zoom_start=6,
    tiles="CartoDB dark_matter"   # 🔥 BEST LOOKING STYLE
)

# =====================================================
# CLICK SYSTEM (OPTIONAL INTERACTION)
# =====================================================
map_data = st_folium(base_map, height=650, width=1100)

clicked = map_data.get("last_clicked")

if clicked:
    lat = clicked["lat"]
    lon = clicked["lng"]

    if st.session_state.start is None:
        st.session_state.start = (lat, lon)
        st.success("START selected")

    elif st.session_state.end is None:
        st.session_state.end = (lat, lon)
        st.success("END selected")

# =====================================================
# ROUTE GENERATION (ONLY WHEN READY)
# =====================================================
if st.session_state.start and st.session_state.end:

    a = st.session_state.start
    b = st.session_state.end

    d = distance_km(a, b)

    mode, scores = ai_engine(d)

    route_map = folium.Map(
        location=[(a[0]+b[0])/2, (a[1]+b[1])/2],
        zoom_start=6,
        tiles="CartoDB dark_matter"
    )

    # route line
    folium.PolyLine([a, b], color="purple", weight=6).add_to(route_map)

    # markers
    folium.Marker(a, tooltip="START").add_to(route_map)
    folium.Marker(b, tooltip="END").add_to(route_map)

    # distance label ON MAP
    mid = [(a[0]+b[0])/2, (a[1]+b[1])/2]

    folium.Marker(
        mid,
        icon=folium.DivIcon(html=f"""
        <div style="
            background: black;
            color: white;
            padding: 6px;
            border-radius: 6px;
            font-size: 14px;
        ">
        {d:.2f} km
        </div>
        """)
    ).add_to(route_map)

    st_folium(route_map, height=650, width=1100)

    # =================================================
    # AI OUTPUT
    # =================================================
    st.subheader("🤖 AI ANALYSIS")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Distance", f"{d:.2f} km")

    with col2:
        st.metric("Best Mode", mode)

    with col3:
        st.metric("Metro Cost", f"{metro_cost(d)} QAR")

    st.write("### AI Scores")
    st.json(scores)

    # history
    st.session_state.history.append({
        "time": str(datetime.now()),
        "start": str(st.session_state.start),
        "end": str(st.session_state.end),
        "distance": d,
        "mode": mode
    })

    st.write("### Recent Routes")
    st.write(st.session_state.history[-5:])

else:
    st.info("👉 Select START and END then click Set Route or click map points")
