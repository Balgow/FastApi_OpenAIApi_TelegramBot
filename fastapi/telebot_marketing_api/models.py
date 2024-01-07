from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey,  VARCHAR, BOOLEAN
from .databases import Base
import json


class Prompts(Base):
    __tablename__ = 'prompts_marketing'

    prompt_id = Column(Integer, primary_key = True,  autoincrement = True)
    role = Column(VARCHAR(10))
    message = Column(VARCHAR(200))

class Chat_messages(Base):
    __tablename__ = 'chat_messages_marketing'

    chat_message_id = Column(Integer, primary_key = True, autoincrement = True)
    client_id = Column(VARCHAR(20)) # telegram id
    message = Column(VARCHAR(1000))
    is_bot = Column(BOOLEAN)

class Managers(Base):
    __tablename__ = 'managers'

    username = Column(VARCHAR(30), primary_key = True)
    password = Column(VARCHAR(30))


class Leads(Base):
    __tablename__ = 'leads_info'

    lead_id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(VARCHAR(50)) 
    phone_number = Column(VARCHAR(50))
    email = Column(VARCHAR(50))
    whatsapp = Column(VARCHAR(50))
    tg = Column(VARCHAR(50))
    manager_username = Column(VARCHAR(50), ForeignKey("managers.username"))
    lang = Column(VARCHAR(10))
    ls_start = Column(DateTime)
    ls_answer = Column(DateTime)
    ls_agree = Column(DateTime)
    ls_ping = Column(DateTime)

class Arrangements(Base):
    __tablename__ = 'arrangements'

    arrangement_id = Column(Integer, primary_key = True, autoincrement = True)
    client_id = Column(VARCHAR(50))
    platform = Column(VARCHAR(50))
    datetime = Column(DateTime)