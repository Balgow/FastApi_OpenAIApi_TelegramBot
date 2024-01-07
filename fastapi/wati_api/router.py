from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from .schemas import *
from .wati import WATI
from .web_application_api_aI import WebApplicationApiAI
from fastapi.encoders import jsonable_encoder
import requests


router = APIRouter()


@router.get("/get_message_templates/")
async def get_message_templates():
    wati = WATI()
    return wati.getMessageTemplates()

@router.get("/get_messages/")
async def get_messages(number):
    try:
        wati = WATI()
        return wati.getMessages(number)
    except Exception as inst:
            raise HTTPException(status_code=500, detail=jsonable_encoder(inst))

@router.get("/get_last_owner_message/")
async def get_last_owner_message(number):
    try:
        wati = WATI()
        message_list = wati.getMessages(number)

        text = '-'
        for element in message_list.get('messages', {}).get('items', []):
            if element.get('eventType', '') == 'message' and element.get('owner', True) == False:
                text = element.get('text', '')
                break

        return text
    except Exception as inst:
            raise HTTPException(status_code=500, detail=jsonable_encoder(inst))

@router.post("/new_message_webhook/")
async def new_message_webhook(params: WebhookMessageDTO):
    resp_data = {}

    try:
        wati = WATI()
        message_list = wati.getMessages(params.waId)

        text = ''
        for element in message_list.get('messages', {}).get('items', []):
            if element.get('eventType', '') == 'message' and element.get('owner', True) == False:
                text = element.get('text', '')
                break

        if text != "":
            resp_data['text'] = text

            apiAi = WebApplicationApiAI()
            ai_params = {
                "client_id": "whatsapp_" + params.waId,
                "message": text
            }
            response = apiAi.getAnswer(ai_params)

            response_text = response.get('message', '')

            if response_text != '':
                resp_data['response_text'] = response_text

                return wati.sendMessage({'number': params.waId, 'text': response_text})
    except Exception as inst:
        raise HTTPException(status_code=500, detail=jsonable_encoder({'inst': inst, 'data': resp_data}))

    return resp_data

@router.post("/send_template_messages/")
async def send_template_messages(params: SendTemplateMessagesDTO):
    wati = WATI()
    return wati.sendTemplateMessages(jsonable_encoder(params))

@router.post("/send_message/")
async def send_message(params: SendMessageDTO):
    wati = WATI()
    return wati.sendMessage(jsonable_encoder(params))