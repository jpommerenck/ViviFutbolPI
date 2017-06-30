from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPTokenAuth
from fileUtil import image_monitor_device, convert_image_to_base64
from dateUtil import get_current_date_str, get_current_short_date_str, set_time
from dbUtil import modify_configuration_value, get_config_value, insert_download_code, count_available_download_codes, maintenance_token_exists, get_used_codes, get_used_codes_without_downloads, mark_codes_as_sent, get_config_value
from logger import latest_log_activity, log_info, log_error
import time
import json

API_MANAGEMENT_PORT = 0
PATH_VIDEO_LOCALIZATION = ''
PATH_PICTURES_LOCALIZATION = ''

#Constantes de la base de datos
def update_variables():
    global API_MANAGEMENT_PORT
    global PATH_VIDEO_LOCALIZATION
    global PATH_PICTURES_LOCALIZATION
    API_MANAGEMENT_PORT = int(get_config_value("API_MANAGEMENT_PORT"))
    PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
    PATH_PICTURES_LOCALIZATION = get_config_value("PICTURES_LOCALIZATION_PATH")

app = Flask(__name__)
auth = HTTPTokenAuth('Token')


#172.24.1.1:5002/getTime
@app.route('/getTime', methods=['GET', 'POST'])
@auth.login_required
def get_time():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - get_time()')

        response = {
            "status":"ok",
            "currentTime": time.strftime('%H') + ":" + time.strftime('%M')}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - get_time()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingTime",
            "errorMessage":"No se pudo obtener la hora del dispositivo",
            "exception":str(e)}
        return jsonify(response)


