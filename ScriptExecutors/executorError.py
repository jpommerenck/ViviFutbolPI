from datetime import datetime
import sys
import logging

logging.basicConfig(filename='/home/pi/ViviFutbolPI/ScriptExecutors/logs/error.log', level=logging.ERROR)

date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
error = sys.argv[1]
logging.error(date+" - "+error)
