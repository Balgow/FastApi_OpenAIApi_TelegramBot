from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from .crud import *
from .schemas import *
from .databases import *
from .resources import *

descriptions = {
    '/': 'Home',
    '/get_prompts': 'Returns a list of system prompts for the chatbot',
    '/get_messages/': 'Returns a list of messages from chat messages table for the chatbot by client id',
    '/post_messages/': 'Adds a message to the chat messages table',
    '/get_gpt_answer/': '''Generates a GPT answer for the chatbot,\n It first reads the chat messages table, only then generates the answer depending on the last message in the chat messages table''',
    '/get_notification_message/': 'Generates a notification message if client has a arranged meeting within 1 hour',
    '/get_no_answer_message/': 'Generates a message for the client who has not answered for 24 hours',
    '/truncate_chat_messages/': 'Truncates the chat messages for the chatbot for a specific client id'
}

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', summary="Home", description = descriptions['/'])
async def home(db: Session = Depends(get_db)):
    return {'msg':'You are in the telegram sls outgoing api'}

@router.get('/get_prompts', description=descriptions['/get_prompts'])
async def return_prompts(db: Session = Depends(get_db)):
    return get_prompts(db)

@router.post('/get_messages/', description=descriptions['/get_messages/'])
async def return_messages(client_id: ChatMessageID, db: Session = Depends(get_db)):
    return get_messages_by_client_id(client_id, db)

@router.post('/post_messages/' , description=descriptions['/post_messages/'])
async def add_messages(message: ChatMessage, db: Session = Depends(get_db)):
    return post_chat_messages(message, db)

@router.post('/get_gpt_answer/' , description=descriptions['/get_gpt_answer/'])
async def getting_gpt_answer_marketing(client_id: ChatMessageID, db:Session = Depends(get_db)):
    return get_gpt_answer(client_id, db)

@router.post('/get_notification_message/' , description=descriptions['/get_notification_message/'])
async def getting_notification_message(client_id: ChatMessageID, db:Session = Depends(get_db)):
    return get_notification_message(client_id, db)

@router.get('/get_no_answer_message/'   , description=descriptions['/get_no_answer_message/'])
async def getting_no_answer_message(db:Session = Depends(get_db)):
    return get_no_answer_message(db)

@router.post('/truncate_chat_messages/' , description=descriptions['/truncate_chat_messages/'])
async def truncating_chat_messages(client_id: ChatMessageID = None, db:Session = Depends(get_db)):
    return truncate_chat_messages(client_id, db)