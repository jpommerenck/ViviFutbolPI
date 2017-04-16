import time
import os
from fileUtil import get_h264_files_in_directory, delete_file, newest_h264_in_directory
from dateUtil import get_current_short_date_str

# Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
<<<<<<< HEAD
SECONDS_WAITING_FOR_CONVERT_VIDEO=30
=======
SECONDS_WAITING_FOR_CONVERT_VIDEO=15
>>>>>>> 69e60c31ee4b4213f522032b75322c3505056b42
last_newest_file = ''

try:
    var = 0
    while var < 10 :
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
                    #Agrega el audio al video
                    os.system('avconv -i ' + aux_file_name + ' -i ' + audio_file_name + ' -vcodec copy -strict experimental -shortest ' + new_file_name)

                    #Elimino los archivos temporales
                    delete_file(file_name)
                    delete_file(aux_file_name)
                    #delete_file(audio_file_name)
        var = var + 1
        time.sleep(SECONDS_WAITING_FOR_CONVERT_VIDEO)
        last_newest_file = newest_file
finally:
    #Que se hace por si falla el sistema
    var = 0
