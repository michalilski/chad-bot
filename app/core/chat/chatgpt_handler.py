import logging

import openai

from app.exceptions import ChatGPTConnectionError, ChatProcessingException
from app.settings import config


class ChatGPTHandler:
    def __init__(self):
        openai.api_key = config["OpenAI"]["api_key"]

    def request(self, prompt: str) -> str:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
            )
        except ChatGPTConnectionError as e:
            logging.error(f"{type(e).__name__}: {e}")
            raise ChatProcessingException

        return completion.choices[0].message.content
