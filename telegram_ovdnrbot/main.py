# -*- coding: utf-8 -*-
# if __name__ == '__main__':
import uuid

import requests
import telebot
from telebot import TeleBot
from telebot import types
from curs import get_opt_usd_buy
from db import db, get_or_create_user
from time import sleep
import constants
from geopy.distance import vincenty, distance


def RepresentsInt(s):
    newS = s.replace(',', '.')
    try:
        float(newS)
        return True
    except ValueError:
        return False


bot = telebot.TeleBot(constants.token)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_text1 = types.KeyboardButton('Купить $')
btn_text2 = types.KeyboardButton('Продать $')
btn_text5 = types.KeyboardButton('Купить €')
btn_text6 = types.KeyboardButton('Продать €')
btn_text7 = types.KeyboardButton('Купить ₴')
btn_text8 = types.KeyboardButton('Продать ₴')
btn_text9 = types.KeyboardButton('Курс на сейчас')

start_key = [[{'text': 'Купить $'}, {'text': 'Продать $'}], [{'text': 'Купить €'}, {'text': 'Продать €'}],
             [{'text': 'Купить ₴'}, {'text': 'Продать ₴'}], [{'text': 'Курс на сейчас'} ]]
            #[{'text': 'Адреса пунктов обмена', 'request_location': True}]]

markup_menu.add(btn_text1, btn_text2, btn_text5, btn_text6, btn_text7, btn_text8, btn_text9)

