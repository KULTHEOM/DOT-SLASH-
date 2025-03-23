import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import StandardScaler
from services.extract_data import get_data

models = {
    'RELI': r'models/RELI_model.h5',
    'INFY': r'models/INFY_model.h5',
    'AAPL': r'models/AAPL_model.h5'
}

def getPrediction(labels: list, start_date=None, end_date=None):
    """
    Returns a dictionary with labels as keys and tuples (dates, predictions) as values.
    """
    results = {}
    percentage_change = None  # Ensure percentage_change is always defined

    for label in labels:
        try:
            # Load the model with custom objects
            model_path = models[label]  # This may throw KeyError if label is not found
            model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})
            
            # Load new test data
            df_test = get_data(label=label, start_date=start_date, end_date=end_date)
            
            if df_test.empty:
                print(f"No data found for {label}. Skipping.")
                continue  # Skip processing if data is empty

            first_open = df_test['1. open'].iloc[0]
            last_close = df_test['4. close'].iloc[-1]
            percentage_change = (last_close - first_open) / first_open * 100  # Always assigned
            
            dates = df_test['Datetime']
            df_test.drop(['Datetime'], axis=1, inplace=True)
            df_test.to_csv("data.csv")  # Ensure the same format
            
            X_test_new = pd.read_csv("data.csv", index_col=0)  # Select 14 features
            
            # Standardize the test data using the same scaler from training
            scaler = StandardScaler()
            X_test_new = scaler.fit_transform(X_test_new)  # Ensure consistency
            
            # Make predictions
            predictions = model.predict(X_test_new)
            results[label] = (dates, predictions)

        except KeyError:
            print(f"Error: Label '{label}' not found in model dictionary.")
        except Exception as e:
            print(f"Error processing {label}: {e}")

    return results, percentage_change  # percentage_change is now always defined