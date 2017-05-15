import sqlite3

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

def insert_download_code(code):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT code FROM download_codes WHERE code = ?", (code,))
    existingCode = cur.fetchone()
    if existingCode is None:
        cur.execute('INSERT INTO download_codes VALUES("'+code+'", 0)')
        conn.commit()
    conn.close()

def count_available_download_codes():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM download_codes WHERE times_used = 0")
    result = cur.fetchone()
    conn.close()
    return result[0]

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

def get_all_marks_not_processed():
    marks = []
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM video_marks WHERE(is_processed = 0)'):
        marks.append(row[0])
    conn.close()
    return marks

def delete_all_marks():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM video_marks')
    conn.commit()
    conn.close()
    

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
