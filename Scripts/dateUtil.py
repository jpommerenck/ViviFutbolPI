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

def get_time(date_to_convert):
    date_time = date_to_convert.split('_')[1]
    return date_time.split('-')[0] + date_time.split('-')[1] + date_time.split('-')[2]


def get_time_subtraction(date_to_convert, time_recording):
    date_time = date_to_convert.split('_')[1]
    minuts_int = (int(date_time.split('-')[1])-time_recording)%60
    seconds_aux = date_time.split('-')[2]
    seconds = seconds_aux.split('.')[0]
    hours = date_time.split('-')[0]

    if minuts_int>int(date_time.split('-')[1]):
        hours_int = int(date_time.split('-')[0]) - 1
        if hours_int<10:
            hours = '0'+str(hours_int)
        else:
            hours = str(hours_int)   
    
    if minuts_int<10:
        minuts = '0'+str(minuts_int)
    else:
        minuts = str(minuts_int)
     
    return hours + minuts + seconds


def get_time_adition(date_to_convert, time_recording):
    date_time = date_to_convert.split('_')[1]
    minuts_int = (int(date_time.split('-')[1])+time_recording)%60
    seconds_aux = date_time.split('-')[2]
    seconds = seconds_aux.split('.')[0]
    hours = date_time.split('-')[0]

    if minuts_int<int(date_time.split('-')[1]):
        hours_int = int(date_time.split('-')[0]) + 1
        if hours_int<10:
            hours = '0'+str(hours_int)
        else:
            hours = str(hours_int)   
    
    if minuts_int<10:
        minuts = '0'+str(minuts_int)
    else:
        minuts = str(minuts_int)
     
    return hours + minuts + seconds
