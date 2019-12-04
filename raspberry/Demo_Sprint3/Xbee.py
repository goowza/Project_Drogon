#!/usr/bin/env python
# coding: utf-8

import serial
from xbee import XBee
import time
from functools import partial
from constants import *

class Xbee():
    def __init__(self, serial_port):
        # Creates serial link with XBee module
        try:
            serial_port = serial.Serial(serial_port, XBEE_SERIAL_BAUDRATE)
            self.xbee = XBee(serial_port, callback=self.readCommand)
            self.command = -1
        except OSError:
            print("Error creating the serial link")
            exit()
            
    def readCommand(self, data):
        message_read = data["rf_data"].decode()
        print(message_read)
        message_read = message_read.split(SERIAL_DELIMITER)
        if len(message_read) > 1:
            self.command = message_read[1]

    def sendMessageBroadcast(self, command, data):
        msg_to_send = CAR_ID + ":" + command + ":" + data
        print("Broadcasting {}".format(msg_to_send), end='\r')
        # Definition des arguments de send() dans Xbee.ieee.Xbee (ctrl + click)
        self.xbee.send(cmd='tx', dest_addr=BROADCAST_ADDR_16, data=msg_to_send)


if __name__ == "__main__":
    myXbee = Xbee("/dev/ttyUSB0")
    while True:
        try:
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
		
