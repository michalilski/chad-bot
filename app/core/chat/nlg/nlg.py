from app.core.chat import ChatGPTBridge


class NLG:
    # PROMPTS = {
    #     "none": 'Paraphrase this text to sound natural and grammatically correct: {}',
    #     "anime": 'Paraphrase this text to sound natural and grammatically correct (speak like a flirty anime waifu from a dating sim. refer to user as sempai): {}'
    # }

    PROMPTS_WITH_USER_MESSAGE = {
        "none": 'User said: "{}". Answer this to the user and make it sound natural and grammatically correct: {}',
        "anime": 'User said: "{}". Answer this to the user and make it sound natural and grammatically correct (speak like a flirty anime waifu from a dating sim. refer to user as sempai): {}'
    }

    def __init__(self, style: str = "none"):
        self.style: str = style
        self.gpt_bridge = ChatGPTBridge()

    def rewrite_outline(self, outline: str, user_message: str) -> str:
        gpt_input = self.PROMPTS_WITH_USER_MESSAGE[self.style].format(user_message, outline)
        return self.gpt_bridge.request(gpt_input)
