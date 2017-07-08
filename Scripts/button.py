import RPi.GPIO as GPIO
import time
from logger import log_info, log_error
from dateUtil import  get_current_date_str, check_for_insert_mark, str_to_date_time, get_current_short_date_str
from dbUtil import get_last_mark, insert_mark, get_config_value
from fileUtil import newest_h264_in_directory

GPIO.setmode(GPIO.BCM)

button = 19
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
    try:
        SECONDS_WAITING_FOR_ADD_NEW_MARK = int(get_config_value("SECONDS_WAITING_FOR_ADD_NEW_MARK"))
        PATH_VIDEO_LOCALIZATION = get_config_value("VIDEO_LOCALIZATION_PATH")
        video_path = PATH_VIDEO_LOCALIZATION + get_current_short_date_str() + "/"

        while True:
            input_state = GPIO.input(button)
            if input_state == False:
                print('Button Pressed')
                date =  get_current_date_str()
                new_mark = str_to_date_time(date)
                last_mark = str_to_date_time(get_last_mark())

                # Consulto si no se ingreso una marca recientemente
                if check_for_insert_mark(new_mark, last_mark, SECONDS_WAITING_FOR_ADD_NEW_MARK):
                    print('Mark inserted ' + str(date))
                    current_video = newest_h264_in_directory(video_path)
                    insert_mark(date, str(current_video))
                time.sleep(0.2)
                
    except Exception as e:
        print(str(e))
        log_error("SYSTEM", 'SYSTEM', 'button.py - main()', str(e))

if __name__ == '__main__':
    main()
