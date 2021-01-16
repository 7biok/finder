import json
import random
import sqlite3
import requests
import telebot
from telebot import types


site = "xyzteam.ru"
bot_token = "1509100537:AAEHIfePXz7jZYje1aZIbBkSiOamtKVKvQU"
videocdn_token = "i3wzGa2Wjeew5mGnZWpYcXatRNskC5v1"
kinopoisk = "kinopoisk.ru/series/"
admin = "1260854913"
url = 'https://videocdn.tv/api/anime-tv-series?api_token='
vk = "https://vk.com/animefiend"
tg = "https://xyzteam.ru"
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['admin'])
def admin(message):
    con = sqlite3.connect("anime.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
    if cur.fetchone()[0] == 0:
        pass
    else:
        cur.execute("SELECT COUNT(id) from user")
        c = cur.fetchone()[0]
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='Домены')
        button2 = types.KeyboardButton(text='Стол заказов')
        button3 = types.KeyboardButton(text='написать сообщение')
        button5_one = types.KeyboardButton(text='тематические чаты')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
        button5_two = types.InlineKeyboardButton(text="Наша форум", url=tg)
        keyboard_veiw.add(button4, button5_two)
        markup_main.add(button1, button2, button3,button5_one)
        bot.send_message(message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(message.chat.id,
                         'Панель управление animefinder',
                         reply_markup=keyboard_veiw)
        bot.send_message(message.chat.id,f"*Админ панель*\n Краткая стастика\n Всего пользователей:{c}", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start_message(message):
    con = sqlite3.connect("anime.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from user where id = {message.chat.id}")
    if cur.fetchone()[0] == 0:
        id_new = "Нету"
        cur.execute("INSERT INTO user(id,nick,id_new) VALUES(?,?,?)",(message.chat.id,message.chat.username,id_new))
        con.commit()
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='👺Найти аниме👺')
        button2 = types.KeyboardButton(text='🥵Популярно🥵')
        button3 = types.KeyboardButton(text='👾Рандомное аниме👾')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
        button5 = types.InlineKeyboardButton(text="Наша форум", url=tg)
        keyboard_veiw.add(button4,button5)
        markup_main.add(button1, button2, button3)
        bot.send_message(message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(message.chat.id,
                         'Привет, ты написал мне /start\nа это значит что ты можешь выбрать аниме на свой вкус🥳👻',
                         reply_markup=keyboard_veiw)
    else:
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='👺Найти аниме👺')
        button2 = types.KeyboardButton(text='🥵Популярно🥵')
        button3 = types.KeyboardButton(text='👾Рандомное аниме👾')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
        button5 = types.InlineKeyboardButton(text="Наша форум", url=tg)
        keyboard_veiw.add(button4, button5)
        markup_main.add(button1, button2, button3)
        bot.send_message(message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(message.chat.id,
                         'Привет, ты написал мне /start\nа это значит что ты можешь выбрать аниме на свой вкус🥳👻',
                         reply_markup=keyboard_veiw)



@bot.message_handler(content_types="text")
def get_text_message(message):
    if message.text == "👺Найти аниме👺":
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='Назад')
        markup_main.add(button1)
        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,"*Введите название аниме*",reply_markup=hideBoard,parse_mode="Markdown")
        bot.send_message(message.chat.id," _Вводите название правильно_:\n Правильно:*Токийский Гуль*\n Не правильно:*Таксистка гульнул*",reply_markup=markup_main,parse_mode="Markdown")
        bot.register_next_step_handler(message, get_anime)
    if message.text == "🥵Популярно🥵":
        url_quest = url + videocdn_token
        params = {'ordering': "end_date created","limit":4,"translation":2}
        r = requests.get(url_quest, params=params)
        json_true = json.loads(r.text)
        print(json_true)
        if json_true["result"] == True:
            if json_true["data"]:
                for l in json_true["data"]:
                    if l["kinopoisk_id"] == None:
                        kinop = "Нету"
                    else:
                        kinop = kinopoisk + str(l["kinopoisk_id"])
                    title = l["ru_title"] + "(" + l["en_title"] + ")"
                    creat = l["created"]
                    realese = l["updated"]
                    type = l["content_type"]
                    for s in l["translations"]:
                        quility = s["max_quality"]
                        tit = s["title"]
                        div = f"""
                                            *📖Название:*{title}\n
                    *📰Ссылка на кинопоиск:*[Перейти]({kinop})\n
                    *📥Дата создания:*{creat}\n
                    *📤Дата Появления в рекомендациях:*{realese}\n
                    *📎Тип:*{type}\n
                    *🛑Озвучка:*{tit}\n
                    *💻Максимальное качество:*{quility}\n

                                            """
                        keyboard_veiw = types.InlineKeyboardMarkup()
                        urls = s["iframe_src"].split("/")
                        href = "https://bot.xyzteam.ru/films/" + urls[5]
                        print(href)
                        url_button = types.InlineKeyboardButton(text="Смотреть", url=href)
                        keyboard_veiw.add(url_button)
                        bot.send_message(message.chat.id, div, parse_mode="Markdown", reply_markup=keyboard_veiw)
            elif not json_true["data"]:
                bot.send_message(message.chat.id, "Ничего не найденно")
        else:
            bot.send_message(message.chat.id, "Непредвиденная ошибка")
    if message.text == "👾Рандомное аниме👾":
        url_quest = url + videocdn_token
        params = {"id": random.randrange(1, 100)}
        r = requests.get(url_quest, params=params)
        json_true = json.loads(r.text)
        print(json_true)
        if json_true["result"] == True:
            if json_true["data"]:
                for l in json_true["data"]:
                    if l["kinopoisk_id"] == None:
                        kinop = "Нету"
                    else:
                        kinop = kinopoisk + str(l["kinopoisk_id"])
                    title = l["ru_title"] + "(" + l["en_title"] + ")"
                    creat = l["created"]
                    realese = l["updated"]
                    type = l["content_type"]
                    for s in l["translations"]:
                        quility = s["max_quality"]
                        tit = s["title"]
                        div = f"""
                                            *📖Название:*{title}\n
                    *📰Ссылка на кинопоиск:*[Перейти]({kinop})\n
                    *📥Дата создания:*{creat}\n
                    *📤Дата Появления в рекомендациях:*{realese}\n
                    *📎Тип:*{type}\n
                    *🛑Озвучка:*{tit}\n
                    *💻Максимальное качество:*{quility}\n

                                            """ +"\n _Любая карточка которая повторяется,представлена в разных озвучках!_"
                        keyboard_veiw = types.InlineKeyboardMarkup()
                        urls = s["iframe_src"].split("/")
                        href = "https://bot.xyzteam.ru/films/" + urls[5]
                        print(href)
                        url_button = types.InlineKeyboardButton(text="Смотреть", url=href)
                        keyboard_veiw.add(url_button)
                        bot.send_message(message.chat.id, div, parse_mode="Markdown", reply_markup=keyboard_veiw)
            elif not json_true["data"]:
                bot.send_message(message.chat.id, "Ничего не найденно")
        else:
            bot.send_message(message.chat.id, "Непредвиденная ошибка")
    if message.text == "Домены":
        con = sqlite3.connect("anime.db")
        cur = con.cursor()
        cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
        if cur.fetchone()[0] == 0:
            pass
        else:
            result_one = "http://xyzteam.ru"
            result_two = "http://xyzteam.online"
            r1 = requests.get(result_one)
            r2 = requests.get(result_two)
            if r1.status_code == 200:
                result_one = "xyzteam.ru✅"
            else:
                result_one = "xyzteam.ru‼"
            if r2.status_code == 200:
                result_two = "xyzteam.online✅"
            else:
                result_two = "xyzteam.online‼"
            print()
            keyboard_veiw = types.InlineKeyboardMarkup()
            ru = types.InlineKeyboardButton(text=result_one, url="http://xyzteam.ru")
            online = types.InlineKeyboardButton(text=result_two, url="http://xyzteam.online")
            keyboard_veiw.add(ru,online)
            bot.send_message(message.chat.id,"Краткая сводка по вашем доменам",reply_markup=keyboard_veiw)
    if message.text == "Стол заказов":
        con = sqlite3.connect("anime.db")
        cur = con.cursor()
        cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
        if cur.fetchone()[0] == 0:
            pass
        else:
            pass
    if message.text == "тематические чаты":
        con = sqlite3.connect("anime.db")
        cur = con.cursor()
        cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
        if cur.fetchone()[0] == 0:
            pass
        else:
            pass
    if message.text == "написать сообщение":
        con = sqlite3.connect("anime.db")
        cur = con.cursor()
        cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
        if cur.fetchone()[0] == 0:
            pass
        else:
            markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(text='Назад')
            markup_main.add(button1)
            bot.send_message(message.chat.id,"Напишите id человека кому отправить сообщение:",reply_markup=markup_main)
            bot.register_next_step_handler(message,message_send)

