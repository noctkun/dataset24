import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_network_telemetry(start_date, num_records, interval_minutes=15):
    """
    Generate network telemetry data with time series patterns.
    
    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format
    num_records (int): Number of records to generate
    interval_minutes (int): Time interval between records in minutes
    
    Returns:
    pandas.DataFrame: Generated telemetry data
    """
    
    # Define error types and their messages
    error_types = {
        'E001': 'High CPU utilization detected',
        'E002': 'Memory usage exceeded threshold',
        'E003': 'Network connectivity issues',
        'E004': 'Packet loss detected',
        'E005': 'Authentication failure',
        'OK00': 'System operating within normal parameters'
    }
    
    # Define source devices
    devices = ['router-01', 'switch-02', 'firewall-03', 'gateway-04', 'load-balancer-05']
    
    # Generate timestamps
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    timestamps = [start_datetime + timedelta(minutes=i*interval_minutes) 
                 for i in range(num_records)]
    
    # Initialize lists for data
    data = []
    
    # Generate records
    for timestamp in timestamps:
        # Create patterns: More errors during peak hours (9 AM - 5 PM)
        hour = timestamp.hour
        is_peak_hour = 9 <= hour <= 17
        
        # During peak hours, higher chance of errors
        error_chance = 0.4 if is_peak_hour else 0.2
        has_error = random.random() < error_chance
        
        # Select error code and message
        if has_error:
            error_code = random.choice(['E001', 'E002', 'E003', 'E004', 'E005'])
        else:
            error_code = 'OK00'
            
        # Select random device
        device = random.choice(devices)
        
        # Add record
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'error_code': error_code,
            'source_device': device,
            'log_message': error_types[error_code]
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Generate data
if __name__ == "__main__":
    # Parameters
    START_DATE = '2024-01-01'
    NUM_RECORDS = 1000
    INTERVAL_MINUTES = 15
    OUTPUT_FILE = 'network_telemetry.csv'
    
    # Generate telemetry data
    telemetry_data = generate_network_telemetry(
        start_date=START_DATE,
        num_records=NUM_RECORDS,
        interval_minutes=INTERVAL_MINUTES
    )
    
    # Save to CSV
    telemetry_data.to_csv(OUTPUT_FILE, index=False)
    print(f"Generated {NUM_RECORDS} records and saved to {OUTPUT_FILE}")
    
    # Display first few records
    print("\nFirst few records:")
    print(telemetry_data.head())