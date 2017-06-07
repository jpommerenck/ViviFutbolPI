from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPTokenAuth
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str, set_time
from dbUtil import modify_configuration_value, get_config_value, insert_download_code, count_available_download_codes, maintenance_token_exists, log_info, log_error
import time
import json

#Constantes de la base de datos
API_MANAGEMENT_PORT = 5002
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolLocal/Pictures/MonitorDevice/'


app = Flask(__name__)
auth = HTTPTokenAuth('Token')


#172.24.1.1:5002/getTime
@app.route('/getTime', methods=['GET', 'POST'])
@auth.login_required
def get_time():
    try:
        email = request.form.get("email")
        response = {"status":"ok", "currentTime": time.strftime('%H') + ":" + time.strftime('%M')}
        return jsonify(response)
    except:
        response = {"status":"error","error":"errorGettingTime","errorMessage":"No se pudo obtener la hora del dispositivo"}
        return jsonify(response)


#172.24.1.1:5002/postTime
@app.route('/postTime', methods=['POST'])
@auth.login_required
def post_time():
    try:
        hora = request.form.get("time")
        email = request.form.get("email")
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
@auth.login_required
def set_recording_times():
    try:
        startTime = request.form.get("startTime")
        endTime = request.form.get("endTime")
        email = request.form.get("email")
        modify_configuration_value("START_RECORDING_TIME", startTime)
        modify_configuration_value("FINISH_RECORDING_TIME", endTime)
        response = {"status":"ok"}
        return jsonify(response)
    except Exception as e:
        response = {"status":"error","error":"errorChangingRecordingTimes","errorMessage":"No se pudo modificar las horas de grabacion", "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/getRecordingTimes
@app.route('/getRecordingTimes', methods=['POST'])
@auth.login_required
def get_recording_times():
    try:
        startTime = get_config_value("START_RECORDING_TIME")
        endTime = get_config_value("FINISH_RECORDING_TIME")
        email = request.form.get("email")
        response = {"status":"ok", "startTime":startTime, "endTime":endTime}
        return jsonify(response)
    except:
        response = {"status":"error","error":"errorGettingRecordingTimes","errorMessage":"No se pudo obtener las horas de grabacion"}
        return jsonify(response)


#172.24.1.1:5002/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
@auth.login_required
def get_image_monitor_device():
    try:
        email = request.form.get("email")
        picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
        video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
        image_monitor_device(video_directory, picture_path)
        return send_file(picture_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"status":"error", "error":"errorMonitoringDevice", "errorMessage":"Error inesperado", "exception":str(e)})


#172.24.1.1:5002/uploadCodes
@app.route('/uploadCodes', methods=['GET', 'POST'])
@auth.login_required
def upload_codes():
    try:
        email = request.form.get("email")
        codes = json.loads(request.form.get("codes"))
        for code in codes:
            insert_download_code(code['code'])
        return jsonify({"status":"ok", "codes":codes})        
    except Exception as e:
        return jsonify({"status":"error", "error":"errorUploadingCodes", "errorMessage":"Error inesperado", "exception":str(e)})


#172.24.1.1:5002/countCodes
@app.route('/countCodes', methods=['GET', 'POST'])
@auth.login_required
def count_codes():
    try:
        count = count_available_download_codes()
        email = request.form.get("email")
        ##TODO obtener deviceId        
        deviceId = 1
        return jsonify({"status":"ok", "count":count, "deviceId":deviceId})        
    except Exception as e:
        return jsonify({"status":"error", "error":"errorCountingAvailableCodes", "errorMessage":"Error inesperado", "exception":str(e)})


#172.24.1.1:5002/getSpaceLimits
@app.route('/getSpaceLimits', methods=['POST'])
@auth.login_required
def get_space_limits():
    try:
        startLimit = get_config_value("DISK_START_DELETE_SPACE")
        endLimit = get_config_value("DISK_STOP_DELETE_SPACE")
        min_space = request.form.get("min_space")
        max_space = request.form.get("max_space")
        email = request.form.get("email")
        response = {"status":"ok", "startLimit":startLimit, "endLimit":endLimit}
        return jsonify(response)
    except Exception as e:
        response = {"status":"error","error":"errorChangingSpaceLimits","errorMessage":"No se pudo modificar los limites de espacio", "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/setSpaceLimits
@app.route('/setSpaceLimits', methods=['POST'])
@auth.login_required
def set_space_limits():
    try:
        startLimit = int(request.form.get("startLimit"))
        endLimit = int(request.form.get("endLimit"))
        email = request.form.get("email")
        if(startLimit >= 1024):
            if(endLimit <= 15360):
                modify_configuration_value("DISK_START_DELETE_SPACE", str(startLimit))
                modify_configuration_value("DISK_STOP_DELETE_SPACE", str(endLimit))
                response = {"status":"ok"}
            else:
                response = {"status":"error", "error":"invalidMaxLimit", "errorMessage":"El limite mayor no puede ser superior a 15 GB"}
        else:
            response = {"status":"error", "error":"invalidMinLimit", "errorMessage":"El limite inferior no puede ser menor a 1 GB"}
            
        return jsonify(response)
    except Exception as e:
        response = {"status":"error","error":"errorChangingSpaceLimits","errorMessage":"No se pudo modificar los limites de espacio", "exception":str(e)}
        return jsonify(response)


@auth.verify_token
def verify_token(token):
    ##TODO return maintenance_token_exists(token)    
    return True
    

@auth.error_handler
def auth_error():
    response = jsonify({"status":"error", "error":"wrongToken", "errorMessage":"Usted no esta autorizado a realizar esta accion"})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1', port=API_MANAGEMENT_PORT)
