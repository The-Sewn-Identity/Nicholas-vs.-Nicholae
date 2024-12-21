import tkinter as tk
# import tkVideoPlayer # ja nie choczu, nie chcieju kiedykolwiek więcej tego używać
import keyboard
import threading
import random
import pygame
import pyglet

from tkinter import *
#from tkVideoPlayer import TkinterVideo
from read import ReadRules
from PIL import Image, ImageTk

# WARNING: THIS CODE IS ASS
# DOSŁOWNIE
# NAWET NIE WIEM KTÓRYM JĘZYKIEM PISAĆdestroy (to nie powinno tu być)
window = tk.Tk()
window.title("Nicholas vs. Nicolae")
window.state('zoomed')
window.resizable(width=False, height=False)

# Zmienne
winwidth = window.winfo_screenwidth()
winheight = window.winfo_screenheight()
btn_color = "#CC2046"

# Przełączniki
window_switch = False
game_on = False
hp_zeroed = False

opt_switch = False
read_switch = False
inv_switch = False

supply_atk = False
heal_switch = False

passed = False
ptsd_num = 0

sp_atk_used = 0
hl_used = 0

# Muzyka
pygame.init()
pygame.mixer.music.load("music/maintheme.mp3")
pygame.mixer.music.play(-1)

# Dźwięki
smack = pygame.mixer.Sound("sound/smack.wav")
miss = pygame.mixer.Sound("sound/lbp_fail.mp3")
overscream = pygame.mixer.Sound("sound/overscream.wav")

# Czcionki
pyglet.font.add_file('font/AAfont.ttf')
pyglet.font.load('Ace Attorney')

# Funkcje ogólne
def Fullscreen(event):
    global window_switch
    window_switch = not window_switch
    if window_switch:
        window.attributes("-fullscreen", True)
    else:
        window.attributes("-fullscreen", False)

# Gracz
class PlayerAttributes:
    def __init__(player, health, inventory):
        player.health = health
        player.inventory = inventory

player = PlayerAttributes(1000, ["Pepper Pellets", "NUFFIN'", "Candy Cane"])

# Wrogowie
class EnemyAttributes:
    def __init__(enemy, health, attack, max):
        enemy.health = health
        enemy.attack = attack
        enemy.max = max

triglav = EnemyAttributes(1000, 75, 100)
serj = EnemyAttributes(1500, 65, 110)
alfons = EnemyAttributes(1500, 90, 130)
nicolae = EnemyAttributes(1750, 144, 200)

def Start():
    global triglav, serj, alfons, nicolae, fightID, game_on, triglav_on, serj_on, alfons_on, nicolae_on, ptsd_num
    canvas.delete('all')
    startbutton.pack_forget()
    optionbutton.pack_forget()
    helpbutton.pack_forget()
    quitbutton.pack_forget()
    fightID = 0
    game_on = True
    triglav_on = False
    serj_on = False
    alfons_on = False
    nicolae_on = False
    
    triglav = EnemyAttributes(1000, 75, 100)
    serj = EnemyAttributes(1500, 65, 110)
    alfons = EnemyAttributes(1500, 90, 130)
    nicolae = EnemyAttributes(1750, 144, 200)

    ptsd_num = 0
    # IntroCutscene()
    StartGame()

def StartGame():
    window.after(900, FButtons)
    window.after(1000, FightII)

def Quit():
    window.destroy()

# Skróty klawiszowe
window.bind('<F11>', lambda event: Fullscreen(event))

# -- Menu główne
# Płótno
canvas = Canvas(width=winwidth, height=winheight, highlightthickness=0)
canvas.grid(row=0, column=0, sticky=NSEW)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Ładowanie
loadlab = tk.Label(canvas, text="Loading...", bg="#000", fg="white", font=("Arial Black", 48), width=winwidth)
loadlab.pack(expand=True, anchor=CENTER)

# Tło
mbgimg = Image.open("textures/loadromania.png")
mbgimg = mbgimg.resize((winwidth,  winheight))
mbgimg = ImageTk.PhotoImage(mbgimg)
mb = canvas.create_image(winwidth/2, winheight/2, image=mbgimg)

# Opcje i Przeczytaj To!
def ChangeVolume(_=None): # _=None oznacza metodę statyczną, możnaby było też użyć @staticmethod, ale chyba tylko w klasie
    pygame.mixer.music.set_volume(vol.get()/100)

