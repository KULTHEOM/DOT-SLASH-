from prompts import system_prompt
from huggingface_hub import InferenceClient
from clients.llm import *


class ChatChain:
    def __init__(self, chain):
        self.chain = chain

    def __str__(self):
        return '\n'.join(tuple(map(str, self.chain)))

    def __repr__(self):
        return '\n'.join(tuple(map(repr, self.chain)))

    def generate_prompt(self):
        return f'{self.__repr__()} \n <|assistant|> \n'

class ChatModel(ChatChain):
    def __init__(self, chatChain : ChatChain):
        self.client = getInferenceClient()
        self.model = getModel()
        self.chatChain = chatChain
   
    def tokenize(self, role, msg):
        self.role = role
        self.msg = msg
        template = {"role" : f"{self.role}", "content" : f"{self.msg}"}
        return template

    def invoke(self, msg, stream=False):

        human_message = self.tokenize("user", msg)
        self.chatChain.chain.append(human_message)

        response = ''
        response = self.client.chat.completions.create(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                                                        messages=self.chatChain.chain,
                                                        stream=True,
                                                        max_tokens=512,
                                                    )
        
        output = ''
        
        for chunk in response:
            text = chunk.choices[0].delta.content  # Extract token
            output += text  # Append to output string
            print(chunk.choices[0].delta.content, end='', flush=True)  # Print without new line

        ai_message = self.tokenize("assistant", output)
        self.chatChain.chain.append(ai_message)
        return 


# class mintly(ChatModel):
#     def __init__(self)