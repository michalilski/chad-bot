import json
from typing import Any, Dict, List, Type

import pytest

from app.core.chat.dst_module import ChatGPTResponseProcessor
from app.tests.mocks import ChatGPTMockHandler


@pytest.mark.parametrize("text", ["To jest tekst.", "Sample text.", ""])
def test_chatgpt_requests_handler(text: str, chatgpt_handler: ChatGPTMockHandler):
    response: str = chatgpt_handler.request(text)
    assert response.startswith("[ChatGPT response] ")


@pytest.mark.parametrize(
    ["response", "expected_values"],
    [
        ("To jest\n odpowiedź.", "To jest odpowiedź."),
        ("Response\n\n", "Response"),
        ("Value: NA", "Value: "),
        ("Value: Test", "Value: Test"),
        ("NA", ""),
        ("\nNA\n", ""),
    ],
)
def test_removing_special_characters(
    response: str, expected_values: str, chatgpt_response_processor: Type[ChatGPTResponseProcessor]
):
    assert expected_values == chatgpt_response_processor.remove_special_characters(response)


def test_dictionary_parser(
    dummy_person_data: Dict[str, Any],
    dummy_person_query_data: Dict[str, Any],
    chatgpt_response_processor: Type[ChatGPTResponseProcessor],
):
    assert chatgpt_response_processor.parse_to_dictionary(json.dumps(dummy_person_data)) == dummy_person_data

    assert (
        chatgpt_response_processor.parse_to_dictionary(json.dumps(dummy_person_query_data)) == dummy_person_query_data
    )


@pytest.mark.parametrize(
    ["text", "expected_results"],
    [
        ("1, 2, 3", ["1", "2", "3"]),
        ("Test, after test", ["Test", "after test"]),
        ("", [""]),
    ],
)
def test_multiple_values_to_list(
    text: str, expected_results: List[str], chatgpt_response_processor: Type[ChatGPTResponseProcessor]
):
    data: Dict[str, str] = {"data": text}
    assert expected_results == chatgpt_response_processor.multiple_values_to_list(data)["data"]
