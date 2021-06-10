#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial
import time
import vlc
import random
import pyttsx3
import pygame 

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.runAndWait()

userDict={} #Canciones coincidentes de los otros usuarios con el usuario actual
songDict={} #canciones que no tiene el usuario

instance1 = vlc.Instance('--aout=hdmi')
#instance2 = vlc.Instance('--aout=hdmi')

player1 = instance1.media_player_new()
#player2 = instance2.media_player_new()

song1 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Believer.mp3")
song2 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/IDontKnowWhy.mp3")
song3 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/NextToMe.mp3")
song4 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/WalkingTheWire.mp3")
song5 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/WhateverItTakes.mp3")
song6 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/ASkyFullOfStars.mp3")
song7 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Clocks.mp3")
song8 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Paradise.mp3")
song9 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/VivaLaVida.mp3")
song10 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Yellow.mp3")
song11 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Demons.mp3")
song12 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/ItsTime.mp3")
song13 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/OnTopOfTheWorld.mp3")
song14 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Radioactive.mp3")
song15 = instance1.media_new("/home/pi/Documents/PlaylistReto/ArduinoPl/Tiptoe.mp3")

newSong=1

media_list=vlc.MediaList()

player1.set_media(song1)
#player2.set_media(song2)

listaCancionesOrd = [song1, song2, song3, song4, song5, song6, song7, song8, song9, song10, song11, song12, song13, song14, song15]
listaCanciones = [song1, song2, song3, song4, song5, song6, song7, song8, song9, song10, song11, song12, song13, song14, song15]
cancionEnPlay=0;

"""
def createPlaylist():
    for song in listaCanciones:
        media_list.add_media(song)
        
"""

def playSong(cancionEnPlay):
    global newSong
    engine.say("Song now Playing")
    engine.runAndWait()
    if newSong==1:
        player1.set_media(listaCanciones[cancionEnPlay])
    else:
        newSong=1
    player1.play()
    
def stopSong():
    player1.stop()

def pauseSong():
    global newSong
    player1.pause()
    engine.say("Song now Paused")
    engine.runAndWait()
    newSong=0

def nextSong():
    global cancionEnPlay
    stopSong()
    engine.say("Now Playing Next Song")
    engine.runAndWait()
    cancionEnPlay = cancionEnPlay + 1
    player1.set_media(listaCanciones[cancionEnPlay])
    player1.play()


def prevSong():
    global cancionEnPlay
    stopSong()
    engine.say("now Playing Previous Song")
    engine.runAndWait()
    cancionEnPlay = cancionEnPlay - 1
    player1.set_media(listaCanciones[cancionEnPlay])
    player1.play()

def shuffleMusic():
    stopSong()
    engine.say("The playlist has been shuffled")
    engine.runAndWait()
    random.shuffle(listaCanciones)
    player1.set_media(listaCanciones[0])
    player1.play()
    #temp = random.shuffle(listaCanciones)
    #temp[0].play()
    
def sendInfo():
    if listaCanciones[cancionEnPlay]==song1:
        idSong=0
    elif listaCanciones[cancionEnPlay]==song2:
        idSong=1
    elif listaCanciones[cancionEnPlay]==song3:
        idSong=2
    elif listaCanciones[cancionEnPlay]==song4:
        idSong=3
    elif listaCanciones[cancionEnPlay]==song5:
        idSong=4
    elif listaCanciones[cancionEnPlay]==song6:
        idSong=5
    elif listaCanciones[cancionEnPlay]==song7:
        idSong=6
    elif listaCanciones[cancionEnPlay]==song8:
        idSong=7
    elif listaCanciones[cancionEnPlay]==song9:
        idSong=8
    elif listaCanciones[cancionEnPlay]==song10:
        idSong=9
    elif listaCanciones[cancionEnPlay]==song11:
        idSong=10
    elif listaCanciones[cancionEnPlay]==song12:
        idSong=11
    elif listaCanciones[cancionEnPlay]==song13:
        idSong=12
    elif listaCanciones[cancionEnPlay]==song14:
        idSong=13
    elif listaCanciones[cancionEnPlay]==song15:
        idSong=14
    
    f=open("/home/pi/Documents/PlaylistReto/ArduinoPl/canciones.txt", "r")
    for song in f:
        div=song.find(',')
        ID=song[0:div]
        if int(ID)==idSong:
            string=song[div+1:]
            div=string.find(',')
            name=string[0:div]
            string=string[div+1:]
            div=string.find(',')
            artist=string[0:div]
            time.sleep(0.01)
            for char in name:
                ser.write(char.encode('utf-8'))
                time.sleep(0.01)
            ser.write(','.encode('utf-8'))
            time.sleep(0.01)
            for char in artist:
                ser.write(char.encode('utf-8'))
                time.sleep(0.01)
            ser.write('!'.encode('utf-8'))

