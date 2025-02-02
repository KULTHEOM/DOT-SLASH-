from prompts import system_prompt
from huggingface_hub import InferenceClient
from clients.llm import *
import re
import json
from typing import Any
from clients.prediction_model import getPrediction

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

    def extract_until_first_action(self, llm_response: str):
   
        """
        Extracts the portion of the text from the beginning until the first '## Action:' tag and the following tag.

        Args:
            text (str): The input text to extract from.

        Returns:
            str: The extracted portion of the text. If '## Action:' or a subsequent tag is not found, 
            returns the entire text.
        """
        action_index = llm_response.find("## Action:")
        
        if action_index == -1:
            return llm_response
        
        next_tag_index = llm_response.find("##", action_index + len("## Action:"))
        
        if next_tag_index == -1:
            return llm_response
        
        return llm_response[:next_tag_index]

    def invoke(self, msg, stream=False):

        human_message = self.tokenize("user", msg)
        self.chatChain.chain.append(human_message)

        response = ''
        response = self.client.chat.completions.create(model='meta-llama/Meta-Llama-3-8B-Instruct',
                                                        messages=self.chatChain.chain,
                                                        stream=True,
                                                        max_tokens=512,
                                                    )
        
        output = ''
        
        for chunk in response:
            text = chunk.choices[0].delta.content  # Extract token
            output += text  # Append to output string
            print(chunk.choices[0].delta.content, end='', flush=True)  # Print without new line
        improved_llm_response = self.extract_until_first_action(output)
        # print("\n\n-------------------------------------------------\n\n")
        print(improved_llm_response)
        # print("\n\n-------------------------------------------------\n\n")
        ai_message = self.tokenize("assistant", improved_llm_response)
        self.chatChain.chain.append(ai_message)
        return improved_llm_response


class mintly(ChatModel):
    def parse_llm_response(self, improved_llm_response: str) -> dict | str:
        """
        Parse the LLM response into a dictionary or string.

        Args:
            improved_llm_response (str): The response from LLM.

        Returns:
            dict | str: If the action is 'predict', return a dictionary with 'action' key as 'prediction' and extracted data.
                        If the action is 'finish', return a dictionary with 'action' key as 'finish' and the string data.
                        If the input is invalid JSON format, return a string "Invalid JSON format".
        """
        if "predict[" in improved_llm_response:
            match = re.search(r"predict\[\s*(\{.*?\})\s*\]", improved_llm_response, re.DOTALL)
            if match:
                try:
                    # Fix invalid JSON: Replace `{NULL}` with `null`
                    fixed_json = match.group(1).replace("{NULL}", "null")
                    input_data = json.loads(fixed_json)

                    return {
                        "action": "prediction",
                        "data": {
                            "labels": input_data["given"].get("ticker", []),
                            "time_period": input_data["given"].get("time_frame")
                        }
                    }
                except json.JSONDecodeError:
                    return "Invalid JSON format"

        elif "finish[" in improved_llm_response:
            match = re.search(r"finish\[\s*(.*?)\s*\]", improved_llm_response, re.DOTALL)
            if match:
                return {"action": "finish", "data": match.group(1)}

        return {"action": "error", "data": "Invalid Format"}


    
    def get_relevant_data_tool(self, parsed_data: dict):
        """
        Get relevant data from parsed data.

        Args:
            parsed_data (dict): A dictionary of parsed data from the LLM response.

        Returns:
            str: A string of relevant data.
        """
        data = []
        if parsed_data.get("action") == "prediction":
            labels = parsed_data.get("data", {}).get("labels", [])
            if labels is not None:
                data, percentage_change = getPrediction(labels)##dict
            
            indicator = "The percentage change in the stock price is over the duration is :" + str(percentage_change) + "%."
            return indicator
        
        elif parsed_data.get("action") == "finish":
                data = parsed_data.get("data")
        
        else:
            return "Invalid Format"
            

    def _question(self, msg: str) -> str:
        return "## Question: "+ msg

    def _observation(self, msg: str) -> str:
        return "## Observation: \n"+ msg + "\n"

    def identify_msg_type(self, input_string: str) -> str:

        trimmed_string = input_string.strip()
        if trimmed_string.startswith('[') and trimmed_string.endswith(']'):
            return "Observation"

        return "Question"

    def Agent(self, msg: str) -> Any:
        
        if self.identify_msg_type(msg) == "Observation":
            llm_response = self.invoke(self._observation(msg))
        else:
            llm_response = self.invoke(self._question(msg))
        
        action = self.parse_llm_response(llm_response)
        indicator = self.get_relevant_data_tool(action)#This can be either search action data from the api or a finish action response.
        
        return indicator

    def chat(self, query: str) -> str:
        result = self.Agent(query)
        if self.identify_msg_type(result) == "Observation":
            result = self.Agent(result)
        
        return result