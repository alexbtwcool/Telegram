import json
import telebot
from telebot import types # для указание типов
from telebot.types import Message

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')

class screw:

    def __init__(self, user_id):

        #self.message = message
        self.user_id = user_id


    def change_json(self):

        with open('time_user.json', 'r') as f_o:
            data_json = json.load(f_o)

        for user in data_json:

            if self.user_id == user and data_json[user]["counter"] > 0 and data_json[user]['time'] == 0:
                data_json[user]["counter"] = data_json[user]['counter'] - 1
                bot.send_message(user, text=f'Ваши слова для обучения: {self.user_id}')
                data_json[user]['time'] = data_json[user]['time'] +

            else:
                bot.send_message(user, text=f'Вы выучили, теперь тест.')

        with open('time_user.json', 'w') as f_o:
            json.dump(data_json, f_o, indent=4, ensure_ascii=False)



