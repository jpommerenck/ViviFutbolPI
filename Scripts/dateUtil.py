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
    date_aux = date_to_convert.split('_')[1]
    date_time = date_aux.split('.')[0]
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

def get_time_subtr(time_start, time_recording):
    seconds_start = time_start[4:6]
    minutes_start = int(time_start[2:4])
    hours_start = int(time_start[0:2])
    minuts_int = (minutes_start-time_recording)%60

    if minuts_int>minutes_start:
        hours_start=hours_start-1
        
    if hours_start<10:
        hours = '0'+str(hours_start)
    else:
        hours = str(hours_start)
            
    if minuts_int<10:
        minuts = '0'+str(minuts_int)
    else:
        minuts = str(minuts_int)
     
    return hours + minuts + seconds_start

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

def get_time_adi(time_start, time_recording):
    seconds_start = time_start[4:6]
    minutes_start = int(time_start[2:4])
    hours_start = int(time_start[0:2])
    minuts_int = (minutes_start+time_recording)%60

    if minuts_int<minutes_start:
        hours_start=hours_start+1

    if hours_start<10:
        hours = '0'+str(hours_start)
    else:
        hours = str(hours_start)   
    
    if minuts_int<10:
        minuts = '0'+str(minuts_int)
    else:
        minuts = str(minuts_int)
     
    return hours + minuts + seconds_start

def get_seconds_cut(time_first_video, time_match):
    second_first_video_str = time_first_video[4:6]
    minutes_first_video_str = time_first_video[2:4]
    hours_first_video_str = time_first_video[0:2]
    seconds_first_video = int(second_first_video_str) + int(minutes_first_video_str)*60 + int(hours_first_video_str)*3600

    second_time_match_str = time_match[4:6]
    minutes_time_match_str = time_match[2:4]
    hours_time_match_str = time_match[0:2]
    seconds_match = int(second_time_match_str) + int(minutes_time_match_str)*60 + int(hours_time_match_str)*3600

    return seconds_match - seconds_first_video


