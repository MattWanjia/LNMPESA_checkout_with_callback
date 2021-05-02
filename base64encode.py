import json

import requests
from requests.auth import HTTPBasicAuth

consumer_key = "aGhPIiqKd0woACQIu0Wdez9xw8l4oR43"
consumer_secret = "SYYixpy9HBHNjW0X"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print(r.text)
json_object = json.loads(r.text)
token = json_object['access_token']
print(token)