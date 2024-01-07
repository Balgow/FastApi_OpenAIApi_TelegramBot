from telebot import TeleBot
import openai
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import datetime
import json
import time
import os


PASSWORD = ''


bot_token =  os.environ.get('TELEGRAM_API_KEY')
openai.api_key = os.environ.get('OPENAI_API_KEY')
DOMEN =  os.environ.get('DOMEN')


class Bot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.columns = {'Name': None, 
                        'Phone Number': None, 
                        'Email': None, 
                        'Whatsapp': None, 
                        'TG': None, 
                        'Lang': None
                        }
        
    
    def start(self, message):
        self.bot.send_message(message.chat.id, "Bot is running")
        if self.manager_verification(message):
            self.bot.send_message(message.chat.id, 'Send lead parameters in the following form:\n\nfullName, phone, email, whatsapp, tg, lang\n\nExample:\n\nJohn Malik, 8978456123, test@gmail.com, None, john_tg, ru')

    def last_leads(self, message):
        url = f"https://{DOMEN}/lead_add/get_last_leads"
        response = requests.get(url)
        if response.json():
            for row in response.json():
                self.bot.send_message(message.chat.id, f'{row["name"]}, {row["phone_number"]}, {row["email"]}, {row["whatsapp"]}, {row["tg"]}, {row["lang"]}')
        else:
            self.bot.send_message(message.chat.id, 'There is no rows yet.')
 
    
    def manager_adding(self, message):
        if message.text == PASSWORD:
            meeting_creds = {
                'username': str(message.from_user.username),
                'password': str(PASSWORD)
            }

            url = f"https://{DOMEN}/lead_add/add_manager/"
            response = requests.post(url, json=meeting_creds)
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id, message.from_user.username + ' was added')
        else:
            pass
        

    def manager_verification(self, message):
        params = {
            "message": str(message.from_user.username)
        }
        url = f"https://{DOMEN}/lead_add/verify_manager/"
        response = requests.post(url, params=params)
        if response.json() and response.json()[0]['password']==PASSWORD:
            return True
        else:
            self.bot.send_message(message.chat.id, 'Secret Key:')
            return False

    # def query_handler(self, call):
    #     message = call.message
    #     data = call.data
    #     self.bot.send_message(message.chat.id, 'Send lead parameters in the following form:\n\nfullName,phone,email,whatsapp,telegram,lang')
        
    def add_lead(self, message):
        try:
            name, phone_number, email, whatsapp, tg, lang = message.text.split(',')
            if tg.strip()[0] == '@':
                tg = tg.strip()[1:]
            lead_data = {
                'name': name.strip(), 
                'phone_number': phone_number.strip(),
                'email': email.strip(),
                'whatsapp': whatsapp.strip(),
                'tg': tg.strip(),
                'manager_username': str(message.from_user.username),
                'lang': lang.strip()
            }

            url = f"https://{DOMEN}/lead_add/add_lead/"
            response = requests.post(url, json=lead_data)
            if response.status_code != 200:
                raise

            self.bot.send_message(message.chat.id, message.from_user.username + ' added 1 more lead. Use /last_leads to see last added leads')

        except:
            self.bot.send_message(message.chat.id, 'Please write in the following format\n\nfullName, phone, email, whatsapp, telegram, lang\n\nExample:\n\nJohn Malik, 8978456123, test@gmail.com, None, john_tg, ru')
        
    def echo(self, message):
        self.manager_adding(message)
        if self.manager_verification(message):
            self.add_lead(message)

        


    def run(self):
        
        @self.bot.message_handler(commands = ['start'])
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(commands = ['last_leads'])
        def handle_message(message):
            self.last_leads(message)

        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            self.echo(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            self.query_handler(call)

        print(' *** Bot is running *** ')
        self.bot.polling(none_stop = True)

bot = Bot(bot_token)
bot.run()
