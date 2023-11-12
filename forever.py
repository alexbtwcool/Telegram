import json
from cron import  screw
import time

while True:

    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if data_json[user]["time"] > 0:
            data_json[user]["time"] = int(data_json[user]['time'] - 1)
            print(data_json[user]["time"])


        else:
            screw_instance = screw(user)
            screw_instance.change_json()

    with open('time_user.json', 'w') as f_o:
        json.dump(data_json, f_o, indent=4, ensure_ascii=False)

    time.sleep(60)