#172.24.1.1:5002/postTime
@app.route('/postTime', methods=['POST'])
@auth.login_required
def post_time():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - post_time()')

        hora = request.form.get("time")
        horaPI = hora.split(':')[0]
        minutosPI = hora.split(':')[1]
        set_time(horaPI, minutosPI)
        response = {
            "status":"ok",
            "newTime":time.strftime('%H') + ":" + time.strftime('%M')}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - post_time()', str(e))
        response = {
            "status":"error",
            "error":"errorSettingTime",
            "errorMessage":"No se pudo modificar la hora del dispositivo",
            "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/changeRecordingTimes
@app.route('/setRecordingTimes', methods=['POST'])
@auth.login_required
def set_recording_times():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - set_recording_times()')
        
        startTime = request.form.get("startTime")
        endTime = request.form.get("endTime")
        modify_configuration_value("START_RECORDING_TIME", startTime)
        modify_configuration_value("FINISH_RECORDING_TIME", endTime)
        response = {"status":"ok"}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - set_recording_times()', str(e))
        response = {
            "status":"error",
            "error":"errorChangingRecordingTimes",
            "errorMessage":"No se pudo modificar las horas de grabacion",
            "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/getRecordingTimes
@app.route('/getRecordingTimes', methods=['POST'])
@auth.login_required
def get_recording_times():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - get_recording_times()')
        
        startTime = get_config_value("START_RECORDING_TIME")
        endTime = get_config_value("FINISH_RECORDING_TIME")
        response = {
            "status":"ok",
            "startTime":startTime,
            "endTime":endTime}
        return jsonify(response)
    except:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - get_recording_times()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingRecordingTimes",
            "errorMessage":"No se pudo obtener las horas de grabacion",
            "exception":str(e)}
        return jsonify(response)


#172.24.1.1:5002/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
@auth.login_required
def get_image_monitor_device():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - get_image_monitor_device()')

        update_variables()
        picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
        video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
        image_monitor_device(video_directory, picture_path)
        encoded_string = convert_image_to_base64(picture_path)
        return jsonify({"status":"ok", "base64Image":encoded_string})
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - get_image_monitor_device()', str(e))
        return jsonify({
            "status":"error",
            "error":"errorMonitoringDevice",
            "errorMessage":"Error inesperado",
            "exception":str(e)})


#172.24.1.1:5002/uploadCodes
@app.route('/uploadCodes', methods=['GET', 'POST'])
@auth.login_required
def upload_codes():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - upload_codes()')

        codes = json.loads(request.form.get("codes"))
        for code in codes:
            insert_download_code(code['code'])
        return jsonify({
            "status":"ok",
            "codes":codes})        
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - upload_codes()', str(e))
        return jsonify({
            "status":"error",
            "error":"errorUploadingCodes",
            "errorMessage":"Error inesperado",
            "exception":str(e)})


#172.24.1.1:5002/countCodes
@app.route('/countCodes', methods=['GET', 'POST'])
@auth.login_required
def count_codes():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - count_codes()')
        
        count = count_available_download_codes()
        ##TODO obtener deviceId        
        deviceId = 1
        return jsonify({
            "status":"ok",
            "count":count,
            "deviceId":deviceId})        
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - count_codes()', str(e))
        return jsonify({
            "status":"error",
            "error":"errorCountingAvailableCodes",
            "errorMessage":"Error inesperado",
            "exception":str(e)})


#172.24.1.1:5002/getSpaceLimits
@app.route('/getSpaceLimits', methods=['POST'])
@auth.login_required
def get_space_limits():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - get_space_limits()')
        
        startLimit = get_config_value("DISK_START_DELETE_SPACE")
        endLimit = get_config_value("DISK_STOP_DELETE_SPACE")
        min_space = request.form.get("min_space")
        max_space = request.form.get("max_space")
        response = {
            "status":"ok",
            "startLimit":startLimit,
            "endLimit":endLimit}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - get_space_limits()', str(e))
        response = {
            "status":"error",
            "error":"errorChangingSpaceLimits",
            "errorMessage":"No se pudo modificar los limites de espacio",
            "exception":str(e)}
        return jsonify(response)

                
#172.24.1.1:5002/setSpaceLimits
@app.route('/setSpaceLimits', methods=['POST'])
@auth.login_required
def set_space_limits():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - set_space_limits()')
        
        startLimit = int(request.form.get("startLimit"))
        endLimit = int(request.form.get("endLimit"))
        
        if(startLimit < endLimit):
            if(startLimit >= 1024):
                if(endLimit <= 15360):
                    modify_configuration_value("DISK_START_DELETE_SPACE", str(startLimit))
                    modify_configuration_value("DISK_STOP_DELETE_SPACE", str(endLimit))
                    response = {"status":"ok"}
                else:
                    response = {
                        "status":"error",
                        "error":"invalidMaxLimit",
                        "errorMessage":"El limite para terminar de borrar no puede ser superior a 15 GB"}
            else:
                response = {
                    "status":"error",
                    "error":"invalidMinLimit",
                    "errorMessage":"El limite para empezar a borrar no puede ser menor a 1 GB"}
        else:
            response = {
                "status":"error",
                "error":"invalidValues",
                "errorMessage":"El limite para empezar a borrar debe ser menor al limite para terminar"}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - set_space_limits()', str(e))
        response = {
            "status":"error",
            "error":"errorChangingSpaceLimits",
            "errorMessage":"No se pudo modificar los limites de espacio",
            "exception":str(e)}
        return jsonify(response)


#172.24.1.1:5002/downloadData
@app.route('/downloadData', methods=['POST'])
@auth.login_required
def download_data():
    try:
        email = request.form.get("email")
        log_info(email, 'MANAGEMENT', 'apiManagement.py - download_data()')
        
        usedCodes = get_used_codes()
        usedCodesWithoutDownloads = get_used_codes_without_downloads()
        logActivity = latest_log_activity()
        mark_codes_as_sent()
        response = {
            "status":"ok",
            "usedCodes":usedCodes,
            "usedCodesWithoutDownload":usedCodesWithoutDownloads,
            "logActivity":logActivity}
        return jsonify(response)
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'MANAGEMENT', 'apiManagement.py - download_data()', str(e))
        response = {
            "status":"error",
            "error":"errorDownloadingData",
            "errorMessage":"No se pudieron descargar los datos",
            "exception":str(e)}
        return jsonify(response)
    
@auth.verify_token
def verify_token(token):
    ##return maintenance_token_exists(token)    
    return True
    

@auth.error_handler
def auth_error():
    response = jsonify({
        "status":"error",
        "error":"wrongToken",
        "errorMessage":"Usted no esta autorizado a realizar esta accion"})
    response.status_code = 200
    return response


if __name__ == '__main__':
    update_variables()
    app.run(debug=True, host='172.24.1.1', port=API_MANAGEMENT_PORT)
