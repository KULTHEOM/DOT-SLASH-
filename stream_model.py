# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import time
# import os
# from datetime import datetime

# # Function to display sentiment data for a given ticker
# def display_sentiment_data(ticker, time_index):
#     folder_path = 'sentiment_data_csv'
    
#     # Get all CSV files in the directory that match the ticker
#     files = [f for f in os.listdir(folder_path) if f.endswith(f'{ticker}.csv')]
    
#     if not files:
#         return f"No sentiment data found for ticker: {ticker}"
    
#     # For now, we'll display the first matching file (you can show all if needed)
#     file_path = os.path.join(folder_path, files[0])
#     sentiment_df = pd.read_csv(file_path)
    
#     # Select news corresponding to the time interval
#     news_at_time = sentiment_df.iloc[time_index:time_index+1]  # Adjust to display news for the interval
    
#     # Prepare news content for display
#     news_content = ""
#     for _, row in news_at_time.iterrows():
#         description = row['Description']
#         sentiment = row['Sentiment']
        
#         # Custom box style for displaying news with better text color
#         news_content += f"""
#             <div style="background-color:#f1f1f1; padding:10px; border-radius:5px; border:1px solid #ccc;">
#                 <p style="color:#333;"><strong>News:</strong> {description}</p>
#                 <p style="color:#333;"><strong>Sentiment:</strong> {sentiment}</p>
#             </div>
#         """
    
#     return news_content
# detail = pd.read_csv(r"C:\Users\Ajay\Desktop\DOT-SLASH-\dates.csv")
# prediction_data = pd.read_csv(r"C:\Users\Ajay\Desktop\DOT-SLASH-\predictions.csv")

# # Create a dictionary to hold stock data
# stock_data = {}

# # Assuming we have a known stock ticker for demonstration; you can modify this as needed
# ticker = 'INFOSYS'  # This can be any stock symbol you choose

# # Create a date range from the dates CSV
# date_range = pd.to_datetime(detail['Datetime'])

# # Convert prediction data to a NumPy array
# predictions_array = prediction_data.to_numpy()

# # Store in the dictionary
# stock_data[ticker] = (date_range, predictions_array)

# # Extract datetime and target/comprehensive RRR data
# datetime_data = stock_data['INFOSYS'][0]
# target_data = stock_data['INFOSYS'][1][:, 0]  # Target: Percentage Change
# comprehensive_rrr_data = stock_data['INFOSYS'][1][:, 1]  # Comprehensive RRR

# # Initialize Streamlit layout
# st.set_page_config(layout="wide")  # Set wide layout

# # Fixed date display at the top of the app (January 31, 2025)
# fixed_date = "Saturday, January 31, 2025"
# st.markdown(f"<h5 style='text-align: right; color: gray;'>{fixed_date}</h5>", unsafe_allow_html=True)

# # Create a sidebar for user inputs
# st.sidebar.header('Stock Query')
# ticker_input = st.sidebar.text_input("Enter Stock Ticker", "INFOSYS")
# st.sidebar.write("This tool displays real-time stock data and sentiment analysis.")

# # Initialize variables for news and plot
# news_placeholder = st.empty()
# chart_placeholder = st.empty()

# # Stream data to the plot with a 1-second delay (real-time effect)
# i = 0
# time_interval = 0  # To keep track of news updates (every 1 minute)

