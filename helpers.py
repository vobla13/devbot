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
devs = {
        'dev2': {'user': 'free', 'time': datetime.now()},
        'dev3': {'user': 'free', 'time': datetime.now()},
        'dev4': {'user': 'free', 'time': datetime.now()},
        'dev5': {'user': 'free', 'time': datetime.now()},
        'dev6': {'user': 'free', 'time': datetime.now()},
        'dev7': {'user': 'free', 'time': datetime.now()},
        'dev8': {'user': 'free', 'time': datetime.now()},
        'dev9': {'user': 'free', 'time': datetime.now()},
        'dev10': {'user': 'free', 'time': datetime.now()},
        'dev11': {'user': 'free', 'time': datetime.now()},
        'dev12': {'user': 'free', 'time': datetime.now()}
    }


# Get tg_bot token
def get_bot_token():
    f = open('setup', mode='r', encoding='UTF-8')
    token = f.read().split('\n')
    f.close()
    return token[0]


# Get <dev>, <user> and user <timedelta> in HH:MM format by <dev>
def get_dev_status(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        user = current_dev.get('user')
        d, h, m, s = timedelta_format(datetime.now() - current_dev.get('time'))
        return f'{dev} | {user} (+{h}h {m}m)'
    else:
        return f'{dev} is not available.'


# Returns all <dev> status
def get_all_status():
    result = ''
    for dev in devs:
        result += get_dev_status(dev) + '\n'
    return result


# Check <dev> for existing <user>: returns False if <user> is not 'free'
def check_dev_user(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        if current_dev['user'] != 'free':
            return False
    else:
        return f'{dev} is busy.'


# Set <user> to <dev>: returns <dev> status if <dev> have existing <user>
def set_dev_user(dev, user):
    current_dev = devs.get(dev)
    if current_dev is not None:
        if check_dev_user(dev) is not False:
            current_dev['user'] = user
            current_dev['time'] = datetime.now()
            return f'{user} -> {dev}'
        else:
            current_user = current_dev['user']
            return f'FAILED. Is busy by {current_user}.'
    else:
        return f'{dev} is not available.'


# Reset <dev> status to "Free"
def free_dev(dev):
    current_dev = devs.get(dev)
    if current_dev is not None:
        current_dev['user'] = 'free'
        current_dev['time'] = datetime.now()
        return f'{dev} is free now!'
    else:
        return f'{dev} is not available.'