def Options():
    global opt1, gbk, volframe, vol, musdes
    startbutton.pack_forget()
    optionbutton.pack_forget()
    helpbutton.pack_forget()
    quitbutton.pack_forget()

    opt1 = tk.Button(canvas, text="Print Rules in Terminal", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=25, command=ReadRules)
    opt1.pack(side=TOP, anchor=CENTER, expand=False, pady=16)

    gbk = tk.Button(canvas, text="Go Back", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=OptGoBack)
    gbk.pack(side=TOP, anchor=CENTER, expand=False)

    volframe = tk.Frame(canvas, bg=btn_color, width=winwidth, bd=5, highlightbackground="#000", highlightthickness=3)
    volframe.pack(side=BOTTOM, anchor=S, expand=False, padx=24, pady=24)
    vol = tk.Scale(volframe, font=("Arial Black", 32), bg=btn_color, fg="white", bd=3, length=winwidth, from_=0, to=100, orient=HORIZONTAL, resolution=1, highlightthickness=0, command=ChangeVolume)
    vol.set(100)
    vol.pack(anchor=CENTER, expand=False, padx=16, pady=8)

    musdes = tk.Label(canvas, text="Music Volume:", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, highlightbackground="#000", highlightthickness=3)
    musdes.pack(side=BOTTOM, anchor=W, expand=False, padx=24, ipady=16)

    canvas.delete(lg)

def ReadThis():
    global reader, gbk
    startbutton.pack_forget()
    optionbutton.pack_forget()
    helpbutton.pack_forget()
    quitbutton.pack_forget()

    reader = tk.Label(canvas, text="The day is December 27th. The Reindeer Communication System receives a message: an impersonator of Santa Claus appears near the South Pole. His name is Sfantul Nicolae (with a Romanian a). He is reported to wear a burgundian wine colored tracksuit and sports a black beard. Nicolae and his aides (Magnus and Aelfons are currently unavailible, wahhh) are trying to undermine your (Santa's) work and are trying to steal presents from children of the nice list. It is up to the Holy Hierarch, Bishop of Myra, Saint Nicholas to stop them. Will you be able to?",
                      font=("Ace Attorney", 28), bg=btn_color, fg="white", highlightbackground="#000", highlightthickness=4, width=winwidth, wraplength=winheight)
    reader.pack(fill="both", expand=False, padx=24, pady=24, ipadx=16, ipady=16, side=TOP, anchor=CENTER)

    gbk = tk.Button(canvas, text="Go Back", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=RTGoBack)
    gbk.pack(side=BOTTOM, anchor=SE, expand=False, padx=24, pady=24)

    canvas.delete(lg)

def OptGoBack():
    startbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
    optionbutton.pack(anchor=NW, expand=False, padx=16)
    helpbutton.pack(anchor=NW, expand=False, padx=16)
    quitbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
    opt1.pack_forget()
    volframe.pack_forget()
    vol.pack_forget()
    musdes.pack_forget()
    gbk.pack_forget()
    CreateLogo()

def RTGoBack():
    startbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
    optionbutton.pack(anchor=NW, expand=False, padx=16)
    helpbutton.pack(anchor=NW, expand=False, padx=16)
    quitbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
    reader.pack_forget()
    gbk.pack_forget()
    CreateLogo()

# Ładowanie i renderowanie obrazów
def Load():
    global pi_obj, frames
    snow = Image.open("textures/snow_resize.gif")
    frames = snow.n_frames
    pi_obj = []

    for i in range(frames):
        obj = PhotoImage(file="textures/snow_resize.gif", format=f"gif -index {i}") # po kiego grzyba i dlaczego pillow nie pozwala na normalne gify (:sob:)
        pi_obj.append(obj)
    Render()

