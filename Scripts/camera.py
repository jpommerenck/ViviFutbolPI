from picamera import PiCamera
from time import sleep
from dateUtil import get_current_date_str, get_current_short_date_str, get_current_time_int
import os

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolPI/Videos/'
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolPI/Pictures/'
TIME_RECORDING_VIDEO=300
START_RECORDING_TIME=843
FINISH_RECORDING_TIME=1200

camera = PiCamera()

try:
    camera.resolution = (640,480)
    total_video = 0
    #camera.start_preview()
    while total_video < 2:
        current_time = get_current_time_int()
        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
            # Obtengo el path de donde se va a crear el video        
            video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/'

            if not os.path.exists(video_path):
                # En caso de no existir el directorio lo creo
                os.makedirs(video_path)

            camera.start_recording(video_path + get_current_date_str() + '.h264')
            camera.wait_recording(TIME_RECORDING_VIDEO)
            camera.stop_recording()
            current_time = get_current_time_int()
        total_video = total_video+1
        camera.close()
finally:
    #camera.stop_preview()
    #Aca para cerrarla falta consultar si esta abierta la camara
    if camera._check_camera_open():
        camera.close()

# Metodo para tomar una foto en caso que la camara no este grabando
def take_picture(picture_path):

    if not os.path.exists(PATH_PICTURES_LOCALIZATION):
        # En caso de no existir el directorio lo creo
        os.makedirs(PATH_PICTURES_LOCALIZATION)

    camera = PiCamera()
    camera.capture(picture_path)
    camera.close()
    return picture_path
