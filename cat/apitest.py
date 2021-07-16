import http.client
import json
import dotenv
import os
import requests
from requests.auth import HTTPBasicAuth, _basic_auth_str
from dotenv.main import load_dotenv
load_dotenv()
payload = {
    "grant_type": "password",
    "username": "ninh",
    "password": "huynhhaininh99"
}
auth = HTTPBasicAuth("XsenlcWOyE8KVpokzVNBD2uMj1jCl2UTbmses8JP",
                     "4Tz08DjR8eSf0qiPPDVhAM5RQfOiBEAFQ1dmBU7twiGznzwcMCyIjK8lRNIqL4mRKLmclnbYfdxldDsDZns75cO9V6BUwITrdoi9tod8zIW5ycXzYZpJDuroDAufzzRY")

headers = {'content-type': "application/json"}
res = requests.post("http://localhost:8000/o/token/",
                    data=payload, auth=auth)
data = res.json()
token = data["access_token"]
url = "http://127.0.0.1:8000/translations/en-vie-38000/this%20is%20a%20very%20useful%20api"
headers = {
    "Authorization": "bearer {}".format(token),
}
res = requests.get(url, headers=headers)
print(res.json())
