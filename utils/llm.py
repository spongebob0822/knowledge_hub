import requests
import os
from dotenv import load_dotenv

class ChatGPT42API:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.url = "https://chatgpt-42.p.rapidapi.com/deepseekai"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }
    
    def format_prompt(self, message):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "web_access": False
        }
    
    def send_message(self, message):
        payload = self.format_prompt(message)
        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
