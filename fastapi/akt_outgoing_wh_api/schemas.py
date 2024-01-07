from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

class SysPrompts(BaseModel):
    role: str
    message: str

class ChatMessage(BaseModel):
    client_id: str
    message: str
    is_bot: bool

class ChatMessageID(BaseModel):
    client_id: str

class Arrangement(BaseModel):
    client_id: str
    platform: str
    datetime: datetime