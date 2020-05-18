import telebot

token = "1269369397:AAFMfPxUtsfBAzHwC9gQqwnlagQUPqo_3s4"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Добрый день')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Всего хорошего')

bot.polling(none_stop=True)
