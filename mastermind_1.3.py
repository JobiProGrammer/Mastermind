"""
Mastermind - Version 1.3

© by Tobias Jülg / Lennhard Wartena
programmed by Tobias Jülg, designed by Lennhard Wartena
contact: e-mail: tobias@juelg.net, website: http://mineyourlife.net/
bug report: http://mineyourlife.net/bug_report/

LICENCE: It's not allowed to copy the program or content of it without asking one of the owners. It's allowed
	to use the software.

08.05.2016
"""


vers = 1.3   #VERSION



#imorts:
from tkinter import *
from visual import *
from threading import Thread
import random
from time import sleep

#constants:

#if no fullscreen, this hight and width will be used
global win_hight
win_hight=600
global win_width
win_width=900

#globals:

global fullscreen
fullscreen=False

global stoppen
stoppen=False
##############################################################
#klassen für die gui Fenster
##############################################################
class score_frame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.text=""
        try: #probiere

            datei = open('Data_master.mind')
            line0=datei.readline() #1. Zeile
            line1=datei.readline() #2. Zeile
            datei.close()
            if line1=="":
                self.text="No highscore available"
            else:
                t=''
                w=''
                b=False
                for i in line1:
                    if b==True:
                        w=w+i
                    elif i==":":
                        b=True
                        
                    elif b==False:
                        t=t+i
                if w=="":
                    self.text="No highscore available"
                else:
                    self.text = w

        
        except IOError: #falls error
            self.text="No highscore available"

        self.widgets(master)
        
    def widgets(self, master):
        self.label=Label(self, text=("Your Highscore is: "+self.text))
        self.label.grid(column = 0, row=0)
        
        done_button = Button(self, text='OK')
        done_button["command"] = lambda: self.Close(master)
        done_button.grid(row=1)
    def Close(self, master):
        master.destroy()

        

class random_info_frame(Frame):
    def __init__(self, master, Info_text=''):
        Frame.__init__(self, master)
        #self.grid()
        self.pack()
        self.widgets(Info_text, master)
    def widgets(self, Info_text, master):
            self.label=Label(self, text=Info_text)
            self.label.grid(column = 0, row=0)
            self.button=Button(self, text="OK")
            self.button["command"] =lambda: self.close(master)
            self.button.grid(column = 0, padx=55, row=2)
    def close(self, master):
        master.destroy()


class win_before_start(Frame):
    def __init__(self, master, highscore):#, x, z):
        Frame.__init__(self, master)
        #self.grid()
        self.pack()
        self.widgets(master, highscore)#x, z, master)

    def widgets(self, master, highscore):# x, z, master):
       # hi="hallo"
        self.label=Label(self, text="Hier bitte den Spielername angeben:").grid()
        self.eingabe=Entry(self)#, textvariable=name_von_spieler)#.grid()
        #self.entry["command"]=self.name_spieler
        self.eingabe.grid()#sticky=W)
        self.button=Button(self, text="Done")#.grid()#, command=name_spieler).grid()
        self.button["command"] =lambda: self.namespieler(master, highscore)#x, z, master)
        self.button.grid()
        
    def namespieler(self, master, highscore):#x, z, master):
        #global name_von_spieler
        name_von_spieler=self.eingabe.get()
        #savepos(x, z, name_von_spieler)
        
        #print("DIESE CONSOLE IST DUMM")
        fobj = open('Data_master.mind', 'w')
        #fobj.write(str(x) + "\n")
        #fobj.write(str(z) + "\n")
        fobj.write('Playersname:' + name_von_spieler + "\n")
        fobj.write(str(highscore))
        fobj.close()
        master.destroy()
        

