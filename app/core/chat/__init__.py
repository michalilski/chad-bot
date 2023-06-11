from app.core.chat.chatgpt_bridge import ChatGPTBridge
from app.core.chat.dialogue_loop import DialogueLoop
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.nlg import NLG

chatgpt_handler: ChatGPTBridge = ChatGPTBridge()
chatgpt_based_dialogue_handler: DialogueLoop = DialogueLoop(
    DSTModule(chatgpt_handler),
    ChatGPTBasedIntentDetectionModule(chatgpt_handler),
    NLG(),
)
