import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# Generate a simulated large dictionary (you can replace this with your own dictionary)
stock_data = {
    'INFOSYS': (
        pd.date_range(start="2025-01-27 04:00:00", periods=2170, freq='T'),
        np.random.rand(2170, 2)  # Simulate some random data
    )
}

# Extract datetime and target/comprehensive RRR data
datetime_data = stock_data['INFOSYS'][0]
target_data = stock_data['INFOSYS'][1][:, 0]  # Target: Percentage Change
comprehensive_rrr_data = stock_data['INFOSYS'][1][:, 1]  # Comprehensive RRR

# Initialize Streamlit layout
st.title('Real-Time Stock Data Plot')
st.write("This is a streaming plot showing the percentage change (Target) and comprehensive RRR over time.")

# Create a figure for interactive plotting
fig = go.Figure()

# Plotly trace for Target and Comprehensive RRR
fig.add_trace(go.Scatter(
    x=[],
    y=[],
    mode='lines',
    name='Target (Percentage Change)',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=[],
    y=[],
    mode='lines',
    name='Comprehensive RRR',
    line=dict(color='red')
))

# Configure plot layout
fig.update_layout(
    title='Real-Time Data Streaming',
    xaxis_title='Time',
    yaxis_title='Value',
    xaxis=dict(type='date'),
    showlegend=True
)

# Create a placeholder to update the chart
chart_placeholder = st.empty()

# Stream data to the plot with a 1-second delay
i = 0
while i < len(datetime_data):
    # Update the traces with new data
    fig.data[0].x = datetime_data[:i+1]
    fig.data[0].y = target_data[:i+1]
    fig.data[1].x = datetime_data[:i+1]
    fig.data[1].y = comprehensive_rrr_data[:i+1]
    
    # Update the existing plot in the placeholder
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Simulate a 1-second delay for real-time streaming effect
    time.sleep(1)
    
    # Increment i for next iteration
    i += 1  # Update every second (each point represents 1 minute)
