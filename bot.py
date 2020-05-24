import telebot
import pyowm
import apiai, json
import pyowm.exceptions
import config
import time as tm
import datetime
from datetime import date
from datetime import timedelta
from weather import *


bot = telebot.TeleBot(config.BOT_TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def starting(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)
    start_markup.row('/forecast', '/weather', '/hide')
    bot.send_message(message.chat.id, "Привет!\n")
    bot.send_message(message.chat.id, "Чтобы скрыть клавиатуру, нажмите /hide\n")
    bot.send_message(message.chat.id,
                     "Чтобы узнать прогноз на определенный день, нажмите /forecast\n")
    bot.send_message(message.chat.id,
                     "Чтобы узнать текущую погоду, нажмите /weather",
                     reply_markup=start_markup)


@bot.message_handler(commands=['hide'])
def hiding(message):
    bot.send_message(message.chat.id,
                     'Клавиатура спрятана',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['help'])
def help(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)
    start_markup.row('/forecast', '/weather', '/hide')
    bot.send_message(message.chat.id, "Чтобы скрыть клавиатуру, введите /hide\n")
    bot.send_message(message.chat.id,
                     "Чтобы узнать прогноз на определенный день, введите /forecast\n")
    bot.send_message(message.chat.id,
                     "Чтобы узнать текущую погоду, введите /weather",
                     reply_markup=start_markup)


@bot.message_handler(commands=['weather'])
def weather_city_receive(message):
    city_request = bot.send_message(message.chat.id,
                                    'Введите город, в котором хотите узнать погоду')
    bot.register_next_step_handler(city_request, send_weather)


def send_weather(message):
    try:
        get_weather(message.text)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id,
                         '❌Город не найден, убедитесь в правильности написания')
    bot.send_message(message.chat.id, get_weather(message.text))


@bot.message_handler(commands=['forecast'])
def forecast_day_request(message):
    day_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    today = date.today()
    possible_days = []

    for i in range(1, 6):
        delta = timedelta(days = i)
        day = months[(today+delta).month] + ', '+(today + delta).strftime(("%d"))
        possible_days.append(day)

    day_markup.row(*possible_days)
    request =  bot.send_message(message.chat.id,
                                    'В какой день вы хотите узнать погоду?',
                                    reply_markup=day_markup)

    bot.register_next_step_handler(request, forecast_city_request)

def forecast_city_request(message):
    today = date.today()
    possible_days = []

    for i in range(1, 6):
        delta = timedelta(days = i)
        day = months[(today+delta).month] + ', '+(today + delta).strftime(("%d"))
        possible_days.append(day)

    if not any(message.text in day for day in possible_days):
        bot.send_message(message.chat.id,
                         "❌Выбирайте день только из предложенных ниже!",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        handler = {possible_days[0]: send_forecast(1),
                possible_days[1]: send_forecast(2),
                possible_days[2]: send_forecast(3),
                possible_days[3]: send_forecast(4),
                possible_days[4]: send_forecast(5)}
        request = bot.send_message(message.chat.id,
                                        'Введите город, в котором хотите узнать погоду')
        bot.register_next_step_handler(request, handler.get(message.text))

def send_forecast(days):
    def forecast(message):
        try:
            get_forecast(message.text, days)
        except pyowm.exceptions.api_response_error.NotFoundError:
            bot.send_message(message.chat.id,
                             '❌Город не найден, убедитесь в правильности написания',
                             reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.send_message(message.chat.id,
                     get_forecast(city=message.text, days=2),
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    return forecast


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower().find('прогноз') > -1:
        forecast_day_request(message)
        return
    elif message.text.lower().find('погод') > -1:
        city_request = bot.send_message(message.chat.id,
                                        'Введите город, в котором хотите узнать погоду')
        bot.register_next_step_handler(city_request, send_weather)
        return

    request = apiai.ApiAI(config.APIAI_TOKEN).text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, 'Я Вас не совсем понял!')

while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)
