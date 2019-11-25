
 # Definition d'un client reseau gerant en parallele l'emission
 # et la reception des messages (utilisation de 2 THREADS).

host = '10.1.5.190'
port = 40001

#host='127.0.0.1'
#port=9999
import socket, sys, threading
import time

#global message_emis

"""
class ThreadSync(threading.Thread):

    def __init__(self, lock, queue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.queue = queue

    def run(self):
        global message_emis
        a = 0
        self.lock.acquire()
        while 1:
            if input() == "S":
                a = a+1
                message_emis=message_emis+str(a)
                print(message_emis)
                self.lock.release()
                print("Relache")
                self.lock.acquire()
                print("Ack")
"""

class ThreadReception(threading.Thread):
   """objet thread gerant la reception des messages"""
   def __init__(self, conn):
       threading.Thread.__init__(self)
       self.connexion = conn           # ref. du socket de connexion
        
   def run(self):
       while 1:
           message_recu = self.connexion.recv(1024)
           print("*" + message_recu.decode('utf-8') + "*")
           if message_recu =='' or message_recu.upper() == "FIN":
               break
       # Le thread <reception> se termine ici.
       # On force la fermeture du thread <emission> :
       th_E._Thread__stop()
       print("Client arrete. Connexion interrompue.")
       self.connexion.close()
   
class ThreadEmission(threading.Thread):
    """objet thread gerant l'emission des messages"""
    def __init__(self, conn, lock, queue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.connexion = conn           # ref. du socket de connexion
        self.queue = queue
        
    def run(self):
        while 1:
            self.lock.acquire()
            message_emis = self.queue.get()
            self.connexion.send(message_emis.encode('utf-8'))
            self.lock.release()
            time.sleep(0.1)

if __name__=="__main__":
    # Programme principal - etablissement de la connexion :
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
    except socket.error:
        print("La connexion a echoue.")
        sys.exit()
    print("Connexion etablie avec le serveur.")
    
    # Dialogue avec le serveur : on lance deux threads pour gerer
    # independamment l'emission et la reception des messages :
    message_emis ="A5B69" #Variable globale
    lock = threading.Lock()
    #th_S= ThreadSync()
    th_E = ThreadEmission(connexion, lock)
    th_R = ThreadReception(connexion)
    #th_S.start()
    th_E.start()
    th_R.start()