def message_send(message):
    global chat_id_send
    chat_id_send = message.text
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Напишите для него сообщение:", reply_markup=hideBoard)
    bot.register_next_step_handler(message,message_role)

def message_role(message):
    print(chat_id_send)
    mess = message.text
    bot.send_message(chat_id_send,mess)
    bot.send_message(message.chat.id,"Сообщение отправленно")
    con = sqlite3.connect("anime.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
    if cur.fetchone()[0] == 0:
        pass
    else:
        cur.execute("SELECT COUNT(id) from user")
        c = cur.fetchone()[0]
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='Домены')
        button2 = types.KeyboardButton(text='Стол заказов')
        button3 = types.KeyboardButton(text='написать сообщение')
        button5_one = types.KeyboardButton(text='тематические чаты')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
        button5_two = types.InlineKeyboardButton(text="Наша форум", url=tg)
        keyboard_veiw.add(button4, button5_two)
        markup_main.add(button1, button2, button3, button5_one)
        bot.send_message(message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(message.chat.id,
                         'Панель управление animefinder',
                         reply_markup=keyboard_veiw)
        bot.send_message(message.chat.id, f"*Админ панель*\n Краткая стастика\n Всего пользователей:{c}",
                         parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "return":
        pass



@bot.message_handler(content_types="text")
def get_anime(message):
    if message.text != "Назад":
        url_quest = url + videocdn_token
        mes = message.text
        print(mes)
        params = {'query': mes}
        r = requests.get(url_quest, params=params)
        json_true = json.loads(r.text)
        print(json_true)
        if json_true["result"] == True:
                if json_true["data"]:
                    for l in json_true["data"]:
                        if l["kinopoisk_id"] == None:
                            kinop = "Нету"
                        else:
                            kinop = kinopoisk + str(l["kinopoisk_id"])
                        title = l["ru_title"] + "(" + l["en_title"] + ")"
                        creat = l["created"]
                        realese = l["updated"]
                        type = l["content_type"]
                        for s in l["translations"]:
                                quility = s["max_quality"]
                                tit = s["title"]
                                div = f"""
                                *📖Название:*{title}\n
        *📰Ссылка на кинопоиск:*[Перейти]({kinop})\n
        *📥Дата создания:*{creat}\n
        *📤Дата выхода:*{realese}\n
        *📎Тип:*{type}\n
        *🛑Озвучка:*{tit}\n
        *💻Максимальное качество:*{quility}\n
                                
                                """ +"\n _Любая карточка которая повторяется с аниме,представлена в разных озвучках!_"
                                keyboard_veiw = types.InlineKeyboardMarkup()
                                urls = s["iframe_src"].split("/")
                                href = "https://bot.xyzteam.ru/films/" + urls[5]
                                print(s["iframe_src"])
                                url_button = types.InlineKeyboardButton(text="Смотреть", url=href)
                                keyboard_veiw.add(url_button)
                                bot.send_message(message.chat.id,div,parse_mode="Markdown",reply_markup=keyboard_veiw)
                elif not json_true["data"]:
                    bot.send_message(message.chat.id,"Ничего не найденно")
                    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button1 = types.KeyboardButton(text='👺Найти аниме👺')
                    button2 = types.KeyboardButton(text='🥵Популярно🥵')
                    button3 = types.KeyboardButton(text='👾Рандомное аниме👾')
                    keyboard_veiw = types.InlineKeyboardMarkup()
                    button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
                    button5 = types.InlineKeyboardButton(text="Наша форум", url=tg)
                    keyboard_veiw.add(button4, button5)
                    markup_main.add(button1, button2, button3)
                    bot.send_message(message.chat.id,
                                     'Попробуйте уточнить название сериала',reply_markup=markup_main)
                    bot.send_message(message.chat.id,
                                     'Вы вернулись в начальное меню \n у нас есть так же *Стол заказов*',
                                     reply_markup=keyboard_veiw,parse_mode="Markdown")

        else:
            bot.send_message(message.chat.id, "Непредвиденная ошибка")
    else:
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='👺Найти аниме👺')
        button2 = types.KeyboardButton(text='🥵Популярно🥵')
        button3 = types.KeyboardButton(text='👾Рандомное аниме👾')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url=vk)
        button5 = types.InlineKeyboardButton(text="Наша форум", url=tg)
        keyboard_veiw.add(button4, button5)
        markup_main.add(button1, button2, button3)
        bot.send_message(message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(message.chat.id,
                         'Привет, ты написал мне /start\nа это значит что ты можешь выбрать аниме на свой вкус🥳👻',
                         reply_markup=keyboard_veiw)


bot.polling()
