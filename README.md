# Plex Listen and WOL (Wake-On-Lan) for Raspbian

## The idea

- When set up, you will have a new Plex server on your Plex account. Call it "X Rasperry Pi Server". This will usually be disconnected and greyed out on your server list in the Plex Mobile/TV app because the Raspberry Pi does not need an actively running Plex Server.
- While it is greyed out, your Plex Mobile/TV app will still try to connect to all Plex servers added to your Plex account. This will be your PC (which is currently sleeping and so it will not respond) and the Raspberry Pi which also does not have a Plex server running so also will not respond.
- However my script running on your Pi will be able to detect that connection attempt and will tell your PC to wake up (using a feature called Wake-On-Lan or WOL). Hopefully, if your PC is connected to the network by ethernet and the Raspberry Pi is also located within the network (Wifi or ethernet, doesn't matter), the PC will begin to wake up and the Plex server can start responding.
- Within a few seconds, your Plex Mobile/TV app should see your PC's Plex server

## How it works

You will need to install Plex on the RasperryPi. I have provided instructions below. I have also provided instructions to make sure Plex does not run automatically at startup. It is just installed to say hi to the Plex network so your Raspberry Pi can be linked to your Plex account. To keep it linked, my script will also periodically start the Plex server so it can say hi to the Plex network and keep the IP address of your Pi fresh.

My Plex python script is designed to run as an autostart daemon on Rasperry Pi. It listens on port 32400 (the port that Plex usually listens to) and when a client such as a mobile device tried to find the Raspberry Pi Plex server, it wouldn't respond normally but it will trigger an attempt to connect to the send some WOL signals out to the PC to wake it up.

It works 23 hours and 58 minutes a day as it spends 2 minutes a day starting Plex temporarily to keep it activated with the Plex account.

The old way I used to do things was to have a network sniffer on the RaspberryPi to listen to connection attempts directly to the PC, but that felt dirty. I like this way now.

You may have to occasionally manually stop the service, start Plex on the raspberry pi and navigate to 127.0.0.1:32400 to refresh the login session and keep the pi connected to your Plex account.

## Pre-requisites
- I don't have a multiuser Plex set up so have not tried if it works with that set up
- WOL only works if the Plex server PC is LAN (ethernet) connected. In my own network, my PC is connected on both Wifi (faster) and Ethernet (through a slow bug reliable powerline adapter). The Raspberry Pi is connected by Wifi. The PC may need bios configuration to enable Wake-On-Lan so that packets successfully wake the PC from sleep.
- You will need port forwarding for both the Pi (port 32400) and the PC (choose a different port in Plex settings) for this to work externally.

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
