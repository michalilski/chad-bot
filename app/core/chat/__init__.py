from app.core.chat.chatgpt_handler import ChatGPTHandler
from app.core.chat.dialogue_handler import DialogueHandler
from app.core.chat.dst.dst_module import ChatGPTBasedDSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.response_generation import ChatGPTBasedResponseGenerationModule

chatgpt_handler: ChatGPTHandler = ChatGPTHandler()
chatgpt_based_dialogue_handler: DialogueHandler = DialogueHandler(
    ChatGPTBasedDSTModule(chatgpt_handler),
    ChatGPTBasedIntentDetectionModule(chatgpt_handler),
    ChatGPTBasedResponseGenerationModule(chatgpt_handler),
)
