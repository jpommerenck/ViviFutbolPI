
from flask import Flask
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str
import time



def get_time():
    print time.strftime('%H %M')
