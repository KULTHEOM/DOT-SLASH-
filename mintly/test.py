from services.chatbot import ChatModel
from huggingface_hub import InferenceClient, login
from services.chatbot import ChatChain
from transformers import AutoTokenizer

system_msg = {"role" : "system", "content" : "You are an AI Assistant that gives detailed correct answers with respect to the context given with each question asked by the user."}
chat_chain = ChatChain([system_msg])
chat_model = ChatModel(chatChain=chat_chain)
chat_model.invoke("How are you?", stream=True)

