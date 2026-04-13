import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Simple Map App", layout="wide")

st.title("🗺️ Working Map Test")

# Qatar center
m = folium.Map(location=[25.3, 51.5], zoom_start=7, tiles="CartoDB positron")

# show map + capture click
map_data = st_folium(m, height=600, width=1000)

# handle click
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"Clicked: {lat:.5f}, {lon:.5f}")

    folium.Marker([lat, lon], tooltip="You clicked here").add_to(m)
