import os
from fileUtil import get_next_video, get_previous_video
from dateUtil import str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date, rest_date_to_seconds, get_current_time_int
from dbUtil import get_all_marks_not_processed, get_config_value, update_mark, add_intent_to_mark
from logger import log_error
import time

FIND_VIDEO = False
TIME_RECORDING_VIDEO = 0
TIME_BEFORE = 0
TIME_AFTER = 0

def main():
    try:
        global FIND_VIDEO
        global TIME_RECORDING_VIDEO
        global TIME_BEFORE
        global TIME_AFTER

        TIME_AFTER = int(get_config_value("TIME_AFTER_RECORD"))
        TIME_BEFORE = int(get_config_value("TIME_BEFORE_RECORD"))
        TIME_RECORDING_VIDEO = int(get_config_value("TIME_RECORDING_VIDEO"))
        PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
        FOLDER_HIGLIGHTS = get_config_value("HIGHLIGHTS_VIDEOS_PATH")
        HIGHLIGHT_NAME = get_config_value("HIGHLIGHT_NAME")
        HIGHLIGHT_AUX_NAME = get_config_value("HIGHLIGHT_AUX_NAME")
        COMPLETE_NAME = get_config_value("COMPLETE_NAME")
        MP4_VIDEOS_PATH = get_config_value("MP4_VIDEOS_PATH")
        SECONDS_WAITING_FOR_CONVERT_VIDEO = int(get_config_value("SECONDS_WAITING_FOR_CONVERT_VIDEO"))

        START_RECORDING_TIME = get_config_value("START_RECORDING_TIME")
        FINISH_RECORDING_TIME = get_config_value("FINISH_RECORDING_TIME")

        START_RECORDING_TIME = START_RECORDING_TIME.replace(":","")
        START_RECORDING_TIME = int(START_RECORDING_TIME.replace(":",""))

        FINISH_RECORDING_TIME = FINISH_RECORDING_TIME.replace(":","")
        FINISH_RECORDING_TIME = int(FINISH_RECORDING_TIME.replace(":",""))
        current_time = get_current_time_int()

        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
            FIND_VIDEO = False
            video_path = ''
            total_record = TIME_AFTER + TIME_BEFORE
            marks = get_all_marks_not_processed()
            
            for row_mark in marks:
                FIND_VIDEO = False
                mark = row_mark[0]
                mark_date = mark.split('_')[0]
                video_marked = row_mark[3]

                video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH
                new_video_path = video_path + FOLDER_HIGLIGHTS

                video_marked = video_marked.replace(PATH_VIDEO_LOCALIZATION + mark_date + '/', PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH)
                video_marked = video_marked.replace('h264','mp4')
                
                mark_date_time = str_to_date_time(mark)
                
                # En caso de no existir el directorio lo creo
                if not os.path.exists(new_video_path):
                    os.makedirs(new_video_path)


                if os.path.exists(video_marked):
                    video_str_date = convert_path_to_str_date(video_marked)
                    video_date = str_to_date_time(video_str_date)
                
                    start_highlight = rest_seconds_to_date(mark_date_time, TIME_BEFORE)
                    finish_highlight = add_seconds_to_date(mark_date_time, TIME_AFTER)
                    video_finish = add_seconds_to_date(video_date, TIME_RECORDING_VIDEO)
                    
                    # Diferencia en segundos entre el inicio del video y la marca
                    difference = rest_date_to_seconds(video_date, mark_date_time)

                    # Creo el nombre del video de la jugada destacada
                    higlight_video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH + FOLDER_HIGLIGHTS + mark + '.mp4'
                    aux_video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH + FOLDER_HIGLIGHTS + HIGHLIGHT_AUX_NAME + mark + '.mp4'

                    
                    # Cuando no preciso concatenar videos
                    if video_date <= start_highlight and video_finish >= finish_highlight:
                        FIND_VIDEO = True
                        start_seconds = difference - TIME_BEFORE
                        finish_seconds = start_seconds + total_record
                        generate_video(start_seconds, finish_seconds, video_marked, higlight_video_path)

                    elif video_date <= start_highlight:
                         # Genero el video de la jugada destacada utilizando el siguiente video
                        generate_highlight_with_next_video(mark, video_marked, difference, aux_video_path, higlight_video_path)
                    else:
                        # Genero el video de la jugada destacada utilizando el anterior video
                        generate_highlight_with_previous_video(mark, mark_date_time, video_marked, difference, aux_video_path, higlight_video_path)
                  
                
                if FIND_VIDEO == True:
                    update_mark(str(mark))
                else:
                    # Luego de 3 intentos no se procesara mas la marca
                    add_intent_to_mark(str(mark))
                    time.sleep(TIME_RECORDING_VIDEO)
                    
            current_time = get_current_time_int()
            
    except Exception as e:
        print('Error ' + str(e))
        log_error("SYSTEM", 'SYSTEM', 'videoHighlights.py - main()', str(e))