class sett(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.widgets(master)
##        if hallo==True:
##            self.destroy(master)
##    def destry(master):
##        master.destroy()
    
    def widgets(self, master):
        "create checkboxes for settings"
        #TODO
        self.label1=Label(self, text='Settings:')
        self.label1.grid()

        #Instructions, checkbuttons
        self.fullscreen = BooleanVar()
        self.checkbutton1 = Checkbutton(self, text="Fullscreen", variable = self.fullscreen, command = self.update_fullscreen).grid()
        #checkboxes: Name bzw Name ändern, Immer koordinaten laden, vlt eigene setzen?
        self.button2 = Button(self, text='Done')
        self.button2["command"] = lambda: self.Close(master)
        self.button2.grid()

    def update_fullscreen(self):
        if self.fullscreen:
            #self.label1["text"]="Fullscreen"
            global fullscreen
            fullscreen=self.fullscreen
            #TODO fullscreen muss noch in eine Datei geschrieben werden

    def Close(self, master):
        master.destroy()
        #einstellungen.destroy()
        
        #window.destroy()
        #hallo=True
        #hi="hi"
        #self.button2["text"]=hi
        
        
class Application(Frame):
    "neues Fenster"
    def __init__(self, master):
        Frame.__init__(self, master)
        #self.grid()
        self.pack()
        self.create_wigets(master)

    def create_wigets(self, master):
        self.button1 = Button(self, text='Spiel starten', height=5, width=50)
        self.button1["command"] = lambda: self.starte_spiel(master)
        self.button1.grid(row = 1, column = 0, pady=20)#, sticky=NE) #columnspan=2, sticky=tk.N)#, padx=55, ipadx=10)  #2

        #self.button1.pack()#fill=BOTH, expand=1)
        self.button4 = Button(self, text='Score', height=3, width=30)
        self.button4["command"] = lambda: self.score(master)
        self.button4.grid(column = 0, padx=55, row=2, pady=20)

        self.button2 = Button(self, text='Settings', height=3, width=30)
        self.button2["command"] = self.settings
        self.button2.grid(column = 0, row=3, sticky=N, pady=20) #padx=55, row=2)

        self.button3 = Button(self, text='Info', height=3, width=30)
        self.button3['command']= self.info
        self.button3.grid(column = 0, row=4, sticky=N, pady=20) #padx=55, row=3)

##    def multiplayer(self, master):
##        master.destroy()
##        
##        choosewin=Tk()
##        choosewin.title('Multiplayer')
##        choosewin.geometry('400x200')
##        choosewinframe=random_info_frame(choosewin, button=1)
##        choosewin.mainloop()

    def score(self, master):
        ri=Tk()
        ri.title('Highscore')
        ri.geometry('300x150')
        ri2 = score_frame(ri)
        #window=einstellungen
        ri.mainloop()
        
    def info(self):
        info_win=Tk()
        info_win.title('Info about the Developers')
        info_win.geometry('400x200')
        infoframe=Frame(info_win)
        #infoframe.grid()
        infoframe.pack()
        info_label= Label(infoframe, text='Programmed by Tobias Jülg\ndesigned by Lenni Wartena')#.grid()
        info_label.grid()
        info_label2= Label(infoframe, text='Email: Tobias@juelg.net')#.grid()
        info_label2.grid()
        done_button = Button(infoframe, text='OK')
        done_button["command"] = lambda: self.Close_info(info_win)
        done_button.grid()
        #window=info_win
        info_win.mainloop()

    def Close_info(self, master):
        master.destroy()

    def starte_spiel(self, master):
        #TODO
        #beende Menü
        master.destroy()
        #main task
        maintask()
        #stopwatch=watch()
        #h=Spielbrett(stopwatch)





    def settings(self):
        einstellungen=Tk()
        einstellungen.title('Settings')
        einstellungen.geometry('200x100')
        nw = sett(einstellungen)
        window=einstellungen
        einstellungen.mainloop()
##############################################################
#klassen für Spielbrett
##############################################################

class Spielbrett():
    def __init__(self, stopwatch):
        self.ground=box(length = 50, height = 0, width = 50,
                 material = materials.bricks, pos=(0,-0.2,7.5))
        self.spielbrett = box(length = 6, height = 0.2, width = 15,
                 material = materials.wood, pos=(0,0,7.5))
        self.loch=[[0 for x in range(4)] for x in range(12)]
        self.antwort=[[0 for x in range(4)] for x in range(12)]
        #self.label(pos=(0,0.25,0), text='This is a box')

        #klickkugeln
        self.klickkugel1=sphere(pos=(-5,0.5,15), radius=0.2, color=color.red)
        self.klickkugel2=sphere(pos=(-5,0.5,14.5), radius=0.2, color=color.blue)
        self.klickkugel3=sphere(pos=(-5,0.5,14), radius=0.2, color=color.yellow)
        self.klickkugel4=sphere(pos=(-5,0.5,13.5), radius=0.2, color=color.green)
        self.klickkugel5=sphere(pos=(-5,0.5,13), radius=0.2, color=color.orange)
        self.klickkugel6=sphere(pos=(-5,0.5,12.5), radius=0.2, color=color.magenta)

        #reihe 1
        self.loch[0][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,14))
        self.loch[0][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,14))
        self.loch[0][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,14))
        self.loch[0][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,14))

        #reihe 2
        self.loch[1][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black, 
                 pos =(-1,0.2,13))
        self.loch[1][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,13))
        self.loch[1][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,13))
        self.loch[1][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,13))
        #reihe 3
        self.loch[2][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,12))
        self.loch[2][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,12))
        self.loch[2][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,12))
        self.loch[2][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,12))
        #reihe 4
        self.loch[3][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,pos =(-1,0.2,11))
        
        self.loch[3][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,11))
        self.loch[3][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,11))
        self.loch[3][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,11))
        #reihe 5
        self.loch[4][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,10))
        self.loch[4][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,10))
        self.loch[4][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,10))
        self.loch[4][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,10))
        #reihe 6
        self.loch[5][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,9))
        self.loch[5][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,9))
        self.loch[5][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,9))
        self.loch[5][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,9))
        #reihe 7
        self.loch[6][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,8))
        self.loch[6][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,8))
        self.loch[6][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,8))
        self.loch[6][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,8))
        #reihe 8
        self.loch[7][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,7))
        self.loch[7][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,7))
        self.loch[7][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,7))
        self.loch[7][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,7))
        #reihe 9
        self.loch[8][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,6))
        self.loch[8][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,6))
        self.loch[8][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,6))
        self.loch[8][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,6))
        #reihe 10
        self.loch[9][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,5))
        self.loch[9][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,5))
        self.loch[9][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,5))
        self.loch[9][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,5))
        #reihe 11
        self.loch[10][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,4))
        self.loch[10][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,4))
        self.loch[10][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,4))
        self.loch[10][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,4))
        #reihe 12
        self.loch[11][0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(-1,0.2,3))
        self.loch[11][1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(0,0.2,3))
        self.loch[11][2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(1,0.2,3))
        self.loch[11][3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                 pos =(2,0.2,3))

        #antwort reihe 1
        self.antwort[11][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                 pos =(-2.4,0.2,3.2))
        self.antwort[11][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                 pos =(-2.4,0.2,2.8))
        self.antwort[11][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                 pos =(-2,0.2,3.2))
        self.antwort[11][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                 pos =(-2,0.2,2.8))
        #antwort reihe 2 
        self.antwort[10][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,3.8))
        self.antwort[10][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,4.2))
        self.antwort[10][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,3.8))
        self.antwort[10][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,4.2))
        #antwort reihe 3
        self.antwort[9][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,4.8))
        self.antwort[9][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,5.2))
        self.antwort[9][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,4.8))
        self.antwort[9][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,5.2))
        #antwort reihe 4
        self.antwort[8][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,5.8))
        self.antwort[8][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,6.2))
        self.antwort[8][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,5.8))
        self.antwort[8][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,6.2))
        #antwort reihe 5
        self.antwort[7][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,6.8))
        self.antwort[7][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,7.2))
        self.antwort[7][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,6.8))
        self.antwort[7][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,7.2))
        #antwort reihe 6
        self.antwort[6][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,7.8))
        self.antwort[6][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,8.2))
        self.antwort[6][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,7.8))
        self.antwort[6][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,8.2))
        #antwort reihe 7
        self.antwort[5][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,8.8))
        self.antwort[5][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,9.2))
        self.antwort[5][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,8.8))
        self.antwort[5][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,9.2))
        #antwort reihe 8 
        self.antwort[4][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,9.8))
        self.antwort[4][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,10.2))
        self.antwort[4][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,9.8))
        self.antwort[4][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,10.2))
        #antwort reihe 9
        self.antwort[3][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,10.8))
        self.antwort[3][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,11.2))
        self.antwort[3][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,10.8))
        self.antwort[3][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,11.2))
        #antwort reihe 10
        self.antwort[2][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,11.8))
        self.antwort[2][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,12.2))
        self.antwort[2][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,11.8))
        self.antwort[2][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,12.2))
        #antwort reihe 11
        self.antwort[1][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,12.8))
        self.antwort[1][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,13.2))
        self.antwort[1][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,12.8))
        self.antwort[1][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,13.2))
        #antwort reihe 12
        self.antwort[0][0] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,13.8))
        self.antwort[0][1] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2.4,0.2,14.2))
        self.antwort[0][2] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,13.8))
        self.antwort[0][3] = cylinder(radius = 0.05, axis =(0,-1,0), color = color.black,
                         pos =(-2,0.2,14.2))

        #sichtkasten
        stirnseite = box(length = 4.5, width = 0.2, material = materials.wood,
                         pos =(0.5,0.5,2))
        wand1 = box(length = 0.2, material = materials.wood, pos =(2.65,0.5,1.5))
        wand2 = box(length = 0.2, material = materials.wood, pos =(-1.65,0.5,1.5))
        decke = box(length = 4.5, height = 0.2, width = 1.2, material = materials.wood,
                         pos =(0.5,1,1.5))

        #lösung

        self.lösung=[0 for x in range(4)]
        
        self.lösung[0] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.blue,
                         pos =(-1,0.2,1.5))
        self.lösung[1] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                         pos =(0,0.2,1.5))
        self.lösung[2] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                         pos =(1,0.2,1.5))
        self.lösung[3] = cylinder(radius = 0.1, axis =(0,-1,0),color = color.black,
                         pos =(2,0.2,1.5))
        self.lösungskugel=[0 for x in range(4)]

        self.lösungskugel[0]=sphere(pos=self.lösung[0].pos, radius=0.2)
        self.lösungskugel[1]=sphere(pos=self.lösung[1].pos, radius=0.2)
        self.lösungskugel[2]=sphere(pos=self.lösung[2].pos, radius=0.2)
        self.lösungskugel[3]=sphere(pos=self.lösung[3].pos, radius=0.2)
        self.randomgenerator()
        Spielverlauf(self, stopwatch)
        

    def randomgenerator(self):
        for i in range(4):
        #for i in self.lösungskugel:
            b=self.lösungskugel[i]
            #print(i)
            #print(b)
            c=random.randint(1, 6)
            #print(c)
            if c==1:
                b.color=color.yellow
            if c==2:
                b.color=color.red
            if c==3:
                b.color=color.blue
            if c==4:
                b.color=color.green
            if c==5:
                b.color=color.orange
            if c==6:
                b.color=color.magenta
        


