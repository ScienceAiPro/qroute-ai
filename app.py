import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.set_page_config(page_title="Working Map", layout="wide")

st.title("🌍 Interactive Map (Stable Version)")
st.write("Click once = START, click again = END")

# -----------------------------
# SESSION STATE
# -----------------------------
if "start" not in st.session_state:
    st.session_state.start = None

if "end" not in st.session_state:
    st.session_state.end = None

# -----------------------------
# DISTANCE FUNCTION
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
# CREATE MAP (ALWAYS FRESH)
# -----------------------------
m = folium.Map(location=[25.3, 51.5], zoom_start=7, tiles="OpenStreetMap")

# -----------------------------
# DRAW EXISTING POINTS
# -----------------------------
if st.session_state.start:
    folium.Marker(st.session_state.start, tooltip="START", icon=folium.Icon(color="green")).add_to(m)

if st.session_state.end:
    folium.Marker(st.session_state.end, tooltip="END", icon=folium.Icon(color="red")).add_to(m)

# -----------------------------
# DRAW ROUTE
# -----------------------------
if st.session_state.start and st.session_state.end:
    folium.PolyLine([st.session_state.start, st.session_state.end], color="blue", weight=5).add_to(m)

    dist = haversine(st.session_state.start, st.session_state.end)
    st.success(f"Distance: {dist:.2f} km")

# -----------------------------
# RENDER MAP (IMPORTANT LINE)
# -----------------------------
map_data = st_folium(m, height=650, width=1000, key="map")

# -----------------------------
# CLICK HANDLER
# -----------------------------
clicked = map_data.get("last_clicked")

if clicked:
    lat = clicked["lat"]
    lon = clicked["lng"]

    # first click = start
    if st.session_state.start is None:
        st.session_state.start = (lat, lon)
        st.rerun()

    # second click = end
    elif st.session_state.end is None:
        st.session_state.end = (lat, lon)
        st.rerun()

# -----------------------------
# DEBUG (IMPORTANT)
# -----------------------------
st.write("Debug click data:", clicked)
