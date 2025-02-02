import pandas as pd

RELI_data_path = r'dataset/RELI_dataset.csv'
INFY_data_path = r'dataset/INFY_dataset.csv'
AAPL_data_path = r'dataset/AAPL_dataset.csv'

def get_last_week_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the last 7 days of data from the given DataFrame.

    Steps:
    - Renames the datetime column.
    - Converts the datetime column to a proper format.
    - Filters data for the last 7 days.
    - Drops unnecessary columns.

    Returns:
    - A DataFrame containing data from the last 7 days.
    """
    # Rename datetime column and strip spaces from column names
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"datetime": "Datetime"})

    # Convert Datetime column to datetime format
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

    # Determine the last available date in the dataset
    max_date = df["Datetime"].max()

    # Filter data for the last 7 days from the latest available date
    last_7_days = df[df["Datetime"] >= (max_date - pd.Timedelta(days=7))]

    # Drop unwanted columns
    last_7_days = last_7_days.drop(columns=["%Change", "RRR"], errors="ignore")

    return last_7_days

# def filter_by_date_only(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
#     """
#     Filters the dataset based on the given start and end dates (ignoring time).

#     Parameters:
#     - df (pd.DataFrame): The dataset containing a datetime column.
#     - start_date (str): Start date in 'YYYY-MM-DD' format.
#     - end_date (str): End date in 'YYYY-MM-DD' format.

#     Returns:
#     - DataFrame: Filtered entries within the date range.
#     """

#     # Ensure column names are properly formatted
#     df.columns = df.columns.str.strip()

#     # Rename datetime column if necessary
#     if "datetime" in df.columns:
#         df = df.rename(columns={"datetime": "Datetime"})

#     # Convert Datetime column to proper datetime format (ensuring no time component)
#     df["Datetime"] = pd.to_datetime(df["Datetime"], errors='coerce').dt.date

#     # Convert start_date and end_date to date format (ensuring no time component)
#     start_date = pd.to_datetime(start_date, errors='coerce').date()
#     end_date = pd.to_datetime(end_date, errors='coerce').date()

#     print(f"Filtering from {start_date} to {end_date}")

#     # Apply filtering based on dates (not datetime)
#     filtered_df = df[(df["Datetime"] >= start_date) & (df["Datetime"] <= end_date)]

#     # Drop unwanted columns safely
#     filtered_df = filtered_df.drop(columns=["%Change", "RRR"], errors="ignore")
#     filtered_df.to_csv("filtered_data.csv")
#     return filtered_df

def get_data(label: str, start_date: str | None, end_date: str | None) -> pd.DataFrame:
    """
    Get data for the specified label within the specified date range.
    If no date range is provided, the function returns the data for the last 7 days.
    Parameters:
    - label (str): The label of the data to fetch. Valid labels are "RELI", "INFOSYS", and "AAPL".
    - start_date (str): The start date of the date range in 'YYYY-MM-DD' format.
    - end_date (str): The end date of the date range in 'YYYY-MM-DD' format.
    Returns:
    - DataFrame: A DataFrame containing the data for the given label within the specified date range.
    """
    if label == 'RELI':
        df = pd.read_csv(RELI_data_path, index_col=0)
    elif label == 'INFY':
        df = pd.read_csv(INFY_data_path, index_col=0)
    elif label == 'AAPL':
        df = pd.read_csv(AAPL_data_path, index_col=0)
    else:
        raise ValueError("Invalid label. Valid labels are 'RELI', 'INFY', and 'AAPL'.")

    # if start_date and end_date:
    #     print("Filtering by date range...")
    #     print("Start Date:", start_date)
    #     print("End Date:", end_date)
    #     return filter_by_date_only(df=df, start_date=start_date, end_date=end_date)
    
    return get_last_week_data(df=df)
    
    
    
    