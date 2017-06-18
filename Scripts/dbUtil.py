import sqlite3
from dateUtil import get_current_date_in_server_format_str, get_last_week_date_in_server_format_str, rest_days_to_date, get_current_date_str, str_to_date_time

path = "/home/pi/ViviFutbolLocal/BD/"
bd_name = "vivifutbol.db"

def create_video_mark_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE video_marks (markdate TEXT PRIMARY KEY, is_processed INTEGER)')
    conn.close()


# Esta funcion sirve para insertar las marcas de jugadas destacadas en la base de datos
# Ejemplo invocacion : insert_mark("2017-03-26_20-41-10")
def insert_mark(date):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO video_marks VALUES("'+date+'", 0)')
    conn.commit()
    conn.close()

def delete_mark(date):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM video_marks WHERE markdate = "'+date+'"')
    conn.commit()
    conn.close()

def get_last_mark():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    value = cur.execute('SELECT * FROM video_marks ORDER BY markdate DESC LIMIT 1;').fetchone()
    conn.close()
    if str(value)=='None':
        return ''
    else:
        return value[0]

def update_mark(markdate):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('UPDATE video_marks SET is_processed = 1 WHERE markdate = "'+markdate+'"')
    conn.commit()
    conn.close()

def create_configuration_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE configurations (variable TEXT PRIMARY KEY, value TEXT)')
    conn.close()

def create_download_codes_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE download_codes (code TEXT PRIMARY KEY, times_used INTEGER)')
    conn.close()

def create_used_codes_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE used_download_codes (code TEXT PRIMARY KEY, times_used INTEGER, downloads INTEGER, first_used TEXT, last_used TEXT, sent INTEGER)')
    conn.close()
    

def create_user_code_use_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE user_code_uses (code TEXT, phone TEXT, date TEXT, sent INTEGER, PRIMARY KEY(code, phone))')
    conn.close()
    
def create_maintenance_tokens_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE maintenance_tokens (token TEXT PRIMARY KEY)')
    conn.close()

def insert_maintenance_token(token):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT token FROM maintenance_tokens WHERE token = ?", (token,))
    existingToken = cur.fetchone()
    if existingToken is None:
        cur.execute('INSERT INTO maintenance_tokens VALUES("'+token+'")')
        conn.commit()
    conn.close()

def insert_download_code(code):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT code FROM download_codes WHERE code = ?", (code,))
    existingCode = cur.fetchone()
    if existingCode is None:
        cur.execute('INSERT INTO download_codes VALUES("'+code+'", 0)')
        conn.commit()
    conn.close()

def code_used(code, phone):
    currentDate = get_current_date_in_server_format_str()
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_code_uses WHERE code = "'+code+'" AND phone = "'+phone+'"')
    existingUse = cur.fetchone()
    if existingUse is None:
        cur.execute('INSERT INTO user_code_uses VALUES("'+code+'", "'+phone+'", "'+get_current_date_in_server_format_str()+'", 0)')
        conn.commit()
    cur.execute("SELECT * FROM used_download_codes WHERE code = ?", (code,))
    existingCode = cur.fetchone()
    if existingCode is None:
        cur.execute('INSERT INTO used_download_codes VALUES("'+code+'", 1, 0, "'+currentDate+'", "'+currentDate+'", 0)')
        conn.commit()
    else:
        timesUsed = existingCode[1]
        timesUsed = timesUsed + 1
        cur.execute('UPDATE used_download_codes SET times_used = '+str(timesUsed)+', last_used = "'+currentDate+'" WHERE code = ?', (code,))
        conn.commit()
    conn.close()

def code_download(code):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM used_download_codes WHERE code = ?", (code,))
    existingCode = cur.fetchone()
    if existingCode is not None:
        downloads = existingCode[2]
        downloads = downloads + 1
        cur.execute('UPDATE used_download_codes SET downloads = '+str(downloads)+' WHERE code = ?', (code,))
        conn.commit()
    conn.close()

def count_available_download_codes():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM download_codes WHERE times_used = 0")
    result = cur.fetchone()
    conn.close()
    return result[0]

def download_code_exists(code):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM download_codes WHERE code=?",(code,)) 
    data=cur.fetchone()
    if data is None:
        return False
    else:
        return True
    
def maintenance_token_exists(token):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM maintenance_tokens WHERE token=?",(token,)) 
    data=cur.fetchone()
    if data is None:
        return False
    else:
        return True
    
def insert_configuration_value(variable, value):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO configurations VALUES("'+variable+'", "'+value+'")')
    conn.commit()
    conn.close()

def modify_configuration_value(variable, value):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('UPDATE configurations SET value = "'+value+'" WHERE variable = "'+variable+'"')
    conn.commit()
    conn.close()

