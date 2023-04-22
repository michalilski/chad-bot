from typing import Any, Dict

import pytest

from app.core.chat.dst_module import ChatGPTBasedDSTModule, ChatGPTResponseProcessor
from app.tests.mocks import ChatGPTMockHandler


@pytest.fixture
def chatgpt_handler() -> ChatGPTMockHandler:
    return ChatGPTMockHandler()


@pytest.fixture
def chatgpt_dst_module(chatgpt_handler: ChatGPTMockHandler) -> ChatGPTBasedDSTModule:
    return ChatGPTBasedDSTModule(chatgpt_handler)


@pytest.fixture
def chatgpt_response_processor():
    return ChatGPTResponseProcessor


@pytest.fixture
def dummy_person_query_data() -> Dict[str, Any]:
    return {
        "research_interests": ["NLP", "RLHF", "NLG"],
        "projects": ["CLARIN", "UniChat"],
        "languages": ["polish", "english", "japanese"],
    }


@pytest.fixture
def dummy_person_data(dummy_person_query_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": "Juan",
        "surname": "Pablo",
        "organization": "University X",
        "abstracts": ["This is abstract 1.", "This is abstract 2."],
        **dummy_person_query_data,
    }
