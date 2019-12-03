#!/usr/bin/env python
# coding: utf-8
import can
import serial
import os
import time
import argparse

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010

MOVE_LEFT = "0"
MOVE_RIGHT = "1"
MOVE_FORWARD = "2"

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

# Steering angle = 0
steer_cmd = 50 | 0x80
# Stop rear wheels
move_cmd = 0 & ~0x80


# Setup CAN communication bus
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()
while 1:
    # Read message received on the XBee
    msg_xbee=ser.readline().strip()

    # Convert it to a string
    msg_xbee = msg_xbee.decode("utf-8")

    if msg_xbee != "":
        print(msg_xbee)
    # Turn front wheels to the left and stop rear wheels
    if msg_xbee == MOVE_LEFT:
        steer_cmd = 0 | 0x80
        move_cmd = 50 & ~0x80
        print("TURNING LEFT")
    # Turn front wheels to the right and stop rear wheels
    elif msg_xbee == MOVE_RIGHT:
        steer_cmd = 100 | 0x80
        move_cmd = 0 & ~0x80
        print("TURNING RIGHT")
    # Set front wheels at 0° and move rear wheels forward
    elif msg_xbee == MOVE_FORWARD:
        move_cmd = 75 | 0x80
        steer_cmd = 50 | 0x80
        print("GOING FORWARD")
    elif msg_xbee == "":
        pass
    else:
        print("Unknown message : {}".format(msg_xbee))

    # Send msg on the CAN bus
    msg = can.Message(arbitration_id=MCM, data=[move_cmd, move_cmd, steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
    bus.send(msg)
