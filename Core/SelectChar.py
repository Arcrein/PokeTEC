import tkinter as tk
from tkinter import font

class SelectChar:
    def __init__(self, root, selectCallBack):
        titleFont = font.Font(family="System",size=20,weight="bold")
        self.frm = tk.Canvas(root,width=512,height=384,bg="white")
        #self.frm.place(x=0,y=0,relwidth=1,relheight=1)
        self.frm.pack(fill="both", expand=True)
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0,0,image=self.bg,anchor="nw")
        self.charNoMouseimg={}
        self.charMouseimg={}
        self.charButton={}
        self.selectedCallBack=selectCallBack
        self.frm.create_text(252,52,text="Choose your character",fill="black",font=titleFont)
        self.frm.create_text(250,50,text="Choose your character",fill="violet",font=titleFont)
        self.setUpButton("Wen", 50, 100)
        self.setUpButton("Dani", 160, 100)
        self.setUpButton("Alex", 270, 100)
        self.setUpButton("Nicu", 380, 100)

    def onEnter(self, charName):
        self.frm.itemconfig(self.charButton[charName],image=self.charMouseimg[charName])
    
    def onLeave(self, charName):
        self.frm.itemconfig(self.charButton[charName],image=self.charNoMouseimg[charName])
     
    def onClick(self, charName):
        self.selectedCallBack(charName)
        
    def setUpButton(self, charName, x, y):
        self.charNoMouseimg[charName] = tk.PhotoImage(file="assets/trainers/"+charName+"NoMouse.png").subsample(2,2)
        self.charMouseimg[charName] = tk.PhotoImage(file="assets/trainers/"+charName+"Mouse.png").subsample(2,2)
        self.charButton[charName] = self.frm.create_image(x, y, image=self.charNoMouseimg[charName], anchor="nw")
        self.frm.tag_bind(self.charButton[charName], "<Enter>", lambda e, name=charName: self.onEnter(name))
        self.frm.tag_bind(self.charButton[charName], "<Leave>", lambda e, name=charName: self.onLeave(name))
        self.frm.tag_bind(self.charButton[charName], "<Button-1>", lambda e, name=charName: self.onClick(name))