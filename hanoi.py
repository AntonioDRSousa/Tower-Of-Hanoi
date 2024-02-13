import tkinter as tk
from tkinter import Tk, ttk, Label, Spinbox, messagebox
from math import inf

Y0 = 50
Y1 = 200

class Tower:
    def __init__(self,ndisks):
        self.t1 = []
        self.t2 = []
        self.t3 = []
        for i in range(0,ndisks):
            self.t1.append(ndisks-i)
            
    def add(self,id,x):
        if id==1:
            self.t1.append(x)
        elif id==2:
            self.t2.append(x)
        elif id==3:
            self.t3.append(x)
    
    def top(self,id):
        def tp(t):
            if len(t)==0:
                return inf
            else:
                return t[-1]
        if id==1:
            return tp(self.t1)
        elif id==2:
            return tp(self.t2)
        elif id==3:
            return tp(self.t3)
            
    def pop(self,id):
        if id==1:
            return self.t1.pop()
        elif id==2:
            return self.t2.pop()
        elif id==3:
            return self.t3.pop()
            
    def isEmpty(self,id):
        if id==1:
            return len(self.t1)==0
        elif id==2:
            return len(self.t2)==0
        elif id==3:
            return len(self.t3)==0

class Hanoi:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("220x100")
        self.win.resizable(False,False)
        self.win.title("HANOI")
        self.createMenu()
        
    def createMenu(self):
        self.Lab = Label(self.win,text='Number of Disks : ')
        
        self.num = tk.IntVar(value=3)
        self.Spin = Spinbox(self.win,justify = tk.CENTER, from_ = 3, to = 64, state = 'readonly', textvariable=self.num, wrap=True)
        
        self.But = ttk.Button(self.win,text='Start') 
        
        self.Lab.grid(row=0,column=0,sticky="news")
        self.Spin.grid(row=1,column=0,sticky="news")
        self.But.grid(row=2,column=0,sticky="news")
        
        self.But.bind("<Button-1>",self.game)
        
        self.win.mainloop()
        
    def clear(self):
        for i in self.win.winfo_children():
            i.destroy()
        
    def game(self,event):
        self.num_moves = 0
        self.ndisks = int(self.Spin.get())
        self.clear()
        self.dim = (840,300)
        self.win.geometry(str(self.dim[0])+'x'+str(self.dim[1]))
        self.canvas = tk.Canvas(self.win,width=self.dim[0],height=self.dim[1],bg="white")
        self.canvas.pack()
        
        self.select = None
        
        self.towers = Tower(self.ndisks)
          
        self.posy = []
        self.px = []
        self.dr = (self.dim[0]//(3*(2*self.ndisks+1)))
        self.dy = (Y1-Y0)//(self.ndisks+1)
        
        self.color = {  1 : "red",
                        2 : "green1",
                        3 : "blue",
                        4 : "yellow",
                        5 : "cyan",
                        6 : "magenta",
                        7 : "orange",
                        8 : "purple",
                        9 : "pink"
                     }
        
        
        self.calcPos()
        self.draw()
        
        self.canvas.create_rectangle(0,Y0+(self.ndisks+1)*self.dy,self.dim[0],self.dim[1],fill="white")
    
        b1 = ttk.Button(self.win,text='1',width=5)
        b1.place(x=(self.ndisks)*self.dr,y=self.dim[1]-50)
        b1.bind('<Button 1>', self.gtower1)
        
        b2 = ttk.Button(self.win,text='2',width=5)
        b2.place(x=3*(self.ndisks)*self.dr+self.dr,y=self.dim[1]-50)
        b2.bind('<Button 1>', self.gtower2)
        
        b3 = ttk.Button(self.win,text='3',width=5)
        b3.place(x=5*(self.ndisks)*self.dr+2*self.dr,y=self.dim[1]-50)
        b3.bind('<Button 1>', self.gtower3)
        
        
    def calcPos(self):
        for j in self.towers.t1:
            y1 = Y0+self.dy*(j)
            y2 = y1+self.dy
            self.posy.append((y1,y2))
     
    def gtower1(self,event):
        self.gtower(1)
        
    def gtower2(self,event):
        self.gtower(2)
    
    def gtower3(self,event):
        self.gtower(3)
        
    def gtower(self,x):
        if (self.select==None):
            if self.towers.isEmpty(x):
                self.select=None
            else:
                self.select=x
        elif (x!=self.select) and (self.towers.top(self.select)<self.towers.top(x)):
            self.towers.add(x,self.towers.pop(self.select))
            self.num_moves += 1
            self.select = None
            self.draw()
            if (len(self.towers.t3)==self.ndisks):
                z = int((2**self.ndisks)-1)
                s = "YOU WIN !\nYou win with "+str(self.num_moves)+" .\n"
                s += "The optimal solutions has "+str(z)+" moves.\n"
                if self.num_moves==z:
                    s += "Your solution is optimal."
                else:
                    s += "Your solution is not optimal."
                messagebox.showinfo("Victory",s)
                self.clear()
                self.createMenu()
        else:
            self.select = None  
        
    def draw(self):
        self.canvas.create_rectangle(0,0,self.dim[0],Y0+(self.ndisks+1)*self.dy,fill="black")
        self.drawRod()
        self.drawTower(self.towers.t1,0)
        self.drawTower(self.towers.t2,1)
        self.drawTower(self.towers.t3,2)
        
    def drawRod(self):
        for i in range(0,3):
            d0 = (2*i+1)*(self.ndisks)*self.dr+i*self.dr
            d1 = d0+self.dr
            self.px.append(d0)
            self.canvas.create_rectangle(d0,Y0,d1,Y1,fill="white",outline="white")
            
    def drawTower(self,t,id):
        for j in range(0,len(t)):
            d0 = self.px[id]-t[j]*self.dr
            d1 = self.px[id]+(t[j]+1)*self.dr
            d2 , d3 = self.posy[j]
            self.canvas.create_rectangle(d0,d2,d1,d3,fill=self.color[((self.ndisks-t[j])%9)+1])

if __name__=="__main__":
    Hanoi()