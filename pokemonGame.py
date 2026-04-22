import Core.PokemonLib as Pk
import tkinter as tk
import Core.StartMenu as SM
import Core.SelectChar as SC
import Core.SelectPoke as SP

class App(tk.Tk):


    def startCallBack(self,event):
        self.showScreen(self.screen2)
    
    def selectedCallBack(self,charName):
        self.selectedCharacter=charName
        self.showScreen(self.screen3)

    def selectedPokemons(self,pokemons):
        print(pokemons)

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
        self.currentScreen=self.screen1

    def showScreen(self,screen):
        if self.currentScreen:
            self.currentScreen.frm.pack_forget()
        self.currentScreen=screen
        self.currentScreen.frm.pack(fill="both", expand=True)
    
m=Pk.loadMoves("docs\pokemonMoves.csv")
for mst in m:
    print(mst.nombre)
app = App()
app.mainloop()