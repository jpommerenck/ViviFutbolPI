import shutil
import os
from dateUtil import get_current_short_date_str
from dateUtil import get_yesterday_short_date_str

MB_MULTIPLIER = 1024*1024
FOLDERS_PATH = '/home/pi/ViviFutbolLocal/VideosEXPO/'
LOWER_SPACE_LIMIT_IN_MB = 18000 ##1024
UPPER_SPACE_LIMIT_IN_MB = 19250 ##1024*8

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
