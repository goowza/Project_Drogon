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
window.title("Python Tkinter Combo box")
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
    if mynumber.get()=="Tourner droite":
        msg=1
        label1.configure(text="Commande envoyee : " + mynumber.get())
    elif mynumber.get()=="Tourner gauche":
        msg=0
        label1.configure(text="Commande envoyee : " + mynumber.get())
    elif mynumber.get()=="Actionner roues":
        msg=2
        label1.configure(text="Commande envoyee : " + mynumber.get())
    else:
        msg=77
        label1.configure(text="Veuillez saisir une commande valable")
    ser.write(str.encode(str(msg)))


label = ttk.Label(window, text = "Commande a envoyer")
label.grid(column = 0, row = 0)

mynumber = tk.StringVar()
combobox = ttk.Combobox(window, width = 15 , textvariable = mynumber)
combobox['values'] = ("Tourner droite","Tourner gauche","Actionner roues")
combobox.grid(column = 0, row = 1)

button = ttk.Button(window, text = "Envoyer", command = choixMsg)
button.grid(column = 0, row = 2)

label1 = ttk.Label(window, text = "Commande envoyee : En attente")
label1.grid(column = 0, row = 3)



window.mainloop()
