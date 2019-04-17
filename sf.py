from tkinter import *
import tkinter as tk
import lxrTest
import time
import numpy as np
import tkinter.scrolledtext as tkst
import tkinter.messagebox
import config
from PIL import Image, ImageTk
from hoverButton import HoverButton

import playsound
import gtts
import string
import threading
import random
import logging
import traceback


class SummaryFrame:
    # TODO Implement multiprocessing to speed up runtime
    # TODO Prettify GUI
    def __init__(self, master):
        self.prog1 = Frame(master, bg=config.bg_color)  # Frame for Entry and its label
        self.prog2 = Frame(master, bg=config.bg_color)  # Frame for RESET Button
        self.prog3 = Frame(master, bg=config.bg_color)  # Frame for length slider
        self.prog4 = Frame(master, bg=config.bg_color)
        self.bg_image = ImageTk.PhotoImage(Image.open('texture.jpg'))

        self.bg1 = Label(self.prog1, image=self.bg_image)
        self.bg1.image = self.bg_image
        self.bg1.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg2 = Label(self.prog2, image=self.bg_image)
        self.bg2.image = self.bg_image
        self.bg2.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg3 = Label(self.prog3, image=self.bg_image)
        self.bg3.image = self.bg_image
        self.bg3.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg4 = Label(self.prog4, image=self.bg_image)
        self.bg4.image = self.bg_image
        self.bg4.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.speaker_icon = ImageTk.PhotoImage(Image.open('speaker_icon.png'))
        self.prt = ''

        # Labels "Enter URL" and "Output Summary:
        self.lbl_link = Label(self.prog1, text="   Enter URL:    ", bg=config.bg_color, font=config.slider_label_font,
                              relief=tk.SUNKEN)
        # self.lbl_smry = Label(self.prog1, text="Output Summary: ", bg=config.bg_color, font=("Verdana", 12, 'bold'),
        # relief=tk.SUNKEN)

        # Put the labels into the grid, lbl_link at (0,0) and lbl_smry at (1,0)
        self.lbl_link.grid(row=0, sticky=N + E + W + S)
        # self.lbl_smry.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(5, 0))

        # Link Entry and Result Textbox
        self.entry_link = Entry(self.prog1, width=175, relief=tk.SUNKEN, bg=config.entry_color)
        self.smry_text = tkst.ScrolledText(self.prog4, state=tk.DISABLED, wrap=tk.WORD, width=133, height=42,
                                           relief=tk.FLAT, bg=config.entry_color, borderwidth=10)

        self.entry_link.grid(row=0, column=1, sticky="news")
        self.smry_text.grid(row=0, column=0, sticky='news', pady=(0, 5))

        # Reset Button
        self.reset_button = HoverButton(self.prog2, text="RESET", justify=tk.CENTER, height=5, pady=5,
                                        command=self.reset_everything, bg=config.button_color,
                                        fg=config.button_text_color,
                                        font=config.button_font)

        self.play_sound_button = HoverButton(self.prog2, bg=config.button_color, font=config.button_font, height=32,
                                             image=self.speaker_icon)
        self.play_sound_button.bind('<Button-1>', self.on_sound_button_click)
        self.play_sound_button.pack(side=tk.RIGHT)
        self.reset_button.pack()

        # Bind the Entry to the getSmry event through pressing Return
        self.entry_link.bind("<Return>", self.getSmryCustom)

        self.lbl_temp = Label(self.prog3, text="ARTICLE SUMMARY LENGTH", bg=config.slider_label_bg,
                              font=config.slider_label_font,
                              fg=config.slider_label_fg, relief=tk.GROOVE)
        self.lbl_temp.grid(row=0, pady=(4, 4), padx=(4, 4))

        # Article length slider
        self.slider = tk.Scale(self.prog3, from_=0, to=0, length=727, tickinterval=10, orient="vertical", showvalue=0,
                               relief=tk.SUNKEN, bg=config.slider_color)
        self.slider.bind('<ButtonRelease-1>', self.sliderUpdate)

        self.slider.grid(row=1, pady=(5, 0))
        self.slider.grid_remove()

        self.prog3.pack(side="right", fill=BOTH)
        self.prog1.pack(side="top", fill=BOTH)
        self.prog4.pack(side="top", fill=BOTH)
        self.prog2.pack(side="bottom", fill=BOTH)

        self.scores = np.array([0])
        self.sentences = []
        self.title = ''
        self.bound = []
        self.status = 0
        self.keywords = []

    def getSmryCustom(self, event):
        # DEFAULT_SUMMARY = 5

        # Disable reset button during processing, will enable later
        self.reset_button.configure(state=tk.DISABLED)
        self.slider.configure(state=tk.DISABLED)

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
        try:
            self.status, self.title, self.sentences, self.scores, self.bound, self.keywords = lxrTest.generateSummary(
                link,
                'custom')

        except Exception as e:
            tk.messagebox.showerror('Error', traceback.format_exc())
            self.reset_button.configure(state=tk.NORMAL)
            self.entry_link.configure(state=tk.NORMAL)

        # print(self.sentences)
        if self.status == 0:
            leng = self.scores.__len__()
            DEFAULT_SUMMARY = int(round((leng / 5), 0))
            # DEFAULT_SUMMARY = leng

            key_string = 'KEYWORDS:'
            # print(self.keywords)
            for key in self.keywords:
                key_string = key_string + key + ', '
            key_string = key_string[:-2]

            self.slider.configure(from_=1, to=leng, showvalue=1, tickinterval=round((leng / 10), 0))
            self.slider.grid()

            final_list = np.sort(self.scores[:DEFAULT_SUMMARY + 1])
            # summary = [self.sentences[i] for i in final_list]  # Getting the summary based on summary length
            self.prt = ''
            tmp = ''
            bl = -1
            br = -1

            # print(self.bound)
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
                                self.prt += tmp + "\n\n"
                                tmp = "" + self.sentences[s]
                            bl = self.bound[val2 - 1]
                            br = self.bound[val2]
                            break

                # prt += str(val + 1) + ".  " + s + "\n\n"

            self.reset_button.configure(state=tk.NORMAL)
            self.entry_link.configure(state=tk.NORMAL)
            self.slider.configure(state=tk.NORMAL)

            self.slider.set(DEFAULT_SUMMARY)

            self.title = re.sub(r'[\n\t]', r'', self.title)
            self.title = re.sub(r'\s+', r' ', self.title)

            # Inserting summary into the Textfield
            self.smry_text.insert(tk.END, self.title + "\n\n")
            self.smry_text.tag_add("title", "1.0", "1.end")
            self.smry_text.tag_configure("title", font=config.titlefont_sum, foreground=config.title_text_color)

            self.smry_text.insert(tk.END, key_string + "\n")
            self.smry_text.tag_add("key", "3.0", "3.end")
            self.smry_text.tag_configure("key", font=config.keyfont_sum, foreground=config.title_key_color)

            self.smry_text.insert(tk.END, self.prt)
            self.smry_text.tag_add("content", "4.0", tk.END)
            self.smry_text.tag_configure("content", font=config.contentfont_sum, lmargin2=20, lmargin1=20, rmargin=20)

        elif self.status == -69:
            tk.messagebox.showerror("Error", "Invalid Link")
            self.reset_button.configure(state=tk.NORMAL)
            self.entry_link.configure(state=tk.NORMAL)
            self.slider.configure(state=tk.NORMAL)
        else:
            tk.messagebox.showerror("Error", "Failed to Retrieve Website. No Internet Connection?")
            self.reset_button.configure(state=tk.NORMAL)
            self.entry_link.configure(state=tk.NORMAL)
            self.slider.configure(state=tk.NORMAL)

        self.entry_link.delete('0', tk.END)
        self.smry_text.configure(state=tk.DISABLED)

    # Clears all text
    def reset_everything(self):
        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.configure(state=tk.DISABLED)

        self.entry_link.delete('0', tk.END)
        self.scores = np.array([0])
        self.sentences = []
        self.title = ''
        self.bound = []
        self.status = 0
        self.keywords = []
        self.prt = ''
        self.slider.configure(from_=0, to=0, tickinterval=1)
        self.slider.grid_remove()

    def sliderUpdate(self, event):
        # Disable reset button during processing, will enable later
        self.reset_button.configure(state=tk.DISABLED)

        currval = self.slider.get()

        if currval == 0:
            return

        key_string = 'KEYWORDS:'
        # print(self.keywords)
        for key in self.keywords:
            key_string = key_string + key + ', '
        key_string = key_string[:-2]

        self.smry_text.configure(state=tk.NORMAL)
        self.smry_text.delete('1.0', tk.END)
        self.smry_text.update()

        final_list = np.sort(self.scores[:currval + 1])
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

        self.title = re.sub(r'[\n\t]', r'', self.title)
        self.title = re.sub(r'\s+', r' ', self.title)

        self.reset_button.configure(state=tk.NORMAL)
        self.entry_link.configure(state=tk.NORMAL)

        # Inserting summary into the Textfield
        self.smry_text.insert(tk.END, self.title + "\n\n")
        self.smry_text.tag_add("title", "1.0", "1.end")
        self.smry_text.tag_configure("title", font=config.titlefont_sum, foreground=config.title_text_color)

        self.smry_text.insert(tk.END, key_string + "\n")
        self.smry_text.tag_add("key", "3.0", "3.end")
        self.smry_text.tag_configure("key", font=config.keyfont_sum, foreground=config.title_key_color)

        self.smry_text.insert(tk.END, prt)
        self.smry_text.tag_add("content", "4.0", tk.END)
        self.smry_text.tag_configure("content", font=config.contentfont_sum, lmargin2=20, lmargin1=20, rmargin=20)

        self.entry_link.delete('0', tk.END)
        self.smry_text.configure(state=tk.DISABLED)

    def on_sound_button_click(self, event):
        print('Preparing To Play Sound...')
        thread1 = threading.Thread(target=self.playSSS, args=[])
        thread1.setDaemon(True)
        thread1.start()

    def playSSS(self):
        if self.prt == '':
            return
        tts = gtts.gTTS(
            text=self.prt,
            lang='en')
        allchar = string.ascii_letters + string.digits
        filename = "".join(random.choice(allchar) for x in range(12)) + ".mp3"
        tts.save(filename)
        playsound.playsound(filename)
