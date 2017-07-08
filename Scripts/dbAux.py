import shutil
import os
from dateUtil import get_current_short_date_str, get_yesterday_short_date_str
from dbUtil import get_config_value
from logger import log_error

MB_MULTIPLIER = 1024*1024
FOLDERS_PATH = '/home/pi/ViviFutbolLocal/Videos/'
LOWER_SPACE_LIMIT_IN_MB = int(get_config_value("DISK_START_DELETE_SPACE"))
UPPER_SPACE_LIMIT_IN_MB = int(get_config_value("DISK_STOP_DELETE_SPACE"))
        
print("limite inferior "+str(LOWER_SPACE_LIMIT_IN_MB))
print("limite superior "+str(UPPER_SPACE_LIMIT_IN_MB))

current_date = get_current_short_date_str()
yesterday_date = get_yesterday_short_date_str();
usage = shutil.disk_usage(FOLDERS_PATH)
availableMb = usage.free/(MB_MULTIPLIER)
        
print("Available MB: " + str(availableMb))
