from picamera import PiCamera
from time import sleep
from dateUtil import get_current_date_str, get_current_short_date_str, get_current_time_int
from logger import log_info, log_error
import os
from dbUtil import get_config_value


def main():
    try:
        PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
        PATH_AUDIO_LOCALIZATION = get_config_value("AUDIOS_LOCALIZATION_PATH")
        TIME_RECORDING_VIDEO = int(get_config_value("TIME_RECORDING_VIDEO"))
        START_RECORDING_TIME = get_config_value("START_RECORDING_TIME")
        FINISH_RECORDING_TIME = get_config_value("FINISH_RECORDING_TIME")

        START_RECORDING_TIME = START_RECORDING_TIME.replace(":","")
        START_RECORDING_TIME = int(START_RECORDING_TIME.replace(":",""))

        FINISH_RECORDING_TIME = FINISH_RECORDING_TIME.replace(":","")
        FINISH_RECORDING_TIME = int(FINISH_RECORDING_TIME.replace(":",""))

        camera = PiCamera()        
        camera.resolution = (640,480)
        camera.framerate = 30

        current_time = get_current_time_int()
        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
                
            # Obtengo el path de donde se va a crear el video        
            video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/'
            audio_path = PATH_AUDIO_LOCALIZATION + get_current_short_date_str() + '/'

            if not os.path.exists(video_path):
                # En caso de no existir el directorio lo creo
                os.makedirs(video_path)

            if not os.path.exists(audio_path):
                # En caso de no existir el directorio lo creo
                os.makedirs(audio_path)

            camera.start_recording(video_path + get_current_date_str() + '.h264', format='h264', quality=23, intra_period=10)
            os.system('arecord -D plughw:1 --duration=' + str(TIME_RECORDING_VIDEO) + ' -f cd -vv ' + audio_path + get_current_date_str() + '.wav')
                
            if os.path.exists(audio_path):
                camera.stop_recording()
            else :
                camera.wait_recording(TIME_RECORDING_VIDEO)
                camera.stop_recording()
                    
            current_time = get_current_time_int()
        camera.close()

    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'camera.py - main()', str(e))
    finally:
        try:
            print('Aca se debe cerrar la camara')
            #camera.close()
        except OSError:
            log_error("SYSTEM", 'SYSTEM', 'camera.py - main()', str(e))
            pass


if __name__ == '__main__':
    main()
