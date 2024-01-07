from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from .crud import *
from .schemas import *
from .databases import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def home(db: Session = Depends(get_db)):
    return {'msg':'You are in the telebot_lead_adder api'}


@router.post('/add_manager/')
async def adding_manager(message: Manager, db:Session = Depends(get_db)):
    return add_manager_if_not_exists(message, db)

@router.post('/verify_manager/')
async def verifying_manager(message: str, db:Session = Depends(get_db)):
    return veryfy_manager_by_username(message, db)

@router.post('/add_lead/')
async def adding_lead(message: Lead_adder, db:Session = Depends(get_db)):
    return add_lead_if_not_exists(message, db)

@router.get('/get_last_leads')
async def return_last_leads(db: Session = Depends(get_db)):
    return get_last_five_leads(db)

@router.get('/get_last_leads_not_started')
async def return_last_leads_not_started(db: Session = Depends(get_db)):
    return get_last_leads_not_started(db)

@router.get('/get_leads_not_answering/')
async def return_not_answering_leads(db: Session = Depends(get_db)):
    return get_not_answering_leads(db)

@router.get('/get_leads_meeting_in_hour/')
async def return_leads_meeting_in_hour(db: Session = Depends(get_db)):
    return get_leads_meeting_in_hour(db)