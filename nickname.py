import  Tkinter
from Tkinter import *

win = Tk
win.geometry('300*100')

t1 = Label(win, text = "enter your nickname", fg = "blue")
t1.config(font = ("Verdana", 25))
t1.pack()


edit = Entry(win, width = 20, bg = "violet")
edit.pack()

win.mainloop()