from fileUtil import get_h264_files_in_directory, delete_file, newest_h264_in_directory
from dateUtil import get_current_short_date_str, get_current_time_int
from logger import log_error
from dbUtil import get_config_value
import time
import os


def main():
    try:
        PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
        SECONDS_WAITING_FOR_CONVERT_VIDEO = int(get_config_value("SECONDS_WAITING_FOR_CONVERT_VIDEO"))
        START_RECORDING_TIME = get_config_value("START_RECORDING_TIME")
        FINISH_RECORDING_TIME = get_config_value("FINISH_RECORDING_TIME")

        START_RECORDING_TIME = START_RECORDING_TIME.replace(":","")
        START_RECORDING_TIME = int(START_RECORDING_TIME.replace(":",""))

        FINISH_RECORDING_TIME = FINISH_RECORDING_TIME.replace(":","")
        FINISH_RECORDING_TIME = int(FINISH_RECORDING_TIME.replace(":",""))
        
        current_time = get_current_time_int()
        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
                
            last_newest_file = ''
            video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
            video_path_mp4 = video_path + '/mp4/'
            file_array = get_h264_files_in_directory(video_path)
            newest_file = newest_h264_in_directory(video_path + '/')
                
            if len(file_array) > 0 :
                for file_name in file_array:
                    if (file_name != newest_file) | (newest_file == last_newest_file) :
                        if not os.path.exists(video_path_mp4):
                            # En caso de no existir el directorio lo creo
                            os.makedirs(video_path_mp4)
                                
                        aux_file_name = file_name.replace(video_path, video_path_mp4)
                        aux_file_name = aux_file_name.replace('.h264', '_aux.mp4')
                        new_file_name = aux_file_name.replace('_aux.mp4', '.mp4')

                        audio_file_name = file_name.replace("Videos", "Audios")
                        audio_file_name = audio_file_name.replace(".h264", ".wav")

                        #Convierte el video de .264 a .mp4
                        os.system('MP4Box -add '+ file_name +':fps=30 '+ aux_file_name)
                        if os.path.exists(audio_file_name):
                            os.system('avconv -i ' + aux_file_name + ' -i ' + audio_file_name + ' -vcodec copy -strict experimental -shortest ' + new_file_name)
                        os.system('avconv -i ' + aux_file_name + ' -vcodec copy -strict experimental -shortest ' + new_file_name)
                            
                        #Elimino los archivos temporales
                        delete_file(file_name)
                        delete_file(aux_file_name)
                        delete_file(audio_file_name)

            time.sleep(SECONDS_WAITING_FOR_CONVERT_VIDEO)
            last_newest_file = newest_file
            current_time = get_current_time_int()
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'videoConverter.py - main()', str(e))            
    finally:
        #Que se hace por si falla el sistema
        var = 0

if __name__ == '__main__':
    main()
