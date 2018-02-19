# Plex Listen and WOL (Wake-On-Lan) for Raspbian

The Plex python script is designed to run as an autostart daemon on Rasperry Pi to aid a PC on the network that would like to get some sleep but and be awoken as soon as someone wants to connect to Raspberry Pi. It works automatically with mobiles, TVs etc. whether in the local networks or outside.

It works by registering the Pi as a Plex server and pretending you have an extra Plex server there. When a client such as a mobile device tried to find all the Plex servers, it will try to connect to the Rasperry Pi, at this point the Raspberry Pi sends some WOLs out to the PC to wake it up.

It works 23 hours and 58 minutes a day as it spends 2 minutes a day starting Plex temporarily to keep it activated with the Plex account.

This used to work by keep Plex open and having a sniffer, but that used up too much resources.

## Pre-requisites
- I don't have a multiuser Plex set up so have not tried if it works with that set up
- WOL only works if the Plex server PC is LAN (ethernet) connected. In my own network, my PC is connected on both Wifi (faster) and Ethernet (through a slow bug reliable powerline adapter). The PC may need bios configuration to allow Wake-On-Lan so that packets successfully power on the PC.
- You will need port forwarding for both the Pi (port 32400) and the PC (choose a different port) for this to work externally.

## Install Plex

(Thanks to https://thepi.io/how-to-set-up-a-raspberry-pi-plex-server/)
```
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key | sudo apt-key add -
echo "deb https://dev2day.de/pms/ jessie main" | sudo tee /etc/apt/sources.list.d/pms.list
sudo apt-get update
sudo apt-get install -t jessie plexmediaserver
sudo nano /etc/default/plexmediaserver.prev
sudo service plexmediaserver restart
hostname -I
sudo nano /boot/cmdline.txt # At the bottom of the command line text file, type ip= followed by your IP address that you got from the command above. Save and exit the file (CTRL+X, then Y, then Enter).
sudo reboot
```
Then go to http://localhost:32400/web/index.html and log in to your Plex account
```
sudo service plexmediaserver stop # will be started for a minute every day just to keep the account updated
sudo update-rc.d -f plexmediaserver remove
grep -nrI Default-Start /etc/init.d # to check its not being autostarted
```

## Clone the files
```
git clone https://github.com/Ali1/Plex-Listen-and-WOL-for-Raspbian.git
cd Plex-Listen-and-WOL-for-Raspbian
sudo ln -s plexlistenandwol.service /lib/systemd/system/plexlistenandwol.service
sudo chmod 644 /lib/systemd/system/plexlistenandwol.service
chmod +x plexlistenandwol.py
sudo systemctl daemon-reload
sudo systemctl enable plexlistenandwol.service
sudo systemctl start plexlistenandwol.service
sudo systemctl status plexlistenandwol.service # to check status any time
```
## Configure
```sudo nano plexlistenandwol.py```
Change ```conf.mac``` to the mac address of the PC to wake up.

*The PC's Plex should be configured for a different port than 32400 to allow for external connections on both the Pi and the PC*

## 

## TO DO
- Pushbullet notifcation when action takes place and/or other logging
- Check if PC active and if it is, don't even open sockets
