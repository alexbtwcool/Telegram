import json
import Remind

with open('time_user.json', 'r') as fo:
    data_json = json.load(fo)

for i in data_json:
    if data_json[i]['time'] <= 0:
        pass
    else:
        Remind.remind_user(data_json[i]['user_id'], data_json[i]['message'])
        data_json[i]['time'] -= 1

with open('time_user.json', 'w') as fo:
    json.dump(data_json, fo)

