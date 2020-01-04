#!/usr/bin/env python3
# coding: utf-8

import serial
import os
import time
from xbee import XBee
import RPi.GPIO as GPIO
import pygame, picamera
import socket
from random import randint

#HOST = '127.0.0.1'
HOST = "192.168.43.222"
PORT = 50000
PICS_PATH = "image.jpg"
PACKET_SIZE = 1024
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

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

my_sender = ImageSender(PICS_PATH)
            
def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    data = dictionnaire avec les champs :
    {'id': 'rx', 'source_addr': b'\x00\x04', 'rssi': b'>', 'options': b'\x02', 'rf_data': b'Hey'}
    """
    global count
    global my_sender
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
            print("SENDING PICS")
            my_sender.take_pic()
            my_sender.send_to_server()
            
    except:
        print("GNEUGNEU")

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
        #xbee = XBee(serial_port, callback=print_data)
    except:
        print("Error creating serial link")
        exit()

    while True:
        try:
            time.sleep(1)
            my_sender.take_pic()
            my_sender.send_to_server()
        except KeyboardInterrupt:
            break

    print("\n")
    my_sender.camera.close()
    my_sender.sock.close()
    #pygame.quit()
    #xbee.halt()
    serial_port.close()
