import pandas as pd
import os

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

# Example usage of the function
user_risk_tolerance = 'low'  # User-defined risk tolerance
folder_path = r'C:\Users\Ajay\Desktop\DOT-SLASH-\dataset_testing'  # Path to your folder containing CSV files

# Call the function
trading_suggestion = suggest_trading_strategy(user_risk_tolerance, folder_path)

# Display the suggested strategy and matching files
if "error" in trading_suggestion:
    print(trading_suggestion["error"])
else:
    print("Suggested Trading Strategy:")
    print(trading_suggestion['strategy'])
    print("\nMatching CSV Files:")
    for file_info in trading_suggestion['matching_files']:
        print(f"Filename: {file_info['filename']}, Features: {file_info['features']}")