def Render():
    global mbgimg, logo, lg
    mbgimg = Image.open("textures/romania.png")
    mbgimg = mbgimg.resize((winwidth,  winheight))
    mbgimg = ImageTk.PhotoImage(mbgimg)
    canvas.itemconfig(mb, image=mbgimg)
    if nicolae.health<=0 or player.health<=0:
        canvas.create_image(winwidth/2, winheight/2, image=mbgimg)
        pygame.mixer.music.load("music/maintheme.mp3")
        pygame.mixer.music.play(-1)

    sn = canvas.create_image(winwidth/2, winheight/2, image=None)

    def Gif(cur_frame=0):
        snow_gif = pi_obj[cur_frame]
        canvas.itemconfig(sn, image=snow_gif)
        cur_frame = (cur_frame + 1) % frames # reszta modulo, zeruje się gdy dojdzie do liczby klatek
        window.after(50, lambda: Gif(cur_frame))
    Gif()

    logo = Image.open('textures/logo.png')
    logo = ImageTk.PhotoImage(logo)
    CreateLogo()

    loadlab.pack_forget()
    startbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
    optionbutton.pack(anchor=NW, expand=False, padx=16)
    helpbutton.pack(anchor=NW, expand=False, padx=16)
    quitbutton.pack(anchor=NW, expand=False, padx=16, pady=16)
threading.Thread(target=Load, daemon=True).start()

def CreateLogo():
    global lg
    lg = canvas.create_image(winwidth-320, 150, image=logo)

# Przyciski
startbutton = tk.Button(canvas, text="Start", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=Start)
optionbutton = tk.Button(canvas, text="Options", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=Options)
helpbutton = tk.Button(canvas, text="Read This!", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=ReadThis)
quitbutton = tk.Button(canvas, text="Quit", font=("Arial Black", 24), bg=btn_color, fg="white", bd=5, width=20, command=Quit)

# Inne do menu
"""copimg = ImageTk.PhotoImage(file="textures/nicolae.png")
canvas.create_image(winwidth-200, winheight-210, image=copimg)"""

# -- Gra
# Wstęp
"""videoplayer = TkinterVideo(master=canvas, scaled=True)
def IntroCutscene():
    global videoplayer
    pygame.mixer.music.stop()
    videoplayer.load(r"cutscenes/jaruzel_test.mp4")
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()
def EndVideo(event):
    global videoplayer, game_on
    videoplayer.pack_forget()
    if game_on==False:
        StartGame()
videoplayer.bind("<<Ended>>", EndVideo)"""

"""triglav_on = False
serj_on = False
alfons_on = False
nicolae_on = False"""

# Interfejs walki
def FButtons():
    global hp_textbox, en_hp_text, atkbutton, passbutton, invbutton, fgt_textbox
    hp_textbox = tk.Label(canvas, text=f"HP: {player.health}", font=("Arial", 18), bg="white", fg="#3C3C3C",
                        highlightbackground="#3C3C3C", highlightthickness=3, anchor="w", justify="left")
    en_hp_text = tk.Label(canvas, text=f"Enemy HP: 0", font=("Arial", 18), bg="white", fg="#3C3C3C",
                        highlightbackground="#3C3C3C", highlightthickness=3, anchor="w", justify="left")
    atkbutton = tk.Button(canvas, text="⚔ Attack", font=("Arial", 36), bg="#D61C24", fg="white", bd=0, command=Attack)
    passbutton = tk.Button(canvas, text="🖐 Pass", font=("Arial", 36), bg="#D61C24", fg="white", bd=0, command=Pass)
    invbutton = tk.Button(canvas, text="❣ Inventory", font=("Arial", 36), bg="#D61C24", fg="white", bd=0, command=Inventory)
    fgt_textbox = tk.Label(canvas, text="", font=("Arial", 48), bg="white", fg="#3C3C3C",
                        highlightbackground="#3C3C3C", highlightthickness=4, anchor="w", justify="left", width=winwidth)
    
    hp_textbox.pack(expand=False, side=TOP, padx=24, pady=24, ipadx=16, anchor=E)
    en_hp_text.pack(expand=False, side=TOP, padx=24, ipadx=16, anchor=E)
    fgt_textbox.pack(expand=False, side=BOTTOM, padx=24, pady=24, ipadx=16, ipady=24)
    atkbutton.pack(expand=False, side=LEFT, padx=24, anchor=S)
    invbutton.pack(expand=False, side=LEFT, padx=24, anchor=S)
    passbutton.pack(expand=False, side=RIGHT, padx=24, anchor=S)

