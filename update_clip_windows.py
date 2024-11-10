#!python3

from tkinter import Tk

r = Tk()
r.withdraw()
r.clipboard_clear()

with open(r"C:\Users\laksh\Documents\cliptest.txt","r",encoding="utf-8") as fd:
    contents = fd.read().strip()
r.clipboard_clear()
r.clipboard_append(contents)
r.update()
r.destroy()

