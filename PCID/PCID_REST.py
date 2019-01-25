import json
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote


class PCID(object):

    def __init__(self, baseurl, username, password):
        """"
        This class is used to work with Oracle Identity Cloud Service (Oracle IDCS)
        """

        self.baseurl = baseurl
        self.username = username
        self.password = password


    def GetToken(self) -> str:
        """
        Retrieve authorization token

        :return: Bearer authorization token
        """

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


    def GetLogs(self, filter) -> str:
        """
        Retrieve logs using authorization token

        :return: logs in JSON format
        """

        url = f"{self.baseurl}/admin/v1/AuditEvents?{filter}"
        token = PCID(self.baseurl, self.username, self.password).GetToken()

        headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }

        response = requests.get(url=url, headers=headers)
        return json.loads(response.text)


if __name__ == '__main__':

    # Open up the config file to use the configuration parameters
    with open("Config.json", "r") as file:
        data = json.load(file)

        # Generate a start and date time to be used as parameters for the query. Set for 5 minute gaps.
        start_time = datetime.now() - timedelta(minutes=5)
        end_time = datetime.now()
        filter_formatted = data["queryFormatted"]

        time_list = {
            "startYear": start_time.strftime('%Y'),
            "startMonth": start_time.strftime('%m'),
            "startDay": start_time.strftime('%#j'),
            "startHour": start_time.strftime('%H'),
            "startMinute": start_time.strftime('%M'),
            "startSecond": start_time.strftime('%S'),
            "endYear": end_time.strftime('%Y'),
            "endMonth": end_time.strftime('%m'),
            "endDay": end_time.strftime('%#j'),
            "endHour": end_time.strftime('%H'),
            "endMinute": end_time.strftime('%M'),
            "endSecond": end_time.strftime('%S')}

        # Insert the generated time values into the query string
        for key in time_list.keys():
            filter_formatted = filter_formatted.replace(key, str(time_list[key]))
        # Encode the query string into proper format (e.g. replace whitespace with %20
        parameters = urlencode({"filter": filter_formatted}, quote_via=quote)
        # Grab log from REST API client
        logs = PCID(data["client_domain"], data["username"], data["password"]).GetLogs(parameters)
        # Write the output to a JSON file
        with open(f"{start_time.strftime('%Y-%m-%#j_%H-%M-%S_PCID.json')}", "w+") as filewrite:
            json.dump(logs, filewrite)


