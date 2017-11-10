# Plex Listen and WOL for Raspbian

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
```
## Configure
```sudo nano plexlistenandwol.py```
Change ```conf.mac``` to the mac address of the PC to wake up.

*The PC's Plex should be configured for a different IP address than 32400 to allow for external connections on both the Pi and the PC*

## 

## TO DO
- Pushbullet notifcation when action takes place and/or other logging
- Check if PC active and if it is, don't even open sockets
