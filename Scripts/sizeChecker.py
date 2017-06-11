import shutil
import os
from dateUtil import get_current_short_date_str, get_yesterday_short_date_str
from dbUtil import get_config_value
from logger import log_error

def main():
    try:
        MB_MULTIPLIER = 1024*1024
        FOLDERS_PATH = '/home/pi/ViviFutbolLocal/VideosEXPO/'
        LOWER_SPACE_LIMIT_IN_MB = int(get_config_value("DISK_START_DELETE_SPACE"))
        UPPER_SPACE_LIMIT_IN_MB = int(get_config_value("DISK_STOP_DELETE_SPACE"))
        
        print("limite inferior "+str(LOWER_SPACE_LIMIT_IN_MB))
        print("limite superior "+str(UPPER_SPACE_LIMIT_IN_MB))

        current_date = get_current_short_date_str()
        yesterday_date = get_yesterday_short_date_str();
        usage = shutil.disk_usage(FOLDERS_PATH)
        availableMb = usage.free/(MB_MULTIPLIER)
        
        print("Available MB: " + str(availableMb))
        print("Today folder :" +current_date)
        print("Yesterday folder :" + yesterday_date);

        if availableMb < LOWER_SPACE_LIMIT_IN_MB :
            print("Low space. Starting delete...")
            folders = os.listdir(FOLDERS_PATH)
            folders.sort()
            for i, val in enumerate(folders):
                if (val == current_date) or (val == yesterday_date):
                    print("Protected folder found - skipping from delete")
                else:
                    print("DELETING " +val)
                    shutil.rmtree(FOLDERS_PATH+val)
                    usage = shutil.disk_usage(FOLDERS_PATH)
                    availableMb = usage.free/(MB_MULTIPLIER)
                    print("Available MB after delete " + str(availableMb))
                    if availableMb >= UPPER_SPACE_LIMIT_IN_MB:
                        print("Finishing delete...")
                        break
    except Exception as e:
        log_error("SYSTEM", 'SYSTEM', 'sizeChecker.py - main()', str(e))

        
if __name__ == '__main__':
    main()
