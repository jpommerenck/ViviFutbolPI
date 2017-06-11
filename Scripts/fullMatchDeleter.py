import os
import shutil
from dateUtil import get_yesterday_short_date_str, get_current_hour
from dbUtil import log_error

FOLDERS_PATH = '/home/pi/ViviFutbolLocal/Videos/'

yesterday_date = get_yesterday_short_date_str()
folder = FOLDERS_PATH+yesterday_date+'/Match'
if(get_current_hour() > 3):
    if(os.path.isdir(folder)):
        print("Eliminando contenidos de cartpeta "+folder+" ...")
        shutil.rmtree(folder);
        print("Carpeta "+folder+" eliminada")
    else:
        print("Carpeta "+folder+" no encontrada")
else:
    print("Eliminacion de partidos completos pospuesta por hora")
                 
