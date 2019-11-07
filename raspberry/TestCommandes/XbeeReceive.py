#!/usr/bin/env python
# coding: utf-8
import can
import serial
import os
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010

MOVE_LEFT = "0"
MOVE_RIGHT = "1"

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             
 )
counter=0

# Steering angle = 0
steer_cmd = 50 | 0x80

while 1:
    # Setup CAN communication bus
    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    # Read message received on the XBee
    msg_xbee=ser.readline().strip()

    # Convert it to a string
    msg_xbee = msg_xbee.decode("utf-8")

    # Compute steering command based on the xbee msg
    if msg_xbee == MOVE_LEFT:
        steer_cmd = 0 | 0x80
        print("turning left")
    elif msg_xbee == MOVE_RIGHT:
        steer_cmd = 100 | 0x80
        print("turning right")
    else:
        print("Unknown message : {}".format(msg_xbee))

    # Send msg on the CAN bus
    msg = can.Message(arbitration_id=MCM, data=[0, 0, steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
    #bus.send(msg)