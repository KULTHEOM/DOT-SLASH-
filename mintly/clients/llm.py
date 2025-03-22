# from huggingface_hub import InferenceClient, login
# from services.chatbot import ChatChain

# def getInferenceClient():
#     login(token='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')
#     client = InferenceClient()
#     return client

# def getModel():
#     return 'meta-llama/Meta-Llama-3-8B-Instruct'


# def getchatChain():
#     return ChatChain([])
import os
from litellm import completion
import litellm.litellm_core_utils.litellm_logging as litellm_logging
import logging

os.environ["LITELLM_LOGGING"] = "False"
logging.getLogger("litellm").setLevel(logging.CRITICAL)

litellm_logging.log_request = lambda *args, **kwargs: None  # Disable logging
litellm_logging.log_response = lambda *args, **kwargs: None  # Disable response logging


os.environ["GEMINI_API_KEY"] = "AIzaSyCLMZbWkPSiUDwxEkSgH5rVN3KQgtI7o08"

def getModel():
    return "gemini/gemini-2.0-flash"

def getCompletion():
    return completion
