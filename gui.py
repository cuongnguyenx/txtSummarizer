from tkinter import *
from tkinter.font import Font
import tkinter as tk
from tkinter import ttk
import lxrTest
import time
import numpy as np
import tkinter.scrolledtext as tkst


class SummaryFrame:
    # TODO Implement multiprocessing to speed up runtime
    # TODO Prettify GUI
    def __init__(self, master):
        self.prog1 = Frame(master, bg="khaki3", height=640, width=1100)
        self.prog2 = Frame(master, bg='khaki3', height=20, width=1100)

        # Labels "Enter URL" and "Output Summary:
        self.lbl_link = Label(self.prog1, text="Enter URL: ", bg="khaki3", font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)
        self.lbl_smry = Label(self.prog1, text="Output Summary: ", bg="khaki3", font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)
        self.lbl_link.grid(row=0, sticky=N + E + W + S, pady=(3, 0), padx=(5, 0))
        self.lbl_smry.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(5, 0))
        self.filler = Label(self.prog1, text="", bg="khaki3", relief=tk.SUNKEN)
        self.filler.grid(row=1, column=2, sticky="news", pady=(0, 5))

        # Link Entry and Result Textbox
        self.entry_link = Entry(self.prog1, width=150, relief=tk.SUNKEN, bg='turquoise')
        self.smry_text = tkst.ScrolledText(self.prog1, state=tk.DISABLED, wrap=tk.WORD, width=108, height=46,
                                           relief=tk.SUNKEN, bg='white')

        self.entry_link.grid(row=0, column=1, sticky=N + W + S, pady=(3, 0))
        self.smry_text.grid(row=1, column=1, sticky='news', pady=(0, 5))

        # Reset Button
        self.reset_button = Button(self.prog2, text="RESET", justify=tk.CENTER, height=5, pady=5,
                                   command=self.reset_everything, bg="red", font=("Verdana", 12, 'bold'))
        self.reset_button.pack()

        # Dropdown Menu to select summary size
        self.size_drop = ttk.Combobox(self.prog1, value=['# SENTENCES'], width=14, state='readonly')
        self.size_drop.current(0)
        self.size_drop.grid(row=0, column=2, sticky="", pady=(3, 0))
        self.size_drop.bind("<<ComboboxSelected>>", self.dropdown_update)

        # Bind the Entry to the getSmry event through pressing Return
        self.entry_link.bind("<Return>", self.getSmryCustom)

        self.prog1.pack(side="top")
        self.prog2.pack(side="bottom", fill=BOTH)

        self.scores = np.array([0])
        self.sentences = []
        self.title = ''

    def getSmryNormal(self, event):

        titlefont = Font(family="Times New Roman", size=20, weight="bold", underline=1)
        contentfont = Font(family="Interstate", size=14)

        self.reset_button.configure(state=tk.DISABLED)

        link = self.entry_link.get()
        self.entry_link.configure(state='readonly')

        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()
        time.sleep(0.5)

        title, smry = lxrTest.generateSummary(link, 'default')
        self.smry_text.insert(tk.END, title+"\n\n")
        self.smry_text.tag_add("title", "1.0", "1.end")
        self.smry_text.tag_configure("title", font=titlefont, foreground="gray")

        self.smry_text.insert(tk.END, smry)
        self.smry_text.tag_add("content", "2.0", tk.END)
        self.smry_text.tag_configure("content", font=contentfont)

        self.smry_text.configure(state=tk.DISABLED)
        self.reset_button.configure(state=tk.NORMAL)
        self.entry_link.configure(state=tk.NORMAL)

    def getSmryCustom(self, event):
        titlefont = Font(family="Times New Roman", size=20, weight="bold", underline=1)
        contentfont = Font(family="Interstate", size=14)
        DEFAULT_SUMMARY = 5

        # Disable reset button during processing, will enable later
        self.reset_button.configure(state=tk.DISABLED)

        # Get text from User Link
        link = self.entry_link.get()
        self.entry_link.configure(state='readonly')

        # Allows editing of the TextBox to insert summary
        self.smry_text.configure(state=tk.NORMAL)
        # Delete previous content
        self.smry_text.delete('1.0', tk.END)
        # In order for the GUI to update, this line is necessary
        self.smry_text.update()
        time.sleep(0.5)

        # Generate base summary of size 5
        self.title, self.sentences, self.scores = lxrTest.generateSummary(link, 'custom')
        leng = self.scores.__len__()

        choices = ['# SENTENCES']
        for i in range(leng):
            choices.append(str(i + 1))

        '''
        self.size_drop.grid_remove()
        self.size_drop = ttk.Combobox(self.prog1, value=choices, width=14)
        self.size_drop.grid(row=0, column=2, sticky="")
        '''

        self.size_drop['values'] = choices

        final_list = np.sort(self.scores[:DEFAULT_SUMMARY])
        summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
        prt = ''
        for val, s in enumerate(summary):
            prt += str(val + 1) + ".  " + s + "\n\n"
        self.size_drop.current(5)

        # Inserting summary into the Textfield
        self.smry_text.insert(tk.END, self.title + "\n\n")
        self.smry_text.tag_add("title", "1.0", "1.end")
        self.smry_text.tag_configure("title", font=titlefont, foreground="gray")

        self.smry_text.insert(tk.END, prt)
        self.smry_text.tag_add("content", "2.0", tk.END)
        self.smry_text.tag_configure("content", font=contentfont)

        self.smry_text.configure(state=tk.DISABLED)
        self.reset_button.configure(state=tk.NORMAL)
        self.entry_link.configure(state=tk.NORMAL)

    # Clears all text
    def reset_everything(self):
        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.configure(state=tk.DISABLED)

        self.entry_link.delete('0', tk.END)
        self.scores = np.array([0])
        self.sentences = []
        self.title = ''
        self.size_drop['values'] = ['# SENTENCES']
        self.size_drop.current(0)

    def dropdown_update(self, event):
        titlefont = Font(family="Times New Roman", size=20, weight="bold", underline=1)
        contentfont = Font(family="Interstate", size=14)

        # Disable reset button during processing, will enable later
        self.reset_button.configure(state=tk.DISABLED)

        currVal = self.size_drop.get()

        if currVal == '# SENTENCES':
            return
        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()

        final_list = np.sort(self.scores[:int(currVal)])
        summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
        prt = ''
        for val, s in enumerate(summary):
            prt += str(val + 1) + ".  " + s + "\n\n"
        self.size_drop.current(currVal)

        # Inserting summary into the Textfield
        self.smry_text.insert(tk.END, self.title + "\n\n")
        self.smry_text.tag_add("title", "1.0", "1.end")
        self.smry_text.tag_configure("title", font=titlefont, foreground="gray")

        self.smry_text.insert(tk.END, prt)
        self.smry_text.tag_add("content", "2.0", tk.END)
        self.smry_text.tag_configure("content", font=contentfont)

        self.smry_text.configure(state=tk.DISABLED)
        self.reset_button.configure(state=tk.NORMAL)
        self.entry_link.configure(state=tk.NORMAL)


root = Tk()
tabs = ttk.Notebook(root, height=800, width=1080)
progover = Frame(root)
sm = SummaryFrame(progover)
frame2 = Frame(root)

tabs.add(progover, text="Link")
tabs.add(frame2, text="Hello")

tabs.pack(side="top", fill="both")

root.geometry("1190x820")
# root.resizable(0, 0)
root.mainloop()

# https://docs.python.org/3/library/tkinter.ttk.html#combobox
# https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list#45442534
# https://www.tutorialspoint.com/python/tk_entry.htm
# https://stackoverflow.com/questions/21056601/tkinter-readonly-combobox-listener
# https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
