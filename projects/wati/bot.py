import requests
import time
from lead_updater.updater import update
from creds import FIRST_MESSAGE, DOMEN

def main():
    while True:
        leads = update()
        if leads:
            print(' *** New leads *** ')
            
            for lead in leads:
                data = {
                    "number": lead['phone_number'],
                    "text": FIRST_MESSAGE
                }
                print(data)
                url = f"http://{DOMEN}/wati/send_message/"

                response = requests.post(url, json=data)
                if response.status_code == 200:
                    print(f'Message sent to {lead["phone_number"]}')

                
        else:
            print(' *** No new leads *** ')
        # time.sleep(600) 






main()