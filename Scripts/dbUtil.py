import sqlite3

path = "/home/pi/VIviFutbol/BD/"
bd_name = "vivifutbol.db"

def create_video_mark_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE video_marks (markdate TEXT PRIMARY KEY, is_processed INTEGER)')
    conn.close()

def insert_mark(date):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO video_marks VALUES("'+date+'", 0)')
    conn.commit()
    conn.close()

def create_configuration_table():
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE configurations (variable TEXT PRIMARY KEY, value TEXT)')
    conn.close()

def insert_configuration_value(variable, value):
    conn = sqlite3.connect(path + bd_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO configurations VALUES("'+variable+'", "'+value+'")')
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
