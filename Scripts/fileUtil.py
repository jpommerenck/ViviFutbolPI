import os
import glob
from dateUtil import get_current_short_date_str, get_seconds_cut, get_time, convert_seconds_to_minutes
from os.path import basename

# Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolPI/'
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

def get_jpg_files_in_directory(directory):
    return glob.glob(directory+'/*.jpg')
    
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

def get_file_name_without_extension(name):
    filename, file_extension = os.path.splitext(name)
    return os.path.basename(filename)

def get_file_name(file_path):
    head, tail = os.path.split(file_path)
    file_name = get_file_name_without_extension(tail)
    return file_name

def image_monitor_device(directory, picture_path):
    # Si ya existe una imagen la elimino para actualizarla
    try:
        os.remove(picture_path)
    except OSError:
        pass

    # Obtengo el video que se esta grabando para obtener el ultimo frame
    print(directory)
    newest_h264_file = newest_h264_in_directory(directory)
    picture_file = ''

    if len(newest_h264_file) > 0 :
        # Si se esta grabando un video obtengo el frame
        print('entro al if')
        time_last_frame = get_time_last_frame(newest_h264_file, picture_path)
        print("******************")
        print(time_last_frame)
        picture_file = get_last_frame_from_current_video(newest_h264_file, picture_path, time_last_frame)
        print(picture_file)
    else:
        print("poruqe mierda entra al else")
        from camera import take_picture
        # Si la camara no esta grabando, saco una foto
        picture_file = take_picture(picture_path)

    print('-- Logger : Ya saco la foto')

def get_last_frame_from_current_video(h264_file, picture_path, time_last_frame):
    os.system("avconv -i "+ h264_file +" --ss " + time_last_frame + " -vframes 1 -f "+ picture_path)

def get_time_last_frame(newest_h264_file, picture_path):
    h264_name = get_file_name(newest_h264_file)
    h264_time = get_time(h264_name)
    picture_name = get_file_name(picture_path)
    picture_time = get_time(picture_name)
    difference_time = get_seconds_cut(picture_time, h264_time)
    time_last_frame = convert_seconds_to_minutes(difference_time)
    return time_last_frame