# while i < len(datetime_data):
#     # Update the traces with new data for the plot
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatter(
#         x=datetime_data[:i+1],
#         y=target_data[:i+1],
#         mode='lines',
#         name='Target (Percentage Change)',
#         line=dict(color='blue')
#     ))

#     fig.add_trace(go.Scatter(
#         x=datetime_data[:i+1],
#         y=comprehensive_rrr_data[:i+1],
#         mode='lines',
#         name='Comprehensive RRR',
#         line=dict(color='red')
#     ))
    
#     # Configure plot layout
#     fig.update_layout(
#         title='Real-Time Data Streaming',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         xaxis=dict(type='date'),
#         showlegend=True
#     )
    
#     # Display news above the header every minute
#     if i % 60 == 0:  # Update news every 1 minute
#         if ticker_input:
#             news_content = display_sentiment_data(ticker_input.upper(), time_interval)  # Show news for the current interval
            
#             if news_content:
#                 news_placeholder.markdown(news_content, unsafe_allow_html=True)
#             time_interval += 1  # Increment for the next news update

#     # Display the updated plot below the news content
#     chart_placeholder.plotly_chart(fig, use_container_width=True)
    
#     # Simulate a 1-second delay for real-time streaming effect
#     time.sleep(1)
    
#     # Increment i for next iteration
#     i += 1  # Update every second (each point represents 1 minute)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from datetime import datetime

# Set page configuration (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Function to calculate risk tolerance based on portfolio data
def calculate_risk_tolerance(file_path):
    # Load the CSV file
    stock_data = pd.read_csv(file_path)
    
    # Rename columns for easier access
    stock_data.columns = [col.strip() for col in stock_data.columns]

    # Define weights and biases for each stock symbol (these are arbitrary values for demonstration)
    weights = {
        'AAPL': (0.3, 0.5),   # (weight, bias)
        'GOOGL': (0.4, 0.6),
        'AMZN': (0.5, 0.7),
        'MSFT': (0.3, 0.4),
        'TSLA': (0.6, 0.8),
        'FB': (0.4, 0.5),
        'NVDA': (0.5, 0.6),
        'PYPL': (0.3, 0.4),
        'ADBE': (0.4, 0.5),
        'INTC': (0.3, 0.4)
    }

    # Initialize variables to store total weighted scores and counts
    total_weighted_score = 0
    total_count = 0

    # Calculate weighted scores based on transactions
    for index, row in stock_data.iterrows():
        stock_symbol = row['Stock Symbol']
        quantity = row['Quantity']
        
        if stock_symbol in weights:
            weight, bias = weights[stock_symbol]
            # Calculate score based on transaction
            score = weight * quantity + bias
            total_weighted_score += score
            total_count += 1

    # Determine risk tolerance level based on total weighted score
    if total_count > 0:
        average_score = total_weighted_score / total_count
        
        if average_score < 50:
            risk_tolerance = 'low'
        elif 50 <= average_score < 100:
            risk_tolerance = 'medium'
        else:
            risk_tolerance = 'high'
    else:
        risk_tolerance = 'unknown'

    return risk_tolerance

# Function to suggest trading strategy based on risk tolerance
def suggest_trading_strategy(user_risk_tolerance, folder_path):
    """
    Suggests a trading strategy based on user risk tolerance and stock data from multiple CSV files.

    Parameters:
    - user_risk_tolerance (str): The user's risk tolerance ('low', 'medium', 'high').
    - folder_path (str): The path to the folder containing CSV files with stock data.

    Returns:
    - dict: A dictionary containing the suggested trading strategy and matching CSV file names.
    """
    
    # Initialize a list to hold names of matching CSV files and their features
    matching_files_info = []

    # Loop through all CSV files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            stock_data = pd.read_csv(file_path)
            
            # Rename columns for easier access
            stock_data.columns = [col.strip() for col in stock_data.columns]  # Strip any whitespace from column names
            
            # Display the first few rows of each DataFrame for inspection (optional)
            print(f"Processing file: {filename}")
            print(stock_data.head())

            # Define trading strategy based on user risk tolerance
            if user_risk_tolerance == 'low':
                filtered_stocks = stock_data[(stock_data['%Change'].abs() < 5) & 
                                              (stock_data['RRR'] < 0.4)]
                strategy = "Long-term investment in stable stocks."
                
            elif user_risk_tolerance == 'medium':
                filtered_stocks = stock_data[(stock_data['%Change'].abs() >= 5) & 
                                              (stock_data['%Change'].abs() < 10) &
                                              (stock_data['RRR'] >= 0.4) & 
                                              (stock_data['RRR'] < 1)]
                strategy = "Balanced portfolio with a mix of growth and income stocks."
                
            elif user_risk_tolerance == 'high':
                filtered_stocks = stock_data[(stock_data['%Change'].abs() >= 10) & 
                                              (stock_data['RRR'] >= 1)]
                strategy = "Short-term trading in high-risk stocks."
                
            else:
                return {"error": "Invalid risk tolerance level. Please choose 'low', 'medium', or 'high'."}
            
            # If there are any filtered stocks, add the filename without extension to the list
            if not filtered_stocks.empty:
                matching_files_info.append({
                    "filename": os.path.splitext(filename)[0],  # Get filename without extension
                    "features": filtered_stocks[['%Change', 'RRR']].head().to_dict(orient='records')  # Get features of first few matching stocks
                })

    # Return the suggested trading strategy and matching files info
    return {
        "strategy": strategy,
        "matching_files": matching_files_info
    }

# Generate a simulated large dictionary (replace with actual data as needed)
detail = pd.read_csv(r"C:\Users\Ajay\Desktop\DOT-SLASH-\dates.csv")
prediction_data = pd.read_csv(r"C:\Users\Ajay\Desktop\DOT-SLASH-\predictions.csv")

# Create a dictionary to hold stock data
stock_data = {}

# Assuming we have a known stock ticker for demonstration; you can modify this as needed
ticker = 'INFOSYS'  # This can be any stock symbol you choose

# Create a date range from the dates CSV
date_range = pd.to_datetime(detail['Datetime'])

# Convert prediction data to a NumPy array
predictions_array = prediction_data.to_numpy()

# Store in the dictionary
stock_data[ticker] = (date_range, predictions_array)

# Extract datetime and target/comprehensive RRR data
datetime_data = stock_data['INFOSYS'][0]
target_data = stock_data['INFOSYS'][1][:, 0]  # Target: Percentage Change
comprehensive_rrr_data = stock_data['INFOSYS'][1][:, 1]  # Comprehensive RRR

# Fixed date display at the top of the app (January 31, 2025)
fixed_date = "Saturday, January 31, 2025"
st.markdown(f"<h5 style='text-align: right; color: gray;'>{fixed_date}</h5>", unsafe_allow_html=True)

# Create a sidebar for user inputs
st.sidebar.header('Stock Query')
ticker_input = st.sidebar.text_input("Enter Stock Ticker", "INFOSYS")
st.sidebar.write("This tool displays real-time stock data.")

# Portfolio Risk Tolerance Calculation
st.sidebar.header('Portfolio Risk Tolerance')
portfolio_file_path = st.sidebar.text_input("Enter Portfolio CSV File Path", r"DC:\Users\Ajay\Desktop\DOT-SLASH-\stock_transactions.csv")
if st.sidebar.button("Calculate Risk Tolerance"):
    risk_tolerance = calculate_risk_tolerance(portfolio_file_path)
    st.sidebar.write(f"Your Risk Tolerance: *{risk_tolerance}*")

    # Suggest Trading Strategy
    folder_path = r"DC:\Users\Ajay\Desktop\DOT-SLASH"  # Path to your folder containing CSV files
    trading_suggestion = suggest_trading_strategy(risk_tolerance, folder_path)

    if "error" in trading_suggestion:
        st.sidebar.error(trading_suggestion["error"])
    else:
        st.sidebar.success(f"Suggested Trading Strategy: *{trading_suggestion['strategy']}*")
        st.sidebar.write("Matching CSV Files:")
        for file_info in trading_suggestion['matching_files']:
            st.sidebar.write(f"Filename: {file_info['filename']}, Features: {file_info['features']}")

# Initialize variables for plot
chart_placeholder = st.empty()

# Stream data to the plot with a 1-second delay (real-time effect)
i = 0

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
    
    # Display the updated plot
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Simulate a 1-second delay for real-time streaming effect
    time.sleep(1)
    
    # Increment i for next iteration
    i += 1  # Update every second (each point represents 1 minute)