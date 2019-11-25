#!/usr/bin/env python
# coding: utf-8

import argparse
from Car import *
from clienttest import *
import socket, sys, threading
import time

#host = '10.1.5.190'
#port = 40001

host='127.0.0.1'
port=9999


# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port_gps", help="serial port of GPS")
parser.add_argument("serial_port_xbee", help="serial port of xbee")
args = parser.parse_args()

if __name__=="__main__":
	message_emis=""
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connexion.connect((host, port))
	except socket.error:
		print("La connexion a echoue.")
		sys.exit()
	print("Connexion etablie avec le serveur.")

	lock = threading.Lock()
	th_S = Car(42, args.serial_port_gps, args.serial_port_xbee,lock)
	th_E = ThreadEmission(connexion, lock)
	th_R = ThreadReception(connexion)
	th_S.start()
	th_E.start()
	th_R.start()