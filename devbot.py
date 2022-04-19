import telebot
import helpers
from telebot import types, TeleBot




token = helpers.get_bot_token()
bot: TeleBot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message, res=False):
    if message.from_user.username != '':
        user = message.from_user.username
    else:
        user = message.from_user.first_name

    bot.send_message(message.chat.id, f'Hi, @{user}!\n '
                                      f'/status - статусы\n'
                                      f'take dev - забрать dev\n'
                                      f'free dev - освободить dev\n')


@bot.message_handler(commands=['status'])
def status(message, res=False):
    bot.send_message(message.chat.id, helpers.get_all_status())


@bot.message_handler(regexp='[Tt]ake [Dd]ev[0-9]')
def take_dev(message, res=False):
    dev = message.text[5:].lower()
    bot.send_message(message.chat.id, helpers.set_dev_user(dev, f'@{message.from_user.username}'))


@bot.message_handler(regexp='[Ff]ree [Dd]ev[0-9]')
def free_dev(message, res=False):
    dev = message.text[5:].lower()
    result = helpers.free_dev(dev)
    bot.send_message(message.chat.id, result)


bot.polling()
