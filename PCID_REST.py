import json
import requests
import pprint

class PCID(object):

    def __init__(self):
        self.baseurl = "XXXXXXXXXXXXXXXXXXXXX.identity.oraclecloud.com"
        self.username = "XXXXXXXXXXXXXXXXXXXX"
        self.password = "XXXXXXXXXXXXXXXXXXXX"


    def GetToken(self):
        token_url = f"{self.baseurl}/oauth2/v1/token"

        # Headers of GET request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Body of GET request
        data = {
            "grant_type":"client_credentials",
            "scope": "urn:opc:idm:__myscopes__",
             }

        # Create session with username and password
        session = requests.Session()
        session.auth = (self.username, self.password)
        # submit POST request with header and body
        response = session.post(url=token_url, headers=headers, data=data)
        # Get the TOKEN from the JSON response
        return json.loads(response.text)['access_token']


    def GetLogs(self, filter):
        url = f"{self.baseurl}/admin/v1/AuditEvents?filter={filter}"
        token = PCID().GetToken()

        headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }

        response = requests.get(url=url, headers=headers)
        return json.loads(response.text)


if __name__ == '__main__':
    filter = "eventId%20eq%20%22sso.session.create.success%22"
    logs = PCID().GetLogs(filter)
    pprint.pprint(logs)
