import time
import os
import socket, sys, threading
import psutil
from PIL import Image

 # Definition d'un serveur reseau gerant un systeme de CHAT simplifie.
 # Utilise les threads pour gerer les connexions clientes en parallele.

#HOST = '10.105.1.85'
HOST = '192.168.43.9'
#PORT = 40002

#pour tester en local
#HOST = 'localhost'
#PORT = 9998

#HOST = '127.0.0.1'
#PORT = 40002
#HOST = '192.168.43.54'
PORT = 40000

basename = "image.jpg"
#counter = 0
#image_bytes = b''
#imgcounter = 1
PICS_PATH = "server_img.jpg"

class Relevant(threading.Thread):
   '''derivation d'un objet thread pour gerer la connexion avec un client'''
   def __init__(self):
       threading.Thread.__init__(self)
       self.end = False
       
   def run(self):
       cmd='cat < fifo2'
       while not self.end:
           msg=os.popen(cmd,'r').read()
           if msg =="":
               break
           else:
               print("Sent to emergency vehicle : "+str(msg))
               for j in threads:
                   if threads[j].IsEmergency():
                       threads[j].Connexion().send(msg)             

   def stopthread(self):
       self.end = True



 
class ThreadClient(threading.Thread):
   '''derivation d'un objet thread pour gerer la connexion avec un client'''
   def __init__(self, conn):
       threading.Thread.__init__(self)
       self.counter = 0
       self.connexion = conn
       self.image_bytes = b''
       self.Emergency = False
       self.end = False
       
   def run(self):
       PICS_PATH = "server_img.jpg"
       # Dialogue avec le client :
       nom = self.getName()        # Chaque thread possede un nom
       while not self.end:
           msgClient = self.connexion.recv(4096)
           if msgClient.upper() == "FIN" or msgClient =="":
               break
           message = "%s> %s" % (nom, msgClient)
           #print message
           #print msgClient[1]
           if msgClient.startswith("EMERGENCY"):
               self.Emergency = True
           else:
               if msgClient.startswith("SIZE"):
                   # Get size of image
                   size = msgClient.split()[1]
                   #print size
                   #onn.sendall("GOT SIZE".encode(encoding="utf-8"))
                   conn_client[nom].send("GOT SIZE")

                   # Get each packet and rebuild the image
                   for i in range(int(size)):
                       msgClient = self.connexion.recv(4096)
                       if not msgClient:
                           break
                       conn_client[nom].send("OK")
                       self.counter += 1
                       self.image_bytes += msgClient

                   # Check if image was not empty
                   if self.counter != 0:
                       # close previously opened image window
                       for proc in psutil.process_iter():
                           if proc.name() == "display":
                               proc.kill()
                               #sys.stdout.write("\033[F")
                               #sys.stdout.write("\033[K")
                           
                       #print "Received %d packets" %self.counter
                       if os.path.isfile(PICS_PATH):
                           os.remove(PICS_PATH)

                       # Save image
                       image_to_save = open(PICS_PATH, 'wb')
                       image_to_save.write(self.image_bytes)
                       image_to_save.close()
                       self.image_bytes = b''


                           # Display image
                       img = Image.open(PICS_PATH)
                       img.show()

                   self.counter = 0


                    #taille=msgClient[2:]


               else :
                   date=time.strftime("%d/%m/%Y %Hh%Mm%Ss : ")
                   msg=date + msgClient
                   cmd = 'echo ' + str(msg) + '>fifo1'
                   os.popen(cmd, 'w')
                   # Faire suivre le message a tous les autres clients :
                   #for cle in conn_client:
                       #if cle != nom:      # ne pas le renvoyer a l'emetteur
                           #conn_client[cle].send(message.encode('utf-8'))
                   
       # Fermeture de la connexion :
       self.connexion.close()      # couper la connexion cote serveur
       del conn_client[nom]        # supprimer son entree dans le dictionnaire
       print "Client %s deconnected." % nom
       # Le thread se termine ici
       
   def IsEmergency(self):
       return self.Emergency

   def Connexion(self):
       return self.connexion
       
   def stopthread(self):
       self.end = True

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print "Connexion failed"
    sys.exit()
print "Server ready, waiting ..."
#f = open('file.txt', 'a') #Ouverture du fichier de stockage des trames recus
mySocket.listen(10)

# Attente et prise en charge des connexions demandees par les clients :
conn_client = {}                # dictionnaire des connexions clients
threads = {} #dictionnaire des threads
rel = Relevant()
rel.start()

try :
    while 1:    
        connexion, adresse = mySocket.accept()
        # Creer un nouvel objet thread pour gerer la connexion :
        th = ThreadClient(connexion)
        th.start()
        # Memoriser la connexion dans le dictionnaire : 
        it = th.getName()        # identifiant du thread
        threads[it] = th
        conn_client[it] = connexion
        print "Client %s connected, IP adress %s, port %s." %\
               (it, adresse[0], adresse[1])
        # Dialogue avec le client :
        connexion.send("You are connected.")
except KeyboardInterrupt:
        rel.stopthread()
        rel.join()
        for j in threads:
            #print "Thread %s" % j
            threads[j].stopthread()
            threads[j].join()
        
        for i in conn_client:
            #print "Socket %s" % i
            conn_client[i].close()
        mySocket.close()
        print "Closing of sockets. System exit."
        sys.exit()
        
