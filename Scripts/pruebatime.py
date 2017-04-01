
from flask import Flask
from flask import send_file
from fileUtil import image_monitor_device
from dateUtil import get_current_date_str, get_current_short_date_str, set_time
import time
import json
import os



def get_time():
    print time.strftime('%H %M')


def get_time2():
    return '{"currentTime":"' + time.strftime('%H') + ":" + time.strftime('%M')

def post_time(jsonRequest):
    timeRequest = json.loads(jsonRequest)
    hora = timeRequest["currentTime"]
    horaPI = hora.split(':')[0]
    minutosPI = hora.split(':')[1]
    set_time(horaPI, minutosPI)
