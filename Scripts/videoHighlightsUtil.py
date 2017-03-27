import time
import os
from fileUtil import get_mp4_files_in_directory
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time
from dbUtil import get_all_marks_between_dates, get_all_marks_not_processed

TIME_AFTER = 5
TIME_BEFORE = 5
TIME_RECORDING_VIDEO=15
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolPI/Videos/'

video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
file_array = get_mp4_files_in_directory(video_path)
file_array.sort()
marks = get_all_marks_not_processed()
i=0
file_array_highlight=[]
find_video = False
concatString = ""
newVideoPath = video_path + "Highlights/" 

for row in marks:
    find_video = False
    i=0
    while ((find_video == False) and (i+1<len(file_array))):
        if (int(get_time_subtr(get_time(row), TIME_BEFORE)) > int(get_time(file_array[i]))) and (int(get_time_subtr(get_time(row), TIME_BEFORE)) < int(get_time(file_array[i+1]))) and (int(get_time_adi(get_time(row), TIME_AFTER)) < int(get_time(file_array[i+1]))):
            find_video = True
            file_array_highlight.append(file_array[i])
             
            seconds_start_cut = get_seconds_cut(get_time(file_array[i]), get_time_subtr(get_time(row), TIME_BEFORE))
            seconds_finish_cut = get_seconds_cut(get_time(file_array[i]), get_time_adi(get_time(row), TIME_AFTER))
            os.system("MP4Box -splitx " + "2" + ":" + "4 " + file_array[i] + " -out " + newVideoPath + "HightlightSplit_+"+row+".mp4")
        else:
            if (int(get_time_subtr(get_time(row), TIME_BEFORE)) > int(get_time(file_array[i]))) and (int(get_time_subtr(get_time(row), TIME_BEFORE)) < int(get_time(file_array[i+1]))) and (int(get_time_adi(get_time(row), TIME_AFTER)) > int(get_time(file_array[i+1]))):
                find_video = True
                file_array_highlight.append(file_array[i])
                file_array_highlight.append(file_array[i+1])

                for file_name in file_array_highlight:
                    concatString = concatString + " -cat " + file_name
                os.system("MP4Box" + concatString + " -new " + newVideoPath + "HightlightComplete_+"+row+".mp4")

                seconds_start_cut = get_seconds_cut(get_time(file_array[i]), get_time_subtr(get_time(row), TIME_BEFORE))
                seconds_finish_cut = get_seconds_cut(get_time(file_array[i]), get_time_adi(get_time(row), TIME_AFTER))
                os.system("MP4Box -splitx " + "2" + ":" + "4 " + newVideoPath + "HightlightComplete_+"+row+".mp4" + " -out " + newVideoPath + "HightlightSplit_+"+row+".mp4")
            else:
                i = i+1

#MP4Box -cat /home/pi/Desktop/v1.h264:fps=30 -cat /home/pi/Desktop/v2.h264:fps=30 -cat /home/pi/Desktop/v3.h264:fps=30 -cat /home/pi/Desktop/v4.h264:fps=30 -new /home/pi/Desktop/v1234.mp4
