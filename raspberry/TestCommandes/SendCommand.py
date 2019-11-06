# coding: utf-8
from threading import Thread
import time
import can
import os
import struct

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102


'''
 Messages envoyés :
    - ultrason avant gauche
    header : UFL payload : entier, distance en cm
    - ultrason avant centre
    header : UFC payload : entier, distance en cm
    - ultrason avant droite
    header : UFR payload : entier, distance en cm
    - ultrason arriere gauche
    header : URL payload : entier, distance en cm
    - ultrason arriere centre
    header : URC payload : entier, distance en cm
    - ultrason arriere droite
    header : URR payload : entier, distance en cm
    - position volant
    header : POS payload : entier, valeur brute du capteur
    - vitesse roue gauche
    header : SWL payload : entier, *0.01rpm
    - vitesse roue droite
    header : SWR payload : entier, *0.01rpm
    - Niveau de la batterie
    header : BAT payload : entier, mV
    - Pitch
    header : PIT payload : float, angle en degrée
    - Yaw
    header : YAW payload : float, angle en degrée
    - Roll
    header : ROL payload : float, angle en degrée

 Messages reçus :
    - Modification de la vitesse
    header : SPE payload : valeur entre 0 et 50
    - Control du volant (droite, gauche)
    header : STE paylaod : left | right | stop
    - Contra l de l'avancée
    header : MOV payload : forward | backward | stop
'''


class MyReceive(Thread):
    def __init__(self, conn, bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')

        self.speed_cmd = 0
        self.movement = 0
        self.turn = 0
        self.enable_steering = 0
        self.enable = 0

    def run(self):
        self.speed_cmd = 0
        self.movement = 0
        self.turn = 0
        self.enable_steering = 0
        self.enable_speed = 0

        while True:
            data = conn.recv(1024)

            if not data: break

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'SPE'):  # speed
                self.speed_cmd = int(payload)
                print("speed is updated to ", self.speed_cmd)
            elif (header == b'STE'):  # steering
                if (payload == b'left'):
                    self.turn = 1
                    self.enable_steering = 1
                    print("send cmd turn left")
                elif (payload == b'right'):
                    self.turn = -1
                    self.enable_steering = 1
                    print("send cmd turn right")
                elif (payload == b'stop'):
                    self.turn = 0
                    self.enable_steering = 0
                    print("send cmd stop to turn")
            elif (header == b'MOV'):  # movement
                if (payload == b'stop'):
                    self.movement = 0
                    self.enable_speed = 0
                    print("send cmd movement stop")
                elif (payload == b'forward'):
                    print("send cmd movement forward")
                    self.movement = 1
                    self.enable_speed = 1
                elif (payload == b'backward'):
                    print("send cmd movement backward")
                    self.movement = -1
                    self.enable_speed = 1

            print(self.speed_cmd)
            print(self.movement)
            print(self.enable)
            print(self.turn)
            print(self.enable_steering)

            if self.enable_speed:
                cmd_mv = (50 + self.movement*self.speed_cmd) | 0x80
            else:
                cmd_mv = (50 + self.movement*self.speed_cmd) & ~0x80

            if self.enable_steering:
                cmd_turn = 50 + self.turn*30 | 0x80
            else:
                cmd_turn = 50 + self.turn*30 & 0x80

            print("mv:",cmd_mv,"turn:",cmd_turn)

            msg = can.Message(arbitration_id=MCM,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)

            #msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            #msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            print(msg)
            self.bus.send(msg)

        conn.close()

def sendCommand():
    msg = can.Message(arbitration_id=MCM,data=[0, 0, 0,0,0,0,0,0],extended_id=False)

# Echo server program
import socket

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    cmd_turn = 0 | 0x80
    msg = can.Message(arbitration_id=MCM,data=[0,0,cmd_turn,0,0,0,0,0],extended_id=False)
    bus.send(msg)
