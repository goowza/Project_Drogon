#!/usr/bin/env python3
# coding: utf-8
import os
import time

import can
import pygame
from pygame.locals import *
from constants import MCM
from GPSReader import *
import argparse

class Car():
    def __init__(self, serial_port_gps):
        self.driver = Driver()
        self.xbee = "xbee"
        self.gps = GPSReader(serial_port_gps)
        
    def sendSOS(self):
        pass
    
class Driver():
    def __init__(self):
        # Setup CAN communication bus
        print('Bring up CAN0....')
        os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
        time.sleep(0.1)

        try:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        except OSError:
            print('Cannot find PiCAN board.')
            exit()
    
    def moveForward(self):
        move_cmd = 75 | 0x80
        msg = can.Message(arbitration_id=MCM, data=[move_cmd, move_cmd, 0, 0, 0, 0, 0, 0], extended_id=False)
        self.bus.send(msg)
    
    def moveBackward(self):
        move_cmd = 25 | 0x80
        msg = can.Message(arbitration_id=MCM, data=[move_cmd, move_cmd, 0, 0, 0, 0, 0, 0], extended_id=False)
        self.bus.send(msg)
    
    def stop(self):
        move_cmd = 50 | 0x80
        msg = can.Message(arbitration_id=MCM, data=[move_cmd, move_cmd, 0, 0, 0, 0, 0, 0], extended_id=False)
        self.bus.send(msg)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port_gps", help="serial port of GPS")
    args = parser.parse_args()
    
    pygame.init()
    screen = pygame.display.set_mode((50, 50))
    pygame.display.set_caption('VROUM')
    screen.fill((159, 182, 205))
    
    car = Car(args.serial_port_gps)
    done = False
    while not done:
        car.gps.update()
        pygame.display.update()
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            car.driver.moveForward()
            print("UP")
        elif keys[K_DOWN]:
            car.driver.moveBackward()
            print("DOWN")
        elif keys[K_h]:
            car.sendSOS()
            print("SOS")
        elif keys[K_ESCAPE]:
            done = True
            car.driver.stop()
        else:
            car.driver.stop()
            
        time.sleep(0.1)
