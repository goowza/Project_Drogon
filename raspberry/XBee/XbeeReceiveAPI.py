#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
import argparse
from xbee import XBee

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
args = parser.parse_args()

# Compte le nombre de messages recus
count = 0

def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    data = dictionnaire avec les champs :
    {'id': 'rx', 'source_addr': b'\x00\x04', 'rssi': b'>', 'options': b'\x02', 'rf_data': b'Hey'}
    """
    global count
    count = count + 1
    try:
        print("RSSI value : {} ({})".format(ord(data["rssi"].decode()), count), end="\r")
    except:
        print("GNEUGNEU")

try:
    serial_port = serial.Serial(args.serial_port, 9600)
    xbee = XBee(serial_port, callback=print_data)
except:
    print("Error creating serial link")
    exit()

while True:
    try:
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

print("\n")
xbee.halt()
serial_port.close()
