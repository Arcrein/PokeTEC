import tkinter as tk
from tkinter import font
from tkinter import ttk
import Core.PokemonLib as Pk

class Leaderboard:
    def __init__(self, root):
        width=512
        height=384
        marginX=50
        boardY=60
        boardX=width/2
        boardWidth=width-marginX*2
        boardHeight=height-100
        self.frm = tk.Canvas(root, width=512, height=384, bg="white")
        self.frm.pack(fill="both", expand=True)
        titleFont = font.Font(family="System", size=20, weight="bold")
        self.captionFont = font.Font(family="Terminal",size=-17,weight="bold")
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0, 0, image=self.bg, anchor="nw")
        self.frm.create_text(252,22,text="High Scores",fill="black",font=titleFont)
        self.frm.create_text(250,20,text="High Scores",fill="violet",font=titleFont)
        self.leaderboardFrame=tk.Frame(self.frm,bg="black")
        columns=("Ranking","Name","Score")
        self.leaderboardControl=ttk.Treeview(self.leaderboardFrame,columns=columns,show="headings")
        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Custom2.Treeview",font=self.captionFont,background="black",fieldbackground="black",foreground="white")
        self.style.configure("Custom2.Treeview.Heading",font=titleFont,foreground="black")
        self.leaderboardControl.configure(style="Custom2.Treeview")
        self.leaderboardControl.heading("Ranking",text="Rank")
        self.leaderboardControl.heading("Name",text="Name")
        self.leaderboardControl.heading("Score",text="Score")
        self.leaderboardControl.column("Ranking",width=60,anchor="center")
        self.leaderboardControl.column("Name",width=180,anchor="w")
        self.leaderboardControl.column("Score",width=100,anchor="e")
        self.scrollbar=ttk.Scrollbar(self.leaderboardFrame,orient="vertical",command=self.leaderboardControl.yview)
        self.leaderboardControl.configure(yscrollcommand=self.scrollbar.set)
        self.leaderboardControl.grid(row=0,column=0,sticky="nsew")
        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.leaderboardFrame.grid_rowconfigure(0,weight=1)
        self.leaderboardFrame.grid_columnconfigure(0,weight=1)
        self.frm.create_window(boardX,boardY,window=self.leaderboardFrame,width=boardWidth,height=boardHeight,anchor="n")

    def showLeaderboard(self, scoreboard:list[Pk.Leaderboard]):
        scoreboard.sort(key=lambda x: x.Puntaje,reverse=True)
        for i in range(0,len(scoreboard)):
            self.leaderboardControl.insert("","end",values=(i+1,scoreboard[i].PlayerName,int(scoreboard[i].Puntaje)))