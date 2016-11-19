from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    marks = []
    conn = sqlite3.connect("vivifutbol.db")
    cur = conn.cursor()
    to_return = ""
    for row in cur.execute('SELECT * FROM video_marks'):
        to_return = to_return + row[0] + ","
    conn.close()
    return to_return


@app.route('/pruebas/<id>')
def get_prueba(id):
    return "dsa" + id

if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1')
