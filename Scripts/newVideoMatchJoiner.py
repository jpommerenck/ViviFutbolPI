import time
import os
from fileUtil import get_mp4_files_in_directory, get_next_video, video_contains_mark, get_previous_video
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time, str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date, rest_date_to_seconds

TIME_START = '2017-03-26_20-41-10'
TIME_RECORDING_VIDEO=15
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'

def join_match_video(TIME_START):
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
    file_array = get_mp4_files_in_directory(video_path)

    file_array_match=[]

    start_date = str_to_date_time(TIME_START)
    finish_date = add_seconds_to_date(start_date)
    
    for video in file_array:
        video_str_date = convert_path_to_str_date(video)
        video_date = str_to_date_time(video_str_date)

        if video_contains_mark(video_date, start_date):
            start_complete_video = rest_date_to_seconds(start_date, video_date)
            finish_complete_video = start_complete_video + 3600

            next_video = get_next_video(video)
            while next_video!='':
                file_array_match.append(next_video)
                next_video = get_next_video(next_video)

            concatString = ""
            for file_name in file_array_match:
                concatString = concatString + " -cat " + file_name

                
            aux_video_path = video_path + '/Complete/Aux_' + start_date + '.mp4'
            new_video_path = video_path + '/Complete/' + start_date + '.mp4'
            os.system("MP4Box" + concatString + " -new " + aux_video_path)

            os.system("MP4Box -splitx " + str(start_complete_video) + ":" + str(finish_complete_video) +" " + aux_video_path + " -out " + new_video_path)
