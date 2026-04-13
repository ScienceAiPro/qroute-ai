import streamlit as st
import folium
from streamlit_folium import st_folium
import math
from datetime import datetime

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(page_title="GCC AI Logistics PRO", layout="wide")

st.title("🌍 GCC AI Logistics PRO SYSTEM (STABLE EDITION)")
st.markdown("Click map → select points → generate AI route")

# =====================================================
# SESSION STATE
# =====================================================
if "start" not in st.session_state:
    st.session_state.start = None

if "end" not in st.session_state:
    st.session_state.end = None

if "logs" not in st.session_state:
    st.session_state.logs = []

# =====================================================
# FULL NETWORK (QATAR + GCC + METRO)
# =====================================================
locations = {

    # ---------------- QATAR MAIN ----------------
    "Doha": (25.2854, 51.5310),
    "Lusail": (25.4207, 51.4905),
    "Al Wakrah": (25.1659, 51.5970),
    "Al Khor": (25.6804, 51.4966),
    "Hamad Airport": (25.2731, 51.6081),
    "Mesaieed": (24.9923, 51.5519),

    # ---------------- DOHA METRO RED ----------------
    "Msheireb": (25.2855, 51.5330),
    "DECC": (25.3269, 51.5310),
    "West Bay": (25.3239, 51.5273),
    "Katara": (25.3548, 51.5247),
    "Qatar University": (25.3743, 51.4876),
    "Legtaifiya": (25.3610, 51.4970),
    "Free Zone": (25.2340, 51.5600),
    "Ras Bu Fontas": (25.2050, 51.5750),

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

# =====================================================
# DISTANCE ENGINE (REAL EARTH MATH)
# =====================================================
def haversine(a, b):
    R = 6371
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))

    return R * c

# =====================================================
# AI ENGINE (REAL SCORING SYSTEM)
# =====================================================
def ai_engine(distance):
    # lower score = better option
    car_score = distance / 90
    metro_score = (distance / 60) + 0.3
    air_score = distance / 850

    scores = {
        "🚗 Car": car_score,
        "🚇 Metro": metro_score,
        "✈️ Air": air_score
    }

    best = min(scores, key=scores.get)
    return best, scores

# =====================================================
# METRO COST SYSTEM
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
if st.button("🔄 Reset System"):
    st.session_state.start = None
    st.session_state.end = None
    st.rerun()

# =====================================================
# MAP BASE (ALWAYS STABLE)
# =====================================================
base_map = folium.Map(location=[25.3, 51.3], zoom_start=6)

# only show markers AFTER route exists
show_markers = st.session_state.start and st.session_state.end

if show_markers:
    for name, coord in locations.items():
        folium.Marker(coord, tooltip=name).add_to(base_map)

# =====================================================
# CLICK SYSTEM
# =====================================================
map_data = st_folium(base_map, height=650, width=1100)
clicked = map_data.get("last_clicked")

if clicked:

    point = (clicked["lat"], clicked["lng"])

    if st.session_state.start is None:
        st.session_state.start = point
        st.info("START selected")

    elif st.session_state.end is None:
        st.session_state.end = point
        st.success("END selected")

# =====================================================
# ROUTE ENGINE (ONLY WHEN READY)
# =====================================================
if st.session_state.start and st.session_state.end:

    a = st.session_state.start
    b = st.session_state.end

    dist = haversine(a, b)

    best_mode, scores = ai_engine(dist)

    route_map = folium.Map(location=[(a[0]+b[0])/2, (a[1]+b[1])/2], zoom_start=6)

    folium.PolyLine([a, b], color="purple", weight=6).add_to(route_map)

    folium.Marker(a, popup="START").add_to(route_map)
    folium.Marker(b, popup="END").add_to(route_map)

    # distance label on map
    mid = [(a[0]+b[0])/2, (a[1]+b[1])/2]

    folium.Marker(
        mid,
        icon=folium.DivIcon(html=f"""
        <div style="background:black;color:white;padding:6px;border-radius:6px">
        {dist:.2f} km
        </div>
        """)
    ).add_to(route_map)

    st_folium(route_map, height=650, width=1100)

    # =================================================
    # AI OUTPUT PANEL (ALWAYS VISIBLE)
    # =================================================
    st.subheader("🤖 AI ROUTE ENGINE")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Distance", f"{dist:.2f} km")

    with col2:
        st.metric("Best Mode", best_mode)

    with col3:
        st.metric("Metro Cost", f"{metro_cost(dist)} QAR")

    st.write("### AI Scores")
    st.json(scores)

    # =================================================
    # HISTORY
    # =================================================
    st.session_state.logs.append({
        "time": str(datetime.now()),
        "distance": dist,
        "mode": best_mode
    })

    st.write("### Recent Routes")
    st.write(st.session_state.logs[-5:])

else:
    st.info("Click START and END points to generate route")