operation_type = "none"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет!\nЯ помогу Вам рассчитать и поменять валюту с лучшим курсом всего в 3 шага:\n"
                     "\n1) указываете вид и сумму операции;\n"
                     "\n2) я подберу ближайший пункт обмена;\n"
                     "\n3) приходите в обменник и совершаете обмен с максимальной выгодой.",
                     reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)

    if message.text == "Курс на сейчас":
        url = 'ввести URL для получения обекта JSON'
        r = requests.get(url).json()
        price_opt_usd_buy = r['acf']['opt_usd_buy']
        price_opt_usd_sell = r['acf']['opt_usd_sell']
        price_opt_eur_buy = r['acf']['opt_eur_buy']
        price_opt_eur_sell = r['acf']['opt_eur_sell']
        price_opt_uah_buy = r['acf']['opt_uah_buy']
        price_opt_uah_sell = r['acf']['opt_uah_sell']

        price_off_usd_buy = r['acf']['official_usd_buy']
        price_off_usd_sell = r['acf']['official_usd_sell']
        price_off_eur_buy = r['acf']['official_eur_buy']
        price_off_eur_sell = r['acf']['official_eur_sell']
        price_off_uah_buy = r['acf']['official_uah_buy']
        price_off_uah_sell = r['acf']['official_uah_sell']
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Курс на сейчас для *Obmen77*:\nUSD: пок. *{}* | прод. *{}*\n"
                                          "EUR: пок. *{}* | прод. *{}*\n"
                                          "UAH: пок. *{}* | прод. *{}*\n\n" 
                                          "Официальный курс:\nUSD: пок. {} | прод. {}\n"
                                          "EUR: пок. {} | прод. {}\n"
                                          "UAH: пок. {} | прод. {}\n".format(price_opt_usd_buy, price_opt_usd_sell,
                                                                                   price_opt_eur_buy, price_opt_eur_sell,
                                                                                   price_opt_uah_buy, price_opt_uah_sell,
                                                                                   price_off_usd_buy, price_off_usd_sell,
                                                                                   price_off_eur_buy, price_off_eur_sell,
                                                                                   price_off_uah_buy, price_off_uah_sell), reply_markup=markup_menu, parse_mode="Markdown")

    elif message.text == "Купить ₴":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "UAH", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "UAH", "type": "sale"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько ₴ вы хотите купить? Введите сумму покупки.")

    elif message.text == "Продать ₴":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "UAH", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "UAH", "type": "buy"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько ₴ вы хотите продать? Введите сумму продажи.")

    elif message.text == "Купить $":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "USD", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "USD", "type": "sale"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько $ вы хотите купить? Введите сумму покупки.")

    elif message.text == "Продать $":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "USD", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "USD", "type": "buy"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько $ вы хотите продать? Введите сумму продажи.")

    elif message.text == "Купить €":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "EUR", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "EUR", "type": "sale"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько € вы хотите купить? Введите сумму покупки.")

    elif message.text == "Продать €":
        mycol = db["chats"]
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            myquery = {"user_id": "{}".format(message.from_user.id), "currency": "EUR", "userName": "{}".format(message.from_user.username)}
            mycol.insert_one(myquery)
        else:
            myquery = {"user_id": "{}".format(message.from_user.id), "userName": "{}".format(message.from_user.username)}
            newvalues = {"$set": {"currency": "EUR", "type": "buy"}}
            mycol.update_one(myquery, newvalues)
        markup_menu.one_time_keyboard = True
        bot.send_message(message.chat.id, "Сколько € вы хотите продать? Введите сумму продажи.")

    elif message.text == "Отменить расчет":
        markup_menu.keyboard = start_key
        bot.send_message(message.chat.id, "Вы вернульсь в главное меню!", reply_markup=markup_menu)
    elif message.text == "Подтвердить":
        #markup_menu.keyboard = [
            #[{'text': 'Отправить  гео-позицию', 'request_location': True}], [{'text': 'Отменить расчет'}]]
        markup_menu.keyboard = [
            [{'text': 'Отправить  контакт', 'request_contact': True}], [{'text': 'Отменить расчет'}]]
        bot.send_message(message.chat.id,
                         "Отправьте свою контакт, чтобы наш менеджер мог связаться с вами.",
                         reply_markup=markup_menu)
    elif RepresentsInt(message.text):
        # markup_menu.one_time_keyboard = True

        mycol = db["chats"]
        for x in mycol.find():
            e = x.get("user_id")
            z = message.from_user.id
            if int(x.get("user_id")) == message.from_user.id:
                currency = x.get("currency")
                type = x.get("type")
                break

        markup_menu.keyboard = [[{'text': 'Подтвердить', 'request_contact': True}, {'text': 'Отменить расчет'}]]
        url = 'ввести URL для получения обекта JSON'
        r = requests.get(url).json()

        if currency == 'USD':
            price = r['acf']['opt_usd_buy']
            off_price = r['acf']['official_usd_buy']
            if type == 'sale':
                price = r['acf']['opt_usd_sell']
                off_price = r['acf']['official_usd_sell']
        elif currency == 'EUR':
            price = r['acf']['opt_eur_buy']
            off_price = r['acf']['official_eur_buy']
            if type == 'sale':
                price = r['acf']['opt_eur_sell']
                off_price = r['acf']['official_eur_sell']
        elif currency == 'UAH':
            price = r['acf']['opt_uah_buy']
            off_price = r['acf']['official_uah_buy']
            if type == 'sale':
                price = r['acf']['opt_uah_sell']
                off_price = r['acf']['official_uah_sell']

        text_type = "продаете"
        if type == 'sale':
            text_type = "покупаете"
        summa = message.text.replace(',', '.')
        sum = float(price) * float(summa)
        off_sum = float(off_price) * float(summa)
        if not db.chats.find_one({"user_id": "{}".format(message.from_user.id)}):
            bot.send_message(message.chat.id, "at the begining select currency")
            return

        mycol = db["chats"]
        myquery = {"user_id": "{}".format(message.from_user.id)}
        newvalues = {"$set": {"bring": "{}".format(message.text), "sum": "{}".format(sum), "uid": "{}".format(uuid.uuid4()), "price": "{}".format(price)}}
        mycol.update_one(myquery, newvalues)

        bot.send_message(message.chat.id,
                         "Хорошо! Вы {} _{} {}_ по курсу *{} руб.* за _{} руб._ \n\n*Ваша выгода {} руб.*👍 \n\n_Вы можете Подтвердить или Отменить расчет._\n"
                          #"\nПосле подтверждения бот запросит ваш номер телефона, чтобы менеджер смог с Вами связаться."
                         .format(
                             text_type,
                             message.text,
                             db.chats.find_one(
                                 {"user_id": "{}".format(
                                     message.from_user.id)})['currency'],
                             price, "{0:.2f}".format(float(sum)), "{0:.2f}".format(abs(float(sum) - float(off_sum)))),
                         reply_markup=markup_menu, parse_mode="Markdown")

    else:
        bot.reply_to(message, "Пожалуйста, введите сумму без букв и лишних знаков (!,&?)!", reply_markup=markup_menu)

