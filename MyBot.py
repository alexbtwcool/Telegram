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
import psycopg2
from config import host, user, password, db_name

env = Env()
TOKEN = env.str('TOKEN')
bot = telebot.TeleBot(token=TOKEN, parse_mode='MARKDOWN')

def user_registration(user_id, username):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('''INSERT INTO users (user_id, username) VALUES (%s, %s);''', [user_id, username])


    cur.execute('''SELECT * FROM users''')
#    print(cur.fetchall())

#user_registration('10', 'SAnek232')

def user_selection(user_id, username, message):

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE user_id = %s;''', [user_id])


    if cur.fetchone() is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("📕 Об авторе")
        btn2 = types.KeyboardButton('🏹 Начать работу')
        markup.add(btn2, btn1)
        user_registration(user_id,username)
        cur.execute('''SELECT * FROM users WHERE user_id = %s;''', [user_id])
        bot.reply_to(message=message, text=f'''Здравствуй, *{message.from_user.first_name} 😎‍*!

        *Немного обо мне:* Я твой помощник, я могу помогать тебе при изучении нового материала.
        Вообще я предназначен для изучения английского, но я думаю, что мой хозяин будет против, если ты будешь использовать меня для других целей 🤫
        \n⚠️ *Подсказка:* для взаимодействия со мной используй меню.''', reply_markup=markup)



    else:
        bot.reply_to(message, text='Ты уже начал взаимодействовать со мной, но я напомню, что основные команды в меню 😉')



@bot.message_handler(commands=['start'])
def start(message):

    with open('reg.json', 'r') as f_o:
        data_from_json = json.load(f_o)
# ООП = user_id, username
    user_id = message.from_user.id
    username = message.from_user.first_name
    user_exists = False
    user_selection(user_id,username,message)




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
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    conn.autocommit = True
    cur = conn.cursor()

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
            return words(message)
        print(text)
    try:

        cur.execute('''SELECT 1 FROM time_user WHERE user_id = %s;''', [user_id])
        if cur.fetchone() is not None:
                bot.reply_to(message=message, text='Вы уже установили напоминание. Если желаете удалить текущие слова - /delete')
                return

        else:
            user_id = str(user_id)
            cur.execute('''INSERT INTO time_user(user_id, time, const_time) VALUES(%s,%s,%s);''', [user_id, text, text])
            bot.reply_to(message=message, text=f'''Отлично, время задержки *{text} минут(а)*''')
            complete_remind(message)

    except ValueError:
        if type(int(text)) != int:
            bot.reply_to(message=message, text=f'Время должно быть указано в минутах!')
            words(message)


def complete_remind(message):

    user_id = message.from_user.id

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('''SELECT english FROM words;''')
    words = cur.fetchall()
    english = random.choices(words, k=4)
    print(english)
    four_word = ''
    translate = {}
    for i in english:
        one_english = ''.join(i)
        print(''.join(i))
        cur.execute('''SELECT russian FROM words WHERE english = %s''', [i])
        russian = ''.join(cur.fetchone())
        print(russian)
        four_word += one_english + ' — ' + russian + ', '
        translate.update({one_english: russian})

    four_word = four_word[:-2]

    with open('time_user.json', 'r') as f_o:
        time_json = json.load(f_o)

    print(four_word)

    for s in time_json:
        if s == str(user_id):
            time_json[s]['Translate'] = translate
            time_json[s]['Four_words'] = four_word

    with open('time_user.json', 'w') as f_o:
        json.dump(time_json, f_o, indent=4, ensure_ascii=False)

    bot.send_message(user_id, text=f'Ваши слова для обучения: {four_word}')


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
            bot.send_message(int(user), text=f'Отправьте перевод слова {random_word}', reply_markup=markup)
            bot.register_next_step_handler(message, next_step, user, random_word)


def next_step(message, user, random_word):
    with open('time_user.json', 'r') as f_o:
        data_json = json.load(f_o)

    it_word = data_json[str(user)]['Translate'].get(random_word)
    print(it_word, '\n', random_word)
    print(message.text)

    if message.text == it_word:
        bot.send_message(int(user), text='Всё верно.')



        del data_json[user]

        with open('time_user.json', 'w') as f_o:
            json.dump(data_json, f_o, indent=4, ensure_ascii=False)
        words(message)


    else:
        bot.send_message(int(user), text='Неверно.')
        data_json[str(message.from_user.id)]['time'] = data_json[message.from_user.id]['const_time']
        complete(message)






bot.polling()