class Spielverlauf():
    def __init__(self, spiel, stopwatch):
        self.spiel=spiel
        self.xsetzen_pos=0
        self.ysetzen_pos=0
        self.object=[[0 for x in range(4)] for x in range(12)]
        #self.ob_array=()
        self.loesung=[[0 for x in range(4)] for x in range(12)]
        self.win=False
        self.farbe=color.black
        #
        self.label=label(pos=(0,0.25,0), text=(str(stopwatch.now)+'Seconds'))
        self.minus=label(pos=(-5,0.5,10), text=("BACK"))
        self.plus=label(pos=(-5,0.5,8), text=("NEXT"))
        self.lock=label(pos=(-5,0.5,6), text=("LOCK"))
        self.pointer = arrow(pos=(0,0.2,15.1), axis=(0,0,-1), shaftwidth=1, color=color.green)
        
        #self.locked=False
        self.set_check=False
                        
        #

        self.run(stopwatch)

    def run(self, stopwatch):
        global stoppen
        while True:
            self.label.text=(str(stopwatch.now)+' Seconds')
            self.pointer.pos[0]= self.spiel.loch[1][self.ysetzen_pos].pos[0]
            
##            if self.ysetzen_pos > 3:
##
##                
##                self.proof(self.xsetzen_pos)
##                if self.win==True:
##                    #gewonnen
##                    win_lose(True, stopwatch, self.xsetzen_pos)
##                    break
##
##                self.ysetzen_pos=0
##                self.xsetzen_pos=self.xsetzen_pos+1
            if self.xsetzen_pos > 11:
                #self.loose()
                #verloren
                self.minus.visible =False
                self.plus.visible =False
                self.lock.visible =False
                
                win_lose(False, stopwatch)
                #pass
                break

            self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.red
            
            if scene.mouse.clicked:
                m = scene.mouse.getclick()
                loc = m.pos
                #print(loc)
                
                if stoppen==False:
                    stoppen=True

                if loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>8.8 and loc[2]<10.2:#BACK button
                    color_label(self, 1)
                    if self.ysetzen_pos > 0:
                        self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.black#vorheriges Loch schwarz machen
                        
                        self.ysetzen_pos=self.ysetzen_pos-1
                        
                        self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.red# neues Loch rot machen
                    else:
                        print("Curser can't put to 0")

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>7.4 and loc[2]<8.5:#NEXT button
                    color_label(self, 2)
                    if self.ysetzen_pos < 3:
                        self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.black#vorheriges Loch schwarz machen
                        
                        self.ysetzen_pos=self.ysetzen_pos+1

                        self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.red# neues Loch rot machen
                    else:
                        print("Curser can't put over 4")

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>5.5 and loc[2]<6.7:#LOCK button
                    color_label(self, 3)
                    if self.ysetzen_pos == 3:
                        if self.set_check==True:
                            
                            self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.black
                            
                            self.proof(self.xsetzen_pos)
                            if self.win==True:
                                #gewonnen
                                self.minus.visible =False
                                self.plus.visible =False
                                self.lock.visible =False
                                
                                win_lose(True, stopwatch, self.xsetzen_pos)
                                break

                            self.ysetzen_pos=0
                            self.xsetzen_pos=self.xsetzen_pos+1
                            self.set_check=False
                        else:
                           print("You have to set spheres on all seats!") 
                        
                    else:
                        print("Curser has to be on postion 4!")
                    
                
                #print(loc)
                #sphere(pos=loc, radius=0.2, color=color.cyan)
                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>13.5 and loc[2]<14:
                    self.farbe=color.red
                    #print("red")
                    self.ob()

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>13.05 and loc[2]<13.5:
                    self.farbe=color.blue
                    #print("blue")
                    self.ob()

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>12.75 and loc[2]<13.05 :
                    self.farbe=color.yellow
                    #print("yellow")
                    self.ob()

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>12.25 and loc[2]<12.75 :
                    self.farbe=color.green
                    #print("green")
                    self.ob()

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>11.8 and loc[2]<12.25 :
                    self.farbe=color.orange
                    #print("orange")
                    self.ob()

                elif loc[0]>=-2 and loc[0]<=-1.5 and loc[1]>=2.5 and loc[1]<=3 and loc[2]>11.2 and loc[2]<11.8 :
                    self.farbe=color.magenta
                    #print("magenta")
                    self.ob()
                  
                #print(self.farbe)
                #self.object[self.xsetzen_pos][self.ysetzen_pos]=sphere(pos=self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].pos, radius=0.2, color=self.farbe)
                #(loch[self.xsetzen_pos][self.ysetzen_pos].pos[0],loch[self.xsetzen_pos][self.ysetzen_pos].pos[1],1), radius=0.2, color=self.farbe)
            
                #self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.black
                #self.ysetzen_pos=self.ysetzen_pos+1

    def ob(self):
        self.object[self.xsetzen_pos][self.ysetzen_pos]=sphere(pos=self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].pos, radius=0.2, color=self.farbe)#radius=0.075
        if self.ysetzen_pos==3:
            self.set_check=True
        
        
        if self.ysetzen_pos < 3:
            self.spiel.loch[self.xsetzen_pos][self.ysetzen_pos].color=color.black
            self.ysetzen_pos=self.ysetzen_pos+1
    
    def proof(self, row):
        c = [0,1,2,3] 
        random.shuffle(c)
