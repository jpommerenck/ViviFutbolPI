import os
from time import sleep
import shutil
from logger import log_error
from dbUtil import get_config_value


def main():
    try:
        PATH_PICTURES_LOCALIZATION = get_config_value("PICTURES_LOCALIZATION_PATH")
        
        while True:
            for root, dirs, files in os.walk(PATH_PICTURES_LOCALIZATION):
                for f in files:
                    os.unlink(os.path.join(root, f))
            sleep(60)
    except Exception as e:
            log_error("SYSTEM", 'SYSTEM', 'picturesDeleter.py - main()', str(e))


if __name__ == '__main__':
    main()