@bot.message_handler(func=lambda messege: True, content_types=['contact'])
def user_contacts(message):
    mycol = db["chats"]
    myquery = {"user_id": "{}".format(message.from_user.id)}
    newvalues = {"$set": {"phone_number": "{}".format(message.contact.phone_number),
                          "first_name": "{}".format(message.contact.first_name)}}
    mycol.update_one(myquery, newvalues)
    markup_menu.keyboard = [
        [{'text': 'Отправить  гео-позицию', 'request_location': True}], [{'text': 'Отменить расчет'}]]
    bot.send_message(message.chat.id,
                     "Отправьте свою гео-позицию, Я подберу ближайший пункт обмена валют.",
                     reply_markup=markup_menu)
    #bot.send_message(message.chat.id, message.contact.phone_number)

@bot.message_handler(func=lambda messege: True, content_types=['location'])
def punctobmena_location(message):
    # print(message)
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for m in constants.punctobmena:
        result = vincenty((m['latm'], m['lonm']), (lat, lon)).kilometers
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайший к Вам фирменный пункт обмена валют.\nВы можете построить маршрут нажав на карту с адресом.')
    markup_menu.keyboard = start_key
    bot.send_venue(message.chat.id,
                   constants.punctobmena[index]['latm'],
                   constants.punctobmena[index]['lonm'],
                   constants.punctobmena[index]['title'],
                   constants.punctobmena[index]['address'])

    responce = db.chats.find_one({"user_id": "{}".format(message.from_user.id)})


    mycol = db["chats"]
    for x in mycol.find():
        if int(x.get("user_id")) == message.from_user.id:
            #userName = x.get("username")
            type = x.get("type")
            break

    if type == 'sale':
        operation_type_text = "Покупка"
    else:
        operation_type_text = "Продажа"

    mycol = db["chats"]
    for x in mycol.find():
        if int(x.get("user_id")) == message.from_user.id:
            userName = x.get("userName")
            userPhone = x.get("phone_number")
            userFirstName = x.get("first_name")
            type = x.get("type")
            break

    site_url = "URL сайта для оформления заявки"\
                .format(responce["user_id"],
                         responce["currency"],
                         userName,
                         responce["bring"].replace(',','.'),
                         responce["price"],
                         "{0:.2f}".format(float(responce["sum"])),
                        operation_type_text,
                        userFirstName,
                        userPhone)
    req = requests.get(site_url).json()
    request_number = req['request_number']

    bot.send_message(message.chat.id,
                     "Спасибо за использование сервиса 👉 obmen77.ru\n"
                     "\nЗаявка №: {}\nПункт: {}\nОперация: {}\nВалюта: {}\nКурс: {}\nСумма в валюте: {}\nИтого руб: {}\n"
                     #"\nСообщите кассиру, что вы делали заяку в сервисе 👉obmen77.ru\n"
                                                     .format(request_number,
                                                     constants.punctobmena[index]['title'],
                                                     operation_type_text,
                                                     responce["currency"],
                                                     responce["price"],
                                                     float(responce["bring"].replace(',','.')),
                                                     "{0:.2f}".format(float(responce["sum"])), ),
                     reply_markup=markup_menu)


    lidChatId = "-id"

    #mycol = db["chats"]
    #for x in mycol.find():
    #    if int(x.get("user_id")) == message.from_user.id:
    #        userName = x.get("userName")
    #        userPhone = x.get("phone_number")
    #        userFirstName = x.get("first_name")
    #        type = x.get("type")
    #        break

    if type == 'sale':
        operation_type_text = "Покупка"
    else:
        operation_type_text = "Продажа"
    bot.send_message(lidChatId,
                     "Заявка: № {}\nПункт: {}\nПользователь: @{}\nИмя: {}\nТел: {}\nВалюта: {}\nОперация: {}\nКурс: {}\nСумма в валюте: {}\nИтого руб: {}\n".format(request_number,
                                                     constants.punctobmena[index]['title'],
                                                     userName,
                                                     userFirstName,
                                                     userPhone,
                                                     responce["currency"],
                                                     operation_type_text,
                                                     responce["price"],
                                                     responce["bring"].replace(',','.'),
                                                     "{0:.2f}".format(float(responce["sum"]))))



    # print('Широта {} долгота {}'.format(lon,lat)) просто получаем ширату и долготу в консоль


bot.polling()
