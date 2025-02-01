from services.chatbot import ChatModel
from huggingface_hub import InferenceClient, login
from services.chatbot import ChatChain
from transformers import AutoTokenizer
from services.extract_data import get_last_week_data
from clients.prediction_model import getPrediction
# from clients.prediction_model import predict_stock
# from clients.alpha_vantage import fetch_monthly_minute_data
import pandas as pd

# system_msg = {"role" : "system", "content" : "You are an AI Assistant that gives detailed correct answers to user queries."}
# chat_chain = ChatChain([system_msg])
# chat_model = ChatModel(chatChain=chat_chain)
# output = chat_model.invoke("How are you?", stream=True)
# print(chat_chain.chain)
 
label = 'INFOSYS'
predictions = getPrediction(label)
print(predictions)
# last_week_data = get_last_week_data(label)
# print(last_week_data.info())

# predictor = StockPredictor("models/RELI_model.pkl", "models/RELI_contrastive.pth", scaler_path=None)
# data = last_week_data
# new_data = predictor.load_and_preprocess_data(data)
# predictions = predictor.predict(new_data)
# print("Predictions:", predictions)

# label = 'RELI'
# predictions = predict_stock(label)

