import os
import glob
from dateUtil import get_current_short_date_str

# Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbol/'
PATH_CONCAT_VIDEOS = '/Concat/'

def get_concat_file_name(file_name):
    file_name_split = file_name.split('/')
    file_only_name = file_name_split[len(file_name_split)-1]
    file_without_extension = file_only_name.split('.')[0]
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
    return video_path + PATH_CONCAT_VIDEOS + file_without_extension + '.mp4'
    
def get_h264_files_in_directory(directory):
    return glob.glob(directory+'/*.h264')

def get_mp4_files_in_directory(directory):
    return glob.glob(directory+'/*.mp4')
    
def delete_file(file_path):
    os.system('rm '+ file_path)

def newest_h264_in_directory(directory):
    file_array = get_h264_files_in_directory(directory)
    if len(file_array) > 0:
        return max(glob.iglob(directory+'*.h264'), key=os.path.getctime)
    else:
        return []

def newest_MP4_in_directory(directory):
    file_array = get_mp4_files_in_directory(directory)
    if len(file_array) > 0:
        return max(glob.iglob(directory+'*.mp4'), key=os.path.getctime)
    else:
        return []
