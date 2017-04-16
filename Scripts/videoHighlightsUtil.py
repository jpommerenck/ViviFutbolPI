import time
import os
from fileUtil import get_mp4_files_in_directory
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time
from dbUtil import get_all_marks_between_dates, get_all_marks_not_processed

TIME_AFTER = 5
TIME_BEFORE = 5
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
    mark_time = row.split('_')[1]
    print(mark_time)
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

    while ((find_video == False) and (i+1<len(file_array))):
        if (int(get_time_subtr(get_time(row), TIME_BEFORE)) > int(get_time(file_array[i]))) and (int(get_time_subtr(get_time(row), TIME_BEFORE)) < int(get_time(file_array[i+1]))) and (int(get_time_adi(get_time(row), TIME_AFTER)) > int(get_time(file_array[i+1]))):
            #if (int(get_time_subtr(get_time(row), TIME_BEFORE)) > int(get_time(file_array[i]))) and (int(get_time_subtr(get_time(row), TIME_BEFORE)) < int(get_time(file_array[i+1]))) and (int(get_time_adi(get_time(row), TIME_AFTER)) < int(get_time(file_array[i+1]))):
            find_video = True
            file_array_highlight.append(file_array[i])
             
            seconds_start_cut = get_seconds_cut(get_time(file_array[i]), get_time_subtr(get_time(row), TIME_BEFORE))
            seconds_finish_cut = get_seconds_cut(get_time(file_array[i]), get_time_adi(get_time(row), TIME_AFTER))
            os.system("MP4Box -splitx " + "2" + ":" + "4 " + file_array[i] + " -out " + new_video_path + HIGHLIGHT_NAME + row + ".mp4")
        else:
            if (int(get_time_subtr(get_time(row), TIME_BEFORE)) > int(get_time(file_array[i]))) and (int(get_time_subtr(get_time(row), TIME_BEFORE)) < int(get_time(file_array[i+1]))) and (int(get_time_adi(get_time(row), TIME_AFTER)) < int(get_time(file_array[i+1]))):
                find_video = True
                file_array_highlight.append(file_array[i])
                file_array_highlight.append(file_array[i+1])

                for file_name in file_array_highlight:
                    concat_string = concat_string + " -cat " + file_name
                #os.system("MP4Box" + concat_string + " -new " + new_video_path + COMPLETE_NAME + row + ".mp4")

                seconds_start_cut = get_seconds_cut(get_time(file_array[i]), get_time_subtr(get_time(row), TIME_BEFORE))
                seconds_finish_cut = get_seconds_cut(get_time(file_array[i]), get_time_adi(get_time(row), TIME_AFTER))
                #os.system("MP4Box -splitx " + "2" + ":" + "4 " + new_video_path + COMPLETE_NAME + row + ".mp4" + " -out " + new_video_path + HIGHLIGHT_NAME + row + ".mp4")
            else:
                i = i+1
