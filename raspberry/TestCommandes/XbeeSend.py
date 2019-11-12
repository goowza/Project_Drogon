#!/usr/bin/env python3
import time
import serial
import argparse
import tkinter as tk
from tkinter import ttk

# Manage arguments used when launching the script
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port of XBee module")
args = parser.parse_args()

#
window = tk.Tk()
window.minsize(400, 200)
window.title("Drogon interface")
msg=77

# Creates serial link with XBee module
try:
    ser = serial.Serial(
        port=args.serial_port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except:
    print("Error creating the serial link")

def choixMsg():
    if mynumber.get()=="Turn right":
        msg=1
        label1.configure(text="Command sent : " + mynumber.get())
    elif mynumber.get()=="Turn left":
        msg=0
        label1.configure(text="Command sent : " + mynumber.get())
    elif mynumber.get()=="Activate wheels":
        msg=2
        label1.configure(text="Command sent : " + mynumber.get())
    else:
        msg=77
        label1.configure(text="Choose a valid command")
    ser.write(str.encode(str(msg)))


label = ttk.Label(window, text = "Choose a command")
label.grid(column = 0, row = 0)

mynumber = tk.StringVar()
combobox = ttk.Combobox(window, width = 15 , textvariable = mynumber)
combobox['values'] = ("Turn right","Turn left","Activate wheels")
combobox.grid(column = 0, row = 1)

button = ttk.Button(window, text = "Send", command = choixMsg)
button.grid(column = 0, row = 2)

label1 = ttk.Label(window, text = "Command sent : ")
label1.grid(column = 0, row = 3)



window.mainloop()
