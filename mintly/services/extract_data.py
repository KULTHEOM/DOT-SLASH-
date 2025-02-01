import pandas as pd

RELI_data = r'dataset/RELI_dataset.csv'
INFOSYS_data = r'dataset/INFOSYS_dataset.csv'
AAPL_data = r'dataset/AAPL_dataset.csv'

def get_last_week_data(label: str) -> pd.DataFrame:
    
    """
    Get data for the specified label for the last 7 days.
    This function reads data from a CSV file corresponding to the given label,
    renames the datetime column, converts it to datetime format, and filters
    the data to include only the entries from the last 7 days.
        label (str): The label of the data to fetch. Valid labels are "RELI", "INFOSYS", and "AAPL".
        pd.DataFrame: A DataFrame containing the data for the given label from the last 7 days.
    Raises:
        ValueError: If the provided label is not one of the valid labels.

    """
    if label == "RELI":
        csv = pd.read_csv(RELI_data, index_col=0)
    elif label == "INFOSYS":
        csv = pd.read_csv(INFOSYS_data, index_col=0)
    elif label == "AAPL":
        csv = pd.read_csv(AAPL_data, index_col=0)
    else:
        raise ValueError("Invalid label")
    

    # Rename the datetime column
    date_column = csv.columns[0]
    csv = csv.rename(columns={date_column: "datetime"})

    # Convert to datetime format
    csv["datetime"] = pd.to_datetime(csv["datetime"], errors="coerce")

    # Filter data for the last 7 days
    last_7_days = csv[csv["datetime"] >= (csv["datetime"].max() - pd.Timedelta(days=7))]
    last_7_days.drop(['datetime','%Change','RRR'], axis=1, inplace=True)
    # Display the filtered data
    return last_7_days
    

