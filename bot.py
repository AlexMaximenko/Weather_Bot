import telebot
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Добрый день')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Всего хорошего')

bot.polling(none_stop=True)