##        r1=c[0]
##        r2=c[1]
##        r3=c[2]
##        r4=c[3]
        test=[0 for x in range(4)]
        test[0]=False
        test[1]=False
        test[2]=False
        test[3]=False
        
        for i in range(4):
            if self.spiel.lösungskugel[i].color == self.object[row][i].color:
                test[i]=True
                if c[0]==-1:
                    if c[1]==-1:
                        if c[2]==-1:
                            y=c[3]
                            c[3]=-1
                        else:
                            y=c[2]
                            c[2]=-1
                                
                    else:
                        y=c[1]
                        c[1]=-1
                else:
                    y=c[0]
                    c[0]=-1
                    
                self.loesung[row][y]=sphere(pos=self.spiel.antwort[row][y].pos, radius=0.1, color=color.black)
                
        if test[0]==True and test[1]==True and test[2]==True and test[3]==True:
            self.win=True
##        elif c[3]==-1:
##            self.win=True
        test2=[0 for x in range(4)]######
        test2[0]=False
        test2[1]=False
        test2[2]=False
        test2[3]=False

        test3=[0 for x in range(4)]######
        test3[0]=False
        test3[1]=False
        test3[2]=False
        test3[3]=False
        
        for b in range(4):
            if test[b]==False:##nür nicht stimmende gesetzte überprüfen
                #print(float(b), ' test[b]==False')
                for a in range(4):
                    if test[a]==False:##########nur nichtstimmende lösungen überprüfen
                        if test3[b]==False:##########nur weiter überprüfen wenn kein treffer
                            if test2[a]==False:#########nur überprüfen wenn noch nicht überprüft worden
                            #print(float(a), ' test[a]==False')
                                if self.spiel.lösungskugel[a].color == self.object[row][b].color:
                                    if c[0]==-1:
                                        if c[1]==-1:
                                            if c[2]==-1:
                                                y=c[3]
                                                c[3]=-1
                                            else:
                                                y=c[2]
                                                c[2]=-1
                                
                                        else:
                                            y=c[1]
                                            c[1]=-1
                                    else:
                                        y=c[0]
                                        c[0]=-1

                                    self.loesung[row][y]=sphere(pos=self.spiel.antwort[row][y].pos, radius=0.1, color=color.white)
                                    test2[a]=True###########wenn überprüft worden, raus nehmen
                                    test3[b]=True###########wenn lösungs kugel passt überprüfung abbrechen
        
