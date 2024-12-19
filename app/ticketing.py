import streamlit as st
import json
import os
import uuid
import pandas as pd
from io import StringIO
import requests

TICKET_FILE = 'tickets.json'

# Helper functions to read and write tickets to the JSON file
def read_tickets():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def write_tickets(tickets):
    with open(TICKET_FILE, 'w') as file:
        json.dump(tickets, file, indent=4)

def create_ticket(issue_type, severity, description, solution, priority):
    tickets = read_tickets()
    ticket_id = str(uuid.uuid4())  # Generate a unique ticket ID
    ticket = {
        "ticket_id": ticket_id,
        "issue_type": issue_type,
        "severity": severity,
        "description": description,
        "solution": solution,
        "priority": priority,
        "timestamp": pd.to_datetime("now").strftime("%Y-%m-%dT%H:%M:%S")
    }
    tickets.append(ticket)
    write_tickets(tickets)

def app():
    st.title("Ticketing System")

    # File Upload for Telemetry Data
    uploaded_file = st.file_uploader("Upload Telemetry Data (CSV or JSON)", type=["csv", "json"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            telemetry_data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            telemetry_data = pd.read_json(uploaded_file)
        
        st.write("### Telemetry Data Preview:")
        st.write(telemetry_data.head())

        # Call FastAPI to get issue type, severity, and description (this is where you would connect to the FastAPI model)
        # For now, we'll assume some dummy values returned by FastAPI for illustration purposes.
        if 'Timestamp' in telemetry_data.columns:
            telemetry_data['Timestamp'] = pd.to_datetime(telemetry_data['Timestamp'])
        
        issue_type = "Network Failure"  # Example, would be returned by FastAPI
        severity = "Critical"  # Example, would be returned by FastAPI
        description = "Router failure detected in data center."  # Example, would be returned by FastAPI
        solution = "Replace the router."  # Example, would be returned by FastAPI
        priority = "High"  # Example, would be returned by FastAPI
        
        # Display the detected issue
        st.write("### Detected Issue Information:")
        st.write(f"Issue Type: {issue_type}")
        st.write(f"Severity: {severity}")
        st.write(f"Description: {description}")
        st.write(f"Proposed Solution: {solution}")

        # Button to create ticket
        if st.button("Create Ticket"):
            create_ticket(issue_type, severity, description, solution, priority)
            st.success("Ticket created successfully!")

    # Display the existing tickets
    st.write("### Existing Tickets")
    tickets = read_tickets()
    if tickets:
        for ticket in tickets:
            st.write(f"Ticket ID: {ticket['ticket_id']}")
            st.write(f"Issue Type: {ticket['issue_type']}")
            st.write(f"Severity: {ticket['severity']}")
            st.write(f"Description: {ticket['description']}")
            st.write(f"Solution: {ticket['solution']}")
            st.write(f"Priority: {ticket['priority']}")
            st.write(f"Timestamp: {ticket['timestamp']}")
            st.write("---")
    else:
        st.write("No tickets raised yet.")
