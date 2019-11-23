#!/usr/bin/env python
# coding: utf-8
import serial
import os
import time
import argparse

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port


# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of GPS")
args = parser.parse_args()

# Creates serial link with XBee module
try:
    ser = serial.Serial(
        port=args.serial_port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except:
    print("Error creating the serial link")

while 1:

    # Read message received on the XBee
    raw_data=ser.readline().strip()
    
    raw_data = raw_data.decode()
    
    if "$GPRMC" in raw_data:
        print(raw_data)

