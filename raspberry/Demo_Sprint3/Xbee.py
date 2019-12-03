#!/usr/bin/env python
# coding: utf-8

import serial
from xbee import XBee
import time

XBEE_SERIAL_BAUDRATE = 9600
SERIAL_DELIMITER = ":"


class Xbee():
	def __init__(self, serial_port):
		self.serial_port = serial_port
		
		# Creates serial link with XBee module
		try:
                    serial_port = serial.Serial(serial_port, XBEE_SERIAL_BAUDRATE)
                    xbee = XBee(serial_port, callback=lambda:readCommand(self))
		except OSError:
			print("Error creating the serial link")
			exit()
	
	def readCommand(self, data):
		command = -1
		message_read = data["rd_data"].decode()
		print(message_read)
		message_read = message_read.split(SERIAL_DELIMITER)
		if len(message_read) > 1:
			command = message_read[1]
		return command
	
	def write(self, msg):
		print("Location : {}".format(msg))
		if msg != "":
			self.ser.write(str.encode(msg))


if __name__ == "__main__":
    myXbee = Xbee("/dev/ttyUSB1")
    while True:
        try:
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
		
