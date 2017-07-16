import os
import os.path
from flask import Flask, send_file, jsonify, request
from fileUtil import get_mp4_between_dates
from dbUtil import code_download, get_config_value
from utils import is_valid_code, decode_time
from dateUtil import get_current_short_date_str, str_to_date_time, add_seconds_to_date
from logger import log_info, log_error


PATH_VIDEO_LOCALIZATION = ''
MP4_VIDEOS_PATH = ''
HIGHLIGHT_NAME = ''
HIGHLIGHTS_PATH = ''
TEMP_FILES_PATH = ''

#Constantes de la base de datos
def update_variables():
    global PATH_VIDEO_LOCALIZATION
    global MP4_VIDEOS_PATH
    global HIGHLIGHT_NAME
    global HIGHLIGHTS_PATH
    global TEMP_FILES_PATH
    PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
    MP4_VIDEOS_PATH = get_config_value("MP4_VIDEOS_PATH")
    HIGHLIGHT_NAME = get_config_value("HIGHLIGHT_NAME")
    HIGHLIGHTS_PATH = get_config_value("HIGHLIGHTS_VIDEOS_PATH")
    TEMP_FILES_PATH = get_config_value("TEMP_FILES_PATH")
    

app = Flask(__name__)


#172.24.1.1:5000/getImages
@app.route('/getImages', methods=['GET', 'POST'])
def get_images():
    try:
        update_variables()
        highlights_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + MP4_VIDEOS_PATH + HIGHLIGHTS_PATH
        temp_folder = TEMP_FILES_PATH
        phone = request.form.get("phone")
        code = request.form.get("code")
        code = 'YKYJROAB'
        log_info(phone, 'USER', 'apiUser.py - get_images()')

        if is_valid_code(code):
            code_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + MP4_VIDEOS_PATH + HIGHLIGHTS_PATH + code + "/"
            
            video_code = code[:-3]
            encrypted_time = code[-3:]
            time = decode_time(encrypted_time)
            match_start_time = get_current_short_date_str() + '_' + time + '-00'
            match_start_time = match_start_time.replace(':','-')
            
            match_start_date_time = str_to_date_time(match_start_time)
            match_finish_date_time = add_seconds_to_date(match_start_date_time,3600)
            
            if(not os.path.exists(highlights_path)):
                os.makedirs(highlights_path)

            if(not os.path.exists(code_directory)):
                os.makedirs(code_directory)    
            
            videos = get_mp4_between_dates(highlights_path,str(match_start_date_time), str(match_finish_date_time))
            for video in videos:
                image_name = video.replace(highlights_path, code_directory)
                image_name = image_name.replace(".mp4",".jpg")
                os.system("avconv -i " + video + " -vframes 1 -f image2 " + image_name);

            zip_name = "thumbs.zip"
            os.system("cd " + code_directory + "; zip " + zip_name + " " + code_directory + "/*")
        
            return send_file(code_directory + "/" + zip_name, mimetype = 'application/zip')
        else:
            log_error(phone, 'OWNER', 'apiUser.py - get_images()', 'El codigo enviado no es valido')
            response = {
                "status":"error",
                "error":"errorGettingImages",
                "errorMessage":"El codigo enviado no es valido"}
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
        log_info(phone, 'USER', 'apiUser.py - get_video()')
        
        update_variables()
        ## TODO hay que ver como recibimos el codigo aca tmb
        ##code_download(video_code)
        
        name = name.split('.')[0] + ".mp4"
        
        directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + MP4_VIDEOS_PATH + HIGHLIGHTS_PATH
        file_path = directory + name
        
        if os.path.isfile(file_path):
            return send_file(file_path, mimetype='video/mp4')
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
        log_info(phone, 'USER', 'apiUser.py - validate_code()')

        update_variables()
        code = 'YKYJROAB'
        if is_valid_code(code):
            ##el codigo es toda la string salvo las ultimas 3 letras
            video_code = code[:-3]
            ##el tiempo son las ultimas tres letras
            encrypted_time = code[-3:]
            time = decode_time(encrypted_time)
            # Format match_start_time : 'yyy-mm-dd_hh-mm-ss'
            time_match = str(time).replace(':','-')
            match_start_time = get_current_short_date_str() + '_' + time_match + '-00'

            # Genero el video del partido completo
            #join_match_video(match_start_time)

            return jsonify({
                "status":"ok",
                "time":time,
                "date":match_start_time})

        else:
            log_error(phone, 'USER', 'apiUser.py - validate_code()', 'El codigo ' + code +  ' es incorrecto')
            return jsonify({
                "status":"error",
                "errorMessage":"El codigo es incorrecto"})
        
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
