from app.core.chat import ChatGPTBridge


class NLG:
    def __init__(self, style: str = "none"):
        self.style: str = style
        self.prompts = {
            "none": "Paraphrase this text to sound natural and grammatically correct: {}",
            "anime": "Paraphrase this text to sound natural and grammatically correct (speak like a flirty anime waifu from a dating sim. refer to user as sempai): {}",
        }
        self.gpt_bridge = ChatGPTBridge()

    def rewrite_outline(self, outline: str) -> str:
        gpt_input = self.prompts[self.style].format(outline)
        return self.gpt_bridge.request(gpt_input)