def orderPlaylist():
    listaCanciones=listaCancionesOrd

def playSongId(idSong):
    stopSong()
    orderPlaylist()
    playSong(idSong)
    
def interfazCancion():
    root = tk.Tk()
    root.title('Reproductor de musica')
    root.geometry("500x350")

    pygame.mixer.init() 
    songbox = tk.Listbox(root, bg = "firebrick1", fg = "black", width = 60, font = "Courier", selectforeground = "Blue")
    songbox.pack(pady=20)
    items = songbox.insert(tk.END, "0. Believer - Imagine Dragons", "1. I Dont Know Why - Imagine Dragons", "2. Next to Me - Imagine Dragons", "3. Walking The Wire - Imagine Dragons", "4. Whatever It Takes - Imagine Dragons", "5. A Sky Full Of Stars - Coldplay", "6. Clocks - Coldplay", "7. Paradise - Coldplay", "8. Viva la Vida - Coldplay", "9. Yellow - Coldplay", "10. Demons - Imagine Dragons", "11. Its Time - Imagine Dragons", "12. On Top Of The World - Imagine Dragons", "13. Radioactive - Imagine Dragons", "14. Tiptoe - Imagine Dragons")

    back_buttoni = tk.PhotoImage(file ='back.png') 
    forward_buttoni = tk.PhotoImage(file ="forward.png")
    play_buttoni = tk.PhotoImage(file ="play.png")
    pause_buttoni = tk.PhotoImage(file ="pause.png")
    stop_buttoni = tk.PhotoImage(file ="stop.png")

    controlsframe = tk.Frame(root)
    controlsframe.pack()

    back_button = tk.Button(controlsframe, image = back_buttoni, borderwidth = 0, command=lambda : prevSong())
    forward_button = tk.Button(controlsframe, image = forward_buttoni, borderwidth = 0, command=lambda : nextSong())
    play_button = tk.Button(controlsframe, image = play_buttoni, borderwidth = 0, command=lambda : playSongInt())
    pause_button = tk.Button(controlsframe, image = pause_buttoni, borderwidth = 0, command=lambda : pauseSong())
    stop_button = tk.Button(controlsframe, image = stop_buttoni, borderwidth = 0, command=lambda : stopSong())

    back_button.grid(row=0, column = 1,padx = 10)
    forward_button.grid(row = 0, column = 3, padx = 10)
    play_button.grid(row = 0, column = 2, padx = 10)
    pause_button.grid(row = 0, column = 4, padx = 10)
    stop_button.grid(row = 0, column = 0, padx = 10)

    mymenu = tk.Menu(root)
    root.config(menu=mymenu)
    
    def playSongInt():
        global cancionEnPlay
        global newSong
        global listaCancionesOrd
        global listaCanciones
        listaCanciones=listaCancionesOrd
        song = songbox.get(tk.ACTIVE)
        div = song.find('.')
        cancionEnPlay=int(song[0:div])
        engine.say("Song now Playing")
        engine.runAndWait()
        if newSong==1:
            player1.set_media(listaCancionesOrd[cancionEnPlay])
        else:
            newSong=1
        player1.play()

    root.mainloop()

