#!/usr/bin/env python3
# coding: utf-8

import serial
import time
from xbee import XBee
from constants import *
import socket
import threading
from queue import Queue
from Driver import Driver
import pygame
from pygame.locals import *
import os

"""
EmergencyCar class contains :
	- 1 Xbee to send messages to other vehicle / bollards
	- 1 connection to the server to receive info
	- 1 message queue to stack messages sent by server
	- 1 driver allowing it to send commands over the CAN bus
	- 1 pygame window to get unbuffered keyboard entries
"""
class EmergencyCar():
	def __init__(self, serial_port):
		try:
			self.serial_port = serial.Serial(serial_port, 9600)
			self.xbee = XBee(self.serial_port)
			pass
		except:
			print("Error creating serial link")
			exit()
			
		#self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.sock.connect((HOST, PORT))
		#answer = self.sock.recv(4096).decode(encoding="utf-8")
		#print("answer = {}".format(answer))
		# Envoyer message au serveur pour dire que c'est l'ambulance
		self.msg_queue = Queue()
		
		self.driver = Driver()
		
		pygame.init()
		self.screen = pygame.display.set_mode((50, 50))
		pygame.display.set_caption("VROUM")
		self.screen.fill((159, 182, 205))
		pygame.display.update()
		
	def sendXbeeMessage(self, data, dest_addr=BROADCAST_ADDR_16):
		self.xbee.send(cmd='tx', dest_addr=dest_addr, data=data)
		
	def buildXbeeMessage(self, id_vehicle, command):
		msg = id_vehicle + SERIAL_DELIMITER + command
		return msg
	
	def readServerThread(self):
		while True:
			try:
				answer = self.sock.recv(4096).decode(encoding="utf-8")
				self.msg_queue.put(answer)
			except KeyboardInterrupt:
				break
		self.sock.close()
		
	def sendXbeeMessagesThread(self):
		while True:
			try:
				self.sendXbeeMessage(self.buildXbeeMessage(EMERGENCY_VEHICLE_ID, EMERGENCY_VEHICLE_INCOMING))
				time.sleep(1/SEND_FREQUENCY)
			except KeyboardInterrupt:
				break
		self.xbee.halt()
		self.serial_port.close()
		
	def driveCarThread(self):
		done = False
		while not done:
			try:
				# Set focus on pygame window
				os.system("wmctrl -a VROUM")
				pygame.display.update()
				pygame.event.pump()
				keys = pygame.key.get_pressed()
				
				if keys[K_a]:
					self.driver.accelerate()
					pass
				if keys[K_e]:
					self.driver.decelerate()
					pass
				if keys[K_z] and keys[K_d]:
					self.driver.moveForwardRight()
					pass
				elif keys[K_z] and keys[K_q]:
					self.driver.moveForwardLeft()
					pass
				elif keys[K_z]:
					self.driver.moveForward()
					pass
				elif keys[K_s] and keys[K_d]:
					self.driver.moveBackwardRight()
					pass
				elif keys[K_s] and keys[K_q]:
					self.driver.moveBackwardLeft()
					pass
				elif keys[K_s]:
					self.driver.moveBackward()
					pass
				elif keys[K_q]:
					self.driver.turnLeft()
					pass
				elif keys[K_d]:
					self.driver.turnRight()
					pass
				elif keys[K_ESCAPE]:
					done = True
				else:
					self.driver.stop()
					pass
				time.sleep(0.1)
			except KeyboardInterrupt:
				break
		pygame.quit()
				
	def run(self):
		#print("Starting server thread...")
		#threading.Thread(target=self.readServerThread).start()
		print("Starting xbee thread...")
		threading.Thread(target=self.sendXbeeMessagesThread).start()
		print("Starting keyboard thread...")
		threading.Thread(target=self.driveCarThread).start()
		while True:
			try:
				if not self.msg_queue.empty():
					msg = self.msg_queue.get()
					print("Received {} from server".format(msg))
			except KeyboardInterrupt:
				break
		
		
if __name__ == "__main__":
	ambulance = EmergencyCar("/dev/ttyUSB0")
	ambulance.run()
