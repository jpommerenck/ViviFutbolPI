from datetime import datetime
from datetime import timedelta

def get_current_date_str():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def get_date_str(date_to_convert):
    return date_to_convert.strftime('%Y-%m-%d_%H-%M-%S')

def str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

def add_seconds_to_date(date_to_add, seconds_to_add):
    date_to_add += timedelta(seconds=seconds_to_add)
    return date_to_add

def get_current_short_date_str():
    return datetime.now().strftime('%Y-%m-%d')

def get_current_time_int():
    return int(datetime.now().strftime('%H%M'))
