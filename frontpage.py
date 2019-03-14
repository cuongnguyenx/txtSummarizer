from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import tkinter as tk
from tkinter import ttk
import lxrTest
import time
import numpy as np
import os
import grabheadline
import tkinter.messagebox
import tkinter.scrolledtext as tkst


class FrontPageGrid:
    def __init__(self, master):

        self.currMaster = master  # the master should be the root
        self.main = Frame(master, bg='khaki3')  # Main Frame, contains Image (2x3) Grid
        self.title = Frame(master, bg='khaki3')  # Contains the title "WHAT"S ON THE FRONT PAGE"

        self.title_lbl = Label(self.title, justify=tk.CENTER, font=("Yu Gothic Medium", 30, 'bold'),
                               text="WHAT'S ON THE FRONT PAGE ?", bg='khaki3')
        self.title_lbl.pack()

        # Photos to populate buttons
        self.photo_ny = ImageTk.PhotoImage(Image.open('./imgs/nytimes_2.jpg'))
        self.photo_wapo = ImageTk.PhotoImage(Image.open('./imgs/wapo_2.jpg'))
        self.photo_bbc = ImageTk.PhotoImage(Image.open('./imgs/bbc_2.jpg'))
        self.photo_reuters = ImageTk.PhotoImage(Image.open('./imgs/reuters.png'))
        self.photo_guardian = ImageTk.PhotoImage(Image.open('./imgs/guardian.png'))
        self.photo_wsj = ImageTk.PhotoImage(Image.open('./imgs/wsj_2.jpg'))
        self.photo_ap = ImageTk.PhotoImage(Image.open('./imgs/apnews.png'))

        # Declaring buttons and putting them in place
        self.btn_ny = Button(self.main, bg='white', width=435, height=350, image=self.photo_ny)
        self.btn_ny.bind('<ButtonRelease-1>', self.ny_listen)  # Bind Left Click Event to a listener
        self.btn_ny.grid(row=0, column=0, sticky='news', padx=(15, 5),
                         pady=(35, 5))  # Add padding for aesthetic purposes

        self.btn_wapo = Button(self.main, bg='white', width=435, height=350, image=self.photo_wapo)
        self.btn_wapo.bind('<ButtonRelease-1>', self.wapo_listen)
        self.btn_wapo.grid(row=0, column=1, sticky='news', padx=(5, 5), pady=(35, 5))

        self.btn_bbc = Button(self.main, bg='white', width=435, height=350, image=self.photo_bbc)
        self.btn_bbc.bind('<ButtonRelease-1>', self.bbc_listen)
        self.btn_bbc.grid(row=0, column=2, sticky='news', padx=(5, 5), pady=(35, 5))

        self.btn_reuters = Button(self.main, bg='white', width=435, height=350, image=self.photo_reuters)
        self.btn_reuters.bind('<ButtonRelease-1>', self.reuters_listen)
        self.btn_reuters.grid(row=1, column=0, sticky='news', padx=(15, 5), pady=(5, 50))

        self.btn_guardian = Button(self.main, bg='white', width=435, height=350, image=self.photo_guardian)
        self.btn_guardian.bind('<ButtonRelease-1>', self.guardian_listen)
        self.btn_guardian.grid(row=1, column=1, sticky='news', padx=(5, 5), pady=(5, 50))

        self.btn_ap = Button(self.main, bg='white', width=435, height=350, image=self.photo_ap)
        self.btn_ap.bind('<ButtonRelease-1>', self.ap_listen)
        self.btn_ap.grid(row=1, column=2, sticky='news', padx=(5, 5), pady=(5, 50))

        self.title.pack(side="top", fill=BOTH)
        self.main.pack(side="bottom", fill=BOTH)

    def ny_listen(self, event):
        # Grab the list of links and titles from the front page of nytimes. See grabheadline.py
        currlinks, currtitles = grabheadline.grabfront('https://nytimes.com')

        # If there are no links to be grabbed, it must mean there's no Internet connection
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            # Replace the GUI of the front grid with the generated headline list of the clicked website (i.e nytimes here)
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'New York Times', currlinks, currtitles)

    def wapo_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://washingtonpost.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Washington Post', currlinks, currtitles)

    def reuters_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://reuters.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Reuters', currlinks, currtitles)

    def bbc_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://bbc.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'BBC', currlinks, currtitles)

    def guardian_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://www.theguardian.com/international')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'The Guardian', currlinks, currtitles)

    def wsj_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://wsj.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Wall Street Journal', currlinks, currtitles)

    def ap_listen(self, event):
        currlinks, currtitles = grabheadline.grabfront('https://apnews.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Associated Press', currlinks, currtitles)


