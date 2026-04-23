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
        print(self.playerName)
        print(self.selectedCharacter)
        self.playerPokemons=[]
        for p in self.selectedPokes.selectedPokemons:
            self.playerPokemons.append(Pk.Pokemon.newPokemon(self.selectedPokes.pokeList[p],self.movementList))
        self.characters.remove(self.selectedCharacter)
        self.selectedEnemyChar=self.characters.pop(random.randint(0,len(self.characters)-1))
        self.enemyPokemons=[]
        for i in range(0,3):
            pok=self.selectedPokes.pokeList[random.randint(0,len(self.selectedPokes.pokeList)-1)]
            self.enemyPokemons.append(Pk.Pokemon.newPokemon(pok,self.movementList))
        print(self.playerPokemons[0].Especie.name)
        print(self.enemyPokemons[0].Especie.name)