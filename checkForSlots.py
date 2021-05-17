import requests
import json
from datetime import datetime, timedelta, date

centers = {}
try:
    resp = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=8&"
        "date=17-05-2021",
        headers={"accept": "application/json", "accept-language": "hi_IN", "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} )
except Exception as e:
    print(e.with_traceback())
#print(resp.text)
centers = json.loads(resp.content.decode("utf-8"))["centers"]
for center in centers:
    if(center["center_id"] == 599686):
        print("Apollo Found")
        apollo = center
        sessions = apollo["sessions"]
        for session in sessions:
            if(session["available_capacity"] > 0 ):
                print("Slot available", session)
            else:
                print("No Slot")