class primeraPagina(tk.Frame):
    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)

      #imagen de fondo#
      cargar = Image.open("img2.jpg")
      foto = ImageTk.PhotoImage(cargar)
      label = tk.Label(self, image=foto)
      label.image=foto
      label.place(x=0,y=0)

      #borde#
      borde = tk.LabelFrame(self, text='Login', bg='spring green', bd = 10, font=("Ubuntu Condensed", 20)) 
      borde.pack(fill="both", expand = "yes",padx = 150, pady = 150)

      lbl1 = tk.Label(borde, text="Usuario", font=("Arial Bold",15), bg = 'spring green')
      lbl1.place(x=50, y=20)
      txt1 = tk.Entry(borde, width = 30, bd = 5)
      txt1.place(x=180, y=20)

      lbl2 = tk.Label(borde, text="Contraseña", font=("Arial Bold",15), bg = 'spring green')
      lbl2.place(x=50, y=80)
      txt2 = tk.Entry(borde, width = 30, show = '*',bd = 5)
      txt2.place(x=180, y=80)

      def verificar():
          try: 
              with open("credential.txt", "r") as palabra:
                info = palabra.readlines()
                i = 0
                for a in info: 
                    ID, usuario, contraseña = a.split(",")
                    if usuario.strip() == txt1.get() and contraseña.strip() == txt2.get():
                        #controller.sho w_frame(terceraPagina)
                        controller.destroy()
                        i = 1
                        break
                if i==0:
                    messagebox.showinfo("Error","Por favor ingresa el usuario o la contraseña corecta!!")
          except:
              messagebox.showinfo("Error", "Por favor ingresa el usuario con su contraseña")

      button1 = tk.Button(borde, text="INGRESAR", font = ("Arial",15),command = verificar)
      button1.place(x=320,y=115)

      def registrar():
          ventana = tk.Tk()
          ventana.resizable(0,0)
          ventana.configure(bg="orange red")
          ventana.title("Registrar")
        
          lbl1 = tk.Label(ventana, text="Usuario:",font = ("Arial",15), bg = "orange red")
          lbl1.place(x=10,y=10)
          txt1 = tk.Entry(ventana, width=30, bd=5)
          txt1.place(x=200,y=10)

          lbl2 = tk.Label(ventana, text="Contraseña:", font = ("Arial",15), bg = "orange red")
          lbl2.place(x=10,y=60)
          txt2 = tk.Entry(ventana, width=30, bd=5)
          txt2.place(x=200,y=60)

          lbl3 = tk.Label(ventana, text="Confirmar Contraseña:", font = ("Arial",15), bg = "orange red")
          lbl3.place(x=10,y=110)
          txt3 = tk.Entry(ventana, width=30, bd=5)
          txt3.place(x=200,y=110)

          def checar():
              if txt1.get()!="" or txt2.get()!="" or txt3.get()!="":
                  if txt2.get() == txt3.get():
                      ID=0
                      existe=0
                      with open("credential.txt",  "r") as palabra:
                        for usua in palabra:
                          div=usua.find(',')
                          ID=usua[0:div]
                          string=usua[div+1:]
                          div=string.find(',')
                          usernam=string[0:div]
                          if usernam==txt1.get():
                            existe=1
                        if existe==0:
                          ID=str(int(ID)+1)
                          with open("credential.txt",  "a") as palabra:
                              palabra.write(ID+","+txt1.get()+","+txt2.get()+ "\n")
                              messagebox.showinfo("Bienvenido","Tu registro se realizo exitosamente")
                              engine.say("Recommenda Thank you "+ txt1.get() + " for joining")
                              engine.runAndWait()
                        else:
                          existe=0
                          messagebox.showinfo("Error","El usuario ya existe")
                  else:
                      messagebox.showinfo("Error","Las contraseñas no coinciden")
              else:
                  messagebox.showinfo("Error","Por favor llena todos los campos!")

          button1 = tk.Button(ventana, text="Inicia Sesión", font = ("Arial",15), bg = "#ffc22a", command = checar)
          button1.place(x=170,y=150)

          ventana.geometry("470x220")
          ventana.mainloop()
    
      button2 = tk.Button(self, text="Registrar", bg = "dark orange", font = ("Arial",15), command=registrar)
      button2.place(x=650, y=20)


