#!/usr/bin/env python
 # wol.py
 #
 # This module is from ActiveState Code Recipes:
 # http://code.activestate.com/recipes/358449-wake-on-lan/
 # and patched for Python 3 with:
 # http://code.activestate.com/recipes/577609-wake-on-lan-for-python-3/
 #
 # Example:
 # import wol
 # wol.wake_on_lan('70:F3:95:15:00:B5')
 #
import socket
import struct

def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep,'')
    else:
        raise ValueError('Incorrect MAC address format')


    # Pad the synchronization stream
    data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += struct.pack('B', int(data[i: i + 2], 16))

    # Broadcast it to the LAN
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('255.255.255.255',7))