##    def loose(self):
##        pass

class win_lose():
    def __init__(self, what, stopwatch, reihe=-1):
        self.what=what
        scene.forward=(0,-0.4,1)
        scene.userspin = True
        scene.userzoom = True
        if what==True:
            print("Victory")
##            self.label = text(text='Victory',
##                align='center', depth=-0.5, color=color.blue)
##            self.label.axis =(-1,0,0)
##            self.label.pos =(0.5,2,0)
            self.reihe=reihe+1
            print('Zeit: '+str(stopwatch.now))
            print('Reihe: '+str(self.reihe))

            self.score=stopwatch.now*self.reihe
            self.score=100000/self.score
            print('Your MASTERscore is: ' + str(self.score))
            
            datei = open("Data_master.mind", "r") #datei öffen
        
            line0=datei.readline() #3.
            line1=datei.readline()
            
            datei.close()
            
            t=''
            w=''
            b=False

            if line1 == '': #falls kein name des Spielers in der Datei steht
                self.highscore=self.score
                print('New highscore')


            else:
##                t=''
##                w=''
##                b=False
                for i in line1:
                    if b==True:
                        w=w+i
                    elif i==":":
                        b=True
                        
                    elif b==False:
                        t=t+i
                if float(w) > self.score:
                    self.highscore=w
                    print('Your highscore is ' + str(self.highscore))
                else:
                    print('New highscore')
                    self.highscore=self.score
            if self.highscore != w:
                fobj = open('Data_master.mind', 'w')
                fobj.write(line0)
                fobj.write('Highscore:' + str(self.highscore))
                fobj.close()
                    
            
            
        else:
            print("Defeat")
