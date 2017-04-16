import time
import os
from fileUtil import get_mp4_files_in_directory, get_next_video
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
    print(mark_date)
    j = 0
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
        print('video: ' + video)
        next_video = get_next_video(video)
        print('next_video: ' + next_video)
        #Pregunto si la marca esta dentro del video
        #if int(get_time(row) > 

