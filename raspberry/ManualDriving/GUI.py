#!/usr/bin/python3
# -*-coding:UTF-8 -*

from tkinter import *
import os
import time
import can
import serial
import argparse

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

STEER_CENTER = 50 | 0x80
STEER_LEFT = 0 | 0x80
STEER_RIGHT = 100 | 0x80
STOP_MOVE = 0
MOVE_INCR = 10
STEER_INCR = 10

class GUI():

	def __init__(self):

		self.bus = 0
		self.move_cmd = STOP_MOVE
		self.steer_cmd = STEER_CENTER
		#self.setupCAN()
		
		######################################################################
		############################# Main Window ############################
		######################################################################
		
		self.root = Tk()
		self.root.title("Manual Driver")
		
		# Activate bindings
		self.root.bind('<Right>', self.moveRight)
		self.root.bind('<Left>', self.moveLeft)
		self.root.bind('<Up>', self.moveForward)
		self.root.bind('<Down>', self.moveBackward)
		
		######################################################################
		######################## Widgets declarations ########################
		######################################################################
		
		# Buttons
		self.forward_button = Button(self.root, text="FORWARD", command=self.moveForwardButton, font=("Courier", 12, "bold"), width=10)
		self.backward_button = Button(self.root, text="BACKWARD", command=self.moveBackwardButton, font=("Courier", 12, "bold"), width=10)
		self.left_button = Button(self.root, text="LEFT", command=self.moveLeftButton, font=("Courier", 12, "bold"), width=10)
		self.right_button = Button(self.root, text="RIGHT", command=self.moveRightButton, font=("Courier", 12, "bold"), width=10)
		self.stop_button = Button(self.root, text="STOP", command=self.stop, font=("Courier", 12, "bold"), width=10)
	
		######################################################################
		############################ Positionning ############################
		######################################################################
		
		self.forward_button.grid(column=1, row=0, padx=0, pady=0)
		self.left_button.grid(column=0, row=1, padx=0, pady=0)
		self.stop_button.grid(column=1, row=1, padx=0, pady=0)
		self.right_button.grid(column=2, row=1, padx=0, pady=0)
		self.backward_button.grid(column=1, row=2, padx=0, pady=0)
	
	# Starts and Opens CAN link
	def setupCAN(self):
		# Setup CAN communication bus
		print('Bring up CAN0....')
		os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
		time.sleep(0.1)
		
		try:
			self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
		except OSError:
			print('Cannot find PiCAN board.')
			exit()
			
	def moveForward(self, event):
		self.move_cmd = self.move_cmd + MOVE_INCR | 0x80
		if (self.move_cmd & ~0x80) > 100:
			self.move_cmd = 100 | 0x80
		
		self.sendCommandCAN()
	
	def moveBackward(self, event):
		if (self.move_cmd & ~0x80) <= 10:
			self.move_cmd = 0 | 0x80
		else:
			self.move_cmd = self.move_cmd - MOVE_INCR | 0x80
		
		self.sendCommandCAN()
	
	def moveLeft(self, event):
		if self.steer_cmd & ~0x80 <= 10:
			self.steer_cmd = 0 | 0x80
		else:
			self.steer_cmd = self.steer_cmd - STEER_INCR | 0x80
		
		self.sendCommandCAN()
	
	def moveRight(self, event):
		self.steer_cmd = self.steer_cmd + STEER_INCR | 0x80
		if self.steer_cmd & ~0x80 > 100:
			self.steer_cmd = 100 | 0x80
		
		self.sendCommandCAN()
	
	# Stop rear wheels and center front wheels
	def stop(self):
		self.steer_cmd = STEER_CENTER
		self.move_cmd = STOP_MOVE
		self.sendCommandCAN()
	
	# Send 1 message on the CAN bus
	def sendCommandCAN(self):
		msg = can.Message(arbitration_id=MCM, data=[self.move_cmd, self.move_cmd, self.steer_cmd, 0, 0, 0, 0, 0], extended_id=False)
		self.printCommandConsole()
		#self.bus.send(msg)
		
	def printCommandConsole(self):
		print("STEER : {0:b} ".format(self.steer_cmd), end='')
		print(" ({}) | ".format(self.steer_cmd & ~0x80), end='')
		print("MOVE : {0:b} ".format(self.move_cmd), end='')
		print(" ({})".format(self.move_cmd & ~0x80))
		
	# Generates events to call move functions on a button press
	def moveForwardButton(self):
		self.root.event_generate("<Up>", when="tail")
	def moveBackwardButton(self):
		self.root.event_generate("<Down>", when="tail")
	def moveLeftButton(self):
		self.root.event_generate("<Left>", when="tail")
	def moveRightButton(self):
		self.root.event_generate("<Right>", when="tail")


if __name__ == "__main__":
	myGUI = GUI()
	myGUI.root.mainloop()
