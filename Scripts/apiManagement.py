from flask import Flask, request
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str, set_time
import time
import json

#Constantes de la base de datos
API_OWNER_PORT = 5002

app = Flask(__name__)

#172.24.1.1:5002/getPrueba
@app.route('/getPrueba', methods=['GET', 'POST'])
def get_prueba():
    return '{"respuesta":"hola"}'

#172.24.1.1:5002/getTime
@app.route('/getTime', methods=['GET', 'POST'])
def get_time():
    return '{"currentTime":"' + time.strftime('%H') + ":" + time.strftime('%M') + '"}'     

#172.24.1.1:5002/postTime
@app.route('/postTime', methods=['POST'])
def post_time():
    try:
        current_json = request.data
        timeRequest = json.loads(current_json)
        hora = timeRequest["currentTime"]
        horaPI = hora.split(':')[0]
        minutosPI = hora.split(':')[1]
        set_time(horaPI, minutosPI)
        return '{"status":"ok"}'
    except:
       return '{"status":"error","error":"noSetTime","errorMessage":"No se pudo modificar la hora del dispositivo"}' 

if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1', port=API_OWNER_PORT)
