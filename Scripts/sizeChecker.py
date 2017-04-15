import shutil

usage = shutil.disk_usage('/home/pi/ViviFutbolLocal')
availableMb = usage.free/(1024*1024)
print("Available MB: " + str(availableMb))
