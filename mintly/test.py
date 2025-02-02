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

system_prompt = """I have time-series data for a stock listing. An example stock listing for a certain label looks like this:

{
  "ticker": "INFY",
  "data": {
    "uid": "1",
    "datetime": "2025-01-02 04:00:00",
    "open": 22.71,
    "high": 22.9,
    "low": 22.71,
    "close": 22.9,
    "volume": 944.0,
    "EMA": 22.9,
    "Volume_Oscillator": 0.0,
    "RSI": 50.21927551695059,
    "%K": 100.0,
    "%D": 100.0,
    "+DI": 22.653346947797505,
    "-DI": 24.24242424242359,
    "ADX": 30.58052962628356,
    "PVT": -15111.818938244143,
    "%Change": -3.4346103038309166,
    "RRR": 0.2565445026178002
  }
}

There are some questions in which you have to predict(Using a model) some data on the basis of the labels and time frame, ALWAYS assume it to be NULL.
To do this, you should provide the following action in the format:

## Action
predict[{
    "given": {
        "ticker": [<ticker1>, <ticker2>, ...], 
        "time_frame": {NULL}
    },
    required: ["prediction"]
}]

If you find all the information you needed from the observation I provided, then you give the action:
        
    finish[<whatever-answer-you-concluded-from-the-observation>]

 VERY IMPORTANT: YOU SHOULD ALWAYS STOP GENERATING TEXT AFTER GIVING ACTION FOR THE OBSERVATION THAT THE USER WILL PROVIDE. Also, you should expect observation only when previous action is the search action.

Now, I want the whole process in the following format:
## Question: <whatever-my-question-is>
## Thought: <your-thoughts-and-action-plan-based-on-my-question-and-observation-i-provided>
## Action: <either-search-action-or-finish-action-in-the-format-i-provided>
## Observation: <whatever-observation-I-WILL-PROVIDE>
## Thought: <your-thoughts-and-action-plan-based-on-observation-i-provided>
## Action: <either-search-action-or-finish-action-in-the-format-i-provided>
... until the action is finish.

Remark: In the process format, I WILL provide the question as ## Question. You are NOT SUPPOSED to again give the ## Question in the tests you will generate.

Following is an example run that show the process:

##Question: Can you give me analysis for Apple in real time?
##Thought: The user is asking for a real-time analysis of Apple (AAPL). Since this requires the latest data, I will perform a search to retrieve up-to-date time-series stock information for AAPL.
##Action:

predict[{
"given": {
"ticker": ["AAPL"],
"time_frame": {NULL}
},
"required": ["prediction"]
}]

##Observation: "The percentage change in the stock price is over the duration is 5%."
##Thought: The observation indicates that Apple's stock price has changed by 5% over the given duration. Based on this, I can conclude that the stock has experienced significant movement, which may indicate strong momentum or volatility.
Action:

finish["Apple's stock has experienced a 5% change over the observed duration, suggesting notable market movement. Further analysis may be required to determine trends, resistance levels, or future projections."]
"""


system_msg = {"role" : "system", "content" : system_prompt}
chatChain = ChatChain(chain=[system_msg])
mintly = mintly(chatChain=chatChain)

output = mintly.chat("Can you give me analysis for Infosys in real time?")
print(output)
print(chatChain.chain)


