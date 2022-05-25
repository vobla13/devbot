import telebot
import helpers
from telebot import types, TeleBot



# Костыль: перейти на getenv
token = helpers.get_bot_token()
bot: TeleBot = telebot.TeleBot(token)


# Ответ на команду /start
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


# Получить статусы по всем dev в одном сообщении командой /status
@bot.message_handler(commands=['status'])
def status(message, res=False):
    answer = helpers.get_all_status()
    bot.send_message(message.chat.id, answer)


# Занять dev по сообщению 'take dev(номер)'разбирается регуляркой
@bot.message_handler(regexp='[Tt]ake [Dd]ev[0-9]')
def take_dev(message, res=False):
    dev = message.text[5:].lower()
    # Помимо пользователя и бота в логику вклинивается еще третья сторона - текущий пользователь dev (если он ранее был занят)
    # Нам небходимо сохранять правильные username и chat_id и корректно передавать их в методы
    # Сохраняем user_name и chat_id запрашивающего (candidate)
    candidate_username = message.from_user.username
    candidate_chat_id = message.chat.id
    
    # Проверяем, что dev существует
    if helpers.get_dev_status(dev) is False:
        bot.send_message(candidate_chat_id, f'{dev} не существует!')

    # Проверяем, что dev занят
    # Если False, то записываем запращивающего хозяином и возвращаем ему ответ с успешным статусом
    elif helpers.check_dev_busy(dev) is False:
        answer = helpers.set_dev_user(dev, candidate_username, candidate_chat_id)    
        bot.send_message(candidate_chat_id, answer)
    
    # Если True и там кто-то уже есть.
    else:
        # Запрашиваем user_name и chat_id текущего хозяина и записываем их в переменные
        dev_username, dev_user_chat_id = helpers.get_dev_user(dev)
        # Пишем запрашивающему сообщение о том, что dev занят и кем
        bot.send_message(candidate_chat_id, f'{dev} занят @{dev_username}. Запрашиваю разрешение...')
        
        # Создаем инлайн клавиатуру
        buttons = ['Yes', 'No']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*buttons)
        # Посылаем запрос текущему пользователю
        bot.send_message(dev_user_chat_id, f'@{candidate_username} хочет отобрать у тебя {dev}!', reply_markup=keyboard)
        
        # Создаем обработчики кнопок
        @bot.message_handler(content_types='text')
        def button_reply(message, res=False):
            if message.text=="Yes":
                # Если ДА, то освобождаем dev и заново устанавливаем нового пользователя
                # helpers.free_dev(dev)
                bot.send_message(dev_user_chat_id, f'Cпасибо :)', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(candidate_chat_id, f'@{dev_username} разрешил')
                # answer = helpers.set_dev_user(dev, message.from_user.username, message.chat.id)
                # bot.send_message(dev_user_chat_id, answer)
            elif message.text=="No":
                # Если НЕТ, то отправляем отказ
                bot.send_message(dev_user_chat_id, f'Грусть, печаль, тоска', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(candidate_chat_id, f'@{dev_username} отказал. Напишите ему.')


# Освободить dev по сообщению 'free dev(номер)' разбирается регуляркой
@bot.message_handler(regexp='[Ff]ree [Dd]ev[0-9]')
def free_dev(message, res=False):
    dev = message.text[5:].lower()
    result = helpers.free_dev(dev)
    bot.send_message(message.chat.id, result, reply_to_message_id=message.message_id)


# Запускаем бота
# Можно использовать try/except с бесконечным циклом, но есть риск попасть в infinityloop
# Возможно, решается таской, которая будет перезапускать бота при падении
bot.infinity_polling(interval=0, timeout=20)
