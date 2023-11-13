import  telebot
import json
import time
import datetime

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')
def change_json(user_id):

    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        print(data_json[user]['time'])
        four_words = data_json[user]['Four_words']

        if user_id == user and data_json[user]["counter"] > 0 and data_json[user]['time'] == 0:
            data_json[user]["counter"] = data_json[user]['counter'] - 1
            bot.send_message(user, text=f'Ваши слова для обучения: {four_words}')
            data_json[user]['time'] = data_json[user]['const_time']

        if data_json[user]["counter"] == 0 and data_json[user]['time'] == 0:

            with open('time_user.json', 'r') as f_o:
                data_json = json.load(f_o)

            bot.send_message(user, text=f'Если Вы готовы напишите /test')
            data_json[user]["time"] = data_json[user]["const_time"]
            with open('time_user.json', 'w') as f_o:
                json.dump(data_json, f_o, indent=4, ensure_ascii=False)




while True:

    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if data_json[user]["time"] > 0:
            data_json[user]["time"] = int(data_json[user]['time'] - 1)

        else:
            change_json(user)

    with open('time_user.json', 'w') as f_o:
        json.dump(data_json, f_o, indent=4, ensure_ascii=False)

    time.sleep(60)
