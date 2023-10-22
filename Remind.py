import json
import time
import random
import re
import schedule
import asyncio
import telebot
from telebot import types # для указание типов

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')



def scheedule(user_id):
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if user == str(user_id):
            four_words = data_json[user]['Four_words']
            bot.send_message(user_id, text=f'Ваши слова для обучения: {four_words}')
            if data_json[user]["counter"] != 0:
                data_json[user]["counter"] = data_json[user]['counter'] - 1

            else:
                bot.send_message(user_id, text=f'ПРОВЕРКА ТЕПЕРЬ ЕЛКИ {four_words}')
            bot.send_message(user_id, text=f'Ваши слова для обучения: {four_words}')
        else:
            pass
        with open('time_user.json', 'w') as f_o:
            json.dump(data_json, f_o, indent=4, ensure_ascii=False)

while True:
    time.sleep(5)
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if data_json[user]['time'] != 0:
            data_json[user]['time'] = int(data_json[user]['time'] - 1)

        else:
            scheedule(user)


    print('-1')