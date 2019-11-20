import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.minsize(400, 400)
window.title("Drogon Projet : Commandes V2V")
msg=77

def choixMsg():
    if mynumber.get()=="Tourner droite":
        msg=1
        label1.configure(text="Commande envoyée : " + mynumber.get())
    elif mynumber.get()=="Tourner gauche":
        msg=0
        label1.configure(text="Commande envoyée : " + mynumber.get())
    elif mynumber.get()=="Actionner roues":
        msg=2
        label1.configure(text="Commande envoyée : " + mynumber.get())
    else:
        msg=77
        label1.configure(text="Veuillez saisir une commande valable")


label = ttk.Label(window, text = "Commande à envoyer")
label.grid(column = 0, row = 0)

mynumber = tk.StringVar()
combobox = ttk.Combobox(window, width = 15 , textvariable = mynumber)
combobox['values'] = ("Tourner droite","Tourner gauche","Actionner roues")
combobox.grid(column = 0, row = 1)

button = ttk.Button(window, text = "Envoyer", command = choixMsg)
button.grid(column = 0, row = 2)

label1 = ttk.Label(window, text = "Commande envoyée : En attente")
label1.grid(column = 0, row = 3)

image = tk.PhotoImage(file="logo.gif")
label2 = tk.Label(image=image)
label2.grid(column = 1)



window.mainloop()