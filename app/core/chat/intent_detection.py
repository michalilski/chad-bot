from abc import abstractmethod

from app.core.schemas.intent import IntentEnum


class AbstractIntentDetectionModule:
    @abstractmethod
    def recognize_intent(self, *args, **kwargs) -> IntentEnum:
        pass


# TODO implement the module
class ChatGPTBasedIntentDetectionModule(AbstractIntentDetectionModule):
    def recognize_intent(self, *args, **kwargs) -> IntentEnum:
        raise NotImplementedError
