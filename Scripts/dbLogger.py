import sqlite3
from txtLogger import log_error

path = "/home/pi/ViviFutbolLocal/BD/"
bd_name = "vivifutbol.db"


#id date user rol action
def create_log_activity_table():
    try:
        conn = sqlite3.connect(path + bd_name)
        cur = conn.cursor()
        cur.execute('CREATE TABLE log_activity (date_time TEXT, type TEXT, user TEXT, rol TEXT, action TEXT, description TEXT)')
        conn.close()
    except Exception as e:
        log_error("Error in dbLogger.create_log_activity_table() --> "+str(e)) 

def insert_log_info(date, user, rol, action):
    try:
        conn = sqlite3.connect(path + bd_name)
        cur = conn.cursor()
        cur.execute('INSERT INTO log_activity VALUES("' + date + '","INFO","' + user + '","' + rol + '","' + action + '","")')
        conn.commit()
        conn.close()
    except Exception as e:
        message = date+" - "+user+" - "+rol+" - "+action
        log_error("Error in dbLogger.insert_log_info(). Message: "+message+". Exception: "+str(e))


def insert_log_error(date, user, rol, action, message):
    try:
        conn = sqlite3.connect(path + bd_name)
        cur = conn.cursor()
        cur.execute('INSERT INTO log_activity VALUES("' + date + '", "ERROR", "' + user + '", "' + rol + '", "' + action + '", "' + str(message) + '")')
        conn.commit()
        conn.close()
    except Exception as e:
        errorMessage = date+" - "+user+" - "+rol+" - "+action+" - "+message
        log_error("Error in dbLogger.insert_log_error(). Message: "+errorMessage+". Exception: "+str(e))


def get_log_activity():
    logs = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM log_activity'):
        log = {
            "date_time": row[0],
            "type": row[1],
            "user":row[2],
            "rol":row[3],
            "action":row[4],
            "description":row[5]
        }
        logs.append(log)
    conn.close()
    return logs


def get_latest_log_activity(start_date):
    logs = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM log_activity WHERE date_time >= "'+start_date+'"'):
        log = {
            "date_time": row[0],
            "type": row[1],
            "user":row[2],
            "rol":row[3],
            "action":row[4],
            "description":row[5]
        }
        logs.append(log)
    conn.close()
    return logs


def delete_old_logs():
    date = get_current_date_str()
    last_date = rest_days_to_date(str_to_date_time(date), 30)
    last_date = str(last_date).split(' ')[0]
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM log_activity WHERE date_time <= "' + last_date + '"')
    conn.commit()
    conn.close()

def empty_db_log():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM log_activity')
    conn.commit()
    conn.close()
