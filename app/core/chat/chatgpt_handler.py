import openai

from app.env import config


class ChatGPTHandler:
    def __init__(self):
        openai.api_key = config["OpenAI"]["api_key"]

    def request(self, prompt: str) -> str:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        return completion.choices[0].message.content
