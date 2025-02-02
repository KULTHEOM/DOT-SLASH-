import pandas as pd 
import pandas as pd
import re

import pandas as pd
import re
import os

def extract_stop_loss(query):
    # Updated regex to handle variations like "stop loss of 7%", "stop loss 7%", etc.
    stop_loss_match = re.search(r'stop loss\s*(?:of\s*)?(\d+)%', query, re.IGNORECASE)
    if not stop_loss_match:
        return None  # Return None if no stop loss value is found
    return int(stop_loss_match.group(1))  # Extract and return the stop loss value

def find_ticker_based_on_stop_loss(query, directory):
    # Extract the stop loss value from the query
    stop_loss = extract_stop_loss(query)
    if stop_loss is None:
        return "Stop loss value not found in the query."
    
    # Rest of the function remains the same
    # Get all CSV files in the directory
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    
    # Calculate the median of the RRR column for each CSV file
    medians = []
    tickers = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            if 'RRR' in df.columns:
                median_rrr = df['RRR'].median()
                medians.append(median_rrr)
                tickers.append(os.path.basename(csv_file).replace('.csv', ''))  # Extract ticker name from file name
            else:
                medians.append(None)
                tickers.append(None)
        except FileNotFoundError:
            medians.append(None)
            tickers.append(None)
    
    # Filter out tickers with missing or invalid data
    valid_tickers = [ticker for ticker, median in zip(tickers, medians) if median is not None]
    valid_medians = [median for median in medians if median is not None]
    
    if not valid_tickers:
        return "No valid data found in the CSV files."
    
    # Sort tickers based on their median RRR values
    sorted_tickers = [ticker for _, ticker in sorted(zip(valid_medians, valid_tickers))]
    
    # Determine the appropriate ticker based on the stop loss value
    if stop_loss < 5:
        selected_ticker = sorted_tickers[0]  # Lowest median
    elif 5 <= stop_loss <= 10:
        selected_ticker = sorted_tickers[-2]  # 2nd highest median
    else:
        selected_ticker = sorted_tickers[-1]  # Highest median
    
    return selected_ticker

# Example usage
query = "Set a stop loss of 2% and search for the best ticker."
directory = r"D:\DOT SLASH\tickercsv"  # Replace with the actual directory path
result = find_ticker_based_on_stop_loss(query, directory)
print(result)