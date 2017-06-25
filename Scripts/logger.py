from dbLogger import insert_log_info, insert_log_error, get_log_activity, get_latest_log_activity, empty_db_log
from datetime import datetime, timedelta

def log_info(user, rol, action):
    insert_log_info(get_current_time(), str(user), rol, action)

def log_error(user, rol, action, message):
    insert_log_error(get_current_time(), str(user), rol, action, message)

def log_activity():
    return get_log_activity()

def latest_log_activity():
    return get_latest_log_activity(get_last_week_date_in_server_format_str())

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_last_week_date_in_server_format_str():
    date = datetime.now()
    last_week = date - timedelta(days=7)
    return last_week.strftime('%Y-%m-%d %H:%M:%S')

def empty_log():
    return empty_db_log()
