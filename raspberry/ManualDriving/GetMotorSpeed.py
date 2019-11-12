#!/usr/bin/env python
# coding: utf-8
import can
import serial
import os
import time
import argparse

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

while 1:
    # Setup CAN communication bus
    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    while True :
        msg = bus.recv()

        #print(msg.arbitration_id, msg.data)
        st = ""

        if msg.arbitration_id == US1:
            # ultrason avant gauche
            distance_avg = int.from_bytes(msg.data[0:2], byteorder='big')
            # ultrason avant droit
            distance_avd = int.from_bytes(msg.data[2:4], byteorder='big')
            # ultrason arriere centre
            distance_arc = int.from_bytes(msg.data[4:6], byteorder='big')
        elif msg.arbitration_id == US2:
            # ultrason arriere gauche
            distance_avg = int.from_bytes(msg.data[0:2], byteorder='big')
            # ultrason arriere droit
            distance_avd = int.from_bytes(msg.data[2:4], byteorder='big')
            # ultrason avant centre
            distance_arc = int.from_bytes(msg.data[4:6], byteorder='big')
        elif msg.arbitration_id == MS:
            # position volant
            angle = int.from_bytes(msg.data[0:2], byteorder='big')
            # Niveau de la batterie
            bat = int.from_bytes(msg.data[2:4], byteorder='big')
            # vitesse roue gauche
            speed_left = int.from_bytes(msg.data[4:6], byteorder='big')
            # vitesse roue droite
            # header : SWR payload : entier, *0.01rpm
            speed_right= int.from_bytes(msg.data[6:8], byteorder='big')
            
            print("Speed Left : {} | Speed Right : {}".format(speed_left,speed_right))
        elif msg.arbitration_id == OM1:
            pass
        elif msg.arbitration_id == OM2:
            pass
