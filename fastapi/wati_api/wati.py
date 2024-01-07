import requests

class WATI():
    api_endpoint = ""
    access_token = ''
    def getMessageTemplates(self):
        url = self.api_endpoint + "/api/v1/getMessageTemplates"
        headers = {
            "Authorization": self.access_token
        }
        response = requests.get(url, headers=headers)

        return response.json()

    def getMessages(self, phone_number):
        url = self.api_endpoint + "/api/v1/getMessages/" + phone_number
        headers = {
            "Authorization": self.access_token
        }
        response = requests.get(url, headers=headers)

        return response.json()

    def sendTemplateMessages(self, params):
        url = self.api_endpoint + "/api/v1/sendTemplateMessages"
        headers = {
            "content-type": "text/json",
            "Authorization": self.access_token
        }
        response = requests.post(url, json=params, headers=headers)

        return response.json()

    def sendMessage(self, params):
        url = self.api_endpoint + "/api/v1/sendSessionMessage/" + params.get("number") + "?messageText=" + params.get("text")
        headers = {
            "Authorization": self.access_token
        }
        response = requests.post(url, json=params, headers=headers)

        return response.json()