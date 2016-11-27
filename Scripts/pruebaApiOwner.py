from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolPI/Videos/'
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolPI/Pictures/'

picture_path = PATH_PICTURES_LOCALIZATION + get_current_date_str() + ".jpg"
video_directory = PATH_VIDEO_LOCALIZATION + get_current_short_date_str()

image_monitor_device(video_directory, picture_path)
