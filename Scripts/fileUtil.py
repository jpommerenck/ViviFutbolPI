import os
import glob
from dateUtil import get_current_short_date_str, get_seconds_cut, get_time, convert_seconds_to_minutes, str_to_date_time, add_seconds_to_date, get_date_str, add_days_to_date, str_to_date, convert_path_to_str_date
from os.path import basename
from picamera import PiCamera

# Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/'
PATH_CONCAT_VIDEOS = '/Concat/'
TIME_RECORDING_VIDEO=15

def get_concat_file_name(file_name):
    file_name_split = file_name.split('/')
    file_only_name = file_name_split[len(file_name_split)-1]
    file_without_extension = file_only_name.split('.')[0]
    video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()
    return video_path + PATH_CONCAT_VIDEOS + file_without_extension + '.mp4'

    
def get_h264_files_in_directory(directory):
    return glob.glob(directory+'/*.h264')


def get_mp4_files_in_directory(directory):
    files = glob.glob(directory+'/*.mp4')
    files.sort(key=lambda x: os.path.getmtime(x))
    return files


def get_jpg_files_in_directory(directory):
    return glob.glob(directory+'/*.jpg')


def get_wav_files_in_directory(directory):
    files = glob.glob(directory+'/*.wav')
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

    
def delete_file(file_path):
    os.system('rm '+ file_path)


def newest_h264_in_directory(directory):
    file_array = get_h264_files_in_directory(directory)
    if len(file_array) > 0:
        return max(glob.iglob(directory+'*.h264'), key=os.path.getctime)
    else:
        return []


def newest_wav_in_directory(directory):
    file_array = get_h264_files_in_directory(directory)
    if len(file_array) > 0:
        return max(glob.iglob(directory+'*.wav'), key=os.path.getctime)
    else:
        return []

    
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

    
def oldest_MP4_in_directory(directory):
    file_array = get_mp4_files_in_directory(directory)
    if len(file_array) > 0:
        return min(glob.iglob(directory+'*.mp4'), key=os.path.getctime)
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
    # Obtengo el video que se esta grabando para obtener el ultimo frame
    newest_h264_file = newest_h264_in_directory(directory + "/")
    picture_file = ''
    
    if len(newest_h264_file) > 0 :
        # Si se esta grabando un video obtengo el frame
        time_last_frame = get_time_last_frame(newest_h264_file, picture_path)
        get_last_frame_from_current_video(newest_h264_file, picture_path, time_last_frame)
    else:
        # Si la camara no esta grabando, saco una foto
        try:
            PiCamera().close()
        except OSError:
            pass
        camera = PiCamera()
        camera.capture(picture_path)
        camera.close()


def get_last_frame_from_current_video(h264_file, picture_path, time_last_frame):
    os.system('avconv -ss ' + time_last_frame + ' -r 30 -i ' + h264_file + ' -t 1 ' + picture_path)


def get_time_last_frame(newest_h264_file, picture_path):
    h264_name = get_file_name(newest_h264_file)
    h264_time = get_time(h264_name)
    picture_name = get_file_name(picture_path)
    picture_time = get_time(picture_name)
    difference_time = get_seconds_cut(h264_time, picture_time)
    time_last_frame = convert_seconds_to_minutes(difference_time)
    return time_last_frame


def get_next_video(video_path):
    video_str_date = convert_path_to_str_date(video_path)
    video_date = str_to_date_time(video_str_date)
    new_video_date = add_seconds_to_date(video_date, TIME_RECORDING_VIDEO)
    new_video_path = PATH_VIDEO_LOCALIZATION + "Videos/" + video_str_date + '/mp4/'+ get_date_str(new_video_date) + ".mp4"
    if not os.path.exists(new_video_path):
        new_video_date = str(new_video_date).split(' ')[0]
        new_video_date = add_days_to_date(str_to_date(new_video_date), 1)
        new_video_date = str(new_video_date).split(' ')[0]
        new_video_path = PATH_VIDEO_LOCALIZATION + "Videos/" + new_video_date + '/mp4/'

        if len(oldest_MP4_in_directory(new_video_path)) !=0 :
            new_video_path = oldest_MP4_in_directory(new_video_path)

    return new_video_path    
    
def video_contains_mark(video_date, mark):
    finish_time = add_seconds_to_date(video_date, TIME_RECORDING_VIDEO)
    mark_date = str_to_date_time(mark)
    if (video_date < mark_date and finish_time > mark_date):
        return True
    else:
        return False
