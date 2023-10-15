import json
import time
import random
import re
import schedule
import asyncio
import telebot
from telebot import types # для указание типов

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')



def reminder():
    with open('reg.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    print(type(data_from_json))
    b = 0
    for key in data_from_json:
        with open('time_user.json', 'r') as f_o:
            data_from_json = json.load(f_o)
        for user in data_from_json:
            if key in user:
                bot.send_message(key, text='Алоооо')
            else:
                break
        with open('time_user.json', 'w') as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    with open('reg.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)



def privyazka():
    with open('time_user.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    for i in data_from_json:
        data_from_json[i]['Russian'] = russian
        data_from_json[i]['English'] = england
        data_from_json[i]['Translate'] = translate
        print(data_from_json[i])



    with open('time_user.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

privyazka()