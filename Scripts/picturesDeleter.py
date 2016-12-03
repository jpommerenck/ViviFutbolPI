import os
from time import sleep
import shutil

#Constantes de la base de datos
PATH_PICTURES_LOCALIZATION = '/home/pi/ViviFutbolPI/Pictures/'


while True:
    for root, dirs, files in os.walk(PATH_PICTURES_LOCALIZATION):
        for f in files:
            os.unlink(os.path.join(root, f))
    sleep(60)
