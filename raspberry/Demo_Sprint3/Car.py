#!/usr/bin/env python
# coding: utf-8

import can
import os
import time
from GPSReader import *
from Xbee import *
from Encodage import *
from threading import Thread, Lock
from queue import Queue
import argparse
from xbee import XBee

MOVE_LEFT = "0"
MOVE_RIGHT = "1"
MOVE_FORWARD = "2"
STOP = "3"
SHARE_LOCATION = "4"
STOP_SHARING_LOCATION = "5"
SERIAL_DELIMITER = ":"

MCM = 0x010
SERVER_SEND_COOLDOWN = 500

# Steering angle = 0
NULL_STEER = 50 | 0x80
# Stop rear wheels
STOP_MOTORS = 0 & ~0x80

#global message_emis

class Car(Thread):
	def __init__(self, id, serial_port_gps, serial_port_xbee, lock, queue):
		Thread.__init__(self)
		self.lock = lock
		self.lock.acquire()
		self.id = id
		self.gps = GPSReader(serial_port_gps)
		self.xbee = Xbee(serial_port_xbee)
		self.queue = queue
		
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
		#print("CAN : {} | {}".format(self.move_cmd, self.steer_cmd))
		# Send msg on CAN to move rear wheels
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.bus.send(msg)
		#time.sleep(0.1)
		# Send msg on CAN to move front wheels
		#msg = can.Message(arbitration_id=MCM, data=[0, 0, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
		#self.bus.send(msg)
		
	
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
		start = time.time() + SERVER_SEND_COOLDOWN
		while 1:
			self.computeCommand()
			self.sendCANCommand()
			if self.share_location:
				self.gps.update()
				msg_to_write = self.buildMessage()
				print("Broadcasting {}".format(msg_to_write))
				self.xbee.write(msg_to_write)
				message_emis=encodage("pieton", "accident", "105.85:43.45")
				self.queue.put(message_emis)
				
				if time() - start > SERVER_SEND_COOLDOWN:
					self.lock.release()
					self.lock.acquire()
					start = time.time()

if __name__=="__main__":
    # Manage arguments used when launching the script
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port_gps", help="serial port of GPS")
    parser.add_argument("serial_port_xbee", help="serial port of xbee")
    args = parser.parse_args()
    lock = Lock()
    queue = Queue()
    myCar = Car(12,args.serial_port_gps, args.serial_port_xbee, lock, queue)
    myCar.run()
