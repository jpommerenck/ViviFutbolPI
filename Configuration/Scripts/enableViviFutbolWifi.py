import os

os.system('sudo service hostapd start')
os.system('sudo service dnsmasq start')
os.system('sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf')