#####################################################################################################
# Metodo que genera una jugada destacado cuando se precisa el siguiente video
# Parametros
#       mark :
#       video : video que contiene la marca
#       difference : diferencia en segundos entre el inicio del video y la marca
#       aux_video_path : video auxilia que en que se concatenan los 2 videos para generar el partido
#       higlight_video_path : nombre del video de la jugada destacada
#
#####################################################################################################
def generate_highlight_with_next_video(mark, video, difference, aux_video_path, higlight_video_path):
    # Obtengo el video siguiente para concatenar para concatenaro
    next_video = get_next_video(video, mark)
    next_video_str_date = convert_path_to_str_date(next_video)
    
    # Consulto a ver si es el ultimo video o se esta grabando otro video
    if (next_video == ''):
        time.sleep(TIME_RECORDING_VIDEO)
        next_video = get_next_video(video, mark)
        next_video_str_date = convert_path_to_str_date(next_video)
    
    seconds_start_cut = difference - TIME_BEFORE
    total_record = TIME_AFTER + TIME_BEFORE
    seconds_finish_cut = seconds_start_cut + total_record

    # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
    if (next_video != ''):
        FIND_VIDEO = True
        next_video_date = str_to_date_time(next_video_str_date)

        os.system("MP4Box -cat "  + video + ' -cat ' + next_video +  " " + aux_video_path)
        generate_video(seconds_start_cut, seconds_finish_cut, aux_video_path, higlight_video_path)
        os.remove(aux_video_path)
                                    
    else:
        FIND_VIDEO = True
        generate_video(seconds_start_cut, seconds_finish_cut, video, higlight_video_path)



#####################################################################################################
# Metodo que genera una jugada destacado cuando se precisa el siguiente video
# Parametros
#       mark :
#       mark_date_time :
#       video : video que contiene la marca
#       difference : diferencia en segundos entre el inicio del video y la marca
#       aux_video_path : video auxilia que en que se concatenan los 2 videos para generar el partido
#       higlight_video_path : nombre del video de la jugada destacada
#
#####################################################################################################
def generate_highlight_with_previous_video(mark, mark_date_time, video, difference, aux_video_path, higlight_video_path):
    # Obtengo el video anterior para concatenar
    previous_video = get_previous_video(video, mark)
    previous_video_str_date = convert_path_to_str_date(previous_video)
    seconds_start_cut = difference - TIME_BEFORE
    total_record = TIME_AFTER + TIME_BEFORE
    seconds_finish_cut = seconds_start_cut + total_record

    if (seconds_start_cut < 0):
        seconds_start_cut = 0

    # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
    if (previous_video != ''):
        FIND_VIDEO = True
        
        previous_video_date = str_to_date_time(previous_video_str_date)
        difference = rest_date_to_seconds(previous_video_date, mark_date_time)
        seconds_start_cut = difference - TIME_BEFORE
        seconds_start_cut = TIME_RECORDING_VIDEO - seconds_start_cut
        seconds_finish_cut = seconds_start_cut + total_record

        os.system("MP4Box -cat "  + previous_video + ' -cat ' + video +  " " + aux_video_path)
        generate_video(seconds_start_cut, seconds_finish_cut, aux_video_path, higlight_video_path)
        os.remove(aux_video_path)
    else:
        FIND_VIDEO = True
        generate_video(seconds_start_cut, seconds_finish_cut, video, higlight_video_path)



#####################################################################################################
# Funcion que se encarga de generar el video de la jugada destacada
# Parametros
#       start_second : segundos en que empieza el video
#       finish_second : segundos en que termina el video
#       video : video que se va a recortar
#       highlight_name : nombre del archivo que se va a crear con la jugada destacada
#
#####################################################################################################
def generate_video(start_second, finish_second, video, highlight_name):
    os.system('MP4Box -splitx ' + str(start_second) + ':' + str(finish_second) + ' ' + video + ' -out ' + highlight_name)



#####################################################################################################
# Invocacion al main del script
#####################################################################################################
if __name__ == '__main__':
    main()


