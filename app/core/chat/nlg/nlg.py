import logging

from app.core.chat import ChatGPTBridge

BASE_MESSAGE = 'You are a cinema bot. User said: "{user_message}". Answer this exactly to the user, don\'t make stuff up: ({clues}) {outline} Response:'


def get_message_with_clues(clues):
    return BASE_MESSAGE.format(clues=clues, user_message="{user_message}", outline="{outline}")


class NLG:
    PROMPTS_WITH_USER_MESSAGE = {
        "professional": get_message_with_clues("sound professional"),
        "anime": get_message_with_clues("speak like a flirty anime waifu from a dating sim. refer to user as sempai"),
        "gen_z": get_message_with_clues("speak in gen z speach. be informal and chilled out."),
        "shakespear": get_message_with_clues("speak like shakespear"),
    }

    def __init__(self, style: str = "professional"):
        self.style: str = style
        self.gpt_bridge = ChatGPTBridge(temperature=0.3)

    def rewrite_outline(self, outline: str, user_message: str) -> str:
        gpt_input = self.PROMPTS_WITH_USER_MESSAGE[self.style].format(user_message=user_message, outline=outline)
        response = self.gpt_bridge.request(gpt_input)
        response = response.replace("~", "\\~")
        return response
