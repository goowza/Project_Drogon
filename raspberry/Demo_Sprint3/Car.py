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
import socket, sys, threading

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

XBEE_SERIAL_BAUDRATE = 9600
SERIAL_DELIMITER = ":"

class Xbee():
    def __init__(self, serial_port):
        # Creates serial link with XBee module
        try:
            serial_port = serial.Serial(serial_port, XBEE_SERIAL_BAUDRATE)
            self.xbee = XBee(serial_port, callback=self.readCommand)
            self.command = -1
            global lockXbee
            self.lock= lockXbee
        except OSError:
            print("Error creating the serial link")
            exit()
            
    def readCommand(self,data):
        self.lock.acquire()
        message_read = data["rf_data"].decode()
        print(message_read)
        message_read = message_read.split(SERIAL_DELIMITER)
        if len(message_read) > 1:
            self.command = message_read[1]
        self.lock.release()

    def write(self, msg):
        print("Location : {}".format(msg))
        if msg != "":
            self.ser.write(str.encode(msg))

class ThreadReception(threading.Thread):
   """objet thread gerant la reception des messages"""
   def __init__(self, conn):
       threading.Thread.__init__(self)
       self.connexion = conn           # ref. du socket de connexion
        
   def run(self):
       while 1:
           message_recu = self.connexion.recv(1024)
           print("*" + message_recu.decode('utf-8') + "*")
           if message_recu =='' or message_recu.upper() == "FIN":
               break
       # Le thread <reception> se termine ici.
       # On force la fermeture du thread <emission> :
       th_E._Thread__stop()
       print("Client arrete. Connexion interrompue.")
       self.connexion.close()
   
class ThreadEmission(threading.Thread):
    """objet thread gerant l'emission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        global lock
        self.lock = lock
        self.connexion = conn           # ref. du socket de connexion
        
    def run(self):
        global message_emis
        while 1:
            self.lock.acquire()
            self.connexion.send(message_emis.encode('utf-8'))
            self.lock.release()
            time.sleep(0.1)

class Car(Thread):
	def __init__(self, id, serial_port_gps, serial_port_xbee):
		Thread.__init__(self)
		global lockXbee
		self.lockXbee = lockXbee
		global lock
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
		#print("CAN : {} | {}".format(self.move_cmd, self.steer_cmd))
		# Send msg on CAN to move rear wheels
		if self.xbee.command != -1:
			msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
			self.bus.send(msg)	
		#time.sleep(0.1)
		# Send msg on CAN to move front wheels
		#msg = can.Message(arbitration_id=MCM, data=[0, 0, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
		#self.bus.send(msg)
		self.xbee.command=-1
		self.lockXbee.release()	
		
	
	def computeCommand(self):
		self.lockXbee.acquire()
		temp = self.xbee.command
		print(temp)	
		if temp == MOVE_LEFT:
			self.steer_cmd = 0 | 0x80
			self.move_cmd = 50 & ~0x80
			print("TURNING LEFT")
		elif temp == MOVE_RIGHT:
			self.steer_cmd = 100 | 0x80
			self.move_cmd = 0 & ~0x80
			print("TURNING RIGHT")
		elif temp == MOVE_FORWARD:
			self.move_cmd = 75 | 0x80
			self.steer_cmd = 50 | 0x80
			print("GOING FORWARD")
		elif temp == STOP:
			self.move_cmd = 50 | 0x80
			self.steer_cmd = 50 | 0x80
			print("STOP")
		elif temp == SHARE_LOCATION:
			self.share_location = True
			print("SHARING_LOCATION")
		elif temp == STOP_SHARING_LOCATION:
			self.share_location = False
			print("STOPPED SHARING LOCATION")
		else:
			pass
			#print("Unknown command : {}".format(self.command))
			
	def buildMessage(self):
		msg = str(self.id)+":"+str(self.command)
		if self.xbee.command == SHARE_LOCATION:
			msg += ":"+str(self.gps.latitude)+":"+str(self.gps.longitude)
		
		return msg
	
	def run(self):
		global message_emis
		start = time.time() + SERVER_SEND_COOLDOWN
		while 1:
			self.computeCommand()
			#if self.xbee.command != -1:
			self.sendCANCommand()
			time.sleep(0.1)
			if self.share_location:
				self.gps.update()
				#msg_to_write = self.buildMessage()
				#print("Broadcasting {}".format(msg_to_write))
				#self.xbee.write(msg_to_write)
				message_emis=encodage("pieton", "accident", "105.85:43.45")

				
				#if time.time() - start > SERVER_SEND_COOLDOWN:
				self.lock.release()
				#print("Envoi de localisation")
				self.lock.acquire()
				start = time.time()



   
  


# Manage arguments used when launching the script

if __name__=="__main__":
	message_emis=""
	
	# Connexion with server
	host = '10.105.1.85'
	port = 40002
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	parser = argparse.ArgumentParser()
	parser.add_argument("serial_port_gps", help="serial port of GPS")
	parser.add_argument("serial_port_xbee", help="serial port of xbee")
	args = parser.parse_args()

	#connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		print("Connecting to server...")
		connexion.connect((host, port))
	except socket.error:
		print("Connection with server failed")
		sys.exit()
	print("Connection with server established")

	# Shared variables
	lock = threading.Lock()
	lockXbee = threading.Lock()
	
	# Threads declaration
	thread_car = Car(42, args.serial_port_gps, args.serial_port_xbee)
	th_E = ThreadEmission(connexion)
	th_R = ThreadReception(connexion)
	
	thread_car.start()
	th_E.start()
	th_R.start()
	thread_car.join()
	th_E.join()
	th_R.join()

	connexion.close()
