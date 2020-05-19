import telebot
import config
import time as tm
from weather import get_weather

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def starting(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)
    start_markup.row('/start', '/hide', '/weather')
    bot.send_message(message.chat.id, "Привет!\n")
    bot.send_message(message.chat.id, "Чтобы скрыть клавиатуру, нажмите \hide\n")
    bot.send_message(message.chat.id,
                     "Чтобы узнать погоду, нажмите \weather",
                     reply_markup=start_markup)


@bot.message_handler(commands=['hide'])
def hiding(message):
    bot.send_message(message.chat.id,
                     '...',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['weather'])
def weather_command(message):
    city_request = bot.send_message(message.chat.id,
                                    'Введите город или страну, в которой хотите узнать погоду')
    bot.register_next_step_handler(city_request, send_weather)

def send_weather(message):
    answer = get_weather(message.text)
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока')

bot.polling(none_stop=True)
