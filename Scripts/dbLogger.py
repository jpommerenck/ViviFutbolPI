import sqlite3

path = "/home/pi/ViviFutbolLocal/BD/"
bd_name = "vivifutbol.db"


#id date user rol action
def create_log_activity_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE log_activity (date_time TEXT, type TEXT, user TEXT, rol TEXT, action TEXT, description TEXT)')
    conn.close()


def insert_log_info(date, user, rol, action):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO log_activity VALUES("' + date + '","INFO","' + user + '","' + rol + '","' + action + '","")')
    conn.commit()
    conn.close()


def insert_log_error(date, user, rol, action, message):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO log_activity VALUES("' + date + '", "ERROR", "' + user + '", "' + rol + '", "' + action + '", "' + str(message) + '")')
    conn.commit()
    conn.close()


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
