import json
import time
import random
import re

import telebot
from telebot import types # для указание типов


bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')



@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📕 Об авторе")
    btn2 = types.KeyboardButton('🏹 Начать работу')

    with open('reg.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.first_name
    user_exists = False
    for user_data in data_from_json:
        if str(user_id) in user_data:
            user_exists = True
            bot.reply_to(message=message,text='Ты уже начал взаимодействовать со мной, но я напомню, что основные команды в меню 😉')
            break

    if not user_exists:
        # Если пользователь не найден, добавляем его в список
        data_from_json.append({user_id: {'username': username}})
        with open('reg.json', 'w') as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        bot.reply_to(message=message, text=f'''Здравствуй, *{message.from_user.first_name} 😎‍*!
    markup.add(btn2, btn1)
*Немного обо мне:* Я твой помощник, я могу помогать тебе при изучении нового материала.
Вообще я предназначен для изучения английского, но я думаю, что мой хозяин будет против, если ты будешь использовать меня для других целей 🤫
\n⚠️ *Подсказка:* для взаимодействия со мной используй меню.''')



@bot.message_handler(commands=['words'])
def words(message):
    bot.reply_to(message=message, text=f"""Отправь задержку, вот так: \n
*60* \n \n(напоминание произойдет через 60 минут) 😉""")
    bot.register_next_step_handler(message, write)


def write(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_60 = types.KeyboardButton("⏰ 60 минут")
    time_180 = types.KeyboardButton('🕜 3 часа')
    time_480 = types.KeyboardButton('🕣 9 часов')
    time_1240 = types.KeyboardButton('🕛 24 часа')
    update_words = types.KeyboardButton('🔄 Обновить слова')


    markup.add(time_60, time_180, time_480, time_1240)

    text = message.text
    user_id = message.from_user.id

    try:
        int(text)
        bot.reply_to(message=message, text=f'''Отлично, Вы указали время задержки = *{text}*''', reply_markup=markup)

        with open('words.json', 'r') as f_o:
            data_from_json = json.load(f_o)

        data_from_json.append({user_id: {'time': text}})


        with open('words.json', 'w') as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except ValueError:
        bot.reply_to(message=message, text=f'Время должно быть указано в минутах!')
    complete_remind(message)

def complete_remind(message):
    okey = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_words = types.KeyboardButton('🔄 Обновить слова')
    okey.add(update_words)

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

        bot.reply_to(message=message, text=f'Ваши слова для обучения: {four_words}', reply_markup=okey)
        bot.register_next_step_handler(message, update)

def update(message):
    if message.text == '🔄 Обновить слова':
        complete_remind(message)
    else:
        return




@bot.message_handler(commands=['reminds'])
def reminds(message):
    user_id = message.from_user.id
    with open('word.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    text = []
    for i in data_from_json:
        if str(user_id) in i:
            text.append((i[str(user_id)]['text']))
    text = ', '.join(text)
    bot.reply_to(message=message, text=f'Ваши напоминания: {text}')


bot.polling()