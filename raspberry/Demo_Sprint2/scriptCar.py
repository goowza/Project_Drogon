#!/usr/bin/env python
# coding: utf-8

import argparse
from Car import *
from clienttest import *
import socket, sys, threading
import time
from queue import Queue

host = '10.105.1.85'
port = 40003

#host='127.0.0.1'
#port=9999

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port_gps", help="serial port of GPS")
parser.add_argument("serial_port_xbee", help="serial port of xbee")
args = parser.parse_args()

if __name__=="__main__":
	
	# Connexion with server
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		print("Connecting to server...")
		connexion.connect((host, port))
	except socket.error:
		print("Connection with server failed")
		sys.exit()
	print("Connection with server established")

	# Shared variables
	queue = Queue()
	lock = threading.Lock()
	
	# Threads declaration
	thread_car = Car(42, args.serial_port_gps, args.serial_port_xbee, lock, queue)
	th_E = ThreadEmission(connexion, lock, queue)
	th_R = ThreadReception(connexion)
	
	thread_car.start()
	th_E.start()
	th_R.start()
	
	thread_car.join()
	th_E.join()
	th_R.join()

	connexion.close()
