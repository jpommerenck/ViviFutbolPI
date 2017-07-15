from datetime import datetime, timedelta
import time
import os
from logger import log_error

def get_current_date_str():
    try:
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_current_date_str()', str(e))

def get_current_date_in_server_format_str():
    try:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_current_date_in_server_format_str()', str(e))

def get_last_week_date_in_server_format_str():
    try:
        date = datetime.now()
        last_week = date - timedelta(days=7)
        return last_week.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_last_week_date_in_server_format_str()', str(e))

def get_date_str(date_to_convert):
    try:
        return date_to_convert.strftime('%Y-%m-%d_%H-%M-%S')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_date_str()', str(e))


def str_to_date_time(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - str_to_date_time()', str(e))


def str_to_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - str_to_date()', str(e))

    
# Obtiene la resta de 2 fechas en segundos
def rest_date_to_seconds(date1, date2):
    try:
        difference = date2 - date1
        return difference.seconds
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - rest_date_to_seconds()', str(e))


# Toma el path de un video y obtiene la fecha del video
def convert_path_to_str_date(video_path):
    try:
        video_str_date = video_path.split('.mp4')[0]
        video_str_date = video_str_date.split('/mp4/')[1]
        return video_str_date
    except Exception as e:
        raise Exception("dateUtil.py - convert_path_to_str_date(" + video_path + "): " + str(e))
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - convert_path_to_str_date()', str(e))


def add_seconds_to_date(date_to_add, seconds_to_add):
    try:
        date_to_add += timedelta(seconds=seconds_to_add)
        return date_to_add
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - add_seconds_to_date()', str(e))


def rest_seconds_to_date(date_to_rest, seconds_to_rest):
    try:
        date_to_rest -= timedelta(seconds=seconds_to_rest)
        return date_to_rest
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - rest_seconds_to_date()', str(e))


def rest_days_to_date(date_to_rest, days_to_rest):
    try:
        date_to_rest -= timedelta(days=days_to_rest)
        return date_to_rest
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - rest_days_to_date()', str(e))


def add_days_to_date(date_to_add, days_to_add):
    try:
        date_to_add += timedelta(days=days_to_add)
        return date_to_add
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - add_days_to_date()', str(e))


def get_current_short_date_str():
    try:
        return datetime.now().strftime('%Y-%m-%d')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_current_short_date_str()', str(e))


def get_yesterday_short_date_str():
    try:
        date = datetime.now()
        yesterday = date - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_yesterday_short_date_str()', str(e))


def get_current_time_int():
    try:
        return int(datetime.now().strftime('%H%M'))
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_current_time_int()', str(e))

        
def get_time(date_to_convert):
    try:
        date_aux = date_to_convert.split('_')[1]
        date_time = date_aux.split('.')[0]
        return date_time.split('-')[0] + date_time.split('-')[1] + date_time.split('-')[2]
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_time()', str(e))


def get_current_hour():
    try:
        return int(datetime.now().strftime('%H'))
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_current_hour()', str(e))


def get_time_subtraction(date_to_convert, time_recording):
    try:
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
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_time_subtraction()', str(e))


def get_time_subtr(time_start, time_recording):
    try:
        seconds_start = time_start[4:6]
        minutes_start = int(time_start[2:4])
        hours_start = int(time_start[0:2])
        minutes_int = (minutes_start-time_recording)%60

        if minutes_int>minutes_start:
            hours_start=hours_start-1
            
        if hours_start<10:
            hours = '0'+str(hours_start)
        else:
            hours = str(hours_start)
                
        if minutes_int<10:
            minutes = '0'+str(minutes_int)
        else:
            minutes = str(minutes_int)
         
        return hours + minutes + seconds_start
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_time_subtr()', str(e))


def get_time_adition(date_to_convert, time_recording):
    try:
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
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_time_adition()', str(e))


def get_time_adi(time_start, time_recording):
    try:
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
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_time_adi()', str(e))


def get_seconds_cut(time_first_video, time_match):
    try:
        second_first_video_str = time_first_video[4:6]
        minutes_first_video_str = time_first_video[2:4]
        hours_first_video_str = time_first_video[0:2]
        seconds_first_video = int(second_first_video_str) + int(minutes_first_video_str)*60 + int(hours_first_video_str)*3600

        second_time_match_str = time_match[4:6]
        minutes_time_match_str = time_match[2:4]
        hours_time_match_str = time_match[0:2]
        seconds_match = int(second_time_match_str) + int(minutes_time_match_str)*60 + int(hours_time_match_str)*3600

        return seconds_match - seconds_first_video
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - get_seconds_cut()', str(e))


def convert_seconds_to_minutes(seconds):
    try:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - convert_seconds_to_minutes()', str(e))


def set_time(hours, minutes):
    try:
        datePI = get_current_short_date_str()
        os.system('sudo date -s "'+datePI+' '+hours+':'+minutes+':00"')
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - set_time()', str(e))


def check_for_insert_mark(new_mark, last_mark, time_blocked):
    try:
        last_mark = add_seconds_to_date(last_mark, time_blocked)
        if new_mark > last_mark:
            return True
        else:
            return False
    except Exception as e:
        raise Exception("dateUtil.py - check_for_insert_mark(): " + str(e))
        log_error("SYSTEM", 'SYSTEM', 'dateUtil.py - check_for_insert_mark()', str(e))
