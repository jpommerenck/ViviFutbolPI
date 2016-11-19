import os
import time
from fileUtil import get_mp4_files_in_directory
from dateUtil import get_current_short_date_str, get_time_subtraction, get_time_adition



TIME_START = '090921'
TIME_FINISH = '100950'
TIME_RECORDING_VIDEO=10
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbol/Videos/'

def join_match_video(TIME_START, TIME_FINISH):
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + '/mp4/'
    find_first_video = False
    file_array = get_mp4_files_in_directory(video_path)
    file_array.sort()
    i=0
    file_array_match=[]

    # Impresion para probar
    for file_name in file_array:
        print(file_name)

    while ((find_first_video == False) and (i<len(file_array))):
        video = file_array[i]
        print(get_time_subtraction(video, TIME_RECORDING_VIDEO))

        # Encuentro el primer video del partido
        if (int(get_time_subtraction(video, TIME_RECORDING_VIDEO)) > int(TIME_START)):
            find_first_video = True
                
            file_array_match.append(video)
            i=i+1

            # Agrego el resto de los videos del partido
            while (int(get_time_adition(file_array[i], TIME_RECORDING_VIDEO)) < int(TIME_FINISH)) and (i<len(file_array)) :
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
    print(concatString)

    os.system("MP4Box" + concatString + " -new /home/pi/ViviFutbol/Videos/2016-11-12/mp4/Match.mp4")
    os.system("MP4Box -splitx int(TIME_START):int(TIME_FINISH) /home/pi/ViviFutbol/Videos/2016-11-12/mp4/Match.mp4 -out /home/pi/ViviFutbol/Videos/2016-11-12/mp4/MatchSplit.mp4")
    
    
        
        
    