class segundaPagina(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl = tk.Label(self, text ="Usuarios actuales", bg = "medium spring green", font = ("Arial",15))
        lbl.place(x=320,y=10)

class terceraPagina(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        self.configure(bg = "Tomato")
        self.button = []

        #lbl1 = tk.Label(self, text = "Canciones del usuario, Haz click para reproducir", bg = "deep sky blue", font = ("Arial Bold",20))
        #lbl1.place(x=20, y= 170)
        
        xPos=15
        yPos=15
        with open("/home/pi/Documents/PlaylistReto/ArduinoPl/canciones.txt",  "r") as canciones:
            IDCan=[]
            cont=0
            for song in canciones:
                div=song.find(',')
                ID=song[0:div]
                string=song[div+1:]
                div=string.find(',')
                title=string[0:div]
                string=string[div+1:]
                div=string.find(',')
                author=string[0:div]
                string=string[div+1:]
                div=string.find(',')
                self.button.append(tk.Button(self, text=title, font = ("Arial",15), height=15, width =50, command=lambda Id=int(ID): playSongId(Id)))
                self.button[cont].place(x=xPos, y=yPos)
                cont+=1
                yPos+=20
                """
                div=string.find(' ')
                users=string[0:-1]
                div=users.find(',')
                listUs=[]
                stringU=""
                while div!=-1:
                    listUs.append(int(users[0:div]))
                    users=users[div+1:]
                    div=users.find(',')
                listUs.append(int(users))
                tempDict={}
                upd=0
                for i in listUs:
                    if i==UserID:
                        IDCan.append(ID)
                        upd=1
                    else:
                        tempDict.update({str(i):userDict[str(i)]+1})
                if upd==1:
                    userDict.update(tempDict)
                else:
                    songDict.update({str(ID):0})
                    """
        button1 = tk.Button(self, text = "Inicio", font = ("Arial", 15), command = lambda: controller.show_frame(primeraPagina))
        button1.place(x=650, y= 450)

        button2 = tk.Button(self, text = "Atrás", font = ("Arial",15), command = lambda: controller.show_frame(segundaPagina))
        button2.place(x=100, y = 450)
        
        

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        ventana = tk.Frame(self)
        ventana.pack()

        ventana.grid_rowconfigure(0,minsize =500)
        ventana.grid_columnconfigure(0, minsize = 800)

        self.frames = {}
        for f in (primeraPagina, segundaPagina, terceraPagina):
            frame = f(ventana,self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.show_frame(primeraPagina)

    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Diseño de Sistemas en Chip")

if __name__=='__main__':
    ser=serial.Serial('/dev/ttyACM0',9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting>0:
            line=ser.read().decode('utf-8')
            if line=='T':
                time.sleep(0.01);
                while ser.in_waiting>0:
                    line=ser.read().decode('utf-8')
                    time.sleep(0.01)
                line='f'
            if line!='f':
                print(line)
                if line== 'p':
                    if player1.is_playing()==0:
                        playSong(cancionEnPlay)
                        playPause=1
                    else:
                        pauseSong()
                        playPause=0
                elif line=='b':
                    if cancionEnPlay>0:
                        prevSong()
                    else:
                        stopSong()
                        engine.say("Song has restarted")
                        engine.runAndWait()
                        playSong(cancionEnPlay)
                elif line=='s':
                    if cancionEnPlay<len(listaCanciones)-1:
                        nextSong()
                    else:
                        stopSong()
                        engine.say("You have reached the end of your playlist")
                        engine.runAndWait()
                elif line=='u':
                    shuffleMusic()
                    cancionEnPlay=0
                elif line=='o':
                    stopSong()
                    engine.say("Song now stopped")
                    engine.runAndWait()
                elif line=='r':
                    app = App()
                    app.maxsize(800,500)
                    app.mainloop()
                    interfazCancion()
                elif line=='1':
                    num="1"
                    cancionEnPlay=int(num)
                    ser.write(chr(cancionEnPlay).encode('utf-8'))
                    sendInfo()
                    ser.write('f'.encode('utf-8'))
                    while line!='E':
                        if ser.in_waiting>0:
                            line=ser.read().decode('utf-8')
                            print(line)
                            if line!='E' and (line=='1' or line=='0' or line=='2' or line=='3'):
                                print(line)
                                num+=line
                                cancionEnPlay=int(num)
                                ser.write(chr(cancionEnPlay).encode('utf-8'))
                                sendInfo()
                                line='E'
                            elif line!='E':
                                ser.write('f'.encode('utf-8'))
                    cancionEnPlay=int(num)
                    playSongId(cancionEnPlay)
                    
                elif (line=='0' or line=='2' or line=='3' or line=='4' or line=='5' or line=='6' or line=='7' or line=='8' or line=='9'):
                    cancionEnPlay=int(line)
                    playSongId(cancionEnPlay)
            ser.write(chr(cancionEnPlay).encode('utf-8'))
            sendInfo()

"""
app = App()
print("aqui si")
app.maxsize(800,500)
app.mainloop()
interfazCancion()
"""


