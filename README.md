# Plex Listen and WOL for Raspbian

## 1. Install Plex

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


## 2. Install the sniffers
```
sudo apt-get install -t jessie libpcap-dev
sudo pip install -U pip
sudo pip install scapy IPython
```

## 3. Clone the files
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
## 4 Set the MAC address
```sudo nano plexlistenandwol.py```
Change ```conf.mac``` to the mac address of the PC to wake up.
