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
        self.prog1 = Frame(master, bg="khaki3")
        self.prog2 = Frame(master, bg='khaki3')
        self.prog3 = Frame(master, bg='khaki3')

        # Labels "Enter URL" and "Output Summary:
        self.lbl_link = Label(self.prog1, text="Enter URL: ", bg="khaki3", font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)
        self.lbl_smry = Label(self.prog1, text="Output Summary: ", bg="khaki3", font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)

        # Put the labels into the grid, lbl_link at (0,0) and lbl_smry at (1,0)
        self.lbl_link.grid(row=0, sticky=N + E + W + S, pady=(3, 0), padx=(5, 0))
        self.lbl_smry.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(5, 0))

        # Link Entry and Result Textbox
        self.entry_link = Entry(self.prog1, width=150, relief=tk.SUNKEN, bg='turquoise')
        self.smry_text = tkst.ScrolledText(self.prog1, state=tk.DISABLED, wrap=tk.WORD, width=110, height=46,
                                           relief=tk.SUNKEN, bg='turquoise')

        self.entry_link.grid(row=0, column=1, sticky="news", pady=(3, 0))
        self.smry_text.grid(row=1, column=1, sticky='news', pady=(0, 5))

        # Reset Button
        self.reset_button = Button(self.prog2, text="RESET", justify=tk.CENTER, height=5, pady=5,
                                   command=self.reset_everything, bg="red", font=("Verdana", 12, 'bold'))
        self.reset_button.pack()
        self.prog2.configure(bg="khaki3")
        self.prog3.configure(bg="khaki3")
        self.prog1.configure(width=100)
        # Bind the Entry to the getSmry event through pressing Return
        self.entry_link.bind("<Return>", self.getSmryCustom)

        self.lbl_temp = Label(self.prog3, text="ARTICLE SUMMARY LENGTH", bg="RoyalBlue3", font=("Verdana", 12, 'bold'),
                              fg="gold2", relief=tk.GROOVE)
        self.lbl_temp.grid(row=0, pady=(4, 4), padx=(4, 4))

        # Article length slider
        self.slider = tk.Scale(self.prog3, from_=0, to=0, length=727, tickinterval=10, orient="vertical", showvalue=0,
                               relief=tk.SUNKEN, bg="brown")
        self.slider.bind('<ButtonRelease-1>', self.sliderUpdate)

        self.slider.grid(row=1, pady=(5, 0))
        self.slider.grid_remove()

        self.prog3.pack(side="right", fill=BOTH)
        self.prog1.pack(side="top", fill=BOTH)
        self.prog2.pack(side="bottom", fill=BOTH)

        self.scores = np.array([0])
        self.sentences = []
        self.title = ''
        self.bound = []

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
        self.smry_text.insert(tk.END, title + "\n\n")
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
        # DEFAULT_SUMMARY = 5

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
        self.title, self.sentences, self.scores, self.bound = lxrTest.generateSummary(link, 'custom')
        leng = self.scores.__len__()
        DEFAULT_SUMMARY = int(round((leng / 5), 0))
        # DEFAULT_SUMMARY = leng
        print(DEFAULT_SUMMARY)

        self.slider.configure(from_=1, to=leng, showvalue=1, tickinterval=round((leng / 10), 0))
        self.slider.grid()

        final_list = np.sort(self.scores[:DEFAULT_SUMMARY])
        # summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
        prt = ''
        tmp = ''
        bl = -1
        br = -1

        for val, s in enumerate(final_list):
            for val2 in range(len(self.bound)):
                if val2 == 0:
                    continue
                else:
                    if self.bound[val2 - 1] < s <= self.bound[val2]:
                        if self.bound[val2 - 1] == bl and self.bound[val2] == br:
                            print(self.sentences[s])
                            tmp += self.sentences[s]
                        else:
                            prt += tmp + "\n\n"
                            tmp = "" + self.sentences[s]
                        bl = self.bound[val2 - 1]
                        br = self.bound[val2]
                        break

            # prt += str(val + 1) + ".  " + s + "\n\n"
        self.slider.set(DEFAULT_SUMMARY)

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
        self.smry_text.configure(state=tk.DISABLED)

        self.entry_link.delete('0', tk.END)
        self.scores = np.array([0])
        self.sentences = []
        self.title = ''
        self.slider.configure(from_=0, to=0, tickinterval=1)
        self.slider.grid_remove()

    def sliderUpdate(self, event):
        titlefont = Font(family="Times New Roman", size=20, weight="bold", underline=1)
        contentfont = Font(family="Interstate", size=14)

        # Disable reset button during processing, will enable later
        self.reset_button.configure(state=tk.DISABLED)

        currval = self.slider.get()

        if currval == 0:
            return
        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()

        final_list = np.sort(self.scores[:currval + 1])
        print(final_list)
        # summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
        prt = ''
        tmp = ''
        bl = -1
        br = -1

        for val, s in enumerate(final_list):
            for val2 in range(len(self.bound)):
                if val2 == 0:
                    continue
                else:
                    if self.bound[val2 - 1] < s <= self.bound[val2]:
                        if self.bound[val2 - 1] == bl and self.bound[val2] == br:
                            print(self.sentences[s])
                            tmp += self.sentences[s]
                        else:
                            prt += tmp + "\n\n"
                            tmp = "" + self.sentences[s]
                        bl = self.bound[val2 - 1]
                        br = self.bound[val2]
                        break

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
tabs = ttk.Notebook(root, height=800, width=1347)
progover = Frame(root, bg="white")
sm = SummaryFrame(progover)
frame2 = Frame(root)

tabs.add(progover, text="Link")
tabs.add(frame2, text="Hello")

tabs.pack(side="top", fill="both")

root.geometry("1347x820")
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
