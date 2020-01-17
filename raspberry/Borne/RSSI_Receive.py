#!/usr/bin/env python3
# coding: utf-8

import serial
import time
from xbee import XBee
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

COOLDOWN = 0
TRESHOLD_INCOMING = 1
TRESHOLD_LEAVING = -1
TRESHOLD_CLOSE = 65
SIZE_BUFFER = 5
TIMEOUT = 2

class XbeeDir():
	def __init__(self, serial_port):
		try:
			self.serial_port = serial.Serial(serial_port, 9600)
			self.xbee = XBee(self.serial_port, callback=self.data_callback)
		except:
			print("Error creating serial link")
			exit()
		self.direction = "NONE"
		self.position = "LOIN"
		self.RSSI_buffer = deque(SIZE_BUFFER*[0], SIZE_BUFFER)
		self.LED_buffer = deque(3*[0], 3)
		self.previous_rcv = 0
		self.counter = 0
		self.sending_pics_flag = False
		self.bollard_command = "OFF"
	
	def data_callback(self, data):
		#print(data)
		self.counter += 1
		now = time.time()
		if (now - self.previous_rcv) >= COOLDOWN:
			ID = data["rf_data"].decode().split(":")[0]
			command = data["rf_data"].decode().split(":")[1]
			if ID == "HL118":
				self.RSSI_buffer.appendleft(ord(data["rssi"].decode()))
				self.compute_bollard_command()
			if command == "1":
				self.sending_pics_flag = True
			else:
				self.sending_pics_flag = False
			self.previous_rcv = now
			
	def compute_direction(self):
		if not 0 in self.RSSI_buffer:
			mean_gradient = np.mean(np.gradient(self.RSSI_buffer))
			
			if mean_gradient > TRESHOLD_INCOMING:
				self.direction = "INCOMING"
			elif mean_gradient < TRESHOLD_LEAVING:
				self.direction = "LEAVING"
			else:
				self.direction = "NONE"
			
			#print("Dir : {} ({}) ({})".format(self.direction, mean_gradient, np.mean(self.RSSI_buffer)))
	
	def connexion_lost(self): 
                now = time.time()
                if now - self.previous_rcv >= TIMEOUT:
                    print("Connexion lost", end="\r")
                    return True
                else:
                    return False
                
	def compute_position(self):
		if not 0 in self.RSSI_buffer:
			mean_RSSI = np.mean(self.RSSI_buffer)
			
			if mean_RSSI < TRESHOLD_CLOSE:
				self.position = "PRES"
			else:
				self.position = "LOIN"
			
			print("Pos : {} ({})".format(self.position, mean_RSSI), end="\r")
			
	def compute_bollard_command(self):
		self.compute_position()
		self.compute_direction()
		
		if self.position == "PRES":
			self.LED_buffer.appendleft(1)
			self.bollard_command = "ON"
		else:
			self.LED_buffer.appendleft(0)
			self.bollard_command = "OFF"
		#if not 0 in self.LED_buffer:
		#	self.bollard_command = "ON"
		#else:
		#	self.bollard_command = "OFF"
		#print(self.bollard_command + " ", end="\r")
			
if __name__ == "__main__":
	
	myXbeeDir = XbeeDir("/dev/ttyUSB0")
	
	while True:
		try:
			time.sleep(0.0001)
		except KeyboardInterrupt:
			break
	
	myXbeeDir.xbee.halt()
	myXbeeDir.serial_port.close()
