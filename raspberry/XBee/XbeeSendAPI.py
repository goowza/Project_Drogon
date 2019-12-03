#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
import argparse
from xbee import XBee

BROADCAST_ADDR_16 = b'\xFF\xFF'
CAR_ID = "HL118"
COMMAND_ID = "0" 

class XbeeSenderAPI():
    def __init__(self, serial_port):
        try:
            self.serial_port = serial.Serial(serial_port, 9600)
            self.xbee = XBee(self.serial_port)
        except:
            print("Error creating serial link")
            exit()
            
    def sendMessageBroadcast(self, data):
        msg = ""
        msg = CAR_ID + ":" + COMMAND_ID + ":" + data
        print("Broadcasting {}".format(msg), end='\r')
        # Definition des arguments de send() dans Xbee.ieee.Xbee (ctrl + click)
        self.xbee.send(cmd='tx',dest_addr=BROADCAST_ADDR_16,data=msg)
        
# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
args = parser.parse_args()

myXbee = XbeeSenderAPI(args.serial_port)

while True:
    try:
        myXbee.sendMessageBroadcast("HEY")
        time.sleep(0.5)
    except KeyboardInterrupt:
        break

myXbee.serial_port.close()

