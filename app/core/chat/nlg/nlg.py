from app.core.chat import ChatGPTBridge


class NLG:
    # PROMPTS = {
    #     "none": 'Paraphrase this text to sound natural and grammatically correct: {}',
    #     "anime": 'Paraphrase this text to sound natural and grammatically correct (speak like a flirty anime waifu from a dating sim. refer to user as sempai): {}'
    # }

    PROMPTS_WITH_USER_MESSAGE = {
        "none": 'You are a cinema bot. User said: "{}". Answer this exactly to the user and make it sound natural and grammatically correct: {} Response:',
        "anime": 'You are a cinema bot. User said: "{}". Answer this exactly to the user and make it sound natural and grammatically correct (speak like a flirty anime waifu from a dating sim. refer to user as sempai): {} Response:',
    }

    def __init__(self, style: str = "none"):
        self.style: str = style
        self.gpt_bridge = ChatGPTBridge()

    def rewrite_outline(self, outline: str, user_message: str) -> str:
        gpt_input = self.PROMPTS_WITH_USER_MESSAGE[self.style].format(user_message, outline)
        response = self.gpt_bridge.request(gpt_input)
        response = response.replace("~", "\\~")
        return response
