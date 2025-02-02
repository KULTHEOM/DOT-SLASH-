import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from datetime import datetime

# Function to display sentiment data for a given ticker
def display_sentiment_data(ticker, time_index):
    folder_path = 'sentiment_data_csv'
    
    # Get all CSV files in the directory that match the ticker
    files = [f for f in os.listdir(folder_path) if f.endswith(f'{ticker}.csv')]
    
    if not files:
        return f"No sentiment data found for ticker: {ticker}"
    
    # For now, we'll display the first matching file (you can show all if needed)
    file_path = os.path.join(folder_path, files[0])
    sentiment_df = pd.read_csv(file_path)
    
    # Select news corresponding to the time interval
    news_at_time = sentiment_df.iloc[time_index:time_index+1]  # Adjust to display news for the interval
    
    # Prepare news content for display
    news_content = ""
    for _, row in news_at_time.iterrows():
        description = row['Description']
        sentiment = row['Sentiment']
        
        # Custom box style for displaying news with better text color
        news_content += f"""
            <div style="background-color:#f1f1f1; padding:10px; border-radius:5px; border:1px solid #ccc;">
                <p style="color:#333;"><strong>News:</strong> {description}</p>
                <p style="color:#333;"><strong>Sentiment:</strong> {sentiment}</p>
            </div>
        """
    
    return news_content

# Generate a simulated large dictionary (replace with actual data as needed)
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
st.set_page_config(layout="wide")  # Set wide layout

# Current date display at the top of the app
current_date = datetime.now().strftime("%A, %B %d, %Y, %I %p IST")
st.markdown(f"<h5 style='text-align: right; color: gray;'>{current_date}</h5>", unsafe_allow_html=True)

# Create a sidebar for user inputs
st.sidebar.header('Stock Query')
ticker_input = st.sidebar.text_input("Enter Stock Ticker", "INFOSYS")
st.sidebar.write("This tool displays real-time stock data and sentiment analysis.")

# Initialize variables for news and plot
news_placeholder = st.empty()
chart_placeholder = st.empty()

# Stream data to the plot with a 1-second delay (real-time effect)
i = 0
time_interval = 0  # To keep track of news updates (every 1 minute)

while i < len(datetime_data):
    # Update the traces with new data for the plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=datetime_data[:i+1],
        y=target_data[:i+1],
        mode='lines',
        name='Target (Percentage Change)',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=datetime_data[:i+1],
        y=comprehensive_rrr_data[:i+1],
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
    
    # Display news above the header every minute
    if i % 60 == 0:  # Update news every 1 minute
        if ticker_input:
            news_content = display_sentiment_data(ticker_input.upper(), time_interval)  # Show news for the current interval
            
            if news_content:
                news_placeholder.markdown(news_content, unsafe_allow_html=True)
            time_interval += 1  # Increment for the next news update

    # Display the updated plot below the news content
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Simulate a 1-second delay for real-time streaming effect
    time.sleep(1)
    
    # Increment i for next iteration
    i += 1  # Update every second (each point represents 1 minute)
