#!/usr/bin/env python
import time
import serial
import argparse

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
    # Send user input over XBee
    steer_command = input("Send command (0 = left | 1 = right)")
    ser.write(str.encode(steer_command))
    time.sleep(1)