##            self.label = text(text="Defeat", align="center", depth=-0.5, color=color.red)
##            self.label.axis =(-1,0,0)
##            self.label.pos =(0.5,2,0)
            print('Your score is: BAD')
            #self.score=0
        stopwatch.stop=True  

class watch(Thread):
    def __init__(self):
        self.now=0.0
        Thread.__init__(self)
        self.stop=False
        
##        self.watchy=Tk()
##        self.watchy.title('Watch')
##        self.watchy.geometry('200x100')
##        self.nw2 = random_info_frame(self.watchy, 0)
##        #window=einstellungen
##        self.watchy.mainloop()
        #self.w=Watchframe()
        
        self.start()
    def run(self):
        #sleep(0.5)
        global stoppen
        while True:
            if stoppen==True:
                sleep(1)
                self.now=self.now + 1
            #if self.w.wa=True:
                #self.w.wa.label["text"]=(str(int(self.now))+' seconds') #stoppuhr im window
            #print(str(self.now))
            if self.stop==True:
                 #pass
                 break

##class Watchframe(Thread):
##    def __init__(self):
##        print('hier')
##        Thread.__init__(self)
##        self.watchy=Tk()
##        self.watchy.title('Watch')
##        self.watchy.geometry('200x100')
##        self.wa = random_info_frame(self.watchy, 0)
##        self.start()
##    def run(self):
##
##        #window=einstellungen
##        self.watchy.mainloop()

