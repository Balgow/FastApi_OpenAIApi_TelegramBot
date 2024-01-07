from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

class Manager(BaseModel):
    username: str
    password: str

class Lead_adder(BaseModel):
    name: str 
    phone_number: str
    email: str
    whatsapp: str
    tg: str
    manager_username: str
    lang: str