import tkinter as tk
from tkinter import font
import Core.SelectPoke as SP
import Core.PokemonLib as Pk
import random

class BattleScreen:
    def __init__(self, root, battleCallBack, selectedPoke: SP.SelectPoke):
        self.frm = tk.Canvas(root, width=512, height=384, bg="white")
        self.frm.pack(fill="both", expand=True)
        self.bg = tk.PhotoImage(file="assets\img\Battleground.png")
        self.frm.create_image(0, 0, image=self.bg, anchor="nw")
        self.battleCallBack = battleCallBack
        self.selectedCharacter = ""
        self.playerName = ""
        self.selectedPokes = selectedPoke
        self.movementList=Pk.loadMoves("docs\pokemonMoves.csv")
        self.characters=["Alex","Wen","Nicu","Dani","Mat"]

    def SetSelectedCharacter(self, name):
        self.selectedCharacter = name

    def SetPlayerName(self, name):
        self.playerName = name

    def startCombant(self):
        self.buttonBar=tk.PhotoImage(file="assets/img/buttonBar.png")
        self.playerPokemons=[]
        for p in self.selectedPokes.selectedPokemons:
            self.playerPokemons.append(Pk.Pokemon.newPokemon(self.selectedPokes.pokeList[p],self.movementList))
        self.characters.remove(self.selectedCharacter)
        self.selectedEnemyChar=self.characters.pop(random.randint(0,len(self.characters)-1))
        self.enemyPokemons=[]
        for i in range(0,3):
            pok=self.selectedPokes.pokeList[random.randint(0,len(self.selectedPokes.pokeList)-1)]
            self.enemyPokemons.append(Pk.Pokemon.newPokemon(pok,self.movementList))
        self.setUpChar()
        self.frm.create_image(512/2, 342, image=self.buttonBar, anchor="center")
        self.enemyIntro=True
    
    def moveChar(self):
        #mueve enemigo    
        x,y=self.frm.coords(self.enemyImgPlacement)
        if x > self.targetEnemyImg:
            dx=(self.targetEnemyImg-x)*0.1
            self.frm.move(self.enemyImgPlacement,dx,0)
            if abs(dx)<0.2:
                self.enemyIntro=False

        if self.enemyIntro==False:
            #mueve jugador
            x,y=self.frm.coords(self.playerImgPlacement)
            if x < self.targetPlayerImg:
                dx=(self.targetPlayerImg-x)*0.1
                self.frm.move(self.playerImgPlacement,dx,0)

        self.frm.after(33,self.moveChar)

    def setUpChar(self):
        self.playerCharimg = tk.PhotoImage(file="assets/trainers/"+self.selectedCharacter+"Back.png")
        self.enemyCharimg = tk.PhotoImage(file="assets/trainers/"+self.selectedEnemyChar+".png")
        self.targetPlayerImg = 88
        self.targetEnemyImg = 353
        self.playerImgPlacement = self.frm.create_image(-230, 100, image=self.playerCharimg, anchor="nw")
        self.frm.after(33,self.moveChar)
        self.enemyImgPlacement = self.frm.create_image(513, 32, image=self.enemyCharimg, anchor="nw")