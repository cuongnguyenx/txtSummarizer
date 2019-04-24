from sf import SummaryFrame
from frontpage import FrontPageGrid
from tkinter import *
from tkinter import ttk
from keyword_interface import keywordFrame
import os
from PIL import Image, ImageTk
import config

for file in os.listdir('./'):
    if 'mp3' in file:
        os.remove(file)

root = Tk()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

config.ratio_w = screen_w/1920
config.ratio_h = screen_h/1080

config.curr_height = screen_h
config.curr_width = screen_w

config.generate_fonts(config.ratio_w, config.ratio_h)
print(config.ratio_h)

tabs = ttk.Notebook(root, height=int(screen_h*3/4), width=int(screen_w*3/4))
bg_color = 'gray67'

progover = Frame(root, bg=bg_color)
frontover = Frame(root, bg=bg_color)
keyover = Frame(root, bg=bg_color)

bg_image = ImageTk.PhotoImage(Image.open('texture.jpg'))

bg_label_1 = Label(keyover, image=bg_image)
bg_label_1.image = bg_image
bg_label_1.place(x=0, y=0, relwidth=1, relheight=1)

bg_label_2 = Label(progover, image=bg_image)
bg_label_2.image = bg_image
bg_label_2.place(x=0, y=0, relwidth=1, relheight=1)

bg_label_3 = Label(frontover, image=bg_image)
bg_label_3.image = bg_image
bg_label_3.place(x=0, y=0, relwidth=1, relheight=1)

sm = SummaryFrame(progover)
fm = FrontPageGrid(frontover, 1, screen_w, screen_h)
km = keywordFrame(keyover)

tabs.add(frontover, text="Read the Frontpages")
tabs.add(keyover, text='Hot Keywords')
tabs.add(progover, text="Summary From Link")

tabs.pack(side="top", fill="both")

root.title('QNews')
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
