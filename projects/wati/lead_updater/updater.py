import requests
from .creds import DOMEN


def update():
    url = f"https://{DOMEN}/lead_add/get_last_leads_not_started"
    response = requests.get(url)
    return response.json()
