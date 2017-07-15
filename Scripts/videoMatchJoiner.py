import asyncio
import time
import os
from fileUtil import get_mp4_files_in_directory, get_next_video, get_previous_video, video_between_marks
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time, str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date, rest_date_to_seconds
from logger import log_error
from dbUtil import get_config_value

#join_match_video('2017-06-17_14-00-16')
#@asyncio.coroutine
def join_match_video(TIME_START):
    try:
        #TIME_START = '2017-06-17_14-00-16'
        TIME_RECORDING_VIDEO = int(get_config_value("TIME_RECORDING_VIDEO"))
        PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
        # VIDEO_TOTAL_TIME = int(get_config_value("VIDEO_TOTAL_TIME"))
        VIDEO_TOTAL_TIME = 675
        
        video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
        
        file_array = get_mp4_files_in_directory(video_path)
        file_array.sort()
        file_array_match=[]

        start_date = str_to_date_time(TIME_START)
        finish_date = add_seconds_to_date(start_date, VIDEO_TOTAL_TIME)

        TIME_FINISH = str(finish_date).replace(' ','_')
        TIME_FINISH = TIME_FINISH.replace(':','-')
        encontre_video = False
        start_complete_video = 0

        # Recorro los videos del dia 
        for video in file_array:
            video_str_date = convert_path_to_str_date(video)
            video_date = str_to_date_time(video_str_date)

            # Consulto si el video pertenece al partido
            if video_between_marks(video_date, TIME_START, TIME_FINISH):
                if not encontre_video:
                    # Calculo para el primer video en que segundo arranca el partido
                    start_complete_video = rest_date_to_seconds(video_date, start_date)
                encontre_video = True
                # Agrego el video al array de videos del partido
                file_array_match.append(video)
            else:
                if encontre_video:
                    break

        # Armo el string para concatenar todos los videos
        concatString = ""
        for file_name in file_array_match:
            concatString = concatString + " -cat " + file_name

        # Calculo cuantos segundos demora el video para cortar el video generado por todos los videos del array
        array_length = len(file_array_match)
        finish_complete_video = (array_length -1) * TIME_RECORDING_VIDEO
        finish_complete_video = finish_complete_video + start_complete_video

        if not os.path.exists(video_path + 'Complete/'):
            # En caso de no existir el directorio lo creo
            os.makedirs(video_path + 'Complete/')
                
        aux_video_path = video_path + 'Complete/Aux_' + str(start_date) + '.mp4'
        aux_video_path = aux_video_path.replace(':','-')
        aux_video_path = aux_video_path.replace(' ','_')
                
        new_video_path = video_path + 'Complete/' + str(start_date) + '.mp4'
        new_video_path = new_video_path.replace(':','-')
        new_video_path = new_video_path.replace(' ','_')

        # Genero un video con todos los partidos del array                
        os.system("MP4Box" + concatString + " -new " + aux_video_path)
        # Recorto el video generado con el segundo en que debe empezar y el video en que debe termiar
        os.system('MP4Box -splitx ' + str(start_complete_video) + ':' + str(finish_complete_video) + ' "' + aux_video_path + '" -out "' + new_video_path + '"')
        os.remove(aux_video_path)
        #yield from end()    
    except Exception as e:
        print(str(e))
        log_error('SYSTEM', 'SYSTEM', 'videoMatchJoiner.py - main()', str(e))


#@asyncio.coroutine
#def end():
#    print('completed')

#def join_match_video(TIME_START):
#    try:
#        loop = asyncio.get_event_loop()
#        loop.create_task(join_match_video(TIME_START))
#        loop.close()
#    except Exception as e:
#        print(str(e))
