from flask import Flask
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str
import time

#Constantes de la base de datos
API_OWNER_PORT = 5002

app = Flask(__name__)

#172.24.1.1:5002/getPrueba
@app.route('/getPrueba', methods=['GET', 'POST'])
def get_prueba():
    return '{"respuesta":"hola"}'

#172.24.1.1:5002/getPrueba
@app.route('/getTime', methods=['GET', 'POST'])
def get_time():
    return time.strftime('%H %M')

if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1', port=API_OWNER_PORT)
