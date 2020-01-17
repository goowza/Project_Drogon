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
import socket, select
from random import randint

#HOST = '192.168.43.9'
HOST = '127.0.0.1'
PORT = 6673
COOLDOWN = 4

class ImageSender():
    def __init__(self, pics_path):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        #connexion initiale
        #answer = self.sock.recv(4096)
        #print("answer = {}".format(answer))
        
        self.pics_path = pics_path
        self.img_buffer = list()

        pygame.init()
        res = pygame.display.list_modes()  # return the best resolution for your monitor
        width, height = res[0]
        self.camera = picamera.PiCamera()
        self.camera.resolution = (int(width/4), int(height/4))
        
    def take_pic(self):
        """Saves picture by overwriting previously saved pic"""
        
        try:
            if os.path.isfile(self.pics_path):
                os.remove(self.pics_path)
            self.camera.start_preview()
            time.sleep(0.1)
            self.camera.capture(self.pics_path, use_video_port=True)
            self.camera.stop_preview()
        except:
            print("Error when recording image")
            exit()
        try:
            image = open(self.pics_path, 'rb')
            img_bytes = image.read()
            size = len(img_bytes)
            self.img_buffer.append((size, img_bytes))
            print("image size : {}".format(size))
            image.close()
        except:
            print("Error when opening image")
            exit()
    
    def send_to_server(self):
        (size, img_bytes) = self.img_buffer.pop()
        img_bytes = bytearray(img_bytes)
        print("Buffer lenght : {}".format(len(self.img_buffer)))
        
        
        # send image size to server
        #self.sock.sendall(("13" + str(size)).encode(encoding="utf-8"))
        self.sock.sendall("SIZE {}".format(size).encode(encoding="utf-8"))
        answer = self.sock.recv(4096)
        print("answer = {}".format(answer))
        contenu_envoye = 0
        try:
            # send image to server
            if answer == b'GOT SIZE':
                print("Sending image ! {}".format(len(img_bytes)))
                nb_msgs,last_msg_size = divmod(size,1024)
                print("Sending {}*1024 + {} bytes".format(nb_msgs, last_msg_size))
                print("first bytes : {}".format(img_bytes[0:5]))
                for i in range(nb_msgs):
                    self.sock.sendall(img_bytes[0:1024])
                    img_bytes = img_bytes[1024:]
                    answer = self.sock.recv(1024)
                    print("answer = {}".format(answer))
                    if answer != b'GOT DATA':
                        print("Error : did not received ack")
                        break
                if last_msg_size != 0:
                    self.sock.send(img_bytes[0:last_msg_size])
                    
                # check what server send
                answer = self.sock.recv(4096)
                print("answer = {}".format(answer))
    
                if answer == b'GOT IMAGE':
                    print("Image successfully sent to server")
        except:
            print("Error when sending image")
            exit()


my_sender = ImageSender("pics/image.jpg")
last_msg_received = 0
            
def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    data = dictionnaire avec les champs :
    {'id': 'rx', 'source_addr': b'\x00\x04', 'rssi': b'>', 'options': b'\x02', 'rf_data': b'Hey'}
    """
    global last_msg_received
    global count
    global my_sender
    count = count + 1
    
    last_msg_received = time.time()

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
        my_sender.take_pic()
        my_sender.send_to_server()

if __name__=="__main__":

    # Parametre les GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    Gyro = 13

    GPIO.setup(Gyro, GPIO.OUT)
    GPIO.output(Gyro, GPIO.LOW)

    # Compte le nombre de messages recus
    count = 0
    
    try:
        serial_port = serial.Serial("/dev/ttyAMA0", 9600)
        xbee = XBee(serial_port, callback=print_data)
    except:
        print("Error creating serial link")
        exit()

    while True:
        try:
            now = time.time()
            if now - last_msg_received > COOLDOWN:
                #Desactiver borne
                #GPIO.output(Gyro, GPIO.LOW)
                #print("LOIN")
                pass
            time.sleep(0.001)
        except KeyboardInterrupt:
            break

    print("\n")
    my_sender.camera.close()
    pygame.quit()
    xbee.halt()
    serial_port.close()
