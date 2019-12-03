#!/usr/bin/python3
# -*-coding:UTF-8 -*

import serial

GPS_SERIAL_BAUDRATE = 9600


class GPSReader():
	def __init__(self, serial_port):
		self.serial_port = serial_port
		self.latitude = -1
		self.longitude = -1
		
		# Creates serial link with GPS
		try:
			self.ser = serial.Serial(
				port=self.serial_port,
				baudrate=GPS_SERIAL_BAUDRATE,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS,
				timeout=1
			)
		except:
			print("Error creating the serial link")
	
	# Update latitude and longitude values.
	# This function needs to be called periodically
	def update(self):
		# Read message received from GPS
		raw_data = self.ser.readline().strip()
		
		raw_data = raw_data.decode()
		if raw_data != "":
			# GPRMC is the part of the NMEA sentence we need
			if "$GPRMC" in raw_data:
				# Format : $GPRMC,22056,A,5133.82,N,00042.24,W,173.8 ...
				raw_data = raw_data.split(",")
				if raw_data[2] == "A":
					self.latitude = float(raw_data[3]) / 10.0
					self.longitude = float(raw_data[5]) / 10.0
				else:
					self.latitude = -1
					self.longitude = -1
		else:
			print("No GPS data available")