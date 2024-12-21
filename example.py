'''import tkinter as tk
from PIL import Image

root = tk.Tk()
root.title("Displaing Gif")

file = "gif_file.gif"
info = Image.open(file)

frames = info.n_frames  # number of frames

photoimage_objects = []
for i in range(frames):
    obj = tk.PhotoImage(file=file, format=f"gif -index {i}")
    photoimage_objects.append(obj)


def animation(current_frame=0):
    global loop
    image = photoimage_objects[current_frame]

    gif_label.configure(image=image)
    current_frame = current_frame + 1

    if current_frame == frames:
        current_frame = 0

    loop = root.after(50, lambda: animation(current_frame))


def stop_animation():
    root.after_cancel(loop)


gif_label = tk.Label(root, image="")
gif_label.pack()

start = tk.Button(root, text="Start", command=lambda: animation(current_frame=0))
start.pack()

stop = tk.Button(root, text="Stop", command=stop_animation)
stop.pack()

root.mainloop()'''

'''import tkinter as tk

root = tk.Tk()

sib = tk.Label(root, text='Give em hell Harry', wraplength=8, justify='center')
sib.grid()

root.mainloop()'''

'''from tkinter import * 
  
  
root = Tk()   
root.geometry("400x300")  
  
v1 = DoubleVar() 
  
def show1():   
      
    sel = "Horizontal Scale Value = " + str(v1.get()) 
    l1.config(text = sel, font =("Courier", 14))   
  
  
s1 = Scale( root, variable = v1,  
           from_ = 1, to = 100,  
           orient = HORIZONTAL)    
  
l3 = Label(root, text = "Horizontal Scaler") 
  
b1 = Button(root, text ="Display Horizontal",  
            command = show1,  
            bg = "yellow")   
  
l1 = Label(root) 
  
  
s1.pack(anchor = CENTER)  
l3.pack() 
b1.pack(anchor = CENTER) 
l1.pack()  
  
root.mainloop()'''

import tkinter as tk
import pygame
from tkinter import *

w = tk.Tk()
pygame.init()

def change_vol(_=None):
    pygame.mixer.music.set_volume(vol.get())
    print(vol.get())
    vol.config(showvalue=vol.get())
#########################################

##########################
pygame.mixer.music.load("sound/smack.wav")
pygame.mixer.music.play(-1)

dob = DoubleVar()


vol = tk.Scale(w, from_ = 0, to = 1, orient = 'horizontal', resolution = .1, command=change_vol)
vol.grid(row = 3, column = 1)

w.mainloop()
