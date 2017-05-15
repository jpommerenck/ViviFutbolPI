from flask import Flask, request, jsonify
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str, set_time
from dbUtil import modify_configuration_value, get_config_value, insert_download_code, count_available_download_codes
import time
import json

#Constantes de la base de datos
API_MANAGEMENT_PORT = 5002
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolLocal/Pictures/MonitorDevice/'


app = Flask(__name__)


#172.24.1.1:5002/getTime
@app.route('/getTime', methods=['GET', 'POST'])
def get_time():
    response = {"status":"ok", "currentTime": time.strftime('%H') + ":" + time.strftime('%M')}
    return jsonify(response)                


#172.24.1.1:5002/postTime
@app.route('/postTime', methods=['POST'])
def post_time():
    try:
        hora = request.form.get("time")
        horaPI = hora.split(':')[0]
        minutosPI = hora.split(':')[1]
        set_time(horaPI, minutosPI)
        response = {"status":"ok", "newTime":time.strftime('%H') + ":" + time.strftime('%M')}
        return jsonify(response)
    except:
        response = {"status":"error","error":"errorSettingTime","errorMessage":"No se pudo modificar la hora del dispositivo"}
        return jsonify(response)

                
#172.24.1.1:5002/changeRecordingTimes
@app.route('/setRecordingTimes', methods=['POST'])
def set_recording_times():
    try:
        startTime = request.form.get("startTime")
        endTime = request.form.get("endTime")
        modify_configuration_value("START_RECORDING_TIME", startTime)
        modify_configuration_value("FINISH_RECORDING_TIME", endTime)
        response = {"status":"ok"}
        return jsonify(response)
    except Exception as e:
        response = {"status":"error","error":"errorChangingRecordingTimes","errorMessage":"No se pudo modificar las horas de grabacion", "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/getRecordingTimes
@app.route('/getRecordingTimes', methods=['POST'])
def get_recording_times():
    try:
        startTime = get_config_value("START_RECORDING_TIME")
        endTime = get_config_value("FINISH_RECORDING_TIME")
        response = {"status":"ok", "startTime":startTime, "endTime":endTime}
        return jsonify(response)
    except:
        response = {"status":"error","error":"errorGettingRecordingTimes","errorMessage":"No se pudo obtener las horas de grabacion"}
        return jsonify(response)

#172.24.1.1:5002/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
def get_image_monitor_device():
    try:
        picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
        video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
        image_monitor_device(video_directory, picture_path)
        return send_file(picture_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"status":"error", "error":"errorMonitoringDevice", "errorMessage":"Error inesperado", "exception":str(e)})

#172.24.1.1:5002/uploadCodes
@app.route('/uploadCodes', methods=['GET', 'POST'])
def upload_codes():
    try:
        codes = json.loads(request.form.get("codes"))
        for code in codes:
            insert_download_code(code['code'])
        return jsonify({"status":"ok", "codes":codes})        
    except Exception as e:
        return jsonify({"status":"error", "error":"errorUploadingCodes", "errorMessage":"Error inesperado", "exception":str(e)})

#172.24.1.1:5002/countCodes
@app.route('/countCodes', methods=['GET', 'POST'])
def count_codes():
    try:
        count = count_available_download_codes()
        ##TODO obtener deviceId        
        deviceId = 1
        return jsonify({"status":"ok", "count":count, "deviceId":deviceId})        
    except Exception as e:
        return jsonify({"status":"error", "error":"errorCountingAvailableCodes", "errorMessage":"Error inesperado", "exception":str(e)})





if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1', port=API_MANAGEMENT_PORT)
