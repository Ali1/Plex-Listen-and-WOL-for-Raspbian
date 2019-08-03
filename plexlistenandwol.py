#!/usr/bin/env python2
# https://github.com/Ali1/Plex-Listen-and-WOL-for-Raspbian/
# Ali: The script opens port 32400 acting as Plex for most of the day and starts Plex once a day just to keep the raspberry pi server activated on the Plex account

# sudo systemctl status plexlistenandwol.service to check status once running
import os
import datetime
import subprocess
import logging
import socket
from sys import exit
import argparse
from subprocess import Popen, PIPE
from wol import * # ali
import time
class Object(object):
    pass # for conf
conf=Object()
conf.mac = '60:45:cb:82:06:d0' # ali

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ])

logging.basicConfig(filename='app.log', filemode='w', format='%(nprintame)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def main():
    logging.info('Starting app');
    # Check for root
    if os.geteuid():
        exit('[-] Please run as root')

    # creating a socket object
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    # get local Host machine name
    host = ''
    port = 32400
    
    logging.info("Attempting to bind port");
    try:
        s.bind((host, port))
    except socket.error as e:
        if e.errno == 98:
            logging.warning("Port is already in use. Shutting Plex and trying in 45 secs")
            os.system("sudo service plexmediaserver stop")
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
            time.sleep(45)
            logging.info("Now try again")
            try:
                s.bind((host, port))
            except:
                logging.error("Did not work, trying to kill the process")
                os.system("pid=$(lsof -i:32400 -t); kill -TERM $pid || kill -KILL $pid")
                time.sleep(45)
                logging.info("Ok, last try")
                s.bind((host, port))
        else:
            raise

    s.settimeout(45);
    s.listen(1) # up to 2 connections
    logging.info("Binded successfully");
    first_run=1 # to prevent the Plex shutdown process from occurring right away
    while True:
        now = datetime.datetime.now()
        if now.hour==9 and now.minute==49 and first_run==0:
            logger.info("shutting sockets down to prepare for plex");
            try:
                s.shutdown(socket.SHUT_RDWR)
            except:
                pass
            s.close()
            time.sleep(60)
            logger.info("starting plex for 60 seconds");
            os.system("sudo service plexmediaserver start")
            time.sleep(60)
            logger.info("stopping plex");
            os.system("sudo service plexmediaserver stop")
            time.sleep(60)
            logger.info("re-opening sockets")
            s = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
            try:
                s.bind((host, port))
            except:
                logger.error("Did not work, trying to kill processes hogging port 32400")
                os.system("pid=$(lsof -i:32400 -t); kill -TERM $pid || kill -KILL $pid")
                time.sleep(45)
                logger.info("Ok, last try")
                s.bind((host, port))
            s.settimeout(45);
            s.listen(1) # up to 2 connections
        first_run=0
        try:
            clientSocket, addr = s.accept()
        except socket.timeout:
            pass
        except:
            raise
        else:
            logger.info("got a connection from %s" % str(addr))
            clientSocket.close()
            wake_on_lan(conf.mac)
            time.sleep(1)
            wake_on_lan(conf.mac)
            time.sleep(1)
            wake_on_lan(conf.mac)
            time.sleep(1)
            wake_on_lan(conf.mac)
            time.sleep(1)
            wake_on_lan(conf.mac)
            time.sleep(1)
            wake_on_lan(conf.mac)
            time.sleep(1)
            logging.info('sent 6 WOLs to ' + conf.mac + '. Now sleeping');
            time.sleep(10)
    logger.info("dying")


if __name__ == "__main__":
   main()

