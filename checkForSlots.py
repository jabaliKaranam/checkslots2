import requests
import json
from datetime import datetime, timedelta
from jproperties import Properties
import logging

configs = Properties()
with open('properties.txt', 'rb') as config_file:
    configs.load(config_file)
MODE = int(configs.get("MODE").data)
CENTER_ID_LIST = configs.get("CENTER_ID_LIST").data
if(not CENTER_ID_LIST == 'ALL'):
    CENTER_ID_LIST =CENTER_ID_LIST.split(',')
DISTRICT_ID = str(configs.get("DISTRICT_ID").data)
IFTTT_WEBHOOK = str(configs.get("IFTTT_WEBHOOK_URL").data)
LOG_LOCATION = str(configs.get("SCRIPT_LOCATION").data)
NOTIFICATION_TYPE = str(configs.get("NOTIFICATION_TYPE").data)
DOSE = str(configs.get("DOSE").data)
VACCINE = str(configs.get("VACCINE").data)


logging.basicConfig(level=logging.INFO, filename='D:/PyStuff/checkslots2/app.log', format='%(asctime)s || %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def main():
    centers = {}
    start_date = datetime.today().date()
    number_of_days = 5
    date_list = []
    for day in range(number_of_days):
      a_date = (start_date + timedelta(days = day))
      date_list.append(a_date.strftime("%d-%m-%y"))
    for date in date_list:
        #time.sleep(5)
        try:
            resp = requests.get(
                "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" +DISTRICT_ID + "&"
                "date="+date,
                headers={"accept": "application/json", "accept-language": "hi_IN", "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} )
        except Exception as e:
            logging.critical("Request Failed!", date)
            #print(e.with_traceback())
        centers = json.loads(resp.content.decode("utf-8"))["centers"]
        print(resp.text)
        if len(centers) == 0:
            logging.info("No centers found for %s", date)
        else:
            for center in centers:
                if str(center["center_id"]) in CENTER_ID_LIST or CENTER_ID_LIST == 'ALL':
                    sessions = center["sessions"]
                    for session in sessions:
                        if session["available_capacity"] > 0:
                            if session["available_capacity_dose1"] > 0 and (DOSE == '1' or DOSE == 'ALL') and (session["vaccine"].upper() == VACCINE or VACCINE == 'ALL'):
                                print("Slots found ", session["available_capacity_dose1"], session)
                                logging.info("Slot available Dose 1 on %s \n %s", date, center)
                                data = {"NOTIFICATION_TYPE": NOTIFICATION_TYPE}
                                data["center_name"] = str(center["name"])
                                data["vaccine"] = str(session["vaccine"]).lower()
                                data["dose"] = str(1)
                                data["slots"] = str(session["available_capacity_dose2"])
                                data["date"] = str(date)
                                notify(data)
                                exit()
                            if session["available_capacity_dose2"] > 0 and (DOSE == '2' or DOSE == 'ALL') and (session["vaccine"].upper() == VACCINE or VACCINE == 'ALL'):
                                print("Slots found  %s %s", session["available_capacity_dose1"], session)
                                logging.info("Slot available Dose 2 on %s \n %s", date, center)
                                data = {"NOTIFICATION_TYPE" : NOTIFICATION_TYPE}
                                data["center_name"] = str(center["name"])
                                data["vaccine"] = str(session["vaccine"]).lower()
                                data["dose"] = str(2)
                                data["slots"] = str(session["available_capacity_dose2"])
                                data["date"] = str(date)
                                notify(data)
                                exit()
                        else:
                            logging.info("No Slots on " + date + " for center " + center["name"])

def notify(data):
    if data["NOTIFICATION_TYPE"] == "IFTTT":
        print("Calling webhook")
        message = data["center_name"] + " has " + data["slots"] + " slots for dose " + data["dose"] + " of " + data["vaccine"] + " on " + data["date"]
        print(message)
        #requests.get(IFTTT_WEBHOOK, params={"value1": message})
    elif data["NOTIFICATION_TYPE"] == "EMAIL":
        pass
    elif data["NOTIFICATION_TYPE"] == "SYSTEM":
        pass
    elif data["NOTIFICATION_TYPE"] == "LOG":
        pass

if __name__ == '__main__':
    main()