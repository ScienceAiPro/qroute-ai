import streamlit as st
import networkx as nx
import random

st.set_page_config(page_title="QROUTE AI", layout="wide")

st.title("🚀 QROUTE AI Logistics System")
st.subheader("Qatar Smart Transport Optimizer (Land • Air • Sea)")

# Create simple simulated graph (demo AI network)
G = nx.Graph()

nodes = ["Doha", "Al Khor", "Al Wakrah", "Ras Laffan", "Hamad Port", "HIA Airport"]

for n in nodes:
    G.add_node(n)

edges = [
    ("Doha", "Al Khor"),
    ("Doha", "Al Wakrah"),
    ("Doha", "Hamad Port"),
    ("Doha", "HIA Airport"),
    ("Al Khor", "Ras Laffan"),
    ("Al Wakrah", "Hamad Port"),
]

for e in edges:
    G.add_edge(e[0], e[1], weight=random.randint(10, 60))

st.sidebar.header("📍 Route Selector")

start = st.sidebar.selectbox("Start Location", nodes)
end = st.sidebar.selectbox("End Location", nodes)

transport = st.sidebar.radio("Transport Mode", ["🚗 Land", "✈️ Air", "🚢 Sea"])

if st.sidebar.button("Find Best AI Route"):

    try:
        path = nx.shortest_path(G, start, end, weight="weight")
        distance = nx.shortest_path_length(G, start, end, weight="weight")

        # AI simulation factors
        traffic = random.randint(1, 30)
        weather_delay = random.randint(0, 20)

        if transport == "✈️ Air":
            speed_factor = 0.6
        elif transport == "🚢 Sea":
            speed_factor = 1.5
        else:
            speed_factor = 1.0

        time = int((distance * speed_factor) + traffic + weather_delay)

        st.success("AI Route Found 🚀")

        st.write("### 🧭 Best Route:")
        st.write(" → ".join(path))

        st.write("### 📊 AI Analysis")
        st.write(f"Distance Score: {distance}")
        st.write(f"Traffic Delay: {traffic} min")
        st.write(f"Weather Impact: {weather_delay} min")
        st.write(f"Estimated Time: {time} minutes")

        st.info(f"Transport Mode: {transport}")

    except:
        st.error("No route found between selected locations")
