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
        bg_color = '#c6c8c9'

        self.currMaster = master  # the master should be the root
        self.main = Frame(master, bg=bg_color)  # Main Frame, contains Image (2x3) Grid
        self.title = Frame(master, bg=bg_color)  # Contains the title "WHAT"S ON THE FRONT PAGE"

        self.title_lbl = Label(self.title, justify=tk.CENTER, font=("Yu Gothic Medium", 30, 'bold'),
                               text="WHAT'S ON THE FRONT PAGE ?", bg=bg_color)
        self.title_lbl.pack()

        # Photos to populate buttons
        self.photo_ny = ImageTk.PhotoImage(Image.open('nytimes_2.png'))
        self.photo_wapo = ImageTk.PhotoImage(Image.open('wapo_2.png'))
        self.photo_bbc = ImageTk.PhotoImage(Image.open('bbc_2.png'))
        self.photo_reuters = ImageTk.PhotoImage(Image.open('reuters.png'))
        self.photo_guardian = ImageTk.PhotoImage(Image.open('guardian.png'))
        # self.photo_wsj = ImageTk.PhotoImage(Image.open('./imgs/wsj_2.jpg'))
        self.photo_ap = ImageTk.PhotoImage(Image.open('apnews.png'))

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
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://nytimes.com')

        # If there are no links to be grabbed, it must mean there's no Internet connection
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            # Replace the GUI of the front grid with the generated headline list of the clicked website (i.e nytimes here)
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'New York Times', currlinks, currtitles, currcategories)

    def wapo_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://washingtonpost.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Washington Post', currlinks, currtitles, currcategories)

    def reuters_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://reuters.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Reuters', currlinks, currtitles, currcategories)

    def bbc_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://bbc.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'BBC', currlinks, currtitles, currcategories)

    def guardian_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://www.theguardian.com/international')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'The Guardian', currlinks, currtitles, currcategories)

    def wsj_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://wsj.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Wall Street Journal', currlinks, currtitles, currcategories)

    def ap_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://apnews.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Associated Press', currlinks, currtitles, currcategories)

    def latimes_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront('https://latimes.com')
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Los Angeles Times', currlinks, currtitles, currcategories)

    def huffington_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront("http://huffpost.com")
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'Huffington Post', currlinks, currtitles, currcategories)

    def npr_listen(self, event):
        currlinks, currtitles, currcategories = grabheadline.grabfront("https://www.npr.org/")
        if len(currlinks) == 0:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
        else:
            self.title.pack_forget()
            self.main.pack_forget()
            fpl = FrontPageList(self.currMaster, 'National Public Radio', currlinks, currtitles, currcategories)


