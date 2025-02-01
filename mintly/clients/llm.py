from huggingface_hub import InferenceClient, login
# from services.chatbot import ChatChain

def getInferenceClient():
    login(token='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')
    client = InferenceClient()
    return client

def getModel():
    return 'meta-llama/Meta-Llama-3-8B-Instruct'


# def getchatChain():
#     return ChatChain([])