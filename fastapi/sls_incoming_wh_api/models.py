from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey,  VARCHAR, BOOLEAN
from .databases import Base
import json


class Prompts(Base):
    __tablename__ = 'sls_incoming_wh_prompts'
    __table_args__ = {"schema": "whatsapp_service"}

    prompt_id = Column(Integer, primary_key = True,  autoincrement = True)
    role = Column(VARCHAR(10))
    message = Column(VARCHAR(500))

class Chat_messages(Base):
    __tablename__ = 'sls_incoming_wh_chat_messages'
    __table_args__ = {"schema": "whatsapp_service"}

    chat_message_id = Column(Integer, primary_key = True, autoincrement = True)
    client_id = Column(VARCHAR(20))
    message = Column(VARCHAR(1000))
    is_bot = Column(BOOLEAN)

class Leads(Base):
    __tablename__ = 'leads_info'
    __table_args__ = {"schema": "whatsapp_service"}

    lead_id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(VARCHAR(50)) 
    phone_number = Column(VARCHAR(50))
    email = Column(VARCHAR(50))
    whatsapp = Column(VARCHAR(50))
    tg = Column(VARCHAR(50))
    manager_username = Column(VARCHAR(50))
    lang = Column(VARCHAR(10))
    ls_start = Column(DateTime)
    ls_answer = Column(DateTime)
    ls_agree = Column(DateTime)
    ls_ping = Column(DateTime)

class Arrangements(Base):
    __tablename__ = 'sls_incoming_wh_arrangements'
    __table_args__ = {"schema": "whatsapp_service"}

    arrangement_id = Column(Integer, primary_key = True, autoincrement = True)
    client_id = Column(VARCHAR(50))
    platform = Column(VARCHAR(50))
    datetime = Column(DateTime)