def Attack():
    global atk, chance, fightID, supply_atk, inven, inv_switch
    chance = random.randint(0,3)
    if chance != 0:
        if supply_atk==True:
            atk = random.randint(72,150) + random.randint(75, 100)
        else:
            atk = random.randint(72,150)
        pygame.mixer.Sound.play(smack)
    elif chance==0:
        atk = 0
        pygame.mixer.Sound.play(miss)
        fgt_textbox.config(text="MISS!")
    if atk != 0:
        if fightID==1:
            triglav.health = triglav.health - atk
            fgt_textbox.config(text=f"Triglav lost {atk} HP!")
            en_hp_text.config(text=f"Enemy HP: {triglav.health}")
        if fightID==2:
            serj.health = serj.health - atk
            fgt_textbox.config(text=f"Selferč lost {atk} HP!")
            en_hp_text.config(text=f"Enemy HP: {serj.health}")
        if fightID==3:
            alfons.health = alfons.health - atk
            fgt_textbox.config(text=f"Älfons lost {atk} HP!")
            en_hp_text.config(text=f"Enemy HP: {alfons.health}")
        if fightID==5:
            nicolae.health = nicolae.health - atk
            fgt_textbox.config(text=f"Sfântul Nicolae lost {atk} HP!")
            en_hp_text.config(text=f"Enemy HP: {nicolae.health}")

    if inv_switch==True:
        inv_switch = False
        inven.destroy()
    atkbutton.config(state=DISABLED, bg="#C0C0C0")
    invbutton.config(state=DISABLED, bg="#C0C0C0")
    passbutton.config(state=DISABLED, bg="#C0C0C0")
    window.after(2000, EnemyAttack)

obtable = ["null", triglav, serj, alfons, "null", nicolae]

def EnemyAttack():
    global enem_atk, enem_chance, fightID, hp_zeroed, passed, ptsd_num, enemynametable, sliprand, obtable
    
    enem_chance = random.randint(0, 5)

    if passed and ptsd_num==3:
        sliprand = random.randint(100, 200)
        fgt_textbox.config(text=f"{enemynametable[fightID]} SLIPPED and lost {sliprand} HP!")
        obtable[fightID].health = obtable[fightID].health - sliprand
        en_hp_text.config(text=f"Enemy HP: {obtable[fightID].health}")
        PlayerHealthCheck()
    else:
        if passed==True:
            enem_chance = enem_chance - random.randint(2,4)
        else:
            enem_chance = enem_chance

        if enem_chance > 0:
            if fightID==1:
                enem_atk = random.randint(triglav.attack, triglav.max)
            if fightID==2:
                enem_atk = random.randint(serj.attack, serj.max)
            if fightID==3:
                enem_atk = random.randint(alfons.attack, alfons.max)
            if fightID==5:
                enem_atk = random.randint(nicolae.attack, nicolae.max)
        elif enem_chance<=0:
            enem_atk = 0
            pygame.mixer.Sound.play(miss)
            fgt_textbox.config(text="The enemy MISSED!")
        PlayerHealthCheck()

    HealthCheck()
    ButtonDisable()
    
def ButtonEnable():
    global atkbutton, invbutton, passbutton
    if game_on==True:
        atkbutton.config(state=NORMAL, bg="#D61C24")
        invbutton.config(state=NORMAL, bg="#D61C24")
        passbutton.config(state=NORMAL, bg="#D61C24")

def ButtonDisable():
    global hp_zeroed, passed, supply_atk, ptsd_num
    passed = False
    supply_atk = False
    if ptsd_num==3:
        ptsd_num = 0
    if hp_zeroed!=True and player.health>0:
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")
        window.after(2000, ButtonEnable)
    elif hp_zeroed:
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")

def PlayerHealthCheck():
    global hp_zeroed, gamover, go, game_on, ptsd_num
    if hp_zeroed==False and enem_atk>0 and ptsd_num!=3:
        player.health = player.health - enem_atk
        pygame.mixer.Sound.play(smack)
        fgt_textbox.config(text=f"You lost {enem_atk} HP!")
        hp_textbox.config(text=f"HP: {player.health}")
        if player.health<=0:
            game_on = False
            window.after(3000, YouDied)
        
def YouDied():
    global gamover, go
    canvas.delete('all')
    SeekAndDestroy()
    gamover = Image.open("textures/gameover.png")
    gamover = gamover.resize((winwidth, winheight))
    gamover = ImageTk.PhotoImage(gamover)
    go = canvas.create_image(winwidth/2, winheight/2, image=gamover)
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(overscream)
    window.after(26000, Clear)

