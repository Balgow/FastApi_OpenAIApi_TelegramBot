from fastapi import FastAPI
from telebot_lead_adder_api import databases as lead_adder_database, router as lead_adder_router, models as lead_adder_models
from telebot_meeting_arranger_api import databases as meeting_arranger_database, router as meeting_arranger_router, models as meeting_arranger_models
from wati_api import router as wati_router
from telebot_marketing_api import router as marketing_router, models as marketing_models, databases as marketing_database

from sls_incoming_wh_api import router as sls_incoming_wh_router, models as sls_incoming_wh_models, databases as sls_incoming_wh_database
from sls_outgoing_wh_api import router as sls_outgoing_wh_router, models as sls_outgoing_wh_models, databases as sls_outgoing_wh_database
from akt_outgoing_wh_api import router as akt_outgoing_wh_router, models as akt_outgoing_wh_models, databases as akt_outgoing_wh_database

from email_endpoint.akt_outgoing_email_api import databases as akt_outgoing_email_database, router as akt_outgoing_email_router, models as akt_outgoing_email_models
from email_endpoint.sls_outgoing_email_api import databases as sls_outgoing_email_database, router as sls_outgoing_email_router, models as sls_outgoing_email_models

from telegram_endpoint.sls_outgoing_tg_api import databases as sls_outgoing_tg_database, router as sls_outgoing_tg_router, models as sls_outgoing_tg_models

lead_adder_models.Base.metadata.create_all(bind=lead_adder_database.engine)
meeting_arranger_models.Base.metadata.create_all(bind=meeting_arranger_database.engine)
marketing_models.Base.metadata.create_all(bind=marketing_database.engine)
sls_incoming_wh_models.Base.metadata.create_all(bind=sls_incoming_wh_database.engine)
sls_outgoing_wh_models.Base.metadata.create_all(bind=sls_outgoing_wh_database.engine)
akt_outgoing_wh_models.Base.metadata.create_all(bind=akt_outgoing_wh_database.engine)

akt_outgoing_email_models.Base.metadata.create_all(bind=akt_outgoing_email_database.engine)
sls_outgoing_email_models.Base.metadata.create_all(bind=sls_outgoing_email_database.engine)

sls_outgoing_tg_models.Base.metadata.create_all(bind=sls_outgoing_tg_database.engine)

app = FastAPI()


@app.get('/')
async def home():
    return {'msg':'You got message'}

app.include_router(lead_adder_router.router, prefix = '/lead_add', tags =['lead_add'])
app.include_router(meeting_arranger_router.router, prefix = '/meeting_arrange', tags =['meeting_arrange'])
app.include_router(wati_router.router, prefix = '/wati', tags =['wati'])
app.include_router(marketing_router.router, prefix = '/marketing', tags =['marketing'])
app.include_router(sls_incoming_wh_router.router, prefix = '/sls_incoming_whatsapp', tags =['sls_incoming_whatsapp'])
app.include_router(sls_outgoing_wh_router.router, prefix = '/sls_outgoing_whatsapp', tags =['sls_outgoing_whatsapp'])
app.include_router(akt_outgoing_wh_router.router, prefix = '/akt_outgoing_whatsapp', tags =['akt_outgoing_whatsapp'])

app.include_router(akt_outgoing_email_router.router, prefix = '/akt_outgoing_email', tags =['akt_outgoing_email'])
app.include_router(sls_outgoing_email_router.router, prefix = '/sls_outgoing_email', tags =['sls_outgoing_email'])

app.include_router(sls_outgoing_tg_router.router, prefix = '/sls_outgoing_telegram', tags =['sls_outgoing_telegram'])

from test_api import router as test_router, models as test_models, databases as test_database
test_models.Base.metadata.create_all(bind=test_database.engine)
app.include_router(test_router.router, prefix = '/test', tags =['test'])