class FrontPageList:
    def __init__(self, master, title, currlinks, currtitles):
        self.sub = Frame(master, bg='khaki3', width=1370, height=820)
        self.currMaster = master

        self.currtitles = currtitles
        self.currlinks = currlinks
        self.uptitle = title

        self.subtitle = Label(self.sub, text=self.uptitle, font=('Yu Gothic Medium', 26, 'bold'), padx=5, pady=5,
                              bg='khaki3')
        self.subtitle.pack(side='top')

        self.listhead = Listbox(self.sub, height=22, highlightcolor='blue', font=('Yu Mincho', 18),
                                selectmode=tk.SINGLE)
        self.listhead.pack(expand=1, fill=tk.BOTH)
        self.listhead.bind('<<ListboxSelect>>', self.genSummary)

        for val, title in enumerate(currtitles):
            self.listhead.insert(val + 1, title)

        self.backmain = Button(self.sub, text='Return', pady=5, font=('Verdana', 20, 'bold'), bg='red')
        self.backmain.bind('<ButtonRelease-1>', self.retMain)
        self.backmain.pack()

        self.sub.pack(fill=BOTH)

    def genSummary(self, event):
        x = self.listhead.curselection()
        print(x)
        self.sub.pack_forget()
        if len(x) != 0:
            sum_frame = SummaryFrame(self.currlinks[x[0]], self.currMaster, self.uptitle, self.currlinks,
                                     self.currtitles)
            sum_frame.getSmryCustom()

    def retMain(self, event):
        self.sub.pack_forget()
        self.listhead.delete(0, tk.END)
        fpg = FrontPageGrid(self.currMaster)


