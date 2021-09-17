import requests, json, requests_cache
from datetime import datetime
from dateutil import tz
from dotenv import load_dotenv
import dateutil.parser
import os
load_dotenv()  # take environment variables from .env.

requests_cache.install_cache(cache_name='.cache', backend='filesystem', expire_after=18000)

PAGE_ID = "1444572979139258"
BASE = "https://graph.facebook.com/v12.0"

url = f"{BASE}/{PAGE_ID}/events"
params = (
    ('access_token', os.environ.get("TOKEN")),
)

response = requests.get(url, params=params).json()
data = response['data']

# print(response["paging"]["next"])
try:
    while True:
        print(response["paging"]["next"])
        response = requests.get(response["paging"]["next"]).json()
        data.extend(response['data'])
except KeyError: # no more pages
    pass

print("\n\n")
# remember to save data
# with open('docs/data.json', 'w') as outfile:
#     json.dump(response, outfile)

for event in data:
    name = event.get("name", "")
    time = dateutil.parser.isoparse(event.get("start_time", ""))
    place = event.get("place", {}).get("name", "")
    description = event.get("description", "")

    # check if event is in the future
    london = tz.gettz('Europe/London')
    if time > datetime.now(tz=london):
        print("=======================================")
        print(f"{name} @ {place}")
        print(f"{time}")
        print(f"{description}")
        print("=======================================\n\n")
