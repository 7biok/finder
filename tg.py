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


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['admin'])
def admin(message):
    con = sqlite3.connect("anime.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from Admin where id = {message.chat.id}")
    c = cur.execute("SELECT COUNT(*) FROM user")
    if cur.fetchone()[0] == 0:
        pass
    else:
        bot.send_message(message.chat.id,f"*Админ панель*\n Краткая стастика:\n Всего пользователей:{c}", parse_mode="Markdown")

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
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url="https://vk.com/animefiend")
        button5 = types.InlineKeyboardButton(text="Наша форум", url="https://xyzteam.ru")
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
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url="https://vk.com/animefiend")
        button5 = types.InlineKeyboardButton(text="Наша форум", url="https://xyzteam.ru")
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
        markup_main = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Назад',callback_data="return")
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
                        url_button = types.InlineKeyboardButton(text="Смотреть", url=l["preview_iframe_src"])
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
                        url_button = types.InlineKeyboardButton(text="Смотреть", url=l["preview_iframe_src"])
                        keyboard_veiw.add(url_button)
                        bot.send_message(message.chat.id, div, parse_mode="Markdown", reply_markup=keyboard_veiw)
            elif not json_true["data"]:
                bot.send_message(message.chat.id, "Ничего не найденно")
        else:
            bot.send_message(message.chat.id, "Непредвиденная ошибка")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "return":
        markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text='👺Найти аниме👺')
        button2 = types.KeyboardButton(text='🥵Популярно🥵')
        button3 = types.KeyboardButton(text='👾Рандомное аниме👾')
        keyboard_veiw = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(text="Наша группа в вк", url="https://vk.com/animefiend")
        button5 = types.InlineKeyboardButton(text="Наша форум", url="https://xyzteam.ru")
        keyboard_veiw.add(button4, button5)
        markup_main.add(button1, button2, button3)
        bot.send_message(call.message.chat.id,
                         'AnimeFinder № 0.0.1',
                         reply_markup=markup_main)
        bot.send_message(call.message.chat.id,
                         'Привет, ты написал мне /start\nа это значит что ты можешь выбрать аниме на свой вкус🥳👻',
                         reply_markup=keyboard_veiw)




def get_anime(message):
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
                            url_button = types.InlineKeyboardButton(text="Смотреть", url=l["preview_iframe_src"])
                            keyboard_veiw.add(url_button)
                            bot.send_message(message.chat.id,div,parse_mode="Markdown",reply_markup=keyboard_veiw)
            elif not json_true["data"]:
                bot.send_message(message.chat.id,"Ничего не найденно")
    else:
        bot.send_message(message.chat.id, "Непредвиденная ошибка")

bot.polling()
