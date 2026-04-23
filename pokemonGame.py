import Core.PokemonLib as Pk
import tkinter as tk
import Core.StartMenu as SM
import Core.SelectChar as SC
import Core.SelectPoke as SP
import Core.BattleScreen as BS

class App(tk.Tk):

    def startCallBack(self,event):
        self.showScreen(self.screen2)
        self.screen4.SetPlayerName(self.screen1.playerName)
    
    def selectedCallBack(self,charName):
        self.selectedCharacter=charName
        self.screen4.SetSelectedCharacter(charName)
        self.showScreen(self.screen3)

    def selectedPokemons(self,pokemons):
        self.showScreen(self.screen4)
        self.screen4.startCombant()
    
    def battleCallBack(self,pokemons):
        print("funca")

    def __init__(self):
        super().__init__()
        self.geometry("512x384")
        self.resizable(False,False)
        self.frm = tk.Frame(self, width=512, height=384, background="red")
        self.frm.pack(fill="both", expand=True)
        #bg = tk.PhotoImage(file="assets\img\Battleground.png")S
        #lbg = tk.Label(root,image=bg)
        #lbg.place(x=0,y=0,relwidth=1,relheight=1)
        self.screen1 = SM.StartMenu(self.frm, self.startCallBack)
        self.screen2 = SC.SelectChar(self.frm, self.selectedCallBack)
        self.screen3 = SP.SelectPoke(self.frm, self.selectedPokemons)
        self.screen4 = BS.BattleScreen(self.frm, self.battleCallBack, self.screen3)
        self.currentScreen=self.screen1

    def showScreen(self,screen):
        if self.currentScreen:
            self.currentScreen.frm.pack_forget()
        self.currentScreen=screen
        self.currentScreen.frm.pack(fill="both", expand=True)
    

app = App()
app.mainloop()