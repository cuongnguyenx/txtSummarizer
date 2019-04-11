import tkinter as tk
import numpy as np
from sf import SummaryFrame
from frontpage import FrontPageGrid
from tkinter import *
from tkinter import ttk
from keyword_interface import keywordFrame
import os
from tkinter.font import Font

'''
for filename in os.listdir("build"):
      os.rename("build\\" + filename + "\lib\multiprocessing\Pool.pyc",
                  "build\\" + filename + "\lib\multiprocessing\pool.pyc")
'''

for file in os.listdir('./'):
    if 'mp3' in file:
        os.remove(file)

root = Tk()
tabs = ttk.Notebook(root, height=800, width=1347)
bg_color = 'gray67'


progover = Frame(root, bg=bg_color)
frontover = Frame(root, bg=bg_color)
keyover = Frame(root, bg=bg_color)

sm = SummaryFrame(progover)
fm = FrontPageGrid(frontover, 1)
km = keywordFrame(keyover)

tabs.add(frontover, text="Read the Frontpages")
tabs.add(keyover, text='Hot Keywords')
tabs.add(progover, text="Summary From Link")

tabs.pack(side="top", fill="both")

# root.geometry("1380x840")
root.title('QNews')
# root.resizable(0, 0)
root.mainloop()

# https://docs.python.org/3/library/tkinter.ttk.html#combobox
# https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list#45442534
# https://www.tutorialspoint.com/python/tk_entry.htm
# https://stackoverflow.com/questions/21056601/tkinter-readonly-combobox-listener
# https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
# https://stackoverflow.com/questions/3966303/tkinter-slider-how-to-trigger-the-event-only-when-the-iteraction-is-complete#comment75690571_16970862
# https://stackoverflow.com/questions/47200625/how-to-make-ttk-scale-behave-more-like-tk-scale
# https://www.tutorialspoint.com/python/tk_scale.htm
# https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Notebook.html
