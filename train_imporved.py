import torch
import torch.nn as nn
import joblib
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# Supervised Contrastive Loss (SCL)
class SupervisedContrastiveLoss(nn.Module):
    def _init_(self, temperature=0.07):
        super(SupervisedContrastiveLoss, self)._init_()
        self.temperature = temperature
    
    def forward(self, features, labels):
        """
        Compute the supervised contrastive loss.
        Arguments:
            features: Tensor of shape (batch_size, feature_dim)
            labels: Tensor of shape (batch_size,)
        """
        features = nn.functional.normalize(features, p=2, dim=-1)
        similarity_matrix = torch.matmul(features, features.T)
        labels = labels.unsqueeze(0) == labels.unsqueeze(1)
        logits = similarity_matrix / self.temperature
        labels = labels.float()
        loss = torch.mean(torch.sum(-labels * nn.functional.log_softmax(logits, dim=-1), dim=-1))
        return loss

class StockPredictor:
    def _init_(self):
        self.scaler = MinMaxScaler()
        self.model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.01)
        self.neural_net = nn.Sequential(
            nn.Linear(15, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        self.criterion = SupervisedContrastiveLoss()

    def load_data_from_csv(self, file_path: str):
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
            expected_columns = [
                "date", "1. open", "2. high", "3. low", "4. close", "5. volume",
                "EMA", "Volume_Oscillator", "RSI", "%K", "%D", "+DI", "-DI", "ADX", "PVT", "Target"
            ]
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns in CSV file: {missing_cols}")
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df.dropna(subset=["date"], inplace=True)
            df.set_index("date", inplace=True)
            df[expected_columns[1:]] = df[expected_columns[1:]].apply(pd.to_numeric, errors="coerce")
            X = df.drop(columns=["Target"]).values
            y = df["Target"].values
            return X, y
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None, None

    def prepare_data_for_training(self, X, y, test_size=0.2):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
        X_train = self.scaler.fit_transform(X_train)
        X_val = self.scaler.transform(X_val)
        return X_train, X_val, y_train, y_val

    def train_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train, dtype=torch.long)
        feature_output = self.neural_net(X_train_tensor)
        loss = self.criterion(feature_output, y_train_tensor)
        print(f"Contrastive learning loss: {loss.item()}")

    def save_model(self, model_save_path: str):
        joblib.dump(self.model, model_save_path)
        torch.save(self.neural_net.state_dict(), 'contrastive_model.pth')
        print(f"Model saved to {model_save_path}")

    def evaluate(self, X_val, y_val):
        predictions = self.model.predict(X_val)
        mse = mean_squared_error(y_val, predictions)
        r2 = r2_score(y_val, predictions)
        return predictions, mse, r2

if _name_ == "_main_":
    predictor = StockPredictor()
    X, y = predictor.load_data_from_csv(r"C:\Users\Ajay\Desktop\DOT-SLASH-\features.csv")
    X_train, X_val, y_train, y_val = predictor.prepare_data_for_training(X, y)
    predictor.train_model(X_train, y_train)
    predictor.save_model("svm_model.pkl")
    predictions, mse, r2 = predictor.evaluate(X_val, y_val)
    print(f"Predictions: {predictions}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")