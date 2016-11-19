from fileUtil import getH264FilesInDirectory
from dateUtil import getCurrentShortDateStr
import os
from time import sleep

while True:
    path =    '/home/pi/Desktop/'+getCurrentShortDateStr()
    fileArray = getH264FilesInDirectory(path)
    if len(fileArray) > 0 :
        for file in fileArray:
            fileNewName = file.replace('.h264', '.mp4')
            sleep(3)
            os.system('MP4Box -add '+file+' '+fileNewName)
            os.system('rm '+file)
