#!/usr/bin/env python3
# coding: utf-8
import os
import time

import can
from constants import *

class Driver():
	def __init__(self):
		# Setup CAN communication bus
		print('Bring up CAN0....')
		os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
		time.sleep(0.1)
		
		self.move_cmd = 50 | 0x80
		self.turn_cmd = 50 | 0x80
		
		self.speed = 0
		
		try:
			self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
		except OSError:
			print('Cannot find PiCAN board.')
			exit()
	def moveForward(self):
		self.move_cmd = (50 + self.speed) | 0x80
		self.turn_cmd = 50 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE FW")
	def moveForwardRight(self):
		self.move_cmd = (50 + self.speed) | 0x80
		self.turn_cmd = 100 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE FW RIGHT")
	def moveForwardLeft(self):
		self.move_cmd = (50 + self.speed) | 0x80
		self.turn_cmd = 0 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE FW LEFT")
	def moveBackward(self):
		self.move_cmd = (50 - self.speed) | 0x80
		self.turn_cmd = 50 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE BW")
	def moveBackwardRight(self):
		self.move_cmd = (50 - self.speed) | 0x80
		self.turn_cmd = 100 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE BW RIGHT")
	def moveBackwardLeft(self):
		self.move_cmd = (50 - self.speed) | 0x80
		self.turn_cmd = 0 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("MOVE BW LEFT")
	def turnLeft(self):
		self.move_cmd = 50 | 0x80
		self.turn_cmd = 0 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("TURN LEFT")
		pass
	def turnRight(self):
		self.move_cmd = 50 | 0x80
		self.turn_cmd = 100 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[0, 0, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		print("TURN RIGHT")
		pass
	
	def stop(self):
		self.move_cmd = 50 | 0x80
		self.turn_cmd = 50 | 0x80
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.turn_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		
	def accelerate(self):
		self.speed += SPEED_INCR
		if self.speed > 50:
			self.speed = 50
	
	def decelerate(self):
		self.speed -= SPEED_INCR
		if self.speed < 0:
			self.speed = 0
