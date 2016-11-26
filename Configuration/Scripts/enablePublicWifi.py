import os
import time

print("[INICIO] -- Enable Public WiFi")
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Enable/interfaces /etc/network')
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Enable/dhcpcd.conf /etc')
os.system('sudo cp /home/pi/ViviFutbolPI/Configuration/ConfigFiles/PublicWifi/Enable/hostapd /etc/default')
os.system('sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.ap')
os.system('sudo mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf')
os.system('sudo service dnsmasq restart')
os.system('sudo service hostapd restart')
os.system('sudo ifdown wlan0; sudo ifup wlan0')
print("[FIN]    -- Enable Public WiFi")
print("[CONFIG] -- Se va a reiniciar el Raspberry")
time.sleep(2)
os.system('sudo reboot')
