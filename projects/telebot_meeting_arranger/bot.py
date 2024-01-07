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
        self.first_message = ''
        self.notification_chat_id = ''

    def start(self, message):
        self.bot.send_message(message.chat.id, 'Выберите действие', reply_markup = self.start_buttons_markup())

    def send_message_to_hr_chat(self, message):
        self.bot.send_message(self.notification_chat_id, message)
        

    def start_buttons_markup(self):
        markup = ReplyKeyboardMarkup()
        markup.add(KeyboardButton(text = 'Просмотреть текущий промпт'))
        markup.add(KeyboardButton(text = 'Приветсвенное сообщение'))
        markup.add(KeyboardButton(text = 'Обнулить контекст'))
        return markup
    
    def parse_gpt_answer_final(self, text):
        def get_day_delta(need_day):
            now_day = int(datetime.datetime.now().strftime("%w"))
            day_delta = need_day - now_day
            if day_delta == 0:
                day_delta = 7
            elif day_delta < 0:
                day_delta = 7 + day_delta
                
            return day_delta


        
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')

        event = {
            'name': '',
            'email': '',
            'phone': '',
            'date': '',
            'time': '',
            'platform': '',
            # 'timestamp': 0
        }

        ''' Get Name '''
        
        str_start = text.lower().find('имя: ')
        if  str_start > 0:
            str_start = str_start + 5
            str_end = text.find('\n', str_start)
            event['name'] = text[str_start:str_end]

        ''' Get Email '''
        
        str_start = text.lower().find('почта: ')
        if  str_start > 0:
            str_start = str_start + 7
            str_end = text.find('\n', str_start)
            event['email'] = text[str_start:str_end]

        ''' Get Phone '''
        
        str_start = text.lower().find('телефон: ')
        if  str_start > 0:
            str_start = str_start + 9
            str_end = text.find('\n', str_start)
            event['phone'] = text[str_start:str_end]


        ''' Get Date '''
        str_start = text.lower().find('дата: ')
        if  str_start > 0:
            str_start = str_start + 6
            str_end = text.find('\n', str_start)
            event['date'] = text[str_start:str_end]

        ''' Get Time '''
        str_start = text.lower().find('время: ')
        if  str_start > 0:
            str_start = str_start + 7
            str_end = text.find('\n', str_start)
            event['time'] = text[str_start:str_end]
        elif text.lower().find('в '):
            str_start = str_start + 2
            str_end = text.find('\n', str_start)
            event['time'] = text[str_start:str_end]
            

        ''' Get Time '''
        search_text = 'платформа для встречи: '
        str_start = text.lower().find(search_text)
        if  str_start > 0:
            str_start = str_start + len(search_text)
            str_end = text.find('\n', str_start)
            event['platform'] = text[str_start:str_end]



        now = datetime.datetime.now()
        if event['date'].lower().find('завтра'):
            new_date = now + datetime.timedelta(days=1)
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('послезавтра'):
            new_date = now + datetime.timedelta(days=2)
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('понедельник') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(1))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('вторник') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(2))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('сред') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(3))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('четверг') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(4))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('пятниц') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(5))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('суббот') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(6))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
        elif event['date'].lower().find('воскресен') >= 0:
            new_date = now + datetime.timedelta(days=get_day_delta(7))
            event['date'] = datetime.datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")

        event['datetime'] = datetime.datetime.strptime(event['date'] + ' ' + event['time'], "%Y-%m-%d %H:%M")
        # event['timestamp'] = datetime.datetime.strptime(event['date'] + ' ' + event['time'], "%Y-%m-%d %H:%M").timestamp()

        return event


    def echo(self, message):
        if message.text == 'Просмотреть текущий промпт':
        
            url = f"https://{DOMEN}/meeting_arrange/get_prompts"

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

        elif message.text == 'Обнулить контекст':
            
            url = f"https://{DOMEN}/meeting_arrange/clear_chat/"
            response = requests.post(url, json={'client_id': str(message.chat.id)})
            if response.status_code == 200:
                prompts = response.json()
            else:
                print(f"Error: {response.json()}")
                return
            
            self.bot.send_message(message.chat.id, 'Контекст обнулен')
            print(response.json())
        

        elif message.text == 'Приветсвенное сообщение':
            self.bot.send_message(message.chat.id, self.first_message)

            chat_message = {
                'client_id': str(message.chat.id),
                'message': self.first_message,
                'is_bot': True
            }

            url = f"https://{DOMEN}/meeting_arrange/chat_messages/"
            
            response = requests.post(url, json=chat_message)

            if response.status_code == 200:
                pass
            else:
                print(f"Error: {response.json()}")
                return
            

            
        else:
            url = f"https://{DOMEN}/meeting_arrange/get_prompts"
            response = requests.get(url)

            if response.status_code == 200:
                sys_prompts = response.json()
            else:
                print(f"Error: {response.json()}")
                return


            url = f"https://{DOMEN}/meeting_arrange/get_messages"
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
            while True:
                try:
                    gpt_answer = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages = gpt_prompts
                    )
                    break
                except:
                    print('Trying again')

            parsable_text = gpt_answer['choices'][0]['message']['content']
            if 'Имя' in parsable_text \
            and 'Платформа для встречи' in parsable_text \
            and 'Телефон' in parsable_text \
            and 'Дата' in parsable_text \
            and 'Почта' in parsable_text:
                print(notification_message := self.parse_gpt_answer_final(parsable_text))
                output_msg = f'''Имя: {notification_message['name']}
Платформа для встречи: {notification_message['platform']}
Телефон: {notification_message['phone']}
Дата: {notification_message['date']}
Время: {notification_message['time']}
Почта: {notification_message['email']}'''
                # self.bot.send_message(self.notification_chat_id, str(notification_message)[1:-1].replace(', ', '\n'))
                self.bot.send_message(message.chat.id, output_msg)

                client_creds = {
                    'client_id': str(message.from_user.id),
                    'username': str(message.from_user.username),
                    'fullname': str(notification_message['name']),
                    'email': str(notification_message['email']),
                    'phone': str(notification_message['phone'])
                }

                url = f"https://{DOMEN}/meeting_arrange/add_client/"
                response = requests.post(url, json=client_creds)

                meeting_creds = {
                    'client_id': str(message.from_user.id),
                    'platform': str(notification_message['platform']),
                    'datetime': str(notification_message['datetime'])
                }

                url = f"https://{DOMEN}/meeting_arrange/arrange_meeting/"
                response = requests.post(url, json=meeting_creds)

            chat_message = {
                'client_id': str(message.chat.id),
                'message':  message.text,
                'is_bot': False
            }


            url = f"https://{DOMEN}/meeting_arrange/chat_messages/"
            
            response = requests.post(url, json=chat_message)

            if response.status_code == 200:
                pass
            else:
                print(f"Error: {response.json()}")
                return
            
            self.bot.send_message(message.chat.id, gpt_answer['choices'][0]['message']['content'])

            chat_message = {
                'client_id': str(message.chat.id),
                'message': gpt_answer['choices'][0]['message']['content'],
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
