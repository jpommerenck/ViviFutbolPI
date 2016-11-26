import os
import time

print("[INICIO] -- Disable Public WiFi")
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Disable/interfaces /etc/network')
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Disable/dhcpcd.conf /etc')
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Disable/hostapd /etc/default')
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Disable/dnsmasq.conf /etc')
os.system('sudo service dnsmasq restart')
os.system('sudo service hostapd restart')
os.system('sudo ifdown wlan0; sudo ifup wlan0')
print("[FIN]    -- Disable Public WiFi")
print("[CONFIG] -- Se va a reiniciar el Raspberry")
time.sleep(2)
os.system('sudo reboot')
