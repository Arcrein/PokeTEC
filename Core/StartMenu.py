import tkinter as tk

class StartMenu:
    def __init__(self, root, startCallBack):
        self.frm = tk.Canvas(root,width=512,height=384,bg="white")
        #self.frm.place(x=0,y=0,relwidth=1,relheight=1)
        self.frm.pack(fill="both",expand=True)
        self.bg = tk.PhotoImage(file="assets\img\BackMenu.png")
        self.frm.create_image(0,0,image=self.bg,anchor="nw")
        self.btImg = tk.PhotoImage(file="assets\img\Play.png")
        self.startButton = self.frm.create_image(512/2,384/2,image=self.btImg,anchor="center")
        self.frm.tag_bind(self.startButton,"<Button-1>",startCallBack)