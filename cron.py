import json
import telebot
from telebot import types # для указание типов
from telebot.types import Message
import MyBot

bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')

class screw:

    def __init__(self, user_id):

        #self.message = message
        self.user_id = user_id



def change_json(message):

    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:

        four_words = data_json[user]['Four_words']

        if self.user_id == user and data_json[user]["counter"] > 0 and data_json[user]['time'] == 0:
            data_json[user]["counter"] = data_json[user]['counter'] - 1
            bot.send_message(user, text=f'Ваши слова для обучения: {four_words}')
            data_json[user]['time'] = data_json[user]['const_time']

        else:
            bot.send_message(user, text=f'Если Вы готовы напишите /test')



    with open('time_user.json', 'w') as f_o:
        json.dump(data_json, f_o, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['test'])
def complete(message):
    print(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    for user in data_json:
        if user == str(message.from_user.id):
            random_word = random.choice(list(data_json[user]['Translate'].keys()))
            print(random_word)
            ok = list((data_json[user]['Translate'].values()))
            word1, word2, word3, word4 = types.KeyboardButton(ok[0]), types.KeyboardButton(
                ok[1]), types.KeyboardButton(ok[2]), types.KeyboardButton(ok[3])
            markup.add(word1, word2, word3, word4)
            bot.send_message(int(user), text=f'Отправьте перевод слова {random_word}', reply_markup=markup)
            time.sleep(2)
            bot.register_next_step_handler(message, next_step, user, random_word)


def next_step(message, user, random_word):
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    it_word = data_json[user]['Translate'].get(random_word)
    print(it_word, '\n', random_word)
    print(message.text)

    if message.text == it_word:
        bot.send_message(int(user), text='Всё верно.')
        MyBot.words(message)

    else:
        bot.send_message(int(user), text='Неверно.')
        complete(message)



bot.polling()