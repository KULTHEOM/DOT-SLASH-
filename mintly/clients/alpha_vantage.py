from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import numpy as np

## THIS IS A DUMMY SERVICE FOR GETTING REAL TIME DATA FROM API.

# # Define your API key
# api_key = "DZN0SFNNTOZKAY20"

# # Initialize the Alpha Vantage TimeSeries object
# ts = TimeSeries(key=api_key, output_format='pandas')

# # Function to fetch data in chunks
# def fetch_monthly_minute_data(symbol: str, start_date : str, end_date: str):
#     """
#     Fetch 1-minute data for a stock over a month using Alpha Vantage API.

#     Args:
#         symbol (str): Stock ticker (e.g., "AAPL").
#         start_date (str): Start date in YYYY-MM-DD format.
#         end_date (str): End date in YYYY-MM-DD format.

#     Returns:
#         DataFrame: Combined 1-minute data over the specified range.
#     """
#     all_data = []
#     current_date = pd.to_datetime(start_date)

#     while current_date <= pd.to_datetime(end_date):
#         # Fetch 1-minute intraday data (compact mode)
#         try:
#             print(f"Fetching data for {current_date.strftime('%Y-%m-%d')}...")
#             data= ts.get_intraday(symbol=symbol, interval="1min", outputsize="full")
#             all_data.append(data)

#             # Wait to respect API limits (5 requests per minute for free tier)
#             time.sleep(12)  # Add delay to avoid exceeding request limits
#         except Exception as e:
#             print(f"Error fetching data for {current_date.strftime('%Y-%m-%d')}: {e}")

#         # Move to the next day
#         current_date += pd.Timedelta(days=1)

#     # Combine all dataframes into one
#     if all_data:
#         full_data = pd.concat(all_data)
#         full_data.sort_index(inplace=True)
#         data =  full_data.drop_duplicates().reset_index(drop=True)
#         return data
#     else:
#         return Exception("No data fetched.")
    # ema=data['4. close'].head(3).mean()
    # data['EMA'] = None  # Initialize SMA column
    # n = 5  # EMA period
    # data['EMA'] = data['4. close'].ewm(span=n, adjust=False).mean()
    # short_time_period=1
    # long_time_period=60
    # data['Short_Volume_MA'] = data['5. volume'].rolling(window=short_time_period, min_periods=1).mean()
    # data['Long_Volume_MA'] = data['5. volume'].rolling(window=long_time_period, min_periods=1).mean()
    # data['Volume_Oscillator'] = ((data['Short_Volume_MA'] - data['Long_Volume_MA']) / data['Long_Volume_MA']) * 100

    # # Drop the intermediate moving average columns if you don't need them
    # data.drop(['Short_Volume_MA', 'Long_Volume_MA'], axis=1, inplace=True)
    # n=15 #minutes
    # data['price change']=data['4. close'].diff()
    # data['gain']=data['price change'].apply(lambda x: x if x>0 else 0)
    # data['Loss'] = data['price change'].apply(lambda x: -x if x < 0 else 0)
    # data['Avg Gain'] = data['gain'].rolling(window=n, min_periods=1).mean()
    # data['Avg Loss'] = data['Loss'].rolling(window=n, min_periods=1).mean()
    # data['RS'] = data['Avg Gain'] / data['Avg Loss']
    # data['RSI'] = 100 - (100 / (1 + data['RS']))
    # data.drop(['price change', 'gain', 'Loss', 'Avg Gain', 'Avg Loss', 'RS'], axis=1, inplace=True)
    # n=15
    # m=3
    # data['Lowest Low'] = data['3. low'].rolling(window=n, min_periods=1).min()
    # data['Highest High'] = data['2. high'].rolling(window=n, min_periods=1).max()
    # data['%K'] = ((data['4. close'] - data['Lowest Low']) / (data['Highest High'] - data['Lowest Low'])) * 100
    # data['%D'] = data['%K'].rolling(window=m, min_periods=1).mean()
    # data.drop(['Lowest Low', 'Highest High'], axis=1, inplace=True)
    # period = 15
    # data['Previous Close'] = data['4. close'].shift(1)
    # data['TR'] = np.maximum(
    #     data['2. high'] - data['3. low'],
    #     np.maximum(
    #         abs(data['2. high'] - data['Previous Close']),
    #         abs(data['3. low'] - data['Previous Close'])
    #     )
    # )
    # data['+DM'] = np.where(
    #     (data['2. high'] - data['2. high'].shift(1)) > (data['3. low'].shift(1) - data['3. low']),
    #     np.maximum(data['2. high'] - data['2. high'].shift(1), 0),
    #     0
    # )
    # data['-DM'] = np.where(
    #     (data['3. low'].shift(1) - data['3. low']) > (data['2. high'] - data['2. high'].shift(1)),
    #     np.maximum(data['3. low'].shift(1) - data['3. low'], 0),
    #     0
    # )
    # data['Smoothed_TR'] = data['TR'].rolling(window=period, min_periods=1).sum()
    # data['Smoothed_+DM'] = data['+DM'].rolling(window=period, min_periods=1).sum()
    # data['Smoothed_-DM'] = data['-DM'].rolling(window=period, min_periods=1).sum()
    # data['+DI'] = (data['Smoothed_+DM'] / data['Smoothed_TR']) * 100
    # data['-DI'] = (data['Smoothed_-DM'] / data['Smoothed_TR']) * 100
    # data['DX'] = (abs(data['+DI'] - data['-DI']) / (data['+DI'] + data['-DI'])) * 100

    # # Step 6: Calculate the Average Directional Index (ADX)
    # data['ADX'] = data['DX'].rolling(window=period, min_periods=1).mean()

    # # Drop unnecessary columns
    # data.drop(['Previous Close', 'TR', '+DM', '-DM', 'Smoothed_TR', 'Smoothed_+DM', 'Smoothed_-DM', 'DX'], axis=1, inplace=True)
    # data['Percentage Price Change'] = data['4. close'].pct_change()

    # # Step 2: Calculate the Price Volume Trend (PVT)
    # data['PVT'] = (data['Percentage Price Change'] * data['5. volume']).cumsum()

    # # Drop unnecessary columns
    # data.drop(['Percentage Price Change'], axis=1, inplace=True)
    # data['Target'] = data['4. close'].pct_change()
    # rsi_mean = data['RSI'].mean()

    # # Fill NaN values in the 'RSI' column with the mean value
    # data['RSI'].fillna(rsi_mean, inplace=True)
    # percent_changeink = data['%K'].median()
    # data['%K'].fillna(percent_changeink, inplace=True)

    # percent_changeind=data['%D'].median()
    # data['%D'].fillna(percent_changeind, inplace=True)

    # plus_d=data['+DI'].median()
    # data['+DI'].fillna(plus_d, inplace=True)

    # minus_d=data['-DI'].median()
    # data['-DI'].fillna(minus_d, inplace=True)

    # adx=data['ADX'].median()
    # data['ADX'].fillna(adx, inplace=True)

    # pvt=data['PVT'].median()
    # data['PVT'].fillna(pvt, inplace=True)

    # target=data['Target'].median()
    # data['Target'].fillna(target, inplace=True)
    
    # return data


# def calculate_all_features(data):
    
# Save to a CSV file for later use
# if data is not None:
#     data.to_csv(f"{symbol}1min{start_date}to{end_date}.csv")
#     print(f"Data saved to {symbol}1min{start_date}to{end_date}.csv")
# else:
#     print("No data fetched.")