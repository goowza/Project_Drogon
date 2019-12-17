#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
import argparse
from xbee import XBee
import RPi.GPIO as GPIO
import pygame, picamera
import traceback

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
args = parser.parse_args()

pygame.init()
res = pygame.display.list_modes() # return the best resolution for your monitor
width, height = res[0] # Having trouble getting the right resolution? Manually set with: 'width, height = 1650, 1050' (where the numbers match your monitor)
camera = picamera.PiCamera()
camera.resolution = (width, height)
      
# Parametre les GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Gyro = 13

GPIO.setup(Gyro, GPIO.OUT)
GPIO.output(Gyro, GPIO.LOW)

# Compte le nombre de messages recus
count = 0

def take_pic(pics_path):
    """Saves picture by overwriting previously saved pic"""
    try:
        if os.path.isfile(pics_path):
            os.remove(pics_path)
        camera.capture(pics_path, use_video_port = True)
        #sendtoserver
    except:
        print("erreur capture")
            
def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    data = dictionnaire avec les champs :
    {'id': 'rx', 'source_addr': b'\x00\x04', 'rssi': b'>', 'options': b'\x02', 'rf_data': b'Hey'}
    """
    pics_path = os.path.join('pics', 'record.jpg')
    global count
    count = count + 1

    try:
        ID = data["rf_data"].decode().split(":")[0]
        command = data["rf_data"].decode().split(":")[1]
        if ID == "HL118":
            RSSI = ord(data["rssi"].decode())
            if RSSI < 60:
                print("pres")
                GPIO.output(Gyro, GPIO.HIGH)
            else:
                print("loin")
                GPIO.output(Gyro, GPIO.LOW)
        elif command == "1":
            take_pic(pics_path)
            
    except:
        print("GNEUGNEU")

if __name__=="__main__":
    try:
        serial_port = serial.Serial(args.serial_port, 9600)
        xbee = XBee(serial_port, callback=print_data)
    except:
        print("Error creating serial link")
        exit()

    while True:
        try:
            time.sleep(0.001)
        except KeyboardInterrupt:
            break

    print("\n")
    camera.close()
    pygame.quit()
    xbee.halt()
    serial_port.close()
