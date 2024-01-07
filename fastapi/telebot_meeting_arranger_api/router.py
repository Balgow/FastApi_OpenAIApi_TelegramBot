from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from .crud import *
from .schemas import *
from .databases import *
from .resources import *


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def home(db: Session = Depends(get_db)):
    return {'msg':'You are in the telebot_meeting_arranger api'}

@router.get('/get_prompts')
async def return_prompts(db: Session = Depends(get_db)):
    return get_prompts(db)
    
@router.post('/chat_messages/')
async def add_messages(message: ChatMessage, db: Session = Depends(get_db)):
    return post_chat_messages(message, db)

@router.post('/clear_chat/')
async def clear_messages(client_id: ChatMessageID, db:Session = Depends(get_db)):
    delete_messages_by_client_id(client_id, db)
    return client_id

@router.post('/get_messages/')
async def get_messages(client_id: ChatMessageID, db:Session = Depends(get_db)):
    return get_messages_by_client_id(client_id, db)
    
@router.post('/add_client/')
async def adding_client(message: Client, db:Session = Depends(get_db)):
    return add_client_if_not_exists(message, db)

@router.post('/arrange_meeting/')
async def arranging_meeting(message: Arrangement, db:Session = Depends(get_db)):
    return add_arrangement(message, db)

@router.post('/get_gpt_answer/')
async def getting_gpt_answer(client_id: ChatMessageID, db:Session = Depends(get_db)):
    return get_gpt_answer(client_id, db)

@router.post('/get_notification_message/')
async def getting_notification_message(client_id: ChatMessageID, db:Session = Depends(get_db)):
    return get_notification_message(client_id, db)

@router.get('/get_no_answer_message/')
async def getting_no_answer_message(db:Session = Depends(get_db)):
    return get_no_answer_message(db)

@router.post('/truncate_chat_messages/')
async def truncating_chat_messages(client_id: ChatMessageID = None, db:Session = Depends(get_db)):
    return truncate_chat_messages(client_id, db)


