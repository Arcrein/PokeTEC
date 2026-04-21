import tkinter as tk
from tkinter import font
import Core.PokemonEspecie as Pk

class SelectPoke:
    def __init__(self, root, selectCallBack):
        titleFont = font.Font(family="System",size=20,weight="bold")
        self.frm = tk.Canvas(root,width=512,height=384,bg="white")
        #self.frm.place(x=0,y=0,relwidth=1,relheight=1)
        self.frm.pack(fill="both", expand=True)
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0,0,image=self.bg,anchor="nw")
        self.pokemonimg={}
        self.charButton={}
        self.selectedPokemons=[]
        self.selectedCallBack=selectCallBack
        self.frm.create_text(252,52,text="Choose 3 pokemon",fill="black",font=titleFont)
        self.frm.create_text(250,50,text="Choose 3 pokemon",fill="violet",font=titleFont)
        self.pokeButton=[]
        pokeNumber=0 
        self.pokeList = Pk.loadPokemons("docs\pokemonStats.csv")
        for i in range (0,2):
            for j in range (0,4):
                bt=self.setUpButton(pokeNumber,self.pokeList[pokeNumber].name,40 + j*100 + 10*j,100 + i*100 + 10*i)
                self.pokeButton.append(bt)
                pokeNumber=pokeNumber+1
        

    def onEnter(self, index, charName):
        bt=self.pokeButton[index]
        if index not in self.selectedPokemons:
            bt.config(background="black")
    
    def onLeave(self, index, charName):
        bt=self.pokeButton[index]
        if index not in self.selectedPokemons:
            bt.config(background="dimgray")
     
    def onClick(self, index, charName):
        bt=self.pokeButton[index]
        if index not in self.selectedPokemons and len(self.selectedPokemons)<3:
            bt.config(background="orange")
            self.selectedPokemons.append(index)
        else:
            self.selectedPokemons.remove(index)
            bt.config(background="black")

        
    def setUpButton(self, pokeNumber, charName, x, y):
        if charName not in self.pokemonimg:
            self.pokemonimg[charName] = tk.PhotoImage(file="assets/img/"+charName+".png")
        
        bt = tk.Label(self.frm, image=self.pokemonimg[charName], background="dimgray")
        bt.place(x=x,y=y,width=100,height=100)
        bt.bind("<Enter>", lambda e, name=charName,index=pokeNumber: self.onEnter(index,name))
        bt.bind("<Leave>", lambda e, name=charName,index=pokeNumber: self.onLeave(index,name))
        bt.bind("<Button-1>", lambda e, name=charName,index=pokeNumber: self.onClick(index,name))
        return bt