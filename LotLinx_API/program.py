""""
TODO:
- Basic error handling should be implemented, but no heroics necessary.
- The URLs for images to be processed should be inputs to the program, as arguments, stdin or read from a file.
- API responses should be logged
- Provide a ZIP/archive of the program code, logged output and resulting images downloaded from the API results.
"""

from logging import FileHandler
import requests
import logging
import credentials


# Init Logging
logger = logging.getLogger("LotLinxAPI")
filehandle = logging.FileHandler("LogLinx.log")
format = logging.Formatter("%(asctime)")
logger.addHandler(filehandle)

# API Authentication credentials
username = credentials.username
password = credentials.password
session = requests.Session()
session.auth = (username, password)

base_url = "https://photoai.lotlinx.com"



# 1) Submit Requests
def PostRequest(dealerId, vehicleId, imageId, imageUrl):
    endpoint = base_url + "/images/optimize"
    data = [{"dealerId": dealerId,
            "vehicles": [{"id": vehicleId,
                        "images": [{"imageId": imageId, "imageUrl": imageUrl}]}]
            }]
    resp = session.post(url=endpoint, json=data)
    resp.raise_for_status()
    return resp


# 2) GET REQUEST to query using token
def GetStatus(token):
    endpoint = base_url + f"/images/{token}/status"
    resp = session.get(url=endpoint)
    resp.raise_for_status()
    return resp


# 2b) GET REQUEST to query using specified status and start date
def GetRequest(status, startDate):
    endpoint = base_url + f"/images/requests?status={status}&startDate={startDate}"
    resp = session.get(url=endpoint)
    resp.raise_for_status()
    return resp


# 3) LOAD RESPONSE using token
def GetResponse(token):
    endpoint = base_url + f"/images/{token}"
    resp = session.get(url=endpoint)
    resp.raise_for_status()
    return resp


if __name__ == '__main__':
    # 1) POST
    # post = PostRequest(dealerId=9876655, vehicleId=987676, imageId=76554, imageUrl="https://img.lotlinx.com/vdn/7416/jeep_wrangler%20unlimited_2014_1C4BJWFG3EL326863_7416_5_339187295.jpg")
    # post = post.json()
    # token = post["data"][0]["token"]
    token="51uA18oltVr6S0SdY2EDZhczppOrC4LALCTSyDu8cCslvYVHQLYmwu6hgz2kHTua"

    # 2) GET /w Token
    getStat = GetStatus(token)
    # 2b) GET /w status & startdate
    getReq = GetRequest("completed", "2018-09-05T01:22:33")
    getReq = getReq.json()

    # 3) GET LOAD RESPONSE
    load = GetResponse(token)
    load = load.json()
    print(load)
