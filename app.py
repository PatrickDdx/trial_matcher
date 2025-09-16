from logging import exception

import streamlit as st
import asyncio

from app_logic import run_pipeline
from apis.maps import place_to_coordinates

from dotenv import load_dotenv

st.set_page_config(
    page_title="Trial Matcher",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Initialize the session state variable for the output text area.
if "output_display" not in st.session_state:
    st.session_state.output_display = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "location" not in st.session_state:
    st.session_state.location = "Germany" # Default value
if "geo" not in st.session_state:
    st.session_state.geo = None
if "distance" not in st.session_state:
    st.session_state.distance = None

# 2. Define the async callback function to handle the entire pipeline.
async def on_submit():
    with st.spinner("Searching for trials..."):
        # The run_pipeline function is awaited directly inside this async function.
        result = await run_pipeline(message_desc=st.session_state.user_input, region=st.session_state.location, geo=st.session_state.geo, distance=st.session_state.distance)
        final_output_text = "\n".join(result)
        # Update the session state directly.
        st.session_state.output_display = final_output_text

# 3. Create a synchronous wrapper to run the async callback.
def run_async_callback():

    address, lat, lon = place_to_coordinates(st.session_state.location)
    st.session_state.geo = (lat, lon)
    print(st.session_state.geo)
    st.session_state.location = address
    try:
        print("Searching for trials...")
        asyncio.run(on_submit())
    except Exception as e:
        st.error(f"An error occurred: {e}")

with st.container():
    # 4. Use keys to bind widget values to session state.
    st.text_area(label="Describe the Patient", placeholder="placeholder", key="user_input")
    st.text_input(label="Location", placeholder="Type an address, country or location", key="location")
    st.selectbox(label="Distance", options=["50km", "100km", "150km", "200km", "500km", "no restriction"], key="distance")

    # 5. Connect the button to the synchronous wrapper function.
    st.button("Submit", on_click=run_async_callback)

# 6. Create the output text area, linked by key to the session state.
st.text_area(
    label="Trials",
    key="output_display",
    placeholder="A ranked list of trials will appear here...",
    height=400
)