import tkinter as tk
from tkinter import font
from tkinter import ttk
import Core.SelectPoke as SP
import Core.PokemonLib as Pk
import math
import random
from enum import Enum
from PIL import Image,ImageTk

class BattleState(Enum):
    EnemyIntro=0
    PlayerIntro=1
    EnemyOutro=2
    EnemyPokemon=3
    PlayerOutro=4
    PlayerPokemon=5
    StartingCombatStart=6
    CombatStart=7
    PlayerFight=8
    EnemyFight=9
    PlayerPokemonOut=10
    EnemyPokemonOut=11
    PkChangeAction=12
    NextEnemyPoke=13
    NextPlayerPoke=14
    Waiting=100

class BattleScreen:
    def __init__(self, root, battleCallBack, selectedPoke: SP.SelectPoke):
        self.titleFont = font.Font(family="System",size=20,weight="bold")
        self.captionFont = font.Font(family="Terminal",size=-17,weight="bold")
        self.subCaptionFont = font.Font(family="Terminal",size=-14,weight="bold")
        self.frm = tk.Canvas(root, width=512, height=384, bg="white")
        self.frm.pack(fill="both", expand=True)
        self.bg = tk.PhotoImage(file="assets\img\Battleground.png")
        self.frm.create_image(0, 0, image=self.bg, anchor="nw")
        self.battleCallBack = battleCallBack
        self.selectedCharacter = ""
        self.playerName = ""
        self.selectedPokes = selectedPoke
        self.movementList:list[Pk.PokemonMove]=Pk.loadMoves("docs\pokemonMoves.csv")
        self.effectiveness:list[Pk.PokemonEffectiveness]=Pk.loadEffectiveness("docs\pokemonEffectiveness.csv")
        self.characters=["Alex","Wen","Nicu","Dani","Mat"]
        self.visualControlText=-1
        self.enemyPokemonPos=382
        self.currentEnemyPkPlacement=self.frm.create_image(self.enemyPokemonPos, 135, image=None, anchor="center")
        self.playerPokemonPos=166
        self.currentPlayerPkPlacement=self.frm.create_image(self.playerPokemonPos, 240, image=None, anchor="center")
        self.buttonBar=tk.PhotoImage(file="assets/img/buttonBar.png")
        self.enemyPokeScale=1.7
        self.playerPokeScale=1.7
        self.runningText = False
        self.attackNum=0
        self.attackSpeedAnim=6
        self.selectPokemonControl=ttk.Treeview(self.frm)
        self.selectPokemonControl["columns"]=("name",)
        self.selectPokemonControl.column("#0",width=50)
        self.selectPokemonControl.column("name",width=150)
        self.selectPokemonControl.heading("name",text="Pokemon")
        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Custom.Treeview",font=self.captionFont,rowheight=50,background="royalblue",fieldbackground="royalblue",foreground="white")
        self.style.configure("Custom.Treeview.Heading",font=self.titleFont)
        self.selectPokemonControl.configure(style="Custom.Treeview")
        self.selectPokemonControl.bind("<<TreeviewSelect>>",self.onSelectPoke)
        self.selPkImg={}
        self.targetPlayerPoke = 0
        self.puntuacion = 0

    def onSelectPoke(self,event):
        selected=self.selectPokemonControl.selection()
        if selected:
            item_id = selected[0]
            item = self.selectPokemonControl.item(item_id)
            pkId = item["values"][1]
            self.hideSelectPoke()
            self.targetPlayerPoke = next((i for i, p in enumerate(self.playerPokemons) if p.id == pkId), None)
            self.currentState = BattleState.PlayerPokemonOut
            

    def fillPokeList(self):
        self.selectPokemonControl.delete(*self.selectPokemonControl.get_children())
        for pk in self.playerPokemons:
            self.selPkImg[pk.id]=tk.PhotoImage(file=f"assets\img\{pk.Especie.name}.png").subsample(2,2)
            self.selectPokemonControl.insert("","end",text="",image=self.selPkImg[pk.id],values=(pk.Especie.name,pk.id))

    def showSelectPoke(self):
        self.fillPokeList()
        self.selectPokemonControl.pack(fill="both",expand=True)

    def hideSelectPoke(self):
        self.selectPokemonControl.pack_forget()

    def SetSelectedCharacter(self, name):
        self.selectedCharacter = name

    def SetPlayerName(self, name):
        self.playerName = name

    def startCombant(self):
        self.currentState=BattleState.EnemyIntro
        self.playerPokemons:list[Pk.Pokemon]=[]
        idPk =0
        for p in self.selectedPokes.selectedPokemons:
            self.playerPokemons.append(Pk.Pokemon.newPokemon(idPk,self.selectedPokes.pokeList[p],self.movementList))
            idPk = idPk + 1
        self.characters.remove(self.selectedCharacter)
        self.selectedEnemyChar=self.characters.pop(random.randint(0,len(self.characters)-1))
        self.enemyPokemons:list[Pk.Pokemon]=[]
        for i in range(0,3):
            pok=self.selectedPokes.pokeList[random.randint(0,len(self.selectedPokes.pokeList)-1)]
            self.enemyPokemons.append(Pk.Pokemon.newPokemon(idPk, pok,self.movementList))
            idPk = idPk + 1
        self.setUpChar()
        self.enemyIntro=True
        self.frm.create_image(512/2, 342, image=self.buttonBar, anchor="center")
        self.textboxImg=tk.PhotoImage(file="assets/img/textBar.png")
        self.textbox=self.frm.create_image(4,291,image=self.textboxImg,anchor="nw")
        self.frm.itemconfig(self.textbox,state="hidden")
        if self.visualControlText==-1:
            self.visualControlText=self.frm.create_text(512/2,340,text=self.actualText,fill="black",font=self.titleFont,anchor="center",width=500)
        self.ButtonsImg={}
        self.ButtonsImgDis={}
        self.Buttons={}
        self.AttackButton= []
        self.AttactLabel = []
        self.AttactSubLabel = []
        self.setUpButton("bag",380,295)
        self.setUpButton("pokemon",254,339)
        self.setUpButton("run",378,340)
        self.setUpButton("fight",251,294)
        self.frm.itemconfig(self.Buttons["bag"],state="hidden")
        self.frm.itemconfig(self.Buttons["pokemon"],state="hidden")
        self.frm.itemconfig(self.Buttons["run"],state="hidden")
        self.frm.itemconfig(self.Buttons["fight"],state="hidden")
        self.createEnemyLifeBar()
        self.createPlayerLifeBar()
        self.tapada=self.frm.create_image(512/2, 342, image=self.buttonBar, anchor="center")
        self.frm.itemconfig(self.tapada,state="hidden")
        self.createAttackButton(4,297)
        self.createAttackButton(4,338)
        self.createAttackButton(185,297)
        self.createAttackButton(185,338)
        self.hideAttackButtons()

    def newEnemyPk(self,nextState):
        self.animateText(self.selectedEnemyChar+" envio a "+self.enemyPokemons[self.currentEnemyPokeIndex].Especie.name)
        self.currentEnemyPkImg=Pk.loadGif(f"assets\gif\{self.enemyPokemons[self.currentEnemyPokeIndex].Especie.front_gif}",1.7)
        self.currentEnemyPkFrm=0
        w,h = self.currentEnemyPkImg[self.currentEnemyPkFrm].size
        self.enemyPokeScale=0.2
        self.currentEnemyPkFrmImg=ImageTk.PhotoImage(self.currentEnemyPkImg[self.currentEnemyPkFrm].resize((int(w*self.enemyPokeScale),int(h*self.enemyPokeScale)),Image.Resampling.LANCZOS))
        self.frm.itemconfig(self.currentEnemyPkPlacement,image=self.currentEnemyPkFrmImg)
        self.showEnemyLifeBar(self.enemyPokemons[self.currentEnemyPokeIndex])
        self.currentState=nextState

    def newPlayerPk(self,nextState):
        self.animateText(self.playerName+" envio a "+self.playerPokemons[self.currentPlayerPokeIndex].Especie.name)
        self.currentPlayerPkImg=Pk.loadGif(f"assets\gif\{self.playerPokemons[self.currentPlayerPokeIndex].Especie.back_gif}",1.7)
        self.currentPlayerPkFrm=0
        w,h = self.currentPlayerPkImg[self.currentPlayerPkFrm].size
        self.playerPokeScale=0.2
        self.currentPlayerPkFrmImg=ImageTk.PhotoImage(self.currentPlayerPkImg[self.currentPlayerPkFrm].resize((int(w*self.playerPokeScale),int(h*self.playerPokeScale)),Image.Resampling.LANCZOS))
        self.frm.itemconfig(self.currentPlayerPkPlacement,image=self.currentPlayerPkFrmImg)
        self.showPlayerLifeBar(self.playerPokemons[self.currentPlayerPokeIndex])
        self.currentState=nextState

    def disableButtons(self):
        for btName in self.Buttons:
            self.frm.itemconfig(self.Buttons[btName],image=self.ButtonsImgDis[btName])
            self.frm.tag_unbind(self.Buttons[btName], "<Button-1>")

    def enableButtons(self):
        for btName in self.Buttons:
            self.frm.itemconfig(self.Buttons[btName],image=self.ButtonsImg[btName])
            self.frm.tag_bind(self.Buttons[btName], "<Button-1>", lambda e, name=btName: self.onClick(name))
    
    def moveChar(self):
        if self.currentState == BattleState.EnemyIntro:
            #mueve enemigo    
            x,y=self.frm.coords(self.enemyImgPlacement)
            if x > self.targetEnemyImg:
                dx=(self.targetEnemyImg-x)*0.1
                self.frm.move(self.enemyImgPlacement,dx,0)
                if abs(dx)<0.2:
                    self.currentState=BattleState.PlayerIntro

        elif self.currentState == BattleState.PlayerIntro:
            #mueve jugador
            x,y=self.frm.coords(self.playerImgPlacement)
            if x < self.targetPlayerImg:
                dx=(self.targetPlayerImg-x)*0.05
                self.frm.move(self.playerImgPlacement,dx,0)
                if abs(dx)<0.2:
                    self.currentState=BattleState.EnemyOutro
        
        elif self.currentState == BattleState.EnemyOutro:
            #saca el enemigo
            x,y=self.frm.coords(self.enemyImgPlacement)
            if x < 513:
                dx=max((x-self.targetEnemyImg)*0.1,-0.1)
                self.frm.move(self.enemyImgPlacement,dx,0)
            if x>=513:
                self.currentEnemyPokeIndex=0
                self.newEnemyPk(BattleState.EnemyPokemon)
                
        
        elif self.currentState == BattleState.EnemyPokemon:
           
            if self.enemyPokeScale < 1:
                self.enemyPokeScale=self.enemyPokeScale+0.05
            else:
                self.currentState = BattleState.PlayerOutro
            self.enemyPermaAnim(self.enemyPokeScale)

        elif self.currentState == BattleState.PlayerOutro:
            self.enemyPermaAnim(self.enemyPokeScale)
            x,y=self.frm.coords(self.playerImgPlacement)
            if x > -230:
                dx=min((x-self.targetPlayerImg)*0.05,-1)
                self.frm.move(self.playerImgPlacement,dx,0)
            if x<=-230:
                self.currentState=BattleState.PlayerPokemon
                self.currentPlayerPokeIndex=0
                self.animateText(self.playerName+" envio a "+self.playerPokemons[self.currentPlayerPokeIndex].Especie.name)
                self.currentPlayerPkImg=Pk.loadGif(f"assets\gif\{self.playerPokemons[self.currentPlayerPokeIndex].Especie.back_gif}",2.5)
                self.currentPlayerPkFrm=0
                w,h = self.currentPlayerPkImg[self.currentPlayerPkFrm].size
                self.playerPokeScale=0.2
                self.playerPermaAnim(self.playerPokeScale)
        
        elif self.currentState == BattleState.PlayerPokemon or self.currentState == BattleState.StartingCombatStart:
            self.enemyPermaAnim(self.enemyPokeScale)
            if self.playerPokeScale < 1:
                self.playerPokeScale=self.playerPokeScale+0.05
            else:
                if self.currentState == BattleState.PlayerPokemon:
                    self.currentState = BattleState.StartingCombatStart
                    self.frm.after(3000,self.startBattle)
            self.playerPermaAnim(self.playerPokeScale)
            
        
        elif self.currentState == BattleState.CombatStart:
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)

        
        elif self.currentState == BattleState.PlayerFight:
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)
            x,y=self.frm.coords(self.currentPlayerPkPlacement)
            if self.startingAttack==True and x>=self.playerPokemonPos-50:
                self.frm.move(self.currentPlayerPkPlacement,-self.attackSpeedAnim,0)
            else:
                self.startingAttack=False
                if x<self.playerPokemonPos:
                    self.frm.move(self.currentPlayerPkPlacement,self.attackSpeedAnim,0)
                else:
                    if not self.attackCompleted:
                        self.attackCompleted = True
                        self.playerDealDamage()
        
        elif self.currentState == BattleState.EnemyFight:
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)
            x,y=self.frm.coords(self.currentEnemyPkPlacement)
            if self.startingAttack==True and x>=self.enemyPokemonPos-50:
                self.frm.move(self.currentEnemyPkPlacement,-self.attackSpeedAnim,0)
            else:
                self.startingAttack=False
                if x<self.enemyPokemonPos:
                    self.frm.move(self.currentEnemyPkPlacement,self.attackSpeedAnim,0)
                else:
                    if not self.attackCompleted:
                        self.attackCompleted = True
                        self.enemyDealDamage()
        
        elif self.currentState == BattleState.NextEnemyPoke:
            if self.enemyPokeScale < 1:
                self.enemyPokeScale=self.enemyPokeScale+0.05
            else:
                self.currentState = BattleState.CombatStart
                self.enableButtons()
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)

        elif self.currentState == BattleState.NextPlayerPoke:
            self.enemyPermaAnim(self.enemyPokeScale)
            if self.playerPokeScale < 1.4:
                self.playerPokeScale=self.playerPokeScale+0.05
            else:
                self.currentState = BattleState.CombatStart
                self.enableButtons()
            self.playerPermaAnim(self.playerPokeScale)

        elif self.currentState == BattleState.PlayerPokemonOut:
            if self.playerPokeScale > 0.2:
                self.playerPokeScale=self.playerPokeScale-0.05
            else:
                if self.playerPokemons[self.currentPlayerPokeIndex].Health == 0:
                    deadPoke=self.playerPokemons.pop(self.currentPlayerPokeIndex)
                    deadPoke.Health=deadPoke.MaxHealth
                    self.enemyPokemons.append(deadPoke)
                    if len(self.playerPokemons)>0:
                        self.showSelectPoke()
                    else:
                        self.battleCallBack(self.puntuacion)
                    self.currentState = BattleState.Waiting
                else:
                    self.currentPlayerPokeIndex = self.targetPlayerPoke
                    self.newPlayerPk(BattleState.NextPlayerPoke)
               
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)
        
        elif self.currentState == BattleState.EnemyPokemonOut:
            self.playerPermaAnim(self.playerPokeScale)
            if self.enemyPokeScale > 0.2:
                self.enemyPokeScale=self.enemyPokeScale-0.05
            else:
                deadPoke=self.enemyPokemons.pop(self.currentEnemyPokeIndex)
                deadPoke.Health=deadPoke.MaxHealth
                self.playerPokemons.append(deadPoke)
                self.puntuacion = self.puntuacion + 1
                if len(self.enemyPokemons)>0:
                    self.currentEnemyPokeIndex=random.randint(0,len(self.enemyPokemons)-1)
                    self.frm.after(3000,self.newEnemyPk,BattleState.NextEnemyPoke)
                else:
                    self.battleCallBack(self.puntuacion)
                self.currentState = BattleState.Waiting
            self.enemyPermaAnim(self.enemyPokeScale)
        
        elif self.currentState == BattleState.Waiting:
            self.enemyPermaAnim(self.enemyPokeScale)
            self.playerPermaAnim(self.playerPokeScale)

        
        self.frm.after(35,self.moveChar)

    def startBattle(self):
        self.currentState = BattleState.CombatStart
        self.frm.itemconfig(self.Buttons["bag"],state="normal")
        self.frm.itemconfig(self.Buttons["pokemon"],state="normal")
        self.frm.itemconfig(self.Buttons["run"],state="normal")
        self.frm.itemconfig(self.Buttons["fight"],state="normal")
        self.frm.itemconfig(self.textbox,state="normal")
        self.frm.coords(self.visualControlText,116,337)
        self.frm.itemconfig(self.visualControlText,width=220)
        self.animateText(f"Que quires que haga {self.playerPokemons[self.currentPlayerPokeIndex].Especie.name}?")
        self.showEnemyLifeBar(self.enemyPokemons[self.currentEnemyPokeIndex])
        self.showPlayerLifeBar(self.playerPokemons[self.currentPlayerPokeIndex])

    def createEnemyLifeBar(self):
        self.enemyLifeBarBgImg=tk.PhotoImage(file="assets\img\pokeLifeBarLeft.png")
        self.enemyLifeBarBg=self.frm.create_image(0,0,image=self.enemyLifeBarBgImg, anchor="nw")
        self.enemyPkNameLbl=self.frm.create_text(10,14,text="tyranitar",font=self.captionFont,anchor="nw",fill="dimgray")
        self.enemyPkLifeBar=self.frm.create_rectangle(103,40,198,45,fill="green")
        self.frm.itemconfig(self.enemyLifeBarBg,state="hidden")
        self.frm.itemconfig(self.enemyPkNameLbl,state="hidden")
        self.frm.itemconfig(self.enemyPkLifeBar,state="hidden")

    def createPlayerLifeBar(self):
        self.playerLifeBarBgImg=tk.PhotoImage(file="assets\img\pokeLifeBarRight.png")
        self.playerLifeBarBg=self.frm.create_image(511,286,image=self.playerLifeBarBgImg, anchor="se")
        self.playerPkNameLbl=self.frm.create_text(302,224,text="tyranitar",font=self.captionFont,anchor="nw",fill="dimgray")
        self.playerPkLifeBar=self.frm.create_rectangle(404,252,499,257,fill="green")
        self.lifeNum=self.frm.create_text(443,271,text="69/69",font=self.captionFont,anchor="center",fill="dimgray")
        self.frm.itemconfig(self.playerLifeBarBg,state="hidden")
        self.frm.itemconfig(self.playerPkNameLbl,state="hidden")
        self.frm.itemconfig(self.playerPkLifeBar,state="hidden")
        self.frm.itemconfig(self.lifeNum,state="hidden")

    def showEnemyLifeBar(self,pokemon:Pk.Pokemon):
        self.frm.itemconfig(self.enemyLifeBarBg,state="normal")
        self.frm.itemconfig(self.enemyPkNameLbl,state="normal",text=pokemon.Especie.name)
        self.frm.itemconfig(self.enemyPkLifeBar,state="normal")
        self.updateEnemyLifeBar(pokemon)
        
    def updateEnemyLifeBar(self,pokemon:Pk.Pokemon):
        hpPercent=pokemon.Health/pokemon.MaxHealth
        maxWidth=198-103
        newX=103+(maxWidth*hpPercent)
        self.frm.coords(self.enemyPkLifeBar,103,40,newX,45)

    def showPlayerLifeBar(self,pokemon:Pk.Pokemon):
        self.frm.itemconfig(self.playerLifeBarBg,state="normal")
        self.frm.itemconfig(self.playerPkNameLbl,state="normal",text=pokemon.Especie.name)
        self.frm.itemconfig(self.playerPkLifeBar,state="normal")
        self.updatePlayerLifeBar(pokemon)
    
    def updatePlayerLifeBar(self,pokemon:Pk.Pokemon):
        hpPercent=pokemon.Health/pokemon.MaxHealth
        maxWidth=499-404
        newX=404+(maxWidth*hpPercent)
        self.frm.itemconfig(self.lifeNum,state="normal",text=f"{int(pokemon.Health)}/{int(pokemon.MaxHealth)}")
        self.frm.coords(self.playerPkLifeBar,404,252,newX,257)

    def playerDoAttack(self,movement:int):
        self.disableButtons()
        self.PlayerAttackToUse=movement
        self.EnemyAttackToUse=random.randint(0,3)
        pkmovement=self.playerPokemons[self.currentPlayerPokeIndex].Moveset[self.PlayerAttackToUse]
        enemyMovement=self.enemyPokemons[self.currentEnemyPokeIndex].Moveset[self.EnemyAttackToUse]
        self.hideAttackButtons()
        self.attackNum=0
        self.startingAttack=True
        self.attackCompleted = False
        if self.playerPokemons[self.currentPlayerPokeIndex].Especie.speed >= self.enemyPokemons[self.currentEnemyPokeIndex].Especie.speed:
            self.currentState=BattleState.PlayerFight
            self.animateText(f"{self.playerPokemons[self.currentPlayerPokeIndex].Especie.name} uso {pkmovement.nombre}")
        else:
            self.currentState=BattleState.EnemyFight
            self.animateText(f"{self.enemyPokemons[self.currentEnemyPokeIndex].Especie.name} uso {enemyMovement.nombre}")

    def playerDealDamage(self):
        pkmovement=self.playerPokemons[self.currentPlayerPokeIndex].Moveset[self.PlayerAttackToUse]
        dmg,mod=Pk.dmgCalc(self.effectiveness,
                       self.playerPokemons[self.currentPlayerPokeIndex],
                       pkmovement,
                       self.enemyPokemons[self.currentEnemyPokeIndex]
                       )
        self.enemyPokemons[self.currentEnemyPokeIndex].Health=self.enemyPokemons[self.currentEnemyPokeIndex].Health-dmg
        if self.enemyPokemons[self.currentEnemyPokeIndex].Health <= 0:
            self.enemyPokemons[self.currentEnemyPokeIndex].Health = 0

        self.updateEnemyLifeBar(self.enemyPokemons[self.currentEnemyPokeIndex])
        self.attackNum=self.attackNum+1
        self.waitForAnimText(self.showEffectiveness,mod,True)

    def enemyDealDamage(self):
        pkmovement=self.enemyPokemons[self.currentEnemyPokeIndex].Moveset[self.EnemyAttackToUse]
        dmg,mod=Pk.dmgCalc(self.effectiveness,
                       self.enemyPokemons[self.currentEnemyPokeIndex],
                       pkmovement,
                       self.playerPokemons[self.currentPlayerPokeIndex]
                       )
        self.playerPokemons[self.currentPlayerPokeIndex].Health=self.playerPokemons[self.currentPlayerPokeIndex].Health-dmg
        if self.playerPokemons[self.currentPlayerPokeIndex].Health <= 0:
            self.playerPokemons[self.currentPlayerPokeIndex].Health = 0

        self.updatePlayerLifeBar(self.playerPokemons[self.currentPlayerPokeIndex])
        self.attackNum=self.attackNum+1
        self.waitForAnimText(self.showEffectiveness,mod,False)

    def showEffectiveness(self, mod,isPlayer):
        if mod == 4:
            self.animateText("El ataque fue super efectivo")
        elif mod == 2:
            self.animateText("El ataque fue efectivo")
        elif mod <= 0.5:
            self.animateText("El ataque fue poco efectivo")
        self.frm.after(3000, self.CheckNextAttack, isPlayer)
    
    def CheckNextAttack(self, isPlayer):
        if self.attackNum < 2:
            if isPlayer == True:
                if self.enemyPokemons[self.currentEnemyPokeIndex].Health>0:
                    self.currentState=BattleState.EnemyFight
                    self.startingAttack=True
                    self.attackCompleted = False
                    enemyMovement=self.enemyPokemons[self.currentEnemyPokeIndex].Moveset[self.EnemyAttackToUse]
                    self.animateText(f"{self.enemyPokemons[self.currentEnemyPokeIndex].Especie.name} uso {enemyMovement.nombre}")
                else:
                    self.currentState=BattleState.EnemyPokemonOut
                    self.animateText(f"El {self.enemyPokemons[self.currentEnemyPokeIndex].Especie.name} de {self.selectedEnemyChar} ya no puede continuar")
            else:
                if self.playerPokemons[self.currentPlayerPokeIndex].Health>0:
                    self.currentState=BattleState.PlayerFight
                    self.startingAttack=True
                    self.attackCompleted = False
                    pkmovement=self.playerPokemons[self.currentPlayerPokeIndex].Moveset[self.PlayerAttackToUse]
                    self.animateText(f"{self.playerPokemons[self.currentPlayerPokeIndex].Especie.name} uso {pkmovement.nombre}")
                else:
                    self.currentState=BattleState.PlayerPokemonOut
                    self.animateText(f"{self.playerPokemons[self.currentPlayerPokeIndex].Especie.name} ya no puede continuar") 
        else:
            if isPlayer == True:
                if self.enemyPokemons[self.currentEnemyPokeIndex].Health == 0:
                    self.currentState=BattleState.EnemyPokemonOut
                    self.animateText(f"El {self.enemyPokemons[self.currentEnemyPokeIndex].Especie.name} de {self.selectedEnemyChar} ya no puede continuar")
                else:
                    self.attackNum=0
                    self.currentState=BattleState.CombatStart
                    self.animateText(f"Que quires que haga {self.playerPokemons[self.currentPlayerPokeIndex].Especie.name}?")
                    self.enableButtons()
            else:
                if self.playerPokemons[self.currentPlayerPokeIndex].Health == 0:
                    self.currentState=BattleState.PlayerPokemonOut
                    self.animateText(f"{self.playerPokemons[self.currentPlayerPokeIndex].Especie.name} ya no puede continuar") 
                else:
                    self.attackNum=0
                    self.currentState=BattleState.CombatStart
                    self.animateText(f"Que quires que haga {self.playerPokemons[self.currentPlayerPokeIndex].Especie.name}?")
                    self.enableButtons()


    def createAttackButton(self,x,y):
        self.AttackButton.append(self.frm.create_rectangle(x,y, x+180, y+40, fill="whitesmoke", outline="dimgray", width=2))
        self.AttactLabel.append(self.frm.create_text(x+4, y+4, text="Psychic Fangs", font=self.captionFont, anchor="nw"))
        self.AttactSubLabel.append(self.frm.create_text(x+4, y+20, text="Electric", font=self.subCaptionFont, fill="gray", anchor="nw"))
        self.frm.tag_bind(self.AttackButton[len(self.AttackButton)-1], "<Button-1>", lambda e,index=len(self.AttackButton)-1: self.playerDoAttack(index))
        self.frm.tag_bind(self.AttactLabel[len(self.AttackButton)-1], "<Button-1>", lambda e,index=len(self.AttackButton)-1: self.playerDoAttack(index))
        self.frm.tag_bind(self.AttactSubLabel[len(self.AttackButton)-1], "<Button-1>", lambda e,index=len(self.AttackButton)-1: self.playerDoAttack(index))

    def hideAttackButtons(self):
        self.frm.itemconfig(self.tapada,state="hidden")
        for i in range(0,len(self.AttackButton)):
            self.frm.itemconfig(self.AttackButton[i], state="hidden")
            self.frm.itemconfig(self.AttactLabel[i], state="hidden")
            self.frm.itemconfig(self.AttactSubLabel[i], state="hidden")

    def showAttackButtons(self,attacks: list[Pk.PokemonMove]):
        self.frm.itemconfig(self.tapada,state="normal")
        for i in range(0,len(self.AttackButton)):
            self.frm.itemconfig(self.AttackButton[i], state="normal")
            self.frm.itemconfig(self.AttactLabel[i], state="normal", text=attacks[i].nombre )
            self.frm.itemconfig(self.AttactSubLabel[i], state="normal", text=attacks[i].tipo)
        

    def enemyPermaAnim(self,scale):
        self.currentEnemyPkFrm = self.currentEnemyPkFrm+1
        if self.currentEnemyPkFrm >= len(self.currentEnemyPkImg):
            self.currentEnemyPkFrm=0
        if scale != 1:
            w,h = self.currentEnemyPkImg[self.currentEnemyPkFrm].size
            self.currentEnemyPkFrmImg=ImageTk.PhotoImage(self.currentEnemyPkImg[self.currentEnemyPkFrm].resize((int(w*scale),int(h*scale)),Image.Resampling.LANCZOS))
        else:
            self.currentEnemyPkFrmImg=ImageTk.PhotoImage(self.currentEnemyPkImg[self.currentEnemyPkFrm])
        self.frm.itemconfig(self.currentEnemyPkPlacement,image=self.currentEnemyPkFrmImg)
    
    def playerPermaAnim(self,scale):
        self.currentPlayerPkFrm = self.currentPlayerPkFrm+1
        if self.currentPlayerPkFrm >= len(self.currentPlayerPkImg):
            self.currentPlayerPkFrm=0
        if scale != 1:
            w,h = self.currentPlayerPkImg[self.currentPlayerPkFrm].size
            self.currentPlayerPkFrmImg=ImageTk.PhotoImage(self.currentPlayerPkImg[self.currentPlayerPkFrm].resize((int(w*scale),int(h*scale)),Image.Resampling.LANCZOS))
        else:
            self.currentPlayerPkFrmImg=ImageTk.PhotoImage(self.currentPlayerPkImg[self.currentPlayerPkFrm])
        self.frm.itemconfig(self.currentPlayerPkPlacement,image=self.currentPlayerPkFrmImg)

    def setUpChar(self):
        self.playerCharimg = tk.PhotoImage(file="assets/trainers/"+self.selectedCharacter+"Back.png")
        self.enemyCharimg = tk.PhotoImage(file="assets/trainers/"+self.selectedEnemyChar+".png")
        self.targetPlayerImg = 88
        self.targetEnemyImg = 353
        self.playerImgPlacement = self.frm.create_image(-230, 100, image=self.playerCharimg, anchor="nw")
        self.frm.after(35,self.moveChar)
        self.enemyImgPlacement = self.frm.create_image(513, 32, image=self.enemyCharimg, anchor="nw")
        self.animateText("Fuiste retado por "+self.selectedEnemyChar)
    
    def animateText(self,text):
        self.targetText=text
        self.actualText=""
        self.runningText = True
        self.escrituraAnimada(0)

    def escrituraAnimada(self,index=0):
        if index <= len(self.targetText):
            self.actualText = self.targetText[:index]
            self.frm.itemconfig(self.visualControlText,text=self.actualText)
            self.frm.after(50,self.escrituraAnimada,index+1)
        else:
            self.runningText = False
    
    def onClick(self,btName):
        if btName == "fight":
            self.showAttackButtons(self.playerPokemons[self.currentPlayerPokeIndex].Moveset)
        elif btName == "bag":
            print(btName)
        elif btName == "pokemon":
            self.showSelectPoke()
        elif btName == "run":
            print(btName)
    
    def setUpButton(self, btName, x, y):
        img=Image.open("assets/img/"+btName+".png")
        self.ButtonsImg[btName] = ImageTk.PhotoImage(img)
        self.ButtonsImgDis[btName]=ImageTk.PhotoImage(img.convert("L"))
        self.Buttons[btName] = self.frm.create_image(x, y, image=self.ButtonsImg[btName], anchor="nw")
        self.frm.tag_bind(self.Buttons[btName], "<Button-1>", lambda e, name=btName: self.onClick(name))

    def waitForAnimText(self, func, *args):
        if self.runningText:
            self.frm.after(50, lambda: self.waitForAnimText(func, *args))
        else:
            func(*args)