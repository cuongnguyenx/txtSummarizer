from tkinter import *
from tkinter.font import Font
import tkinter as tk
import lxrTest
import time

class SummaryFrame:
    # TODO Implement multiprocessing to speed up runtime
    # TODO Prettify GUI
    def __init__(self, master):
        prog = Frame(master, bg="red", height=640, width=1080)
        self.lbl_link = Label(prog, text="Enter URL: ")
        self.lbl_smry = Label(prog, text="Output Summary: ")

        self.lbl_link.grid(row=0, sticky=N+E+W)
        self.lbl_smry.grid(row=1, sticky=N+E+W+S)

        self.entry_link = Entry(prog)
        self.smry_text = Text(prog, state=tk.DISABLED, wrap=tk.WORD, width=121, height=38)

        self.entry_link.grid(row=0, column=1, sticky=N+E+W)
        self.smry_text.grid(row=1, column=1, sticky=N+E+W+S)

        self.entry_link.bind("<Return>", self.getSmry)

        # Grid.rowconfigure(root, 0, weight=1)  # Configure the first row of the grid, so that it will expand into extra space
        # Grid.columnconfigure(root, 0, weight=1)  # Ditto, but for the first column

        # Grid.rowconfigure(root, 1, weight=1)
        # Grid.columnconfigure(root, 1, weight=1)

        prog.pack()

    def getSmry(self, event):

        titlefont = Font(family="Times New Roman", size=20, weight="bold", underline=1)
        contentfont = Font(family="Interstate", size=14)

        link = self.entry_link.get()
        self.entry_link.configure(state='readonly')

        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()
        time.sleep(0.5)

        title, smry = lxrTest.generateSummary(link)
        self.smry_text.insert(tk.END, title+"\n\n")
        self.smry_text.tag_add("title", "1.0", "1.end")
        self.smry_text.tag_configure("title", font=titlefont, foreground="gray")

        self.smry_text.insert(tk.END, smry)
        self.smry_text.tag_add("content", "2.0", tk.END)
        self.smry_text.tag_configure("content", font=contentfont)

        self.smry_text.configure(state=tk.DISABLED)

        self.entry_link.configure(state=tk.NORMAL)


root = Tk()
root.geometry("1080x640")
root.resizable(0, 0)
sm = SummaryFrame(root)
root.mainloop()

