from flask import Flask
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolLocal/Pictures/MonitorDevice/'
API_OWNER_PORT = 5001

app = Flask(__name__)

#172.24.1.1:5001/getImageMonitorDevice
@app.route('/getImageMonitorDevice', methods=['GET', 'POST'])
def get_image_monitor_device():
    picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
    video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
    image_monitor_device(video_directory, picture_path)
    return send_file(picture_path, mimetype='image/jpeg')

if __name__ == '__main__':
    #app.run(debug=True, host='192.168.1.110', port=API_OWNER_PORT)
    app.run(debug=True, host='172.24.1.1', port=API_OWNER_PORT)
