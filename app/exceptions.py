import openai
import requests


class ChatProcessingException(Exception):
    pass


ChatGPTConnectionError = (openai.error.AuthenticationError, requests.exceptions.RequestException)
PROCESSING_ERROR_MESSAGE: str = "I am sorry, but I can't help you now. Please, try again in a moment."
