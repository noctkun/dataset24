import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

def app():
    st.title("Data Analysis")

    # Load data from a file
    telemetry_data = pd.read_csv('data.csv')

    # Normalize column names
    telemetry_data.columns = telemetry_data.columns.str.strip().str.lower()

    # Check for required columns
    if 'timestamp' not in telemetry_data.columns or 'error_code' not in telemetry_data.columns:
        st.error("The dataset must contain 'timestamp' and 'error_code' columns.")
        return

    # Convert 'timestamp' to datetime
    telemetry_data['timestamp'] = pd.to_datetime(telemetry_data['timestamp'])

    # Sort data by timestamp
    telemetry_data = telemetry_data.sort_values(by='timestamp')

    # Create an error indicator (1 for error, 0 for no error)
    telemetry_data['is_error'] = telemetry_data['error_code'].apply(lambda x: 0 if x == 'OK00' else 1)

    # Plot time series of error_code with highlights for errors
    st.subheader("Time Series Visualization")
    plt.figure(figsize=(12, 6))

    plt.plot(telemetry_data['timestamp'], telemetry_data['is_error'], label='Error Indicator', color='blue')

    # Highlight error points
    error_data = telemetry_data[telemetry_data['is_error'] == 1]
    plt.scatter(error_data['timestamp'], error_data['is_error'], color='red', label='Error', zorder=5)

    plt.title('Time Series of Errors')
    plt.xlabel('Timestamp')
    plt.ylabel('Error Indicator')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Seasonal decomposition
    st.subheader("Seasonal Decomposition")
    telemetry_data.set_index('timestamp', inplace=True)
    telemetry_data = telemetry_data.asfreq('H')  # Resample to hourly frequency

    # Fill missing values for decomposition
    telemetry_data['is_error'].fillna(0, inplace=True)
    decomposition = seasonal_decompose(telemetry_data['is_error'], model='additive', period=24)

    # Plot decomposed components
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8))
    decomposition.observed.plot(ax=ax1, title='Observed', color='blue')
    decomposition.trend.plot(ax=ax2, title='Trend', color='orange')
    decomposition.seasonal.plot(ax=ax3, title='Seasonal', color='green')
    decomposition.resid.plot(ax=ax4, title='Residual', color='red')

    fig.tight_layout()
    st.pyplot(fig)

    # Heatmap of error patterns
    st.subheader("Heatmap of Error Patterns")
    telemetry_data['hour'] = telemetry_data.index.hour
    telemetry_data['day'] = telemetry_data.index.dayofweek

    # Pivot data for heatmap
    heatmap_data = telemetry_data.pivot_table(values='is_error', index='day', columns='hour', aggfunc='sum')

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='g')
    plt.title('Heatmap of Error Patterns')
    st.pyplot(plt)

if __name__ == "__main__":
    app()
