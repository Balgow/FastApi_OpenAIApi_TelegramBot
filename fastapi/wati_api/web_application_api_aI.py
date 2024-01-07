import time
import httpx

class WebApplicationApiAI():
    api_endpoint = ""

    def getAnswer(self, params):
        params["is_bot"] = False

        url = self.api_endpoint + "post_messages/"
        headers = {}
        response = httpx.post(url, json=params)

        if response.status_code == 200:
            response = httpx.post(self.api_endpoint + "get_gpt_answer/", json={"client_id": params["client_id"]}, timeout=50)

        return response.json()