class color_label(Thread):
    def __init__(self, h, p):
        self.p=p
        self.h=h
        Thread.__init__(self)
        self.start()
    def run(self):
        if self.p==1:
            self.h.minus.background=color.yellow
            sleep(0.25)
            self.h.minus.background = (0,0,1)
        elif self.p==2:
            self.h.plus.background=color.yellow
            sleep(0.25)
            self.h.plus.background = (0,0,1)
        elif self.p==3:
            self.h.lock.background=color.yellow
            sleep(0.25)
            self.h.lock.background = (0,0,1)

        

def maintask():
##    scene = display(title='Mastermind')
    try: #probiere

        datei1 = open('Data_master.mind')
        datei1.close()

        
    except IOError: #falls error
        fobj = open('Data_master.mind', 'w')
        fobj.write("")
        #fobj.write("x" + "\n")
        #fobj.write("z" + "\n")
        
        
        fobj.close()

    #global name_von_spieler    
    datei = open("Data_master.mind", "r") #datei öffen
        
    #dateiinhalt0=datei.readline() #1. zeile lesen
    #dateiinhalt1=datei.readline() #2.
    line0=datei.readline() #3.
    line1=datei.readline()
            
    datei.close()




    if line0 == '': #falls kein name des Spielers in der Datei steht
        name=Tk()
        name.title("Name")
        name.geometry("200x100")
        nameframe=win_before_start(name, line1)#, dateiinhalt0, dateiinhalt1)
        #nameframe.grid()
        name.mainloop()

    else:
        t=''
        w=''
        b=False
        for i in line0:
            if b==True:
                w=w+i
            elif i==":":
                b=True
                        
            elif b==False:
                t=t+i
        if w=="":
            name=Tk()
            name.title("Name")
            name.geometry("200x100")
            nameframe=win_before_start(name, line1)#, dateiinhalt0, dateiinhalt1)
            #nameframe.grid()
            name.mainloop()
        else:
            name_von_spieler = w
            

    
    scene.height = win_hight
    scene.width = win_width
    scene.title='Mastermind'
    scene.fullscreen = bool(fullscreen)
    scene.userzoom = False
    scene.center=(0,1,7)
    scene.forward=(-1,-1,0)
    scene.autoscale = False
    scene.userspin = False
    scene.background = (0,0,1)
    stopwatch=watch()
    h=Spielbrett(stopwatch)


