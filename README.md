# Plex Listen and WOL (Wake-On-Lan) for Raspbian

If you have a raspberry pi, why not save some energy and allow the server that hosts a Plex Media Server to go to sleep! The Raspberry Pi will sit on your network listening for incoming Plex connections and then wake your real Plex Media Server up when needed (e.g. when you open your Plex app on your mobile when you're in another country!).

## Pre-requisites
- Single User Plex set up (I haven't tried multi-user set ups)
- The computer hosting the real Plex Media Server needs to be connected to the local area network using ethernet (as this is usually the only way for Wake-On-Lan to work)
- The computer hosting the real Plex Media Server needs to have Wake-On-Lan functionality enabled usually from the BIOS.
- You will need port forwarding for both the Pi (port 32400) and the PC (choose a different port in Plex settings) for this to work externally. This will need playing about in your router settings.

## How does the magic work

As well as this script running on your Respberry Pi, you will also install and set up a fake Plex Media Server on the Raspberry Pi that's connected to your Plex account. When a client (e.g. phone app) is started, it usually pings all plex media servers and by pinging this fake server on the Raspberry Pi, the script knows you are in need of the real Plex Media Server and will start the PC that hosts it.

To keep the fake Plex Media Server ploy going, this script will run the Plex Media Server for a few minutes a day to keep in touch with your Plex account.

## Installation

### Step 1: Install Plex

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
sudo service plexmediaserver stop # willlater be started for a minute every day just to keep the account updated
sudo update-rc.d -f plexmediaserver remove # stop auto-start
grep -nrI Default-Start /etc/init.d # check in here that its not being autostarted
```

### Step 2: Clone the files
```
git clone https://github.com/Ali1/Plex-Listen-and-WOL-for-Raspbian.git
cd Plex-Listen-and-WOL-for-Raspbian
sudo ln -s plexlistenandwol.service /lib/systemd/system/plexlistenandwol.service
sudo chmod 644 /lib/systemd/system/plexlistenandwol.service
chmod +x plexlistenandwol.py
sudo systemctl daemon-reload
sudo systemctl enable plexlistenandwol.service
````

### Step 3: Configure
```
sudo mv config.ini.new config.ini
sudo nano config.ini
```
Change the mac address to the mac address of the PC to wake up (remember to use the ethernet adapter's mac address - it will be different to the Wifi mac address.

*The PC's Plex should be configured for a different port than 32400 to allow for external connections on both the Pi and the PC*

### Step 4: Start the service
```
sudo systemctl start plexlistenandwol.service
sudo systemctl status plexlistenandwol.service # to check status any time
```

## Running Plex Temporarily
If you need to re-login to your Plex account on the Pi, or otherwise need to change other settings, you may need to run the Plex server properly on the pi. To do this follow these steps:
```
sudo systemctl stop plexlistenandwol.service # stop the listener
sudo systemctl start plexmediaserver.service # Start Plex

# Now navigate to [IP of RaspberryPi]:32400 or if you using a browser on the Pi 127.0.0.1:32400

sudo systemctl stop plexmediaserver.service # Stop Plex
sudo systemctl start plexlistenandwol.service # start this app
```

## Checking the log
It's in the app.log file.

## TO DO
- Pushbullet notifcation when action takes place and/or other logging
- Check if PC active and if it is, don't even open sockets
