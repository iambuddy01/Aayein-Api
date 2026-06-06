from pydantic import BaseModel


class ChatRequest(BaseModel):
    api_key: str
    chat_id: int
    user_id: int
    message: str


class ClearRequest(BaseModel):
    api_key: str
    chat_id: int
    user_id: int
