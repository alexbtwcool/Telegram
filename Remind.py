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
    for key in data_from_json[0]:
        b += 1
        a = data_from_json[1].keys()
        print(key)
    with open('reg.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

    with open('time_user.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    print(data_from_json)

reminder()