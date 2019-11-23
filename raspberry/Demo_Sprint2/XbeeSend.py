#!/usr/bin/env python3
import time
import serial
import argparse
from tkinter import *
from tkinter import ttk

MOVE_LEFT = "0"
MOVE_RIGHT = "1"
MOVE_FORWARD = "2"
STOP = "3"
SHARE_LOCATION = "4"
STOP_SHARING_LOCATION = "5"
SERIAL_DELIMITER = ":"
ID = 777

class GUI():
    def __init__(self, serial_port):
        #Creates serial link with XBee module
        try:
            self.ser = serial.Serial(
                port=serial_port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except:
            print("Error creating the serial link")
        
        # GUI layout
        self.window = Tk()
        self.window.minsize(400, 200)
        self.window.title("Drogon interface")

        self.choose_command_frame = LabelFrame(self.window, text="Choose a command", font=("Courier", 12, "bold"))

        self.command_choice = StringVar()
        self.combobox = ttk.Combobox(self.choose_command_frame, width=15, textvariable=self.command_choice)
        self.combobox['values'] = (
        "Turn Right", "Turn Left", "Activate Wheels", "Stop", "Share Location", "Stop Sharing Location")
        self.choose_command_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        self.combobox.pack(fill=X, padx=(5, 5), pady=(5, 5))

        self.button_frame = LabelFrame(self.window, text="Send Command", font=("Courier", 12, "bold"))
        self.button = Button(self.button_frame, text="SEND", font=("Courier", 12, "bold"), command=self.sendMsg)
        self.button_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        self.button.pack(fill=X, padx=(5, 5), pady=(5, 5))

        self.infos_frame = LabelFrame(self.window, text="Infos", font=("Courier", 12, "bold"))
        self.command_choice_label = Label(self.infos_frame, text="Command sent : ")
        self.infos_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        self.command_choice_label.pack(fill=X, padx=(5, 5), pady=(5, 5))
        
        self.coords_frame = LabelFrame(self.window, text="Coordinates", font=("Courier", 12, "bold"))
        self.coords_label = Label(self.coords_frame, text=". . .", font=("Courier", 12, "bold"))
        self.coords_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        self.coords_label.pack(fill=X, padx=(5, 5), pady=(5, 5))


    def sendMsg(self):
        if self.command_choice.get() == "Turn Right":
            msg = self.buildMessage(MOVE_RIGHT)
        elif self.command_choice.get() == "Turn Left":
            msg = self.buildMessage(MOVE_LEFT)
        elif self.command_choice.get() == "Activate Wheels":
            msg = self.buildMessage(MOVE_FORWARD)
        elif self.command_choice.get() == "Stop":
            msg = self.buildMessage(STOP)
        elif self.command_choice.get() == "Share Location":
            msg = self.buildMessage(SHARE_LOCATION)
        elif self.command_choice.get() == "Stop Sharing Location":
            msg = self.buildMessage(STOP_SHARING_LOCATION)
        else:
            msg = ""
            self.command_choice_label.configure(text="Choose a valid command")
        
        if msg != "":
            self.ser.write(str.encode(msg))
            self.command_choice_label.configure(text="Command sent : " + self.command_choice.get())

    def readCoords(self):
        msg = self.ser.readline().decode().split(":")
        lat = 0
        long = 0
        if len(msg) > 1:
            if msg[1] == SHARE_LOCATION:
                lat = msg[2]
                long = msg[3]
        self.coords_label.configure(text="Latitude : {} | Longitude : {}".format(lat, long))
    
    def buildMessage(self, command):
        msg_to_write = str(ID) + ":" + str(command)
        return msg_to_write
    
if __name__=="__main__":
    # Manage arguments used when launching the script
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port", help="serial port of XBee module")
    args = parser.parse_args()
    
    myGUI = GUI(args.serial_port)
    while True:
        myGUI.readCoords()
        myGUI.window.update()
