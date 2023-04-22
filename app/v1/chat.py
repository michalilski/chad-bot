from typing import Any, Dict

from fastapi import APIRouter

from app.core.chat.exceptions import UtteranceHandlerException
from app.core.schemas.chat_schemas import UserUtterance

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Chat API root directory. See API docs for details."}


@router.post("/utterance")
async def user_utterance(user_utterance: UserUtterance) -> Dict[str, Any]:
    try:
        # TODO handle by a dialogue handler and return a response
        pass
    except UtteranceHandlerException:
        response = {"error": f"Exception occurred while processing your utterance. Please try again later."}
    return response
