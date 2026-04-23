import tkinter as tk
from tkinter import font

class StartMenu:
    def __init__(self, root, startCallBack):
        self.frm = tk.Canvas(root, width=512, height=384, bg="white")
        self.frm.pack(fill="both", expand=True)
        self.playerName = ""
        self.name_var = tk.StringVar()
        self.startCallBack = startCallBack
        self.canStart = False
        titleFont = font.Font(family="System", size=20, weight="bold")
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0, 0, image=self.bg, anchor="nw")
        self.disabeledBtImg = tk.PhotoImage(file="assets\img\PlayDisable.png")
        self.btImg = tk.PhotoImage(file="assets\img\Play.png")
        self.startButton = self.frm.create_image(256, 250, image=self.disabeledBtImg, anchor="center")
        self.frm.tag_bind(self.startButton, "<Button-1>", self.onStartClick)
        self.entry = tk.Entry(root, textvariable=self.name_var, font=titleFont)
        self.entry.place(x=512/2, y=384/2, width=250, height=40, anchor="center")
        # Solo Enter guarda y habilita
        self.entry.bind("<Return>", self.guardar)
        self.frm.create_text(252,142,text="Choose your name",fill="black",font=titleFont)
        self.frm.create_text(250,140,text="Choose your name",fill="violet",font=titleFont)

    def guardar(self, event=None):
        nombre = self.name_var.get().strip()
        if nombre != "":
            self.playerName = nombre
            self.canStart = True
            self.frm.itemconfig(self.startButton, image=self.btImg)
            print("Guardado:", self.playerName)
        else:
            self.playerName = ""
            self.canStart = False
            self.frm.itemconfig(self.startButton, image=self.disabeledBtImg)

    def onStartClick(self, event):
        if not self.canStart:
            return

        self.startCallBack(event)