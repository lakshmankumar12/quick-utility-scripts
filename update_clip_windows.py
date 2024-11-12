#!python3

from tkinter import Tk
import win32clipboard
import win32con

r = Tk()
r.withdraw()
r.clipboard_clear()

with open(r"C:\Users\laksh\Documents\cliptest.txt","r",encoding="utf-8") as fd:
    contents = fd.read().strip()
r.clipboard_clear()
r.clipboard_append(contents)
r.update()
a = r.clipboard_get()
if a != contents:
    printf(f"Huh! I dont see the same content")
r.destroy()

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardText(contents, win32con.CF_UNICODETEXT)
win32clipboard.CloseClipboard()
