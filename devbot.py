import telebot
import helpers
from telebot import types, TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton



# Костыль: перейти на getenv
token = helpers.get_bot_token()
bot: TeleBot = telebot.TeleBot(token)


# Создаем объект Inline-клавиатуры
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


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
    bot.reply_to(message, answer)


# Занять dev по сообщению 'take dev(номер)'разбирается регуляркой
@bot.message_handler(regexp='[Tt]ake [Dd]ev[0-9]')
def take_dev(message):
    candidate_username = message.from_user.username
    candidate_chat_id = message.chat.id
    dev = message.text[5:].lower()
    dev_username, dev_user_chat_id = helpers.get_dev_user(dev)

    # Помимо пользователя и бота в логику вклинивается еще третья сторона - текущий пользователь dev (если он ранее был занят)
    # Нам небходимо сохранять правильные username и chat_id и корректно передавать их в методы
    # Сохраняем user_name и chat_id запрашивающего (candidate)
    
    # Проверяем, что dev существует
    if helpers.get_dev_status(dev) is False:
        bot.reply_to(message, f'{dev} не существует!')
    # Проверяем, что dev занят
    # Если False, то записываем запрашивающего хозяином и возвращаем ему ответ с успешным статусом
    elif helpers.check_dev_busy(dev) is False:
        answer = helpers.set_dev_user(dev, candidate_username, candidate_chat_id)    
        bot.reply_to(message, answer)
    # Если True и там кто-то уже есть.
    else:
        # Пишем запрашивающему сообщение о том, что dev занят и кем
        bot.reply_to(message, f'{dev} занят @{dev_username}. Запрашиваю разрешение...')
        # Создаем обработчик колбеков нажатий
        @bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "cb_yes":
                bot.answer_callback_query(call.id, "Спасибо :)")
                helpers.free_dev(dev)
                # helpers.set_dev_user(dev, candidate_username, candidate_chat_id)
                bot.send_message(candidate_chat_id, f'from: {dev_username} - Разрешено')
            elif call.data == "cb_no":
                bot.answer_callback_query(call.id, "А ты жадный :)")
                bot.send_message(candidate_chat_id, f'from: {dev_username} - Отказано!')
        
        # Отправляем запрос хозяину dev
        # Проблема при смене ролей - перестают правильно разруливаться сообщения "Разрешено / Отказано"
        # Дебаг выявил проблему, что переменные dev, candidate_username, candidate_chat_id после первого круга фиксируются
        # Подумать, как прокидывать переменные в другие переменные и переиспользовать их внутри отдельных кусков функции
        bot.send_message(dev_user_chat_id, f'@{candidate_username} хочет отобрать у тебя dev!', reply_markup=gen_markup())



# Освободить dev по сообщению 'free dev(номер)' разбирается регуляркой
@bot.message_handler(regexp='[Ff]ree [Dd]ev[0-9]')
def free_dev(message, res=False):
    dev = message.text[5:].lower()
    result = helpers.free_dev(dev)
    bot.send_message(message.chat.id, result, reply_to_message_id=message.message_id)


# Возвращает пользователя на dev (для отладки)
@bot.message_handler(regexp='[Uu]ser [Dd]ev[0-9]')
def user_dev(message, res=False):
    dev = message.text[5:].lower()
    user, chat = helpers.get_dev_user(dev)
    result = str(user) + str(chat)
    bot.send_message(message.chat.id, result, reply_to_message_id=message.message_id)

# Запускаем бота
# Можно использовать try/except с бесконечным циклом, но есть риск попасть в infinityloop
# Возможно, решается таской, которая будет перезапускать бота при падении
bot.infinity_polling(interval=0, timeout=20)
