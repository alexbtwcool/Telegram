import json
import time
import random
import re
import schedule
import asyncio
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
# ООП = user_id, username
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_60 = types.KeyboardButton("⏰ 1 час")
    time_180 = types.KeyboardButton('🕜 3 часа')
    time_480 = types.KeyboardButton('🕣 9 часов')
    time_1240 = types.KeyboardButton('🕛 24 часа')


    markup.add(time_60, time_180, time_480, time_1240)
    bot.reply_to(message=message, text=f"""Отправь задержку, вот так: \n
*60* \n \n(напоминание произойдет через 60 минут), также можешь использовать кнопки в панели 😉""", reply_markup=markup)
    bot.register_next_step_handler(message, write)



def write(message):


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
            data_from_json.append({user_id: {'time': text}})
            bot.reply_to(message=message, text=f'''Отлично, время задержки *{text} минут(а)*''')
            complete_remind(message)

            with open('time_user.json', 'w') as f_o:
                json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

    except ValueError:
        if type(int(text)) != int:
            bot.reply_to(message=message, text=f'Время должно быть указано в минутах!')
            words(message)


def complete_remind(message):
    okey = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_words = types.KeyboardButton('🔄 Обновить слова')
    okey.add(update_words)
    user_id = message.from_user.id

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
            print(four_words)
            four_words = ', '.join(four_words)
            print(only_england, russian)


            bot.send_message(user_id, text=f'Ваши слова для обучения: {four_words}', reply_markup=okey)
            with open('bind.json', 'r') as f_o:
                data_from_json = json.load(f_o)

            data_from_json.append({user_id: [only_england, russian, translate]})

            with open('bind.json', 'w') as f_o:
                json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)


        bot.register_next_step_handler(message, update)




def update(message):
    test = 1
    if message.text == '🔄 Обновить слова' and test == 1:
        test+=1
        complete_remind(message)


@bot.message_handler(commands=['delete'])
def delete(message):
    user_id = message.from_user.id
    with open('time_user.json', 'r') as f_o:
        data_from_json = json.load(f_o)


    for user in data_from_json:
        if str(user_id) in user:
            data_from_json.remove(user)
    with open('time_user.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

    with open('bind.json') as f_o:
        data_from_json = json.load(f_o)

    for _ in range(2):
        for user in data_from_json:
            if str(user_id) in user:
                data_from_json.remove(user)


    with open('bind.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot.reply_to(message, text="✅ Готово, ваши напоминания были удалены.")


@bot.message_handler(commands=['reminds'])
def reminds(message):
    user_id = message.from_user.id
    with open('bind.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    for i in data_from_json:
        if str(user_id) in i:
            bot.reply_to(message, text='—'.join(i[str(user_id)]))


bot.polling()