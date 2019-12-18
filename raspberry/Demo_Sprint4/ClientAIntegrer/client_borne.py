#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime,sleep
from random import randint
#from picamera import PiCamera

image = "image.jpg"

HOST = '127.0.0.1'
PORT = 6668
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)







try:

    #connexion initiale
    answer = sock.recv(4096)

    print 'answer = %s' % answer
    # open image
    '''camera = PiCamera()
    camera.start_preview()
    sleep(0.1)
    camera.capture('/home/pi/image.jpg')
    camera.stop_preview()'''
    myfile = open(image, 'rb')
    bytes = myfile.read()
    size = len(bytes)

    # send image size to server
    sock.send("13" + str(size))
    answer = sock.recv(4096)

    print 'answer = %s' % answer

    # send image to server
    if answer == 'GOT SIZE':
        sock.sendall(bytes)

        # check what server send
        answer = sock.recv(4096)
        print 'answer = %s' % answer

        if answer == 'GOT IMAGE' :
             #sock.sendall("BYE BYE ")
            print 'Image successfully send to server'

    myfile.close()

finally:
    sock.close()
