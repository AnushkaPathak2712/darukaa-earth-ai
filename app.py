import streamlit as st
import requests

st.set_page_config(page_title="Darukaa Earth AI", layout="wide")
st.title("🌍 Darukaa.Earth AI Biodiversity Intelligence")


BACKEND_URL = "https://darukaa-earth-ai-ms98.onrender.com" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user1"

with st.sidebar:
    st.header("📊 Structured Environmental Data")
    st.write("Provide numerical data for multi-metric reasoning.")
    
    region = st.text_input("Region", "semi-arid")
    soil_ph = st.number_input("Soil pH", 0.0, 14.0, 8.1)
    organic_carbon = st.number_input("Organic Carbon %", 0.0, 10.0, 0.8)
    rainfall = st.number_input("Rainfall (mm/year)", 0.0, 5000.0, 450.0)
    land_use = st.text_input("Land Use", "wheat monoculture")
    species_richness = st.number_input("Species Richness", 0, 1000, 12)
    pollution = st.selectbox("Pollution Level", ["low", "medium", "high"], index=2)
    moisture = st.selectbox("Soil Moisture", ["low", "medium", "high"], index=0)
    habitat = st.selectbox("Habitat Diversity", ["low", "medium", "high"], index=0)
    
    if st.button("Send Structured Data"):
        structured = {
            "region": region,
            "soil_ph": soil_ph,
            "organic_carbon_pct": organic_carbon,
            "rainfall_mm": rainfall,
            "land_use": land_use,
            "species_richness": species_richness,
            "pollution_level": pollution,
            "moisture": moisture,
            "habitat_diversity": habitat
        }
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={
                "user_id": st.session_state.user_id,
                "message": "Here is my structured environmental data.",
                "structured_data": structured
            })
            response.raise_for_status()
            st.session_state.messages.append({"role": "assistant", "content": response.json()["response"]})
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Describe your land or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        response = requests.post(f"{BACKEND_URL}/chat", json={
            "user_id": st.session_state.user_id,
            "message": prompt
        })
        response.raise_for_status()
        answer = response.json()["response"]
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")