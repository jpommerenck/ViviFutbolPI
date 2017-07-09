import os
from fileUtil import get_mp4_files_in_directory, get_next_video, video_contains_mark, get_previous_video
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time, str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date, rest_date_to_seconds, get_current_time_int
from dbUtil import get_all_marks_between_dates, get_all_marks_not_processed, get_config_value, update_mark, add_intent_to_mark
from logger import log_error
import time

def main():
    try:
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
            find_video = False
            concat_string = ''
            last_mark_date = ''
            video_path = ''
            total_record = TIME_AFTER + TIME_BEFORE
            marks = get_all_marks_not_processed()
            
            for row in marks:
                mark_date = row.split('_')[0]
                row_date = str_to_date_time(row)
                    
                find_video = False
                concat_string = ''
                video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH
                file_array = get_mp4_files_in_directory(video_path)
                new_video_path = video_path + FOLDER_HIGLIGHTS

                if not os.path.exists(new_video_path):
                    # En caso de no existir el directorio lo creo
                    os.makedirs(new_video_path)
                    
                for video in file_array:
                    video_str_date = convert_path_to_str_date(video)
                    video_date = str_to_date_time(video_str_date)
                    
                    # Consulto si la marca se realizo cuando se filmaba el video
                    if video_contains_mark(video_date, row):
                        #add_seconds_to_date, rest_seconds_to_date
                        start_highlight = rest_seconds_to_date(row_date, TIME_BEFORE)
                        finish_highlight = add_seconds_to_date(row_date, TIME_AFTER)
                        video_finish = add_seconds_to_date(video_date, TIME_RECORDING_VIDEO)

                        # Diferencia en segundos entre el inicio del video y la marca
                        difference = rest_date_to_seconds(video_date, row_date)

                        #higlight_video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH + FOLDER_HIGLIGHTS + HIGHLIGHT_NAME + row + '.mp4'
                        higlight_video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH + FOLDER_HIGLIGHTS + row + '.mp4'
                        aux_video_path = PATH_VIDEO_LOCALIZATION + mark_date + MP4_VIDEOS_PATH + FOLDER_HIGLIGHTS + HIGHLIGHT_AUX_NAME + row + '.mp4'
                        
                        # Cuando no preciso concatenar videos
                        if video_date <= start_highlight and video_finish >= finish_highlight:
                            find_video = True
                            seconds_start_cut = difference - TIME_BEFORE
                            os.system('MP4Box -splitx ' + str(seconds_start_cut) + ':' + str(seconds_start_cut + total_record) +' ' + video + ' -out ' + higlight_video_path)
                                
                        elif video_date <= start_highlight:
                            # Obtengo el video siguiente para concatenar para concatenar
                            next_video = get_next_video(video)
                            next_video_str_date = convert_path_to_str_date(next_video)
                            seconds_start_cut = difference - TIME_BEFORE
                                
                            # Consulto a ver si es el ultimo video o se esta grabando otro video
                            if (next_video_str_date == ''):
                                time.sleep(TIME_RECORDING_VIDEO)
                                next_video = get_next_video(video)
                                next_video_str_date = convert_path_to_str_date(next_video)
                                seconds_start_cut = difference - TIME_BEFORE

                            # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
                            if (next_video_str_date != ''):
                                find_video = True
                                next_video_date = str_to_date_time(next_video_str_date)

                                os.system("MP4Box -cat "  + video + ' -cat ' + next_video +  " -out " + aux_video_path)
                                #while not os.path.exists(aux_video_path):
                                #    time.sleep(1)
                                os.system('MP4Box -splitx ' + str(seconds_start_cut) + ':' + str(seconds_start_cut + total_record) + ' ' + aux_video_path + ' -out ' + higlight_video_path)
                                os.remove(aux_video_path)
                                    
                            else:
                                find_video = True
                                os.system('MP4Box -splitx ' + str(seconds_start_cut) + ':' + str(seconds_start_cut + total_record) + ' ' + video + ' -out ' + higlight_video_path)                    
                        else:
                            # Obtengo el video anterior para concatenar
                            previous_video = get_previous_video(video)
                            previous_video_str_date = convert_path_to_str_date(previous_video)
                            seconds_start_cut = difference - TIME_BEFORE
                            
                            if (seconds_start_cut < 0):
                                seconds_start_cut = 0

                            # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
                            if (previous_video_str_date != ''):
                                find_video = True
                                previous_video_date = str_to_date_time(previous_video_str_date)
                                difference = rest_date_to_seconds(previous_video_date, row_date)
                                seconds_start_cut = difference - TIME_BEFORE
                                seconds_start_cut = TIME_RECORDING_VIDEO - seconds_start_cut

                                os.system("MP4Box -cat "  + previous_video + ' -cat ' + video +  " " + aux_video_path)
                                #while not os.path.exists(aux_video_path):
                                #    time.sleep(1)
                                os.system('MP4Box -splitx ' + str(seconds_start_cut) + ':' + str(seconds_start_cut + total_record) + ' ' + aux_video_path + ' -out ' + higlight_video_path)
                                os.remove(aux_video_path)
                            else:
                                find_video = True
                                os.system('MP4Box -splitx ' + str(seconds_start_cut) + ':' + str(seconds_start_cut + total_record) + ' ' + video + ' -out ' + higlight_video_path)                    
                
                if find_video == True:
                    update_mark(str(row))
                else:
                    # LUego de 3 intentos no se procesara mas la marca
                    add_intent_to_mark(str(row))
                    time.sleep(TIME_RECORDING_VIDEO)
                    
            current_time = get_current_time_int()
            
    except Exception as e:
        print('Error ' + str(e))
        log_error("SYSTEM", 'SYSTEM', 'videoHighlights.py - main()', str(e))

if __name__ == '__main__':
    main()