import time
import os
from fileUtil import get_mp4_files_in_directory, get_next_video, video_contains_mark, get_previous_video
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time, str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date
from dbUtil import get_all_marks_between_dates, get_all_marks_not_processed

TIME_AFTER = 3
TIME_BEFORE = 3
TIME_RECORDING_VIDEO=15
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
FOLDER_HIGLIGHTS = 'Highlights/'
HIGHLIGHT_NAME = 'Hightlight_'
COMPLETE_NAME = 'Complete_'

marks = get_all_marks_not_processed()

i=0
file_array_highlight=[]
find_video = False
concat_string = ''
last_mark_date = ''
video_path = ''

for row in marks:

    mark_date = row.split('_')[0]
    j = 0
    row_date = str_to_date_time(row)
    
    if mark_date != last_mark_date:
        find_video = False
        i=0
        file_array_highlight=[]
        concat_string = ''
        video_path = PATH_VIDEO_LOCALIZATION + mark_date + '/mp4/'
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

            #aca tengo que hacer 3 if, y que cada uno se encargue de hacer su logica
            seconds_start_cut = get_seconds_cut(get_time(video), get_time_subtr(get_time(row), TIME_BEFORE))
            seconds_finish_cut = get_seconds_cut(get_time(video), get_time_adi(get_time(row), TIME_AFTER))

            print('video ' + str(video))
            print('row ' + str(row))
            print('seconds_start_cut ' + str(seconds_start_cut))
            print('seconds_finish_cut ' + str(seconds_finish_cut))
            
            # Cuando no preciso concatenar videos
            if video_date <= start_highlight and video_finish >= finish_highlight:
                print('no preciso concatenar video')
                
            elif video_date <= start_highlight:
                # Obtengo el video siguiente para concatenar para concatenar
                next_video = get_next_video(video)
                next_video_str_date = convert_path_to_str_date(next_video)

                # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
                if (next_video_str_date != ''):
                    next_video_date = str_to_date_time(next_video_str_date)
            else:
                # Obtengo el video anterior para concatenar
                previous_video = get_previous_video(video)
                previous_video_str_date = convert_path_to_str_date(previous_video)

                # Consulto si se encontro el siguiente video, si no encontro es que es el ultimo video
                if (previous_video_str_date != ''):
                    previous_video_date = str_to_date_time(previous_video_str_date)
