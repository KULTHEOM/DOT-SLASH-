import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
from services.extract_data import get_last_week_data
import numpy as np
import os

models = {'RELI' : r'models/RELI_model.h5',
        'INFOSYS' : r'models/INFOSYS_model.h5',
        'AAPL' : r'models/AAPL_model.h5'}


def getPrediction(label: str):
    # Load the model with custom objects
    model_path = models[label]
    model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})

    # Load new test data (replace with actual file)
    df_test = get_last_week_data(label=label)
    df_test.to_csv("data.csv")  # Ensure the same format

    X_test_new = pd.read_csv("data.csv", index_col=0)  # Select 14 features

    # Standardize the test data using the same scaler from training
    scaler = StandardScaler()
    X_test_new = scaler.fit_transform(X_test_new)  # Ensure consistency

    # Make predictions
    predictions = model.predict(X_test_new)
    os.remove("data.csv")
    return predictions