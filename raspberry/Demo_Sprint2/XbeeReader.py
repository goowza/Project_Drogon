#!/usr/bin/env python
# coding: utf-8

import serial

XBEE_SERIAL_BAUDRATE = 9600
SERIAL_DELIMITER = ":"

class Xbee():
	def __init__(self, serial_port):
		self.serial_port = serial_port
		
		# Creates serial link with XBee module
		try:
			self.ser = serial.Serial(
				port=self.serial_port,
				baudrate=XBEE_SERIAL_BAUDRATE,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS,
				timeout=1
			)
		except OSError:
			print("Error creating the serial link")
			exit()
		
	def readCommand(self):
		command = -1
		message_read = self.ser.readline().decode()
		print(message_read)
		message_read = message_read.split(SERIAL_DELIMITER)
		if len(message_read) > 1:
			command = message_read[1]
		return command
		
	def write(self, msg):
		if msg != "":
			self.ser.write(str.encode(msg))

if __name__=="__main__":
	myXbee = Xbee("/dev/ttyUSB0")
	while True:
		myXbee.readCommand()
