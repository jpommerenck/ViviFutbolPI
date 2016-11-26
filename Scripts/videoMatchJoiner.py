import os
import time
from fileUtil import get_mp4_files_in_directory
from dateUtil import get_current_short_date_str, get_time_subtr, get_time_adi, get_seconds_cut, get_time



TIME_START = '092903'
TIME_FINISH = '093853'
TIME_RECORDING_VIDEO=10
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolPI/Videos/'

def join_match_video(TIME_START, TIME_FINISH):
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
    find_first_video = False
    file_array = get_mp4_files_in_directory(video_path)
    file_array.sort()
    i=0
    file_array_match=[]
    video=""

    # Impresion para probar
    for file_name in file_array:
        print(file_name)
    
    while ((find_first_video == False) and (i<len(file_array))):
        video = file_array[i]

        # Encuentro el primer video del partido
        if (int(get_time_subtr(TIME_START, TIME_RECORDING_VIDEO)) < int(get_time(video))):

            find_first_video = True
                
            file_array_match.append(video)
            i=i+1

            # Agrego el resto de los videos del partido
            while (int(get_time_adi(TIME_FINISH, TIME_RECORDING_VIDEO)) > int(get_time(file_array[i]))) and (i<len(file_array)) :
                file_array_match.append(file_array[i])
                i=i+1
        else :
            i=i+1
            
    # Impresion para probar
    for file_name in file_array_match:
        print(file_name)

    concatString = ""
    for file_name in file_array_match:
        concatString = concatString + " -cat " + file_name

    # Impresion para probar
    print(video)
    print(concatString)

    newVideoPath = video_path + "Match/" 
    os.system("MP4Box" + concatString + " -new " + newVideoPath + "MatchComplete.mp4")


    # Obtengo los segundos de corte, y corto el video
    seconds_start_cut = get_seconds_cut(get_time(video), TIME_START)
    print(seconds_start_cut)
    seconds_finish_cut = get_seconds_cut(get_time(video), TIME_FINISH)
    print(seconds_finish_cut)
    # Hay que cambiar la hora de fin para seconds_finish_cut
    os.system("MP4Box -splitx " + str(seconds_start_cut) + ":" + "45 " + newVideoPath + "MatchComplete.mp4" + " -out " + newVideoPath + "MatchSplit.mp4")
    
    
        
        
    
