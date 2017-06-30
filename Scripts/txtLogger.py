import logging
logging.basicConfig(filename='/home/pi/ViviFutbolPI/logs/error.log', level=logging.ERROR)

def log_error(error):
    logging.error(error)