def HealthCheck():
    global hp_zeroed, triglav_on, serj_on, alfons_on, nicolae_on

    if triglav.health<=0 and triglav_on==True:
        hp_zeroed = True
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")
        fgt_textbox.config(text="Magnus Triglav was defeated.")
        triglav_on=False
        window.after(5000, Clear)
        window.after(5000, FightII)
    if serj.health<=0 and serj_on==True:
        hp_zeroed = True
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")
        fgt_textbox.config(text="Selferč was defeated.")
        serj_on=False
        window.after(5000, Clear)
        window.after(5000, FightV) #
    if alfons.health<=0 and alfons_on==True:
        hp_zeroed = True
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")
        fgt_textbox.config(text="Älfons G. Trank was defeated.")
        alfons_on=False
        window.after(5000, Clear)
        window.after(5000, FightV)
    if nicolae.health<=0 and nicolae_on==True:
        hp_zeroed = True
        atkbutton.config(state=DISABLED, bg="#C0C0C0")
        invbutton.config(state=DISABLED, bg="#C0C0C0")
        passbutton.config(state=DISABLED, bg="#C0C0C0")
        fgt_textbox.config(text="Sfântul Nicolae was defeated.")
        nicolae_on=False
        window.after(5000, Clear)

# Ekwipunek
def Inventory():
    global inven, itlab, it1, it2, it3, inv_switch
    inv_switch = not inv_switch

    if inv_switch:
        inven = tk.Frame(canvas, bg="white", highlightbackground="#3C3C3C", highlightthickness=3)
        inven.place(x=8, y=8)
        itlab = tk.Label(inven, text="Inventory", font=("Arial Black", 18), bg="white", bd=0, anchor="w", fg="#3C3C3C", justify="left")
        itlab.pack(side=TOP, anchor=W, expand=False, padx=8, pady=8)
        if sp_atk_used<15:
            it1 = tk.Button(inven, text=player.inventory[0], font=("Arial", 18), bg="white", bd=0, anchor="w", fg="#3C3C3C", justify="left", command=SupplyAttack)
            it1.pack(side=TOP, anchor=W, expand=False, padx=8, pady=8)
        it2 = tk.Button(inven, text=player.inventory[1], font=("Arial", 18), bg="white", bd=0, anchor="w", fg="#3C3C3C", justify="left", command=Slipper)
        it2.pack(side=TOP, anchor=W, expand=False, padx=8, pady=8)
        if hl_used<2:
            it3 = tk.Button(inven, text=player.inventory[2], font=("Arial", 18), bg="white", bd=0, anchor="w", fg="#3C3C3C", justify="left", command=Heal)
            it3.pack(side=TOP, anchor=W, expand=False, padx=8, pady=8)
    else:
        inven.destroy()

def SupplyAttack():
    global supply_atk, sp_atk_used, inv_switch
    supply_atk = True
    sp_atk_used += 1
    inv_switch = False
    inven.destroy()
    fgt_textbox.config(text=f"Santa used {player.inventory[0]}! It's gonna get spicy!")

def Slipper():
    fgt_textbox.config(text=f"{player.inventory[1]}...")

def Heal():
    global hl_used, inv_switch
    hl_used += 1
    inv_switch = False
    inven.destroy()

    player.health += 500
    hp_textbox.config(text=f"HP: {player.health}")
    fgt_textbox.config(text=f"The {player.inventory[2]}! You feel sugar in your blood!")

def Pass():
    global passed, ptsd_num, inven, inv_switch
    passed = True
    ptsd_num = (ptsd_num + 1) % 4
    fgt_textbox.config(text="PASSED!")

    if inv_switch==True:
        inv_switch = False
        inven.destroy()
    atkbutton.config(state=DISABLED, bg="#C0C0C0")
    invbutton.config(state=DISABLED, bg="#C0C0C0")
    passbutton.config(state=DISABLED, bg="#C0C0C0")
    window.after(2000, EnemyAttack)

# cZYSTKA
def SeekAndDestroy():
    hp_textbox.destroy()
    en_hp_text.destroy()
    fgt_textbox.destroy()
    atkbutton.destroy()
    invbutton.destroy()
    passbutton.destroy()

