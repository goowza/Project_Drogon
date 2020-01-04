#!/usr/bin/env python3
# coding: utf-8

import socket, select
import psutil
from PIL import Image
import os

imgcounter = 1
PICS_PATH = "server_img.jpg"

#HOST = '127.0.0.1'
HOST = '192.168.43.222'
PORT = 50000

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)
counter = 0
image_bytes = b''

try:
    while True:
    
        read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
    
        for sock in read_sockets:
    
            if sock == server_socket:
    
                conn, client_address = server_socket.accept()
                connected_clients_sockets.append(conn)
                print('Connected by', client_address)
                conn.sendall(b'Connected !')
    
            else:
                try:
                    data = conn.recv(4096)
                    if not data: break
                    
                    # If message received is an image
                    if data.decode().startswith("SIZE"):
                        # Get size of image
                        size = data.decode().split()[1]
                        conn.sendall("GOT SIZE".encode(encoding="utf-8"))
            
                        # Get each packet and rebuild the image
                        for i in range(int(size)):
                            data = conn.recv(4096)
                            if not data: break
                            # print("Received packet n°{}".format(counter))
                            conn.sendall("OK".encode(encoding="utf-8"))
                            counter += 1
                            image_bytes += data
                        
                        # Check if image was not empty
                        if counter != 0:
                            # close previously openned image window
                            for proc in psutil.process_iter():
                                if proc.name() == "display":
                                    proc.kill()
                            print("Received {} packets".format(counter))
                            if os.path.isfile(PICS_PATH):
                                os.remove(PICS_PATH)
                            
                            # Save image
                            image_to_save = open(PICS_PATH, 'wb')
                            image_to_save.write(image_bytes)
                            image_to_save.close()
                            image_bytes = b''
                            
                            # Display image
                            img = Image.open(PICS_PATH)
                            img.show()
                        counter = 0
                    # TODO : If message is not an image
                    else:
                        pass
                except:
                    conn.close()
                    connected_clients_sockets.remove(conn)
                    continue
            imgcounter += 1
except KeyboardInterrupt:
    server_socket.close()