def get_all_marks_between_dates(start, finish):
    marks = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM video_marks WHERE(markdate > "'+start+'" AND markdate < "'+finish+'")'):
        mark = {
            "markdate": row[0],
            "is_processed": row[1]
        }
        marks.append(mark)
    conn.close()
    return marks

def get_used_codes():
    codes = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM user_code_uses WHERE(sent = 0)'):
        code = {
            "code": row[0],
            "phone": row[1],
            "date":row[2]
        }
        codes.append(code)
    conn.close()
    return codes


def get_used_codes_without_downloads():
    codes = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM used_download_codes WHERE (downloads = 0 AND sent = 0)'):
        code = {
            "code": row[0],
            "timesAccessed": row[1],
            "firstUse":row[3],
            "lastUse":row[4]
        }
        codes.append(code)
    conn.close()
    return codes


def mark_codes_as_sent():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('UPDATE used_download_codes SET sent = 1 WHERE (downloads = 0 AND sent = 0)')
    cur.execute('UPDATE user_code_uses SET sent = 1')


def get_all_marks_not_processed():
    marks = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM video_marks WHERE(is_processed = 0)'):
        marks.append(row[0])
    conn.close()
    return marks


def get_all_marks():
    marks = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM video_marks'):
        marks.append(row[0])
    conn.close()
    return marks


def delete_all_marks():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM video_marks')
    conn.commit()
    conn.close()
    
#Ejemplo get_config_value('START_RECORDING_TIME')
def get_config_value(variable):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    value = cur.execute('SELECT * FROM configurations WHERE(variable = "' + variable + '")').fetchone()
    conn.close()
    return value[1]

def create_all_tables():
    create_video_mark_table()
    create_configuration_table()
    create_download_codes_table()
    create_maintenance_tokens_table()
    create_used_codes_table()
    create_user_code_use_table()
    create_configurations_aux_table()


def create_configurations_aux_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE configurations_aux (variable TEXT, value TEXT)')
    conn.close()
    

def insert_configurations_aux_value(variable, value):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO configurations_aux VALUES("'+variable+'", "'+value+'")')
    conn.commit()
    conn.close()


def modify_configurations_aux_value(variable, value):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('UPDATE configurations_aux SET value = "'+value+'" WHERE variable = "'+variable+'"')
    conn.commit()
    conn.close()
    

def get_config_aux_value(variable):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    value = cur.execute('SELECT * FROM configurations_aux WHERE(variable = "' + variable + '")').fetchone()
    conn.close()
    return value[1]

    
# Setea las varaibles de configuracion utilizadas en la base de datos
def create_environment_config():
    create_all_tables()
    insert_configuration_value('VIDEO_LOCALIZATION_PATH','/home/pi/ViviFutbolLocal/Videos/')
    insert_configuration_value('PICTURES_LOCALIZATION_PATH','/home/pi/ViviFutbolLocal/Pictures/MonitorDevice/')
    insert_configuration_value('TEMP_FILES_PATH','tmp')
    insert_configuration_value('CONCAT_VIDEOS_PATH','/Concat/')
    insert_configuration_value('MP4_VIDEOS_PATH','/mp4/')
    insert_configuration_value('HIGHLIGHTS_VIDEOS_PATH','Highlights/')
    insert_configuration_value('API_OWNER_PORT','5001')
    insert_configuration_value('API_MANAGEMENT_PORT','5002')
    insert_configuration_value('API_USER_PORT','5000')
    insert_configuration_value('SECONDS_WAITING_FOR_CONVERT_VIDEO','30')
    insert_configuration_value('TIME_AFTER_RECORD','5')
    insert_configuration_value('TIME_BEFORE_RECORD','5')
    insert_configuration_value('TIME_RECORDING_VIDEO','15')
    insert_configuration_value('START_RECORDING_TIME','0900')
    insert_configuration_value('FINISH_RECORDING_TIME','0000')
    insert_configuration_value('OWNER_TOKEN','0000')
    insert_configuration_value('MANAGEMENT_TOKEN','0000')
    insert_configuration_value('INSTALLER_TOKEN','0000')
    insert_configuration_value('DISK_START_DELETE_SPACE','1024')
    insert_configuration_value('DISK_STOP_DELETE_SPACE','15360')
    #11-07-2017
    insert_configuration_value('HIGHLIGHT_NAME','Hightlight_')
    insert_configuration_value('HIGHLIGHT_AUX_NAME','Hightlight_Aux_')
    insert_configuration_value('COMPLETE_NAME','Complete_')
    insert_configuration_value('AUDIOS_LOCALIZATION_PATH','/home/pi/ViviFutbolLocal/Audios/')
    insert_configuration_value('SECONDS_WAITING_FOR_ADD_NEW_MARK','5')
    insert_configuration_value('VIDEO_TOTAL_TIME','3600')
