from telebot import TeleBot
import openai
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import datetime
import os


bot_token =  os.environ.get('TELEGRAM_API_KEY')
openai.api_key = os.environ.get('OPENAI_API_KEY')
DOMEN =  os.environ.get('DOMEN')

class Bot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.notification_chat_id = ''

    def start(self, message):
        self.bot.send_message(message.chat.id, 'Выберите действие', reply_markup = self.start_buttons_markup())
        # self.bot.send_message(message.chat.id, message.chat.id)
        

    def start_buttons_markup(self):
        markup = ReplyKeyboardMarkup()
        markup.add(KeyboardButton(text = 'Просмотреть текущий промпт'))
        return markup
    
    
    def echo(self, message):
        if message.text == 'Просмотреть текущий промпт':
        
            url = f"https://{DOMEN}/marketing/get_prompts"

            response = requests.get(url)

            if response.status_code == 200:
                prompts = response.json()
            else:
                print(f"Error: {response.json()}")
                return


            output = ''
            
            for pmt in prompts:
                output += pmt['role'] + ': '
                output += pmt['message'] + '\n\n'
            self.bot.send_message(message.chat.id, output)

        else:
            url = f"https://{DOMEN}/marketing/get_prompts"
            response = requests.get(url)

            if response.status_code == 200:
                sys_prompts = response.json()
            else:
                print(f"Error: {response.json()}")
                return


            url = f"https://{DOMEN}/marketing/get_messages"
            response = requests.post(url, json={'client_id': str(message.chat.id)})

            if response.status_code == 200:
                user_chat = response.json()
            else:
                print(f"Error: {response.json()}")
                return
            gpt_prompts=[
                    *[{'role': pmt['role'], 'content': pmt['message']} for pmt in sys_prompts],
                    *[{'role': 'assistant' if msg['is_bot'] else 'user', 'content': msg['message']} for msg in user_chat],
                    {'role': 'user', 'content': message.text}
            ]
            # post request to gpt get answer
            # todo
            gpt_answer = gpt_prompts[-1]['content']


            chat_message = {
                'client_id': str(message.chat.id),
                'message':  message.text,
                'is_bot': False
            }


            url = f"https://{DOMEN}/marketing/chat_messages/"
            
            response = requests.post(url, json=chat_message)

            if response.status_code == 200:
                pass
            else:
                print(f"Error: {response.json()}")
                return
            
            self.bot.send_message(message.chat.id,  gpt_answer)

            chat_message = {
                'client_id': str(message.chat.id),
                'message': gpt_answer,
                'is_bot': True
            }

            url = f"https://{DOMEN}/meeting_arrange/chat_messages/"
            
            response = requests.post(url, json=chat_message)

            if response.status_code == 200:
                pass
            else:
                print(f"Error: {response.json()}")
                return


    def run(self):
        
        @self.bot.message_handler(commands = ['start'])
        def handle_start(message):
            self.start(message)


        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            self.echo(message)
        
        print(' *** Bot is running *** ')
        self.bot.polling(none_stop = True)



bot = Bot(bot_token)
bot.run()
