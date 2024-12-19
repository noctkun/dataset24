# /app/dashboard.py

import streamlit as st
import json
import os

TICKET_FILE = 'tickets.json'

# Helper functions to read tickets from the JSON file
def read_tickets():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def priority_color(priority):
    """Assign colors based on priority."""
    if priority == "High":
        return "red"
    elif priority == "Medium":
        return "orange"
    elif priority == "Low":
        return "green"
    else:
        return "gray"

def app():
    st.title("Dashboard - Tickets Overview")

    tickets = read_tickets()

    if tickets:
        for ticket in tickets:
            priority = ticket['priority']
            color = priority_color(priority)

            # Ticket preview with severity color outside of the expander
            with st.container():
                col1, col2 = st.columns([1, 5])
                
                with col1:
                    # Display the color block for priority
                    st.markdown(f"<div style='width: 20px; height: 20px; background-color: {color}; border-radius: 50%;'></div>", unsafe_allow_html=True)
                
                with col2:
                    # Display the brief preview of the ticket
                    st.markdown(f"**{ticket['issue_type']}** - **{ticket['severity']}**")
                    st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Timestamp:** {ticket['timestamp']}")
                    
                    # Expandable section with full details inside
                    with st.expander("Click to expand for full details"):
                        st.write(f"**Description:** {ticket['description']}")
                        st.write(f"**Solution:** {ticket['solution']}")
                        st.write(f"**Priority:** {ticket['priority']}")
                        st.write(f"**Timestamp:** {ticket['timestamp']}")

    else:
        st.write("No tickets raised yet.")
