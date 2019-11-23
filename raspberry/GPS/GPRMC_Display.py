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

	# Read message received from GPS
	raw_data=ser.readline().strip()
    
	raw_data = raw_data.decode()
	if raw_data != "":
		# GPRMC is the part of the NMEA sentence we need
		if "$GPRMC" in raw_data:
			# Format : $GPRMC,22056,A,5133.82,N,00042.24,W,173.8 ...
			raw_data = raw_data.split(",")
			if raw_data[2] == "A":
				latitude = float(raw_data[3]) / 10.0
				longitude = float(raw_data[5]) / 10.0
			else:
				latitude = -1
				longitude = -1
			print("Lat : {} | Long : {}".format(latitude,longitude), end="\r")
	else:
		print("No GPS data available")
