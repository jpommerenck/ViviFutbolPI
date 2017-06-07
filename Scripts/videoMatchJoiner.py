import time
import os
from fileUtil import get_mp4_files_in_directory, get_next_video, video_contains_mark, get_previous_video
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time, str_to_date_time, convert_path_to_str_date, str_to_date, add_seconds_to_date, rest_seconds_to_date, rest_date_to_seconds

TIME_START = '2017-06-03_21-00-00'
TIME_RECORDING_VIDEO=15
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/'
#VIDEO_TOTAL_TIME = 30
VIDEO_TOTAL_TIME = 3600

def join_match_video(TIME_START):
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
    file_array = get_mp4_files_in_directory(video_path)
    file_array_match=[]

    start_date = str_to_date_time(TIME_START)
    finish_date = add_seconds_to_date(start_date, VIDEO_TOTAL_TIME)
    
    for video in file_array:
        video_str_date = convert_path_to_str_date(video)
        video_date = str_to_date_time(video_str_date)
    
        if video_contains_mark(video_date, TIME_START):
            start_complete_video = rest_date_to_seconds(video_date, start_date)
            finish_complete_video = start_complete_video + VIDEO_TOTAL_TIME

            file_array_match.append(video)

            next_video = get_next_video(video)
            next_video_path = str(next_video)
            next_video_path = next_video_path.replace(video_path,'')

            while next_video_path != '':
                video_str_date = convert_path_to_str_date(next_video)
                next_video_date = str_to_date_time(video_str_date)
                file_array_match.append(next_video)

                next_video = get_next_video(next_video)
                next_video_path = str(next_video)
                next_video_path = next_video_path.split('/mp4/')[1]
                
                str_finish_date = str(finish_date)
                str_finish_date = str_finish_date.replace(':','-')
                str_finish_date = str_finish_date.replace(' ','_')
                
                if video_contains_mark(next_video_date, str_finish_date):
                    break
                
            concatString = ""
            for file_name in file_array_match:
                concatString = concatString + " -cat " + file_name


            if not os.path.exists(video_path + 'Complete/'):
                # En caso de no existir el directorio lo creo
                os.makedirs(video_path + 'Complete/')
            
            aux_video_path = video_path + 'Complete/Aux_' + str(start_date) + '.mp4'
            aux_video_path = aux_video_path.replace(':','-')
            aux_video_path = aux_video_path.replace(' ','_')
            
            new_video_path = video_path + 'Complete/' + str(start_date) + '.mp4'
            new_video_path = new_video_path.replace(':','-')
            new_video_path = new_video_path.replace(' ','_')
            
            os.system("MP4Box" + concatString + " -new " + aux_video_path)
            os.system('MP4Box -splitx ' + str(start_complete_video) + ':' + str(finish_complete_video) + ' "' + aux_video_path + '" -out "' + new_video_path + '"')
            os.remove(aux_video_path)
            break
