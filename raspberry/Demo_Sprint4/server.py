import random
import socket, select
from time import gmtime, strftime, time
from random import randint
from PIL import Image
import psutil

imgcounter = 1
basename = "image.jpg"

HOST = '127.0.0.1'
PORT = 6668

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

while True:
    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:
        if sock == server_socket:
            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)
        else:
            try:
                data = sock.recv(40960000)
                txt = str(data)
                if data:
                    print 'data received !'
                    if data.startswith('SIZE'):
                        tmp = txt.split()
                        size = int(tmp[1])

                        print 'got size'
                        sock.sendall("GOT SIZE")

                    #elif data.startswith('BYE'):
                        #sock.shutdown()

                    else :
                        #if os.path.isfile(basename):
                        #    os.remove(basename)
                        myfile = open(basename , 'wb')
                        myfile.write(data)

                        #data = sock.recv(40960000)
                        if not data:
                            myfile.close()
                            break
                        myfile.write(data)
                        myfile.close()
			
			print 'got image'
                        sock.sendall("GOT IMAGE")
                        
                        for proc in psutil.process_iter():
                            if proc.name() == "display":
                                proc.kill()
                        img = Image.open(basename)
                        img.show()
                        
            except:
                print 'error'
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
        imgcounter += 1
server_socket.close()

