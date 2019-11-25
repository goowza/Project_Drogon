#!/usr/bin/env python
# coding: utf-8

import can
import os
import time
from GPSReader import *
from Xbee import *

MOVE_LEFT = "0"
MOVE_RIGHT = "1"
MOVE_FORWARD = "2"
STOP = "3"
SHARE_LOCATION = "4"
STOP_SHARING_LOCATION = "5"
SERIAL_DELIMITER = ":"

MCM = 0x010

# Steering angle = 0
NULL_STEER = 50 | 0x80
# Stop rear wheels
STOP_MOTORS = 0 & ~0x80

class Car(threading.Thread):
	def __init__(self, id, serial_port_gps, serial_port_xbee, lock):
		threading.Thread.__init__(self)
		self.lock = lock
		self.lock.acquire()
		self.id = id
		self.gps = GPSReader(serial_port_gps)
		self.xbee = Xbee(serial_port_xbee)
		
		self.command = -1
		self.move_cmd = STOP_MOTORS
		self.steer_cmd = NULL_STEER
		self.share_location = False
		
		# Setup CAN communication bus
		print('Bring up CAN0....')
		os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
		time.sleep(0.1)
		
		try:
			self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
		except OSError:
			print('Cannot find PiCAN board.')
			exit()
		
	def sendCANCommand(self):
		# Send msg on CAN to move rear wheels
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, 0, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		# Send msg on CAN to move front wheels
		msg = can.Message(arbitration_id=MCM, data=[0, 0, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		
	
	def computeCommand(self):
		temp = self.xbee.readCommand()
		if temp != -1:
			self.command = temp

		if self.command == MOVE_LEFT:
			self.steer_cmd = 0 | 0x80
			self.move_cmd = 50 & ~0x80
			print("TURNING LEFT")
		elif self.command == MOVE_RIGHT:
			self.steer_cmd = 100 | 0x80
			self.move_cmd = 0 & ~0x80
			print("TURNING RIGHT")
		elif self.command == MOVE_FORWARD:
			self.move_cmd = 75 | 0x80
			self.steer_cmd = 50 | 0x80
			print("GOING FORWARD")
		elif self.command == STOP:
			self.move_cmd = 50 | 0x80
			self.steer_cmd = 50 | 0x80
			print("STOP")
		elif self.command == SHARE_LOCATION:
			self.share_location = True
			print("SHARING_LOCATION")
		elif self.command == STOP_SHARING_LOCATION:
			self.share_location = False
			print("STOPPED SHARING LOCATION")
		else:
			pass
			#print("Unknown command : {}".format(self.command))
			
	def buildMessage(self):
		msg = str(self.id)+":"+str(self.command)
		if self.command == SHARE_LOCATION:
			msg += ":"+str(self.gps.latitude)+":"+str(self.gps.longitude)
		
		return msg
	
	def run(self):
		global message_emis
		while 1:
			self.computeCommand()
			self.sendCANCommand()
			if self.share_location:
				self.gps.update()
				msg_to_write = self.buildMessage()
				print("Broadcasting {}".format(msg_to_write))
				self.xbee.write(msg_to_write)
				self.lock.release()
				self.lock.acquire()
		
