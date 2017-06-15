import os
import shutil
from dateUtil import get_yesterday_short_date_str, get_current_hour
from logger import log_error
from dbUtil import get_config_value

def main():
    try:
        FOLDERS_PATH = get_config_value("VIDEO_LOCALIZATION_PATH")
        
        yesterday_date = get_yesterday_short_date_str()
        folder = FOLDERS_PATH + yesterday_date + '/Match'
        if(get_current_hour() > 3):
            if(os.path.isdir(folder)):
                print("Eliminando contenidos de cartpeta "+folder+" ...")
                shutil.rmtree(folder);
                print("Carpeta "+folder+" eliminada")
            else:
                print("Carpeta "+folder+" no encontrada")
        else:
            print("Eliminacion de partidos completos pospuesta por hora")
                     
    except Exception as e:
            log_error("SYSTEM", 'SYSTEM', 'fullMatchDeleter.py', str(e))


if __name__ == '__main__':
    main()
