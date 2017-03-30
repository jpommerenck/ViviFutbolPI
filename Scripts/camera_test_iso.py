from picamera import PiCamera
from time import sleep
from dateUtil import get_current_date_str, get_current_short_date_str, get_current_time_int
import os

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/VideosEXPO/'
TIME_RECORDING_VIDEO=15
START_RECORDING_TIME=900
FINISH_RECORDING_TIME=1823

camera = PiCamera()

try:
    camera.resolution = (640,480)
    camera.iso = 800
    camera.shutter_speed = 6000000
    
    total_video = 0
    while total_video < 2:
        current_time = get_current_time_int()
        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
            # Obtengo el path de donde se va a crear el video        
            video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/'

            if not os.path.exists(video_path):
                # En caso de no existir el directorio lo creo
                os.makedirs(video_path)

            camera.start_recording(video_path + get_current_date_str() + '.h264', format='h264', intra_period=1)
            camera.wait_recording(TIME_RECORDING_VIDEO)
            camera.stop_recording()
            current_time = get_current_time_int()
        total_video = total_video+1
        camera.close()
finally:
    #camera.stop_preview()
    #Trato de cerrar la camara en caso de que este abierta
    try:
        camera.close()
    except OSError:
        pass
