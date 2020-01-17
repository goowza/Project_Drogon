#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
from xbee import XBee
import RPi.GPIO as GPIO
import picamera
import socket
from RSSI_Receive import *

#HOST = '127.0.0.1'
HOST = "192.168.43.9"
#HOST = "10.105.1.85"
PORT = 40000
PICS_PATH = "image.jpg"
PACKET_SIZE = 1024
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
PIN_LED = 12
PIN_BUZ = 13

class ImageSender():
    def __init__(self, pics_path):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        answer = self.sock.recv(4096)
        print("answer = {}".format(answer))

        self.pics_path = pics_path
        self.img_buffer = list()

        #pygame.init()
        #res = pygame.display.list_modes()  # return the best resolution for your monitor
        #width, height = res[0]
        self.camera = picamera.PiCamera()
        self.camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        
    def take_pic(self):
        """Saves picture by overwriting previously saved pic"""
        
        try:
            if os.path.isfile(self.pics_path):
                os.remove(self.pics_path)
            self.camera.capture(self.pics_path, use_video_port=True)
        except:
            print("Error when recording image")
            exit()
        
        try:
            image = open(self.pics_path, 'rb')
            img_bytes = image.read()
            size = len(img_bytes)
            self.img_buffer.append((size, img_bytes))
            image.close()
        except:
            print("Error when opening image")
            exit()
    
    def send_to_server(self):
        counter = 0
        
        size, img_bytes = self.img_buffer.pop()
        
        nb_packets = self.compute_nb_packets(size)
        packet_lost = False
        print("Sending {} packets...".format(nb_packets))
        
        self.sock.sendall("SIZE {}".format(nb_packets).encode(encoding="utf-8"))
        answer = self.sock.recv(4096)
        
        if answer != b'GOT SIZE':
            exit(1)
        
        for i in range(nb_packets-1):
            # print("Sending packet n°{}".format(counter))
            self.sock.sendall(img_bytes[0:PACKET_SIZE])
            # wait for answer
            answer = self.sock.recv(4096)
            # print("answer = {}".format(answer))
            if answer != b'OK':
                packet_lost = True
                break
            img_bytes = img_bytes[PACKET_SIZE:]
            counter += 1
        if not packet_lost:
            # print("Sending : {}".format(img_bytes))
            # print("Sending packet n°{}".format(counter))
            self.sock.sendall(img_bytes)
            # wait for answer
            answer = self.sock.recv(4096)
            # print("answer = {}".format(answer))
            counter += 1
        print("Sent {} packets".format(counter))
    
    def compute_nb_packets(self, size):
        q,r = divmod(size, PACKET_SIZE)
        if r != 0:
            return q+1
        else:
            return q

class Borne():
    def __init__(self, pin_led, pin_buz):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.sender = ImageSender(PICS_PATH)
        self.xbee_dir = XbeeDir("/dev/ttyAMA0")
        self.pin_led = pin_led
        self.pin_buz = pin_buz
        GPIO.setup(self.pin_led, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_buz, GPIO.OUT, initial=GPIO.LOW)
        
    def run(self):
        while True:
            try:
                if not self.xbee_dir.connexion_lost():
                    if self.xbee_dir.sending_pics_flag:
                        self.sender.take_pic()
                        self.sender.send_to_server()
                    if self.xbee_dir.bollard_command == "ON":
                        self.bollard_on()
                    else:
                        self.bollard_off()
                else:
                    self.bollard_off()
            except KeyboardInterrupt:
                break
    
    def bollard_on(self):
        GPIO.output(self.pin_led, GPIO.HIGH)
        GPIO.output(self.pin_buz, GPIO.HIGH)
        
    def bollard_off(self):
        GPIO.output(self.pin_led, GPIO.LOW)
        GPIO.output(self.pin_buz, GPIO.LOW)
        
    def close(self):
        self.bollard_off()
        self.sender.camera.close()
        self.sender.sock.close()
        self.xbee_dir.xbee.halt()
        self.xbee_dir.serial_port.close()

if __name__=="__main__":
    borne = Borne(PIN_LED, PIN_BUZ)
    borne.run()
    borne.close()

