from .models import *
from sqlalchemy.orm import Session
from .schemas import *
from datetime import datetime, timedelta

def add_manager_if_not_exists(message: Manager, db: Session):

    existing_record = db.query(Managers).filter(Managers.username == message.username).one_or_none()

    if existing_record:
        for key, value in message.dict().items():
            setattr(existing_record, key, value)
        db.commit()

    else:
        new_record = Managers(**message.dict())
        db.add(new_record)
        db.commit()
        db.refresh(new_record) 

def veryfy_manager_by_username(username: str, db: Session):
    return db.query(
        # Managers.password
        Managers
    ).filter(Managers.username == username).all()

def add_lead_if_not_exists(message: Lead_adder, db: Session):

    existing_record = db.query(Leads).filter((Leads.name == message.name) & (Leads.tg == message.tg)).one_or_none()

    if existing_record:
        for key, value in message.dict().items():
            setattr(existing_record, key, value)
        db.commit()

    else:
        new_record = Leads(**message.dict())
        db.add(new_record)
        db.commit()
        db.refresh(new_record) 
    
    
def get_last_five_leads(db: Session):
    return db.query(
        Leads
    ).order_by(Leads.lead_id.desc()).limit(5).all()


def get_last_leads_not_started(db: Session):
    return db.query(Leads).filter(Leads.ls_start == None).all()

def get_not_answering_leads(db: Session):
    not_answering_leads = db.query(Leads).filter(Leads.ls_answer != None).filter(Leads.ls_agree == None).all()
    return_not_answering_leads = []

    for lead in not_answering_leads:
        if (datetime.now() - lead.ls_answer).days >= 1:
            return_not_answering_leads.append(lead)
    return return_not_answering_leads

def get_leads_meeting_in_hour(db: Session):
    return db.query(Arrangements).filter(Arrangements.datetime < datetime.now() + timedelta(hours=1)).all()
    
