import random
import re
import schedule
import json
import asyncio
import telebot
from telebot import types
from telebot.types import Message
import time
from envparse import Env

env = Env()
TOKEN = env.str('TOKEN')
bot = telebot.TeleBot(token=TOKEN, parse_mode='MARKDOWN')

def change_json(user_id):

    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:

        

        if user_id == user and data_json[user]["counter"] > 0 and data_json[user]['time'] == 0:
            four_words = data_json[user]['Four_words']

            with open('time_user.json', 'r') as f_o:
                data_json = json.load(f_o)

            data_json[user]["counter"] = data_json[user]['counter'] - 1
            bot.send_message(user, text=f'''НАПОМИНАНИЕ⚠️\n\nВаши слова для обучения: {four_words}''')
            data_json[user]["time"] = data_json[user]["const_time"]

            with open('time_user.json', 'w') as f_o:
                json.dump(data_json, f_o, indent=4, ensure_ascii=False)

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

            with open('time_user.json', 'r') as f_o:
                data_json = json.load(f_o)

            data_json[user]["time"] = int(data_json[user]['time'] - 1)

            with open('time_user.json', 'w') as f_o:
                json.dump(data_json, f_o, indent=4, ensure_ascii=False)

        else:
            change_json(user)

    time.sleep(60)