##############################################################
#Update Funktion:
##############################################################

def update_check(vers):#version):
    #global version
    
    import urllib.request
    import urllib
    url_web='http://cn-e.de/wp-content/uploads/2014/03/ckecker.txt'
##    version=1.0
##    import urllib.request
##    import urllib
    #global url_web
    #global version

    def updaten(url_web):
        print(url_web)
        source=urllib.request.urlopen(url_web).read()
        #source_write=source.decode('utf-8')
        
        import os
        os.chdir(os.pardir)
    
        file = open('uptodate.zip', 'wb')
        file.write(source)
        file.close()

        import zipfile    
        zip1 = zipfile.ZipFile("uptodate.zip", "r")
        zip1.extractall() #Above password "oy" generates the error here
        zip1.close()
        import os
        os.remove("uptodate.zip")
    
    try:
        h=urllib.request.urlopen(url_web)
        #web = urllib.request.urlopen('http://cn-e.de/wp-content/uploads/2013/12/update_test.txt').readline()
        web = h.readline()#urllib.request.urlopen(url_web).readline()
        url_neu = h.readline()#urllib.request.urlopen(url_web).readline()
        url_neu2=url_neu.decode('utf-8')
        webstr=web.decode('utf-8')
        #print(url_neu2 + " is the newest Version, your version is: " + str(vers))
        #print(webstr)

        webstr2=''
        for i in webstr:
            if i=='#':
                pass
            else:
                webstr2=webstr2+i
    
        webversion=float(webstr2)
        #print(vers)

        if webversion > vers:
            print('Version is not up to date, therefore it will be updated now!')
            print(webstr2 + " is the newest Version, your version is: " + str(vers))
        
            updaten(url_neu2)
            #print("Version is now up to date\nPlease rename the new folder, which can be found in your old directory, in your favour and delete the old one.")
            print("Programm will automatically close in 10 seconds. And reboot!")
            sleep(10)
            import os
            os.system("batch.bat")
            import sys
            sys.exit("Programm closed")#quited")
        else:
            print("Version is up to date!")

            
    except urllib.error.URLError as detail: #falls error
        print("Couldn't check for new versions.\nThis may caused by a conection error.")
        print("\nError report:\n")
        print(detail)
        #raise

                

if __name__ =="__main__":
    
    #update_check(vers)#version

    root=Tk()
    root.title("Main Menu")
    root.geometry("520x400")
    app = Application(root)
    root.mainloop()

    #stefanhueller69

    
            
            







        
