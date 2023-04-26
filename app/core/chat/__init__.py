from app.core.chat.chatgpt_handler import ChatGPTHandler
from app.core.chat.dialogue_handler import DialogueHandler
from app.core.chat.dst_module import ChatGPTBasedDSTModule
from app.core.chat.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.response_generation import ChatGPTBasedResponseGenerationModule

chatgpt_handler: ChatGPTHandler = ChatGPTHandler()
chatgpt_based_dialogue_handler: DialogueHandler = DialogueHandler(
    ChatGPTBasedDSTModule(chatgpt_handler), ChatGPTBasedIntentDetectionModule(), ChatGPTBasedResponseGenerationModule()
)