def Clear():
    global hp_zeroed, hl_used, sp_atk_used
    hp_zeroed = False
    hl_used = 0
    sp_atk_used = 0
    if nicolae.health<=0 or player.health<=0:
        SeekAndDestroy()
        window.after(1000, Render)
    canvas.delete('all')

# Nazwy przeciwników (moziem zrobić wcześniej, ale mi się nie choczu)
enemynametable = ["null", "Magnus Triglav", "Selferč", "Älfons G. Trank", "null", "Sfântul Nicolae"]

# Walki
def FightI():
    global slovenia, slov, santa, fightID, hp_zeroed, triglav_on
    fightID = 1
    triglav_on = True

    en_hp_text.config(text=f"Enemy HP: {triglav.health}")

    pygame.mixer.music.load("music/ubicu_te.mp3")
    pygame.mixer.music.play(-1)

    slovenia = Image.open("textures/slovenia.png")
    slovenia = slovenia.resize((winwidth,  winheight))
    slovenia = ImageTk.PhotoImage(slovenia)
    slov = canvas.create_image(winwidth/2, winheight/2, image=slovenia)

    santa = ImageTk.PhotoImage(file="textures/santa.png")
    canvas.create_image(winwidth/6, winheight-winheight/3 + 50, image=santa)

    fgt_textbox.config(text="Make a move.")

def FightII():
    global armenia, arma, santa, serji, fightID, hp_zeroed, serj_on
    fightID = 2
    player.health = 1000
    hp_textbox.config(text=f"HP: {player.health}")
    serj_on = True
    ButtonEnable()

    en_hp_text.config(text=f"Enemy HP: {serj.health}")

    pygame.mixer.music.load("music/attack.mp3")
    pygame.mixer.music.play(-1)

    armenia = Image.open("textures/armenia.png")
    armenia = armenia.resize((winwidth,  winheight))
    armenia = ImageTk.PhotoImage(armenia)
    arma = canvas.create_image(winwidth/2, winheight/2, image=armenia)

    santa = ImageTk.PhotoImage(file="textures/santa.png")
    canvas.create_image(winwidth/6, winheight-winheight/3 + 50, image=santa)

    serji = ImageTk.PhotoImage(file="textures/serj.png")
    canvas.create_image(winwidth/6 * 5, winheight-winheight/3 + 50, image=serji)

    fgt_textbox.config(text="Make a move.")

def FightIII():
    global namibia, namb, santa, fightID, hp_zeroed, alfons_on
    fightID = 3
    player.health = 1000
    hp_textbox.config(text=f"HP: {player.health}")
    alfons_on = True
    ButtonEnable()

    en_hp_text.config(text=f"Enemy HP: {alfons.health}")
    
    pygame.mixer.music.load("music/2sips.mp3")
    pygame.mixer.music.play(-1)

    namibia = Image.open("textures/namibia.png")
    namibia = namibia.resize((winwidth,  winheight))
    namibia = ImageTk.PhotoImage(namibia)
    namb = canvas.create_image(winwidth/2, winheight/2, image=namibia)

    santa = ImageTk.PhotoImage(file="textures/santa.png")
    canvas.create_image(winwidth/6, winheight-winheight/3 + 50, image=santa)

    fgt_textbox.config(text="Make a move.")    

def FightV():
    global southpole, spol, santa, nicimg, fightID, hp_zeroed, nicolae_on
    fightID = 5
    player.health = 1000
    hp_textbox.config(text=f"HP: {player.health}")
    nicolae_on = True
    ButtonEnable()

    en_hp_text.config(text=f"Enemy HP: {nicolae.health}")

    pygame.mixer.music.load("music/carolofthebells.mp3")
    pygame.mixer.music.play(-1)

    southpole = Image.open("textures/southpole.png")
    southpole = southpole.resize((winwidth,  winheight))
    southpole = ImageTk.PhotoImage(southpole)
    spol = canvas.create_image(winwidth/2, winheight/2, image=southpole)

    santa = ImageTk.PhotoImage(file="textures/santa.png")
    canvas.create_image(winwidth/6, winheight-winheight/3 + 50, image=santa)

    nicimg = ImageTk.PhotoImage(file="textures/nicolae.png")
    canvas.create_image(winwidth/6 * 5, winheight-winheight/3 + 50, image=nicimg)
    
    fgt_textbox.config(text="Make a move.")

window.mainloop()