class SummaryFrame:
    def __init__(self, url, master, title, currlinks, currtitles):
        self.currMaster = master
        self.prog1 = Frame(master, bg="khaki3")  # Frame for Entry, Textbox and their labels
        self.prog2 = Frame(master, bg='khaki3')  # Frame for RESET Button
        self.prog3 = Frame(master, bg='khaki3')  # Frame for length slider
        self.url = url
        self.uptitle = title
        self.currlinks = currlinks
        self.currtitles = currtitles

        # Labels "Enter URL" and "Output Summary:
        self.lbl_smry = Label(self.prog1, text="Output Summary: ", bg="khaki3", font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)

        # Put the labels into the grid, lbl_link at (0,0) and lbl_smry at (1,0)
        self.lbl_smry.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(5, 0))

        # Link Entry and Result Textbox
        self.smry_text = tkst.ScrolledText(self.prog1, state=tk.DISABLED, wrap=tk.WORD, width=110, height=46,
                                           relief=tk.SUNKEN, bg='turquoise')
        self.smry_text.grid(row=1, column=1, sticky='news', pady=(0, 5))

        self.back_button = Button(self.prog2, text="RETURN", justify=tk.CENTER, height=5, pady=5, bg="red",
                                  font=("Verdana", 20, 'bold'))
        self.back_button.bind('<Button-1>', self.backToList)
        self.back_button.pack()

        self.prog2.configure(bg="khaki3")
        self.prog3.configure(bg="khaki3")
        self.prog1.configure(width=100)
        # Bind the Entry to the getSmry event through pressing Return

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
        self.status = 0
        self.keywords = []

    def getSmryCustom(self):
        titlefont = Font(family="Times New Roman", size=22, weight="bold", underline=1)
        keyfont = Font(family="Calibri", size=18, slant="italic")
        contentfont = Font(family="Yu Gothic Medium", size=14)
        # DEFAULT_SUMMARY = 5

        # Disable reset button during processing, will enable later
        self.back_button.configure(state=tk.DISABLED)

        # Get text from User Link
        link = self.url

        # Allows editing of the TextBox to insert summary
        self.smry_text.configure(state=tk.NORMAL)
        # Delete previous content
        self.smry_text.delete('1.0', tk.END)
        # In order for the GUI to update, this line is necessary
        self.smry_text.update()
        time.sleep(0.5)

        # Generate base summary of size 5
        self.status, self.title, self.sentences, self.scores, self.bound, self.keywords = lxrTest.generateSummary(link,
                                                                                                                  'custom')

        if self.status == 0:
            leng = self.scores.__len__()
            DEFAULT_SUMMARY = int(round((leng / 5), 0))
            # DEFAULT_SUMMARY = leng

            key_string = 'KEYWORDS: '
            if self.keywords is None:
                self.smry_text.configure(state=tk.DISABLED)
                self.back_button.configure(state=tk.NORMAL)
                tk.messagebox.showerror("Error", "Unable To Generate Summary")
                return

            for key in self.keywords:
                key_string = key_string + key + ', '
            key_string = key_string[:-2]

            self.slider.configure(from_=1, to=leng, showvalue=1, tickinterval=round((leng / 10), 0))
            self.slider.grid()

            final_list = np.sort(self.scores[:DEFAULT_SUMMARY + 1])
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
                                # print(self.sentences[s])
                                tmp += self.sentences[s]
                            else:
                                prt += tmp + "\n\n"
                                tmp = "" + self.sentences[s]
                            bl = self.bound[val2 - 1]
                            br = self.bound[val2]
                            break

                # prt += str(val + 1) + ".  " + s + "\n\n"
            self.slider.set(DEFAULT_SUMMARY)

            self.title = re.sub(r'[\n\t]', r'', self.title)
            self.title = re.sub(r'\s+', r' ', self.title)

            # Inserting summary into the Textfield
            self.smry_text.insert(tk.END, self.title + "\n\n")
            self.smry_text.tag_add("title", "1.0", "1.end")
            self.smry_text.tag_configure("title", font=titlefont, foreground="DarkOrange3")

            self.smry_text.insert(tk.END, key_string + "\n")
            self.smry_text.tag_add("key", "3.0", "3.end")
            self.smry_text.tag_configure("key", font=keyfont, foreground="gray32")

            self.smry_text.insert(tk.END, prt)
            self.smry_text.tag_add("content", "4.0", tk.END)
            self.smry_text.tag_configure("content", font=contentfont)

        elif self.status == -69:
            tk.messagebox.showerror("Error", "Invalid Link")
        else:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")

        self.smry_text.configure(state=tk.DISABLED)
        self.back_button.configure(state=tk.NORMAL)

    def backToList(self, event):
        self.prog1.pack_forget()
        self.prog2.pack_forget()
        self.prog3.pack_forget()
        fpl = FrontPageList(self.currMaster, self.uptitle, self.currlinks, self.currtitles)

    def sliderUpdate(self, event):
        titlefont = Font(family="Times New Roman", size=22, weight="bold", underline=1)
        keyfont = Font(family="Calibri", size=18, slant="italic")
        contentfont = Font(family="Yu Gothic Medium", size=14)

        # Disable reset button during processing, will enable later

        currval = self.slider.get()

        if currval == 0:
            return
        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()

        final_list = np.sort(self.scores[:currval + 1])
        # summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
        prt = ''
        tmp = ''
        bl = -1
        br = -1

        key_string = 'KEYWORDS:'
        for key in self.keywords:
            key_string = key_string + key + ', '
        key_string = key_string[:-2]

        for val, s in enumerate(final_list):
            for val2 in range(len(self.bound)):
                if val2 == 0:
                    continue
                else:
                    if self.bound[val2 - 1] < s <= self.bound[val2]:
                        if self.bound[val2 - 1] == bl and self.bound[val2] == br:
                            # print(self.sentences[s])
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
        self.smry_text.tag_configure("title", font=titlefont, foreground="DarkOrange3")

        self.smry_text.insert(tk.END, key_string + "\n")
        self.smry_text.tag_add("key", "3.0", "3.end")
        self.smry_text.tag_configure("key", font=keyfont, foreground="gray50")

        self.smry_text.insert(tk.END, prt)
        self.smry_text.tag_add("content", "4.0", tk.END)
        self.smry_text.tag_configure("content", font=contentfont)

        self.smry_text.configure(state=tk.DISABLED)


'''
root = Tk()
fp = FrontPageGrid(root)
root.geometry("1370x820")
root.mainloop()
'''
# https://stackoverflow.com/questions/4297949/image-on-a-button
