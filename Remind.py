import json
import time
import random
import re
import schedule
import asyncio
import telebot
from telebot import types # для указание типов
from telebot.types import Message

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')

def accept():
    a = 1
    return a

@bot.message_handler(content_types='text')

def complete(message):
    if message.text == 'Начнём.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        with open('time_user.json', 'r') as f_o:
            data_json = json.load(f_o)

        for user in data_json:
            if user == "857813877":
                random_word = random.choice(list(data_json[user]['Translate'].keys()))
                print(random_word)
                ok = list((data_json[user]['Translate'].values()))
                word1, word2, word3, word4 = types.KeyboardButton(ok[0]), types.KeyboardButton(ok[1]), types.KeyboardButton(ok[2]), types.KeyboardButton(ok[3])
                markup.add(word1, word2, word3, word4)
                bot.send_message(int(user), text='Отправьте команду /accept, когда ', reply_markup=markup)
                time.sleep(2)
                bot.register_next_step_handler(next_step(user,random_word,message))




def next_step(user,random_word, message):


    it_word = data_json[user]['Translate'].get(random_word)
    print(message)

    if message == it_word:
        bot.send_message(int(user), text='Всё верно.')

    else:
        bot.send_message(int(user), text='Неверно.')


def scheedul(user_id):
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:

            data_json[user]["counter"] = data_json[user]['counter'] - 1
            bot.send_message(user_id, text=f'Ваши слова для обучения: {four_words}')

    with open('time_user.json', 'w') as f_o:
        json.dump(data_json, f_o, indent=4, ensure_ascii=False)

"""while True:
    time.sleep(1)
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if data_json[user]['time'] != 0:
            data_json[user]['time'] = int(data_json[user]['time'] - 1)

    with open('time_user.json', 'w') as f_o:
        json.dump(data_json, f_o, indent=4, ensure_ascii=False)"""


bot.polling()