from flask import Flask, request, jsonify
<<<<<<< HEAD
from fileUtil import image_monitor_device, convert_image_to_base64
from dateUtil import get_current_date_str, get_current_short_date_str
from logger import log_info, log_error
from dbUtil import get_config_value
=======
from flask_httpauth import HTTPTokenAuth
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str
from logger import log_info, log_error
from dbUtil import get_config_value, owner_token_exists
import base64
>>>>>>> c01e8d6df2764862205fb2e829e11da7265c0369

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = ''
PATH_PICTURES_LOCALIZATION = ''
API_OWNER_PORT = 0

def update_variables():
    global PATH_VIDEO_LOCALIZATION
    global PATH_PICTURES_LOCALIZATION
    global API_OWNER_PORT
    PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
    PATH_PICTURES_LOCALIZATION = get_config_value("PICTURES_LOCALIZATION_PATH")
    API_OWNER_PORT = int(get_config_value("API_OWNER_PORT"))


app = Flask(__name__)
auth = HTTPTokenAuth('Token')


#172.24.1.1:5001/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
@auth.login_required
def get_image_monitor_device():
    try:
        email = request.form.get("email")
        log_info(email, 'OWNER', 'apiOwner.py - get_image_monitor_device()')
        
        update_variables()
        picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
        video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
        image_monitor_device(video_directory, picture_path)
        encoded_string = convert_image_to_base64(picture_path)
        return jsonify({"status":"ok", "base64Image":encoded_string})

    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'OWNER', 'apiOwner.py - get_image_monitor_device()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingImageMonitorDevice",
            "errorMessage":"No se pudo obtener la imagen del dispositivo",
            "exception":str(e)}

        return jsonify(response)

@auth.verify_token
def verify_token(token):
    return owner_token_exists(token)
    

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
    app.run(debug=True, host='172.24.1.1', port=API_OWNER_PORT)
