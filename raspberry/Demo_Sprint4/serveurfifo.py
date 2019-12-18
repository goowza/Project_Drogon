import time
import os

 # Definition d'un serveur reseau gerant un systeme de CHAT simplifie.
 # Utilise les threads pour gerer les connexions clientes en parallele.

#HOST = '10.105.1.85'
#HOST = '192.168.43.31'
#PORT = 40002

#pour tester en local
#HOST = 'localhost'
#PORT = 9998

HOST = '127.0.0.1'
PORT = 6668

import socket, sys, threading

basename = "image.jpg"
 
class ThreadClient(threading.Thread):
   '''derivation d'un objet thread pour gerer la connexion avec un client'''
   def __init__(self, conn):
       threading.Thread.__init__(self)
       self.connexion = conn
       
   def run(self):
       # Dialogue avec le client :
       nom = self.getName()        # Chaque thread possede un nom
       while 1:
           msgClient = self.connexion.recv(4096)
           if msgClient.upper() == "FIN" or msgClient =="":
               break
           message = "%s> %s" % (nom, msgClient)
           print message
           print msgClient[1]
           if msgClient[1]=="3":
                taille=msgClient[2:]
                print "Taille de %s"  %taille
                conn_client[nom].send("GOT SIZE")
                myfile = open(basename, 'wb')
                #myfile.write(msgClient)

                msgClient = self.connexion.recv(40960000)
                if not msgClient:
                    myfile.close()
                    break
                myfile.write(msgClient)
                myfile.close()

                print 'got image'
                conn_client[nom].send("GOT IMAGE")

           else :
               date=time.strftime("%d/%m/%Y %Hh%Mm%Ss : ")
               msg=date + msgClient
               cmd = 'echo ' + str(msg) + '>fifo1'
               os.popen(cmd, 'w')
               # Faire suivre le message a tous les autres clients :
               for cle in conn_client:
                   if cle != nom:      # ne pas le renvoyer a l'emetteur
                       conn_client[cle].send(message.encode('utf-8'))
                   
       # Fermeture de la connexion :
       self.connexion.close()      # couper la connexion cote serveur
       del conn_client[nom]        # supprimer son entree dans le dictionnaire
       print "Client %s deconnecte." % nom
       # Le thread se termine ici    

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print "La liaison du socket a l'adresse choisie a echoue."
    sys.exit()
print "Serveur pret, en attente de requetes ..."
#f = open('file.txt', 'a') #Ouverture du fichier de stockage des trames recus
mySocket.listen(10)

# Attente et prise en charge des connexions demandees par les clients :
conn_client = {}                # dictionnaire des connexions clients
while 1:    
    connexion, adresse = mySocket.accept()
    # Creer un nouvel objet thread pour gerer la connexion :
    th = ThreadClient(connexion)
    th.start()
    # Memoriser la connexion dans le dictionnaire : 
    it = th.getName()        # identifiant du thread
    conn_client[it] = connexion
    print "Client %s connecte, adresse IP %s, port %s." %\
           (it, adresse[0], adresse[1])
    # Dialogue avec le client :
    connexion.send("Vous etes connecte. Envoyez vos messages.")
