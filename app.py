import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="CLICK TEST", layout="wide")

st.title("🧪 Click Test Map")

st.write("Click anywhere on the map and check below 👇")

# create map
m = folium.Map(location=[25.3, 51.5], zoom_start=7)

# render map
output = st_folium(m, height=600, width=900, key="test_map")

# show raw output (IMPORTANT DEBUG)
st.subheader("Debug Output")
st.json(output)

# check click
if output and output.get("last_clicked"):
    st.success("CLICK WORKING ✅")

    st.write("Lat:", output["last_clicked"]["lat"])
    st.write("Lng:", output["last_clicked"]["lng"])
else:
    st.error("NO CLICK DETECTED ❌")
