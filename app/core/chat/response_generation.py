from abc import abstractmethod


class AbstractResponseGenerationModule:
    @abstractmethod
    def generate_response(self, *args, **kwargs) -> str:
        pass


# TODO implement the module
class ChatGPTBasedResponseGenerationModule(AbstractResponseGenerationModule):
    def generate_response(self, *args, **kwargs) -> str:
        raise NotImplementedError
