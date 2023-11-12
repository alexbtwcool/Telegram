import random
import re
import schedule
import json
import asyncio
import telebot
from telebot import types
from telebot.types import Message
import time


bot = telebot.TeleBot(token='6479236406:AAEM9osXPYtJPAx5wlPO2VB_eECBvV8NtTA', parse_mode='MARKDOWN')



@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📕 Об авторе")
    btn2 = types.KeyboardButton('🏹 Начать работу')
    markup.add(btn2, btn1)
    with open('reg.json', 'r') as f_o:
        data_from_json = json.load(f_o)
# ООП = user_id, username
    user_id = message.from_user.id
    username = message.from_user.first_name
    user_exists = False
    for user_data in data_from_json:
        if str(user_id) in user_data:
            user_exists = True
            bot.reply_to(message=message,text='Ты уже начал взаимодействовать со мной, но я напомню, что основные команды в меню 😉', reply_markup=markup)
            break

    if not user_exists:
        # Если пользователь не найден, добавляем его в список
        user_id = str(user_id)
        data_from_json[user_id] = {'username': username, 'message': message}
        with open('reg.json', 'w') as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        bot.reply_to(message=message, text=f'''Здравствуй, *{message.from_user.first_name} 😎‍*!
    
*Немного обо мне:* Я твой помощник, я могу помогать тебе при изучении нового материала.
Вообще я предназначен для изучения английского, но я думаю, что мой хозяин будет против, если ты будешь использовать меня для других целей 🤫
\n⚠️ *Подсказка:* для взаимодействия со мной используй меню.''', reply_markup=markup)



@bot.message_handler(commands=['words'])
def words(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_60 = types.KeyboardButton("⏰ 1 час")
    time_180 = types.KeyboardButton('🕜 3 часа')
    time_480 = types.KeyboardButton('🕣 9 часов')
    time_1240 = types.KeyboardButton('🕛 24 часа')


    markup.add(time_60, time_180, time_480, time_1240)
    bot.reply_to(message=message, text=f"""Отправь задержку, вот так: \n
*60* \n \n(повторение слов произойдет через 60 минут, всего 2 повторения), также можешь использовать кнопки в панели 😉""", reply_markup=markup)

    bot.register_next_step_handler(message, write)



def write(message):

    username = message.from_user.first_name
    text = message.text
    user_id = message.from_user.id
    if text == "⏰ 1 час":
        text = 60
    elif text == '🕜 3 часа':
        text = 180
    elif text == '🕣 9 часов':
        text = 480
    elif text == '🕛 24 часа':
        text = 1240
    else:
        text = message.text
        try:
            text = int(text)
        except ValueError:
            bot.reply_to(message, text='⚠️ ЗАДЕРЖКА ДОЛЖНА БЫТЬ УКАЗАНА В ЦИФРАХ!!!')
            return
        print(text)
    try:

        user_exists = False
        with open('time_user.json', 'r') as f_o:
            data_from_json = json.load(f_o)
        for item in data_from_json:
            if str(user_id) in item:
                bot.reply_to(message=message, text='Вы уже установили напоминание. Если желаете удалить текущие слова - /delete')
                user_exists = True
                return

        if user_exists == False:
            user_id = str(user_id)
            data_from_json[user_id] = {'time': text, 'counter': 2, 'const_time': text}

            bot.reply_to(message=message, text=f'''Отлично, время задержки *{text} минут(а)*''')


            with open('time_user.json', 'w') as f_o:
                json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
            complete_remind(message)

    except ValueError:
        if type(int(text)) != int:
            bot.reply_to(message=message, text=f'Время должно быть указано в минутах!')
            words(message)


def complete_remind(message):

    user_id = message.from_user.id

    text_words = []

    with open('word.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    words = data_from_json

    for i in words:
        all = i['words']
        four_words = random.sample(all, 4)
        translate = {}

        for i in four_words:
            i = i.split('—')
            i[1] = i[1].strip()
            translate[i[0]] = i[1]
            print(translate)

        print(type(four_words))
        four_words_text = ', '.join(four_words).replace("'", "**")
        bot.send_message(user_id, text=f'Ваши слова для обучения: {four_words_text}')

        with open('time_user.json', 'r') as f_o:
            time_json = json.load(f_o)


        for i in time_json:
            if i == str(user_id):
                time_json[i]['Translate'] = translate
                time_json[i]['Four_words'] = four_words_text

        with open('time_user.json', 'w') as f_o:
            json.dump(time_json, f_o, indent=4, ensure_ascii=False)

    if message.text == '🔄 Обновить слова':
        bot.register_next_step_handler(message, update)




def update(message):
    complete_remind()



@bot.message_handler(commands=['delete'])
def delete(message):
    user_id = message.from_user.id
    with open('time_user.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    for user in list(data_from_json):
        if str(user_id) == user:
            del data_from_json[user]


    with open('time_user.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)


    bot.reply_to(message, text="✅ Готово, ваши напоминания были удалены.")


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
            bot.send_message(int(user), text='Выберите верное слово', reply_markup=markup)
            time.sleep(2)
            bot.register_next_step_handler(message, next_step, user, random_word)
        else:
            break


def next_step(message, user, random_word):

    it_word = data_json[user]['Translate'].get(random_word)
    print(random_word)

    if message == it_word:
        bot.send_message(int(user), text='Всё верно.')

    else:
        bot.send_message(int(user), text='Неверно.')


bot.polling()
