import logging
import time

import openai

from app.exceptions import ChatGPTConnectionError, ChatProcessingException
from app.settings import config


class ChatGPTBridge:
    def __init__(self):
        openai.api_key = config["OpenAI"]["api_key"]

    def request(self, prompt: str, num_attempts: int = 2) -> str:
        if num_attempts <= 0:
            raise ChatProcessingException
        try:
            return openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content
        except ChatGPTConnectionError as e:
            logging.error(f"{type(e).__name__}: {e}")
        return self.request(prompt, num_attempts=num_attempts-1)
