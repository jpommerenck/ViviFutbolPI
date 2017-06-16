from dbUtil import insert_log_info, insert_log_error, get_log_activity

def log_info(user, rol, action):
    insert_log_info(str(user), rol, action)

def log_error(user, rol, action, message):
    insert_log_error(str(user), rol, action, message)

def log_activity():
    return get_log_activity()
