from tkinter import *
import keyword_interface as ki
import tkinter as tk

root = Tk()

wrap = Frame(root, bg='khaki3')
kf = ki.keywordFrame(wrap)
wrap.pack(expand=True, fill=tk.BOTH)
root.geometry("1400x800")
root.resizable(0, 0)
root.mainloop()
