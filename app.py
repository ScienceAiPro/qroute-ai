import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("TEST MAP")

m = folium.Map(location=[25.3, 51.5], zoom_start=7)

map_data = st_folium(m, height=600, width=900)

st.write(map_data)
