from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

class customParamDTO(BaseModel):
    name: str
    value: str

class ReceiverDTO(BaseModel):
    whatsappNumber: str
    customParams: list[customParamDTO]

class SendTemplateMessagesDTO(BaseModel):
  template_name: str
  broadcast_name: str
  receivers: list[ReceiverDTO]

class SendMessageDTO(BaseModel):
    number: str
    text: str

class WebhookMessageDTO(BaseModel):
    eventType: str
    id: str
    created: str
    waId: str
    senderName: str