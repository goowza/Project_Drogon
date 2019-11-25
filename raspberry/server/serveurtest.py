import time

 # Definition d'un serveur reseau gerant un systeme de CHAT simplifie.
 # Utilise les threads pour gerer les connexions clientes en parallele.

HOST = '10.1.5.190'
PORT = 40001

#pour tester en local
#HOST = 'localhost'
#PORT = 9999

import socket, sys, threading
 
class ThreadClient(threading.Thread):
   '''derivation d'un objet thread pour gerer la connexion avec un client'''
   def __init__(self, conn):
       threading.Thread.__init__(self)
       self.connexion = conn
       
   def run(self):
       # Dialogue avec le client :
       nom = self.getName()        # Chaque thread possede un nom
       while 1:
           msgClient = self.connexion.recv(1024)
           if msgClient.upper() == "FIN" or msgClient =="":
               break
           message = "%s> %s" % (nom, msgClient)
           print message
           date=time.strftime("%d/%m/%Y %Hh%Mm%Ss : ")
           f.write(date + msgClient + "\n" )
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
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print "La liaison du socket a l'adresse choisie a echoue."
    sys.exit()
print "Serveur pret, en attente de requetes ..."
f = open('file.txt', 'a') #Ouverture du fichier de stockage des trames recus
mySocket.listen(5)

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
