import tkinter as tk
from tkinter import font
import Core.PokemonLib as Pk
import math

class SelectPoke:
    def __init__(self, root, selectCallBack):
        titleFont = font.Font(family="System",size=20,weight="bold")
        self.frm = tk.Canvas(root,width=512,height=384,bg="white")
        #self.frm.place(x=0,y=0,relwidth=1,relheight=1)
        self.frm.pack(fill="both", expand=True)
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0,0,image=self.bg,anchor="nw")
        self.pokemonimg={}
        self.pokemonSmallimg={}
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
                bt=self.setUpButton(pokeNumber,pokeNumber,self.pokeList[pokeNumber].name,40 + j*100 + 10*j,100 + i*100 + 10*i)
                self.pokeButton.append(bt)
                pokeNumber=pokeNumber+1

        self.previousimg=tk.PhotoImage(file="assets\img\previousArrow.png")
        self.nextimg=tk.PhotoImage(file="assets/img/nextArrow.png")
        self.previousButton = self.frm.create_image(5, 190, image=self.previousimg, anchor="nw")
        self.NextButton = self.frm.create_image(470,190, image=self.nextimg, anchor="nw")
        self.frm.itemconfigure(self.previousButton,state="hidden")
        self.currentPage=0
        self.pages=math.ceil(len(self.pokeList)/8)
        self.frm.tag_bind(self.NextButton, "<Button-1>", lambda e: self.onNextClick())
        self.frm.tag_bind(self.previousButton, "<Button-1>", lambda e: self.onPreviousClick())
        self.selected=[]
        self.selected.append(tk.Label(self.frm, background="dimgray"))
        self.selected[0].place(x=201,y=315,width=33,height=33)
        self.selected.append(tk.Label(self.frm, background="dimgray"))
        self.selected[1].place(x=241,y=315,width=33,height=33)
        self.selected.append(tk.Label(self.frm, background="dimgray"))
        self.selected[2].place(x=281,y=315,width=33,height=33)
        self.continueButtonDisableimg=tk.PhotoImage(file="assets\img\PlayGreenDisable.png")
        self.continueButtonimg=tk.PhotoImage(file="assets\img\PlayGreen.png")
        self.continueButton=self.frm.create_image(201,349,image=self.continueButtonDisableimg,anchor="nw")
        self.frm.tag_bind(self.continueButton,"<Button-1>",lambda e: self.onConfirm())

    def refreshSelected(self):
        for i in range(0,len(self.selectedPokemons)):
            pokeNumber=self.selectedPokemons[i]
            pokemon=self.pokeList[pokeNumber]
            self.selected[i].configure(image=self.pokemonSmallimg[pokemon.name])
        for i in range(len(self.selectedPokemons), 3):
            self.selected[i].configure(image="")
            self.selected[i].image=None
        if len(self.selectedPokemons)==3:
            self.frm.itemconfig(self.continueButton,image=self.continueButtonimg)
        else:
            self.frm.itemconfig(self.continueButton,image=self.continueButtonDisableimg)

    def onNextClick(self):
        if self.currentPage<self.pages-1:
            self.currentPage=self.currentPage+1
            pokeNumber=self.currentPage*8
            self.frm.itemconfigure(self.previousButton,state="normal")
            if self.currentPage == self.pages-1:
                self.frm.itemconfigure(self.NextButton,state="hidden")
            for bt in self.pokeButton:
                bt.destroy()
            self.pokeButton.clear()
            btIndex=0
            for i in range (0,2):
                for j in range (0,4):
                    if pokeNumber>=len(self.pokeList):
                        return
                    bt=self.setUpButton(btIndex,pokeNumber,self.pokeList[pokeNumber].name,40 + j*100 + 10*j,100 + i*100 + 10*i)
                    self.pokeButton.append(bt)
                    pokeNumber=pokeNumber+1
                    btIndex=btIndex+1 
    
    def onPreviousClick(self):
        if self.currentPage>0:
            self.currentPage=self.currentPage-1
            pokeNumber=self.currentPage*8
            if self.currentPage == 0:
                self.frm.itemconfigure(self.previousButton,state="hidden")
            self.frm.itemconfigure(self.NextButton,state="normal")
            for bt in self.pokeButton:
                bt.destroy()
            self.pokeButton.clear()
            btIndex=0
            for i in range (0,2):
                for j in range (0,4):
                    if pokeNumber>=len(self.pokeList):
                        return
                    bt=self.setUpButton(btIndex,pokeNumber,self.pokeList[pokeNumber].name,40 + j*100 + 10*j,100 + i*100 + 10*i)
                    self.pokeButton.append(bt)
                    pokeNumber=pokeNumber+1 
                    btIndex=btIndex+1

    def onEnter(self, index, pokeNumber, charName):
        bt=self.pokeButton[index]
        if pokeNumber not in self.selectedPokemons:
            bt.config(background="black")
    
    def onLeave(self, index, pokeNumber, charName):
        bt=self.pokeButton[index]
        if pokeNumber not in self.selectedPokemons:
            bt.config(background="dimgray")
     
    def onClick(self, index, pokeNumber, charName):
        bt=self.pokeButton[index]
        if pokeNumber not in self.selectedPokemons and len(self.selectedPokemons)<3:
            bt.config(background="orange")
            self.selectedPokemons.append(pokeNumber)
        elif pokeNumber in self.selectedPokemons:
            self.selectedPokemons.remove(pokeNumber)
            bt.config(background="black")
        self.refreshSelected()
        
    def setUpButton(self, index, pokeNumber, charName, x, y):
        if charName not in self.pokemonimg:
            self.pokemonimg[charName] = tk.PhotoImage(file="assets/img/"+charName+".png")
            self.pokemonSmallimg[charName] = self.pokemonimg[charName].subsample(2,2)
        
        bt = tk.Label(self.frm, image=self.pokemonimg[charName], background="dimgray")
        bt.place(x=x,y=y,width=100,height=100)
        bt.bind("<Enter>", lambda e, name=charName,index=index,pokeNumber=pokeNumber: self.onEnter(index,pokeNumber,name))
        bt.bind("<Leave>", lambda e, name=charName,index=index,pokeNumber=pokeNumber: self.onLeave(index,pokeNumber,name))
        bt.bind("<Button-1>", lambda e, name=charName,index=index,pokeNumber=pokeNumber: self.onClick(index,pokeNumber,name))
        if pokeNumber in self.selectedPokemons:
            bt.config(background="orange")
        return bt
    
    def onConfirm(self):
        if len(self.selectedPokemons)==3:
            self.selectedCallBack(self.selectedPokemons)