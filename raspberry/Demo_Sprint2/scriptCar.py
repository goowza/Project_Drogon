#!/usr/bin/env python
# coding: utf-8

import argparse
from Car import *

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port_gps", help="serial port of GPS")
parser.add_argument("serial_port_xbee", help="serial port of xbee")
args = parser.parse_args()

if __name__=="__main__":
	my_car = Car(42, args.serial_port_gps, args.serial_port_xbee)
	while True:
		my_car.run()