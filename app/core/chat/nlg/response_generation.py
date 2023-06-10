from abc import abstractmethod

from app.core.chat.chatgpt_bridge import ChatGPTBridge


class AbstractResponseGenerationModule:
    @abstractmethod
    def generate_response(self, *args, **kwargs) -> str:
        pass


# TODO implement the module
class ChatGPTBasedResponseGenerationModule(AbstractResponseGenerationModule):
    def __init__(self, chatgpt_handler: ChatGPTBridge):
        self.chatgpt_handler = chatgpt_handler

    def generate_response(self, *args, **kwargs) -> str:
        raise NotImplementedError
