""""
TODO:
- Basic error handling should be implemented, but no heroics necessary.
- The URLs for images to be processed should be inputs to the program, as
  arguments, stdin or read from a file.
- API responses should be logged
- Provide a ZIP/archive of the program code, logged output and resulting images
  downloaded from the API results.
"""

import credentials #credential.py to store api user/pass
import requests
import logging
import time
import pprint

# API Authentication credentials
username = credentials.username
password = credentials.password
session = requests.Session()
session.auth = (username, password)

base_url = "https://photoai.lotlinx.com"

logging.basicConfig(filename=f"LogLinx.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")


# 1) Submit Requests
def PostRequest(dealerId, vehicleId, imageId, imageUrl):
    try:
        endpoint = base_url + "/images/optimize"
        data = [{
                "dealerId": dealerId,
                "vehicles": [{
                            "id": vehicleId,
                            "images": [{
                                        "imageId": imageId,
                                        "imageUrl": imageUrl
                                      }]
                            }]
                }]
        logging.info(msg="POST request for dealerId: {}, vehicleId: {}, imageId:{}, "
                         "imageUrl: {}".format(dealerId, vehicleId, imageId, imageUrl))
        resp = session.post(url=endpoint, json=data)
        # Raise for status in event of non-200 HTTP response
        resp.raise_for_status()
        logging.info(msg="POST Request finished with status code {}".format(resp.status_code))
        return resp

    except requests.exceptions.ConnectionError:
        logging.error("Could not find server; check network connection.")
    except Exception as e:
        logging.error(f"{e}")


# 2) GET REQUEST to query using token
def GetStatus(token):
    try:
        logging.info(f"GET Request with token: {token}")
        endpoint = base_url + f"/images/{token}/status"
        resp = session.get(url=endpoint)
        resp.raise_for_status()
        logging.info("GET Request finished with status code {}".format(resp.status_code))
        return resp
    except Exception as e:
        logging.error(f"{e}")


# 2b) GET REQUEST to query using status and start date
def GetRequest(status, startDate):
    try:
        logging.info(f"GET Request for status: {status} and startDate: {startDate}")
        endpoint = base_url + f"/images/requests?status={status}&startDate={startDate}"
        resp = session.get(url=endpoint)
        resp.raise_for_status()
        logging.info("GET Request finished with status code {}".format(resp.status_code))
        return resp
    except Exception as e:
        logging.error(f"{e}")


# 3) LOAD RESPONSE using token
def GetResponse(token):
    try:
        logging.info(f"GET request for token: {token}")
        endpoint = base_url + f"/images/{token}"
        resp = session.get(url=endpoint)
        resp.raise_for_status()
        logging.info("GET Request finished with status code {}".format(resp.status_code))
        return resp
    except Exception as e:
        logging.error(f"{e}")


if __name__ == '__main__':

    # Get tokens for all images in ImageLinks.txt
    tokens = []
    with open("ImageLinks.txt", "r") as f:
        for line in f:
            # Strip URL otherwise API will not function properly
            line = line.replace("\n", "")
            # 1) POST request for images and tokens
            post = PostRequest(dealerId=9876655, vehicleId=987636, imageId=76554,
                               imageUrl=line)
            try:
                tokens.append(post.json()["data"][0]["token"])
            except AttributeError:
                logging.error("Could not find server; check network connection.")
    
    # 2) GET status /w token
    # Not all image tokens return a successful reply. Generally only 2 or 3 are successful! Successful tokens are stored
    # to be used for retrieving the final image while failed tokens are only logged.
    successfulTokens = []
    for token in tokens:
        while True:
            getStatus = GetStatus(token)
            if getStatus.json()["data"][0]["status"] == "complete":
                successfulTokens.append(token)
                break
            elif getStatus.json()["data"][0]["status"] == "failed":
                logging.error(f"FAILED token: {token} resulted in failed return status")
                break
            else:
                # Wait 2 minutes to poll API again
                print("Sleeping for 120 seconds")
                time.sleep(120)

    # 2b) GET /w status & startdate
    getReq = GetRequest("queued", "2018-09-06T22:00:00")

    # 3) GET LOAD RESPONSE
    for succToken in successfulTokens:
        modified_url = GetResponse(succToken).json()["data"][0]["vehicles"][0]["images"][0]["modifiedUrl"]
        # print(GetResponse(succToken).json()["data"][0]["vehicles"][0]["images"][0]["modifiedUrl"])
        logging.info(f"SUCCESSFUL modified image: {modified_url}")
        print("Run complete for: " + successfulTokens)
