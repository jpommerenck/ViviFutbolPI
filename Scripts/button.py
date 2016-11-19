import RPi.GPIO as GPIO
import time
from dbUtil import insertMark
from dateUtil import  getCurrentDateStr

GPIO.setmode(GPIO.BCM)

button = 19
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(button)
    if input_state == False:
        print('Button Pressed')
        date =  getCurrentDateStr()
        insertMark(date)
        time.sleep(0.2)
