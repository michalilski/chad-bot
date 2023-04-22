from typing import List
from pydantic import BaseModel


class UserUtterance(BaseModel):
    user_id: int
    utterance: str