class FrontPageList:
    def __init__(self, master, title, currlinks, currtitles, currcategories):
        self.bg_color = '#c6c8c9'
        self.button_color = 'gray27'
        self.subcombine = Frame(master, bg=self.bg_color, width=1370, height=820)
        self.subup = Frame(self.subcombine, bg=self.bg_color, width=1370, height=200)
        self.subdown = Frame(self.subcombine, bg=self.bg_color, width=1370, height=620)
        self.currMaster = master

        self.currtitles = currtitles
        self.currlinks = currlinks
        self.currcategories = currcategories
        self.available = []
        self.uptitle = title
        self.categ_dict = dict()

        for i in range(len(self.currtitles)):
            self.available.append(i)

        for categ in self.currcategories:
            if categ not in self.categ_dict.keys():
                self.categ_dict[categ] = 1
            else:
                self.categ_dict[categ] += 1

        self.subtitle = Label(self.subup, text=self.uptitle, font=('Yu Gothic Medium', 26, 'bold'), padx=5, pady=5,
                              bg=self.bg_color)
        self.subtitle.pack()

        drop_style = ttk.Style().configure('list.TListbox', padding=(5, 5))

        choices_categ = ['All (%d)' % len(currlinks)]
        for categ in self.categ_dict.keys():
            choices_categ.append((categ + ' (%d)') % self.categ_dict[categ])
        self.size_drop = ttk.Combobox(self.subup, value=choices_categ, width=26, state='readonly', style=drop_style)

        self.size_drop.current(0)
        self.size_drop.pack()
        self.size_drop.bind("<<ComboboxSelected>>", self.changeCategory)

        self.listhead = Listbox(self.subdown, height=21, highlightcolor='blue', font=('Yu Mincho', 18),
                                selectmode=tk.SINGLE)
        self.listhead.pack(expand=1, fill=tk.BOTH)
        self.listhead.bind('<<ListboxSelect>>', self.genSummary)

        for val, title in enumerate(currtitles):
            self.listhead.insert(val + 1, title)

        self.backmain = Button(self.subdown, text='\u2190', pady=5, font=('Verdana', 20, 'bold'), bg=self.button_color,
                               justify=tk.LEFT)
        self.backmain.bind('<ButtonRelease-1>', self.retMain)
        self.backmain.pack(side=tk.LEFT)

        self.subup.pack(fill=BOTH)
        self.subdown.pack(fill=BOTH)
        self.subcombine.pack(fill=BOTH)

    def genSummary(self, event):
        selection = self.listhead.curselection()
        self.subcombine.pack_forget()
        if len(selection) != 0:
            index_sel = self.available[selection[0]]
            print(index_sel)
            sum_frame = SummaryFrame_Front(self.currlinks[index_sel], self.currMaster, self.uptitle, self.currlinks,
                                           self.currtitles, self.currcategories)
            sum_frame.getSmryCustom()

    def retMain(self, event):
        self.subcombine.pack_forget()
        self.listhead.delete(0, tk.END)
        fpg = FrontPageGrid(self.currMaster)

    def changeCategory(self, event):
        self.listhead.delete(0, tk.END)
        currCateg = self.size_drop.get()
        currCateg = currCateg[0:currCateg.index(' (')]
        self.available = []
        if currCateg == 'All':
            for i in range(len(self.currtitles)):
                self.available.append(i)
                self.listhead.insert(i + 1, self.currtitles[i])
        else:
            count = 1
            for i in range(len(self.currtitles)):
                if self.currcategories[i] == currCateg:
                    self.available.append(i)
                    self.listhead.insert(count, self.currtitles[i])
                    count = count + 1


class SummaryFrame_Front:
    def __init__(self, url, master, title, currlinks, currtitles, currcategories):
        self.currMaster = master
        self.bg_color = '#c6c8c9'
        self.button_color = 'gray27'

        self.prog1 = Frame(master, bg=self.bg_color)  # Frame for Entry, Textbox and their labels
        self.prog2 = Frame(master, bg=self.bg_color)  # Frame for RESET Button
        self.prog3 = Frame(master, bg=self.bg_color)  # Frame for length slider
        self.url = url
        self.uptitle = title
        self.currlinks = currlinks
        self.currtitles = currtitles
        self.currcategories = currcategories

        # Labels "Enter URL" and "Output Summary:
        self.lbl_smry = Label(self.prog1, text="Output Summary: ", bg=self.bg_color, font=("Verdana", 12, 'bold'),
                              relief=tk.SUNKEN)

        # Put the labels into the grid, lbl_link at (0,0) and lbl_smry at (1,0)
        self.lbl_smry.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(5, 0))

        # Link Entry and Result Textbox
        self.smry_text = tkst.ScrolledText(self.prog1, state=tk.DISABLED, wrap=tk.WORD, width=110, height=46,
                                           relief=tk.SUNKEN, bg='turquoise')
        self.smry_text.grid(row=1, column=1, sticky='news', pady=(0, 5))

        self.back_button = Button(self.prog2, text="\u2190", height=5, pady=5, bg=self.button_color,
                                  font=("Verdana", 20, 'bold'), justify=tk.LEFT)
        self.back_button.bind('<Button-1>', self.backToList)
        self.back_button.pack(side=tk.LEFT)

        self.prog2.configure(bg=self.bg_color)
        self.prog3.configure(bg=self.bg_color)
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
        fpl = FrontPageList(self.currMaster, self.uptitle, self.currlinks, self.currtitles, self.currcategories)

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
fp = FrontPageGrid(root)F
root.geometry("1370x820")
root.mainloop()
'''
# https://stackoverflow.com/questions/4297949/image-on-a-button
