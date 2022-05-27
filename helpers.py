from datetime import datetime
from datetime import timedelta




# Converts timedelta to days, hours, minutes and seconds
def timedelta_format(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds


# Setup devs and their status
# Костыль: перейти на класс и передавать объект класса в словарь
# Хранить состояение классов в JSON и поднимать при перезапуске бота
devs = {
        'dev2': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev3': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev4': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev5': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev6': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev7': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev8': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev9': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev10': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev11': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()},
        'dev12': {'user': 'free', 'chat_id:': 0, 'time': datetime.now()}
    }


# Get tg_bot token
# Костыль: заменить на os.getenv и библиотеку dotenv, и передавать в нее токен
def get_bot_token():
    f = open('setup', mode='r', encoding='UTF-8')
    token = f.read()
    f.close()
    return token


# Get <user_name>, <chat_id> by <dev>
def get_dev_user(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        user = current_dev.get('user')
        chat_id = current_dev.get('chat_id')
        return user, chat_id
    else:
        return None


# Get <dev> status
def get_dev_status(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        d, h, m, s = timedelta_format(datetime.now() - current_dev.get('time'))
        user = current_dev.get('user')
        chat_id = current_dev.get('chat_id')
        time = f'(+{h}h {m}m)'
        return user, time, chat_id
    else:
        return False


# Returns all <dev> status
def get_all_status():
    result = ''
    for dev in devs:
        user, time, chat_id = get_dev_status(dev)
        result += f'{dev} | @{user} {time} | {chat_id}\n'
    return result


# Check <dev> for existing <user>: returns True if <user> is not 'free'
def check_dev_busy(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        if current_dev['user'] != 'free':
            return True
        else:
            return False


# Set <user> to <dev>: returns <dev> status if <dev> have existing <user>
# Порефакторить
def set_dev_user(dev, user, chat_id):
    current_dev = devs.get(dev)
    if current_dev is not None:
        current_dev['user'] = user
        current_dev['time'] = datetime.now()
        current_dev['chat_id'] = chat_id
        return f'{dev} занял @{user}'
    else:
        return f'{dev} не существует!'


# Reset <dev> status to "Free"
def free_dev(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        current_dev['user'] = 'free'
        current_dev['time'] = datetime.now()
        current_dev['chat_id'] = None
        return f'{dev} теперь свободен!'
    else:
        return f'{dev} не существует!'


