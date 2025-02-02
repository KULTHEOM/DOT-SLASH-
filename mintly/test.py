from services.chatbot import ChatModel
from huggingface_hub import InferenceClient, login
from services.chatbot import ChatChain
from transformers import AutoTokenizer
from services.extract_data import get_data
from clients.prediction_model import getPrediction
from prompts import system_prompt
from clients.prediction_model import getPrediction
# from clients.alpha_vantage import fetch_monthly_minute_data
import pandas as pd
from services.chatbot import mintly
import json 
import numpy as np

 
# labels = ['INFOSYS']
# results = getPrediction(labels)
# print(results[labels[0]][1])
# print(results)
# print(dates)
# start_date = "2025-01-05"
# end_date =  "2025-01-06"
# df = pd.read_csv("dataset/INFOSYS_dataset.csv", index_col=0)
# data = get_data('INFOSYS', start_date=None, end_date=None)
# print(data.head())

# data = get_data(label='INFOSYS', start_date = None, end_date=None)
# print(data.head())
# 
# predictions = getPrediction(labels=["INFOSYS"])[0]['INFOSYS'][1]
# df = pd.DataFrame(predictions)
# df.to_csv("predictions.csv", index=False, header=False)

# system_msg = {"role" : "system", "content" : "You are an AI Assistant that gives detailed correct answers to user queries."}
# chat_chain = ChatChain([system_msg])
# chat_model = ChatModel(chatChain=chat_chain)
# output = chat_model.invoke("How are you?", stream=True)
# print(chat_chain.chain)

system_msg = {"role" : "system", "content" : system_prompt}
chatChain = ChatChain(chain=[system_msg])
mintly = mintly(chatChain=chatChain)

output = mintly.chat("Can you give me analysis for Apple in real time?")
print(output)

# print(chatChain.chain)

