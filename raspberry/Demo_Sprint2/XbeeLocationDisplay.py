#!/usr/bin/env python
# coding: utf-8
import serial
import argparse

SHARE_LOCATION = 5

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
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
	msg=ser.readline().strip().decode().split(":")
	# Convert it to a string
	lat = 0
	long = 0
	if len(msg) > 1:
		if msg[1] == SHARE_LOCATION:
			lat = msg[2]
			long = msg[3]
	print("Latitude : {} | Longitude : {}".format(lat, long))
