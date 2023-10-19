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

reminder()

def privyazka():
    with open('word.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    wordss = data_from_json
    for i in wordss:
        with open('time_user.json', 'r') as f_o:
            data_from_json = json.load(f_o)
        user_id = "857813877"
        for id in data_from_json:
            if id == user_id:
                data_from_json[id]["Russian"] = "22"



        with open('time_user.json', 'w') as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

def complete_remind():

    user_id = 857813877

    text_words = []
    for _ in range(2):
        with open('word.json', 'r') as f_o:
            data_from_json = json.load(f_o)
        words = data_from_json





        for i in words:
            all = i['words']
            four_words = random.sample(all, 4)
            duplicates = []

            england, russian = random.SystemRandom().sample(four_words,1), random.SystemRandom().sample(four_words, 3)
            if england not in russian:
                russian.pop(1)
                russian.append(''.join(england))
                random.shuffle(russian)

            translate = (' '.join(england)).split('—')[1].replace(' ', '')
            russian, only_england = ', '.join(russian), ', '.join(england)
            only_england = re.sub('[ЁёА-я-—]', '', only_england)
            russian = re.sub("[a-zA-Z-—]", "", russian)

            four_words = ', '.join(four_words)





            with open('time_user.json', 'r') as f_o:
                time_json = json.load(f_o)
            user_id = str(user_id)
            for id in time_json:

                if id == str(user_id):

                    time_json[id]['Russian'] = russian
                    time_json[id]['English'] = only_england
                    time_json[id]['Translate'] = translate


            with open('time_user.json', 'w') as f_o:
                json.dump(time_json, f_o, indent=4, ensure_ascii=False)



complete_remind()