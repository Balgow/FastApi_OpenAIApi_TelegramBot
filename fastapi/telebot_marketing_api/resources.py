OPENAI_API_KEY = ''
BOT_TOKEN = ''
NOTIFICATION_CHAT_ID = ''
FIRST_MESSAGE = ''
NOTIFICATION_MESSAGE = ''
NO_ANSWER_MESSAGE = ''


import os
import sys
import requests
import datetime

def send_notification_to_hr_chat(message):

    send_message_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {'chat_id': NOTIFICATION_CHAT_ID, 'text': message}
    requests.get(send_message_url, params=params)

def send_logs_to_hr_chat(logs_file):
    send_document_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    params = {'chat_id': NOTIFICATION_CHAT_ID}
    
    requests.get(send_document_url, params=params, files={'document': open(logs_file, 'rb')})
   
def add_to_leads(event):
    try:
        dt = datetime.datetime.now()

        send_message_url = f''
        params = {
            'token': '', 
            'leadName': event.get('name'),
            'leadEmail': 'TG' + str(dt.timestamp()) + '@tg.com',
            'leadTel': '+79999999999',
            'leadCountry': 'RU',
            'leadSource': 'tginvesta',
            'prefferedCallTime': event.get('date') + ' ' + event.get('time'),
            'leadKeyword': '',
            'affiliateCode': 'RSLSI',
            'messenger': event.get('client_id'),
            'redirectUrl': 'TG'
        }

        requests.post(send_message_url, json=params)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

def check_if_last_message(parsable_text):
    if 'имя' in parsable_text.lower() and 'дата' in parsable_text.lower() and 'время' in parsable_text.lower():
        return True
    else:
        return False

def parse_gpt_answer(text):

    event = {
        'name': '',
        'date': '',
        'time': '',
        'platform': ''
    }

    if 'имя' in text.lower():
        start_index = text.lower().find('имя')
        end_index = text.lower().find('\n', start_index)
        event['name'] = text[start_index + 5:end_index]
    
    if 'дата' in text.lower():
        start_index = text.lower().find('дата')
        end_index = text.lower().find('\n', start_index)
        event['date'] = text[start_index + 6:end_index]

    if 'время' in text.lower():
        start_index = text.lower().find('время')
        end_index = text.lower().find('\n', start_index)
        event['time'] = text[start_index + 7:end_index]

    if 'онлайн-встреч' in text.lower():
        start_index = text.lower().find('онлайн-встреч')
        end_index = text.lower().find('\n', start_index)
        event['platform'] = text[start_index + 16:end_index]
    elif 'платформ' in text.lower():
        start_index = text.lower().find('платформ')
        end_index = text.lower().find('\n', start_index)
        event['platform'] = text[start_index + 30:end_index]
    
    if 'послезавтра' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=2)
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'сегодня' in event['date'].lower():
        event['date'] = datetime.date.today().strftime('%d.%m.%Y')
    elif 'завтра' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=1)
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'понедельник' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=7 - datetime.date.today().weekday() if datetime.date.today().weekday() != 6 else 1)
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'вторник' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=1 - datetime.date.today().weekday() if 1 - datetime.date.today().weekday() > 0 else 8 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'сред' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=2 - datetime.date.today().weekday() if 2 - datetime.date.today().weekday() > 0 else 9 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'четверг' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=3 - datetime.date.today().weekday() if 3 - datetime.date.today().weekday() > 0 else 10 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'пятниц' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=4 - datetime.date.today().weekday() if 4 - datetime.date.today().weekday() > 0 else 11 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'суббот' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=5 - datetime.date.today().weekday() if 5 - datetime.date.today().weekday() > 0 else 12 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')
    elif 'воскресен' in event['date'].lower():
        event['date'] = datetime.date.today() + datetime.timedelta(days=6 - datetime.date.today().weekday() if 6 - datetime.date.today().weekday() > 0 else 13 - datetime.date.today().weekday())
        event['date'] = event['date'].strftime('%d.%m.%Y')

    return event


