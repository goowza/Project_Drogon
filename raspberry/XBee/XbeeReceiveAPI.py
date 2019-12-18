#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
import argparse
from xbee import XBee
import RPi.GPIO as GPIO

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
args = parser.parse_args()

# Parametre les GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Gyro = 13

GPIO.setup(Gyro, GPIO.OUT)
GPIO.output(Gyro, GPIO.LOW)

# Compte le nombre de messages recus
count = 0

prev_rssi = 100
pres = False

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
    global prev_rssi
    global pres
    
    try:
        ID = data["rf_data"].decode().split(":")[0]
        if ID == "HL118":
            RSSI = ord(data["rssi"].decode())
            #print("RSSI : {} ({})".format(RSSI, count), end = '\r')
            if not pres and RSSI < 60 and prev_rssi < 60:
                #GPIO.output(Gyro, GPIO.HIGH)
                pres = True
                pass
            elif pres and RSSI > 65 and prev_rssi > 65:
                #GPIO.output(Gyro, GPIO.LOW)
                pres = False
                pass
            print("{} ({})".format(pres,RSSI))
            prev_rssi = RSSI
                
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
