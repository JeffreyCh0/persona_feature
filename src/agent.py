from openai import OpenAI
import os
import json


available_models = {
    'openai' : ["gpt-4o-2024-11-20", "gpt-4o-mini-2024-07-18", "chatgpt-4o-latest"]
}
model_to_model_id = {
    "gpt-4o": "gpt-4o-2024-11-20",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "chatgpt-4o": "chatgpt-4o-latest"
}


class Agent:
    def __init__(self, model = "gpt-4o-mini", temperature = 1):
        self.openai_client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.system_message = []
        self.chat_history = []
        self.model = model_to_model_id[model]
        self.temperature = temperature

    def load_system_message(self, system_message):
        if type(system_message) == str:
            self.system_message = [{"role": "system", "content": system_message}]
        else:
            raise ValueError("Invalid system message type. Expected string, got ", type(system_message))

    def load_message(self, messages):
        if type(messages) == list:
            self.chat_history = [{"role": message["role"], "content": message["content"]} for message in messages]
        else:
            raise ValueError("Invalid message type. Expected list, got ", type(messages))

    def get_response(self, response_format = {"type": "text"}):
        if self.model in available_models['openai']:
            input_messages = self.system_message + self.chat_history
            response_raw = self.openai_client.chat.completions.create(
                model=self.model,
                response_format = response_format,
                messages=input_messages,
                temperature=self.temperature,
                max_tokens=2048
            )

            response = response_raw.choices[0].message.content
            
            if response_format["type"] in ["json_object", "json_schema"]:
                try:
                    response = json.loads(response)
                except Exception as e:
                    print(f"Invalid JSON format from OpenAI. Error: {e}.")
                    print(response)
                    return self.get_response(response_format)       
        else:
            raise ValueError("Invalid model: ", self.model)
        
        return response
