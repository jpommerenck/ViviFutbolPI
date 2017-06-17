from flask import Flask, request, jsonify
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str
from logger import log_info, log_error
from dbUtil import get_config_value
import base64

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


#172.24.1.1:5001/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
def get_image_monitor_device():
    try:
        update_variables()
        email = request.form.get("email")
        picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
        video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
        image_monitor_device(video_directory, picture_path)
        log_info(email, 'OWNER', 'apiOwner.py - get_image_monitor_device()')

        with open(picture_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return jsonify({"status":"ok", "base64Image":str(encoded_string)})
    except Exception as e:
        email = request.form.get("email")
        log_error(email, 'OWNER', 'apiOwner.py - get_image_monitor_device()', str(e))
        response = {
            "status":"error",
            "error":"errorGettingImageMonitorDevice",
            "errorMessage":"No se pudo obtener la imagen del dispositivo",
            "exception":str(e)}

        return jsonify(response)

if __name__ == '__main__':
    update_variables()
    app.run(debug=True, host='172.24.1.1', port=API_OWNER_PORT)
