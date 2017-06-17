from flask import Flask, send_file, jsonify, request
from fileUtil import get_mp4_files_in_directory, get_jpg_files_in_directory, get_file_name_without_extension
from dbUtil import download_code_exists, code_used, code_download, get_config_value
import sqlite3
import os
import os.path
from utils import decode_time
from dateUtil import get_current_date_str, get_current_short_date_str
from logger import log_info, log_error

PATH_VIDEO_LOCALIZATION = ''
MP4_VIDEOS_PATH = ''
HIGHLIGHT_NAME = ''


#Constantes de la base de datos
def update_variables():
    global PATH_VIDEO_LOCALIZATION
    global MP4_VIDEOS_PATH
    global HIGHLIGHT_NAME 
    PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
    MP4_VIDEOS_PATH = get_config_value("MP4_VIDEOS_PATH")
    HIGHLIGHT_NAME = get_config_value("HIGHLIGHT_NAME")


app = Flask(__name__)


#172.24.1.1:5000/getImages
@app.route('/getImages', methods=['GET', 'POST'])
def get_images():
    try:
        phone = request.form.get("phone")
        log_info(phone, 'USER', 'apiUser.py - get_images()')

        update_variables()
        directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + MP4_VIDEOS_PATH + HIGHLIGHT_NAME
        newDirectoryName = "tmp"
        newDirectory = directory + newDirectoryName

        if(not os.path.exists(newDirectory)):
            os.makedirs(newDirectory)
            
        videos = get_mp4_files_in_directory(directory)
        for video in videos:
            imageName = video.replace(directory, newDirectory)
            imageName = imageName.replace(".mp4",".jpg")
            os.system("avconv -i "+video+" -vframes 1 -f image2 "+imageName);

        zipName = "thumbs.zip"
        os.system("cd "+directory+"; zip "+zipName+" "+newDirectoryName+"/*")
        
        return send_file(directory+"/"+zipName, mimetype='application/zip')
    except Exception as e:
        phone = request.form.get("phone")
        log_error(phone, 'OWNER', 'apiUser.py - get_images()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingImages",
            "errorMessage":"No se pudieron obtener las imagenes",
            "exception":str(e)}
        return jsonify(response)


#172.24.1.1:5000/getVideo/<name>
@app.route('/getVideo/<name>', methods=['GET', 'POST'])
def get_video(name):
    try:
        phone = request.form.get("phone")
        log_info(phone, 'USER', 'apiUser.py - get_images()')

        update_variables()
        ## TODO hay que ver como recibimos el codigo aca tmb
        ##code_download(video_code)
        name = name.split('.')[0] + ".mp4"
        directory = directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + MP4_VIDEOS_PATH + HIGHLIGHT_NAME
        filePath = directory + name
        
        if os.path.isfile(filePath):
            return send_file(filePath, mimetype='video/mp4')
        else:
            return ('',204)
    except Exception as e:
        phone = request.form.get("phone")
        log_error(phone, 'USER', 'apiUser.py - get_video()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingVideo",
            "errorMessage":"No se  pudo obtener el video",
            "exception":str(e)}
        return jsonify(response)


#172.24.1.1:5000/validateCode/<code>
@app.route('/validateCode/<code>', methods=['GET', 'POST'])
def validate_code(code):
    try:
        phone = request.form.get("phone")
        log_info(phone, 'USER', 'apiUser.py - get_images()')

        update_variables()
        
        if(len(code) > 4):            
            if code == "ABC123":
                ##TODO DEBUG - sacar
                return ('OK', 200)
            else:
                ##el codigo es toda la string salvo las ultimas 3 letras
                video_code = code[:-3]
                ##el tiempo son las ultimas tres letras
                encrypted_time = code[-3:]
                time = decode_time(encrypted_time)
                if time is not None:
                    if(download_code_exists(video_code)):
                        ##code_used(video_code)
                        return jsonify({
                            "status":"ok",
                            "time":time})
                    else:
                        log_error(phone, 'USER', 'apiUser.py - validate_code()', 'El codigo ' + code +  ' es incorrecto')
                        return jsonify({
                            "status":"error",
                            "errorMessage":"El codigo es incorrecto"})
                else:
                    log_error(phone, 'USER', 'apiUser.py - validate_code()', 'El codigo ' + code +  ' es incorrecto')
                    return jsonify({
                        "status":"error",
                        "errorMessage":"El codigo es incorrecto"})
        else:
            log_error(phone, 'USER', 'apiUser.py - validate_code()', 'El codigo debe tener al menos 5 caracteres')

            return jsonify({
                "status":"error",
                "errorMessage":"El codigo debe tener al menos 5 caracteres"})
    except Exception as e:
        phone = request.form.get("phone")
        log_error(phone, 'USER', 'apiUser.py - validate_code()', str(e))
        response = {
            "status":"error",
            "error":"errorValidatingCOde",
            "errorMessage":"No se pudo validar el codigo",
            "exception":str(e)}
        return jsonify(response)
    

if __name__ == '__main__':
    update_variables()
    app.run(debug=True, host='172.24.1.1')
