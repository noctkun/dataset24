import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys
from threading import Thread
import uvicorn

# Importing the pages
import dashboard
import ticketing
import rca
import support
import analysis

# Function to start FastAPI server (for Ticketing)
def start_fastapi():
    os.environ['PYTHONPATH'] = os.getcwd()  # Ensures FastAPI can be found
    from ticketing import app as fastapi_app  # Import FastAPI app from ticketing.py
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)  # Run FastAPI server

# Start FastAPI server in a background thread when Ticketing is selected
def start_fastapi_thread():
    thread = Thread(target=start_fastapi, daemon=True)
    thread.start()

# Sidebar Navbar
with st.sidebar:
    selected = option_menu("NOC Helper App", 
        ["Dashboard", "Ticketing", "Analysis", "RCA", "Support"],
        icons=['house', 'ticket', 'search', 'question-circle'],
        menu_icon="cast", default_index=0)

if selected == "Dashboard":
    dashboard.app()
elif selected == "Ticketing":
    start_fastapi_thread()  # Start FastAPI when Ticketing page is selected
    ticketing.app()
elif selected == "Analysis":
    analysis.app()
elif selected == "RCA":
    rca.app()
elif selected == "Support":
    support.app()
