from tkinter import *
import tkinter as tk
import grabheadline
from multiprocessing.pool import ThreadPool
# import aioprocessing as ap
from tkinter.font import Font
import lxrTest
import time
import numpy as np
import tkinter.messagebox
import tkinter.scrolledtext as tkst

'''
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.button = ttk.Button(text="start", command=self.start)
        self.button.pack(side=tk.BOTTOM)
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.pack(side=tk.TOP, expand=True, fill=tk.X)

        self.bytes = 0
        self.maxbytes = 0

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        # simulate reading 500 bytes; update progress bar
        self.bytes += 500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)
'''

'''
def grabfront_wrapper(source, pos):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    templinks, temptitles, tempcategories = grabheadline.grabfront(source)
    print(templinks)
    print('[RESULT] FINISHED GRABBING from ' + source)
    return pos, templinks, temptitles, tempcategories


def build_dictionary(link, pos):
    currkeys = lxrTest.generateKeywords(link)
    temp_d = dict()
    for key in currkeys:
        if key in temp_d.keys():
            temp_d[key] = temp_d[key] + 1
        else:
            temp_d[key] = 1
    return pos, currkeys, temp_d


def graball_better():
    # https://sebastianraschka.com/Articles/2014_multiprocessing.html
    # Much better version, using python's multiprocessing module. Only takes around 45-50s
    prev = time.time()
    list_news = ['https://nytimes.com', 'https://reuters.com', 'https://bbc.com',
                 'https://www.theguardian.com/international', 'https://apnews.com',
                 'https://latimes.com', 'http://huffpost.com', 'https://www.npr.org/']
    links = []
    titles = []
    bags_key = [[]]
    keywords = dict()
    prevt = time.time()
    if __name__ == '__main__':
        print('[INFO] GRABBING HEADLINES FROM POPULAR NEWSPAPERS...')
        pool_prelim = ThreadPool(processes=4)
        results_prelim = [pool_prelim.apply_async(grabfront_wrapper, args=(source, val), callback=append_result) for val, source in
                          enumerate(list_news)]
        results_prelim = [p.get() for p in results_prelim]

        # Exit the completed processes
        results_prelim.sort(key=lambda tup: tup[0])
        print(results_prelim)

        for elem in results_prelim:
            links.extend(elem[1])
            titles.extend(elem[2])
        print(links)
        print(titles)
        print(time.time() - prev)
        print(len(links))

        output = mp.Queue()
        processes_deux = []
        for val, link in enumerate(links):
            processes_deux.append(mp.Process(target=build_dictionary, args=(link, val, output)))

        # prev = time.time()
        pool_final = ThreadPool(processes=8)
        results_final = [pool_final.apply_async(build_dictionary, args=(link, val)) for val, link in
                         enumerate(links)]
        results_final = [p.get() for p in results_final]
        results_final.sort(key=lambda tup: tup[0])
        print(results_final)
        print(time.time() - prev)

        for elem in results_final:
            bags_key.append(elem[1])
            dict_t = elem[2]
            for key in dict_t.keys():
                if key in keywords.keys():
                    keywords[key] = keywords[key] + dict_t[key]
                else:
                    keywords[key] = dict_t[key]
        sred_dict = sorted(keywords.items(), key=lambda value: value[1], reverse=True)

        bags_key = bags_key[1:]
        print(bags_key)
        print(sred_dict)
        print(time.time() - prev)
        return sred_dict, bags_key, links, titles
'''


class keywordFrame:
    # self, master, links, titles, sred_dict, keyword_occurrence, currSearch
    def __init__(self, *args):
        self.master = args[0]

        self.frame_top = Frame(self.master, bg='khaki3')
        self.frame_middle = Frame(self.master, bg='khaki3')
        self.frame_bottom = Frame(self.master, bg='khaki3')

        self.links = []
        self.titles = []
        self.sred_dict = []
        self.keyword_occurrence = dict()
        self.currSearch = ''

        if len(args) > 2:
            self.links = args[1]
            self.titles = args[2]
            self.sred_dict = args[3]
            self.keyword_occurrence = args[4]
            self.currSearch = args[5]

        self.keywords = dict()

        self.searchVar = StringVar()
        self.search_label = Label(self.frame_top, text="          Search:         ", bg="khaki3",
                                  font=("Verdana", 14, 'bold'),
                                  relief=tk.SUNKEN)
        self.search_box = Entry(self.frame_top, relief=tk.SUNKEN, bg='turquoise', width=200,
                                textvariable=self.searchVar, state=tk.DISABLED)
        self.searchVar.trace_add('write', self.searchKeyword)

        self.keyword_list_display = Listbox(self.frame_middle, height=21, highlightcolor='blue', font=('Yu Mincho', 18),
                                            selectmode=tk.SINGLE, width=106)
        self.keyword_list_display.bind('<<ListboxSelect>>', self.on_keyword_selection)

        # self.loading_bar = ttk.Progressbar(self.frame_middle, orient='horizontal', mode='indeterminate', length=1370)
        # self.loading_bar.start(50)
        self.loading_label = Label(self.frame_middle, text='Press GENERATE To Get Trending Keywords\n|\n|\n|\nv',
                                   bg="khaki3"
                                   , font=("Verdana", 32, 'bold'), justify=tk.CENTER)
        self.generate_button = Button(self.frame_bottom, text='GENERATE', justify=tk.CENTER
                                      , bg="red", font=("Verdana", 28, 'bold'), command=self.populate_keyword_list_gui)

        self.return_to_keyword_button = Button(self.frame_bottom, text='RETURN', justify=tk.CENTER, bg='red',
                                               font=('Verdana', 28, 'bold'), command=self.back_to_list)

        # self.loading_bar.grid(row=0, sticky='news', pady=(300, 0), padx=(5, 5))
        # Alternate (0,100) (80,5) with bar or (300,100) (170,5) without bar

        # self.keyword_list_display.grid(row=0, sticky='news')

        self.search_label.pack(expand=True, fill=tk.BOTH, side='left')
        self.search_box.pack(expand=True, fill=tk.BOTH, side='right')
        if len(args) == 1:
            self.loading_label.grid(row=0, sticky='news', pady=(300, 100), padx=(170, 5))
            self.generate_button.pack(expand=True, fill=tk.BOTH)
        else:
            self.search_box.configure(state=tk.NORMAL)
            self.keyword_list_display.grid(row=0, sticky='news')
            self.return_to_keyword_button.pack(expand=True, fill=tk.BOTH)
            self.gen_prev_state_with_key()

        self.frame_top.grid(row=0, sticky=N + E + W + S, pady=(0, 5), padx=(0, 0))
        self.frame_middle.grid(row=1, sticky=N + E + W + S, pady=(0, 5), padx=(10, 5))
        self.frame_bottom.grid(row=2, sticky=N + E + W + S, pady=(0, 10), padx=(5, 30))

    def reset_data(self):
        self.links = []
        self.titles = []
        self.sred_dict = []
        self.keyword_occurrence = dict()
        self.currSearch = ''
        self.keywords = dict()

    def transition_to_summary(self):
        self.frame_bottom.grid_remove()
        self.frame_middle.grid_remove()
        self.frame_top.grid_remove()

    def grabfront_wrapper(self, source, pos):
        """ Generates a random string of numbers, lower- and uppercase chars. """
        templinks, temptitles, tempcategories = grabheadline.grabfront(source)
        print(templinks)
        print('[RESULT] FINISHED GRABBING from ' + source)
        return pos, templinks, temptitles

    def build_dictionary(self, link, pos):
        currkeys = lxrTest.generateKeywords(link)
        temp_d = dict()
        for key in currkeys:
            if key in temp_d.keys():
                temp_d[key] = temp_d[key] + 1
            else:
                temp_d[key] = 1
        return pos, link, temp_d

    def graball_better(self):
        # https://sebastianraschka.com/Articles/2014_multiprocessing.html
        # Much better version, using python's multiprocessing module. Only takes around 45-50s
        prev = time.time()
        list_news = ['https://nytimes.com', 'https://reuters.com', 'https://bbc.com',
                     'https://www.theguardian.com/international', 'https://apnews.com',
                     'https://latimes.com', 'http://huffpost.com', 'https://www.npr.org/?t=1553745174305']

        prevt = time.time()
        if __name__ == '__main__' or 'keyword_interface':
            print('[INFO] GRABBING HEADLINES FROM POPULAR NEWSPAPERS...')
            pool_prelim = ThreadPool(processes=4)
            results_prelim = [pool_prelim.apply_async(self.grabfront_wrapper, args=(source, val)) for val, source in
                              enumerate(list_news)]
            results_prelim = [p.get() for p in results_prelim]

            # Exit the completed processes
            results_prelim.sort(key=lambda tup: tup[0])
            print(results_prelim)

            for elem in results_prelim:
                self.links.extend(elem[1])
                self.titles.extend(elem[2])
            print(self.links)
            print(self.titles)
            print(time.time() - prev)
            print(len(self.links))

            # prev = time.time()
            pool_final = ThreadPool(processes=8)
            results_final = [pool_final.apply_async(self.build_dictionary, args=(link, val)) for val, link in
                             enumerate(self.links)]

            results_final = [p.get() for p in results_final]
            results_final.sort(key=lambda tup: tup[0])
            print(results_final)
            print(time.time() - prev)

            for val, elem in enumerate(results_final):
                print(val)
                dict_t = elem[2]
                for key in dict_t.keys():
                    tokenized_key = str.split(key, ' ')
                    self.append_keys(key, val)

                    if len(tokenized_key) > 1:
                        for token in tokenized_key:
                            self.append_keys(token, val)

            print(self.keywords)
            self.sred_dict = sorted(self.keywords.items(), key=lambda value: value[1], reverse=True)
            print(self.keyword_occurrence)

            # print(self.sred_dict)
            print(time.time() - prev)

    def append_keys(self, key, val):
        if key in self.keywords.keys():
            self.keywords[key] = self.keywords[key] + 1
        else:
            self.keywords[key] = 1

        if key in self.keyword_occurrence.keys():
            self.keyword_occurrence[key].append(val)
        else:
            self.keyword_occurrence[key] = [val]

    def populate_keyword_list_gui(self):
        self.keyword_list_display.delete(0, tk.END)
        self.loading_label.grid_remove()
        self.keyword_list_display.grid(row=0, sticky='news')
        self.generate_button.configure(state=tk.DISABLED)
        self.keyword_list_display.insert(1,
                                         'PLEASE WAIT ABOUT 45 SECONDS... DO NOT CLICK ON ANYTHING WHILE THE PROGRAM IS RUNNING!')
        self.master.update()

        self.reset_data()
        self.graball_better()

        self.search_box.configure(state=tk.NORMAL)
        self.populate_keyword_list_algol()
        self.generate_button.configure(state=tk.NORMAL)

    def populate_keyword_list_algol(self):
        self.keyword_list_display.delete(0, tk.END)
        for val, elem in enumerate(self.sred_dict):
            # print(elem[0])
            '''
            acceptible = set(chr(i) for i in range(0x0000, 0xFFFF + 1))
            if not set(elem[0]).issubset(acceptible):
                print(elem[0])
                continue
            '''
            if elem[1] < 3:
                continue
            self.keyword_list_display.insert(val + 1, '%d. %s - %d matches' % (val + 1, elem[0], elem[1]))
        self.master.update()

    def back_to_list(self):
        self.return_to_keyword_button.pack_forget()
        self.generate_button.pack(expand=True, fill=tk.BOTH)
        self.master.update()
        self.keyword_list_display.bind('<<ListboxSelect>>', self.on_keyword_selection)
        self.populate_keyword_list_algol()

    def searchKeyword(self, *args):
        self.keyword_list_display.bind('<<ListboxSelect>>', self.on_keyword_selection)
        self.search_box.configure(state=tk.DISABLED)
        self.keyword_list_display.delete(0, tk.END)
        searchString = self.search_box.get()
        lenSearch = len(searchString)

        counter = 1
        for elem in enumerate(self.sred_dict):
            if elem[1][1] < 3:
                continue
            tokened = str.split(elem[1][0], ' ')
            # print(tokened)
            for token in tokened:
                if len(token) < lenSearch:
                    continue
                else:
                    if token[0:lenSearch] == searchString:
                        self.keyword_list_display.insert(counter,
                                                         '%d. %s - %d matches' % (counter, elem[1][0], elem[1][1]))
                        counter = counter + 1
                        break
        self.search_box.configure(state=tk.NORMAL)

    def genTarget(self, link):
        str_out = ''
        if 'nytimes' in link:
            str_out = 'New York Times'
        elif 'reuters' in link:
            str_out = 'Reuters'
        elif 'bbc' in link:
            str_out = 'BBC'
        elif 'guardian' in link:
            str_out = 'The Guardian'
        elif 'apnews' in link:
            str_out = 'Associated Press'
        elif 'latimes' in link:
            str_out = 'Los Angeles Times'
        elif 'huffpost' in link:
            str_out = 'Huffington Post'
        elif 'npr' in link:
            str_out = 'NPR'

        return '(%s)' % str_out

    def on_keyword_selection(self, event):
        selection = self.keyword_list_display.curselection()[0]
        string_sel = self.keyword_list_display.get(selection)
        key_sel = string_sel[string_sel.index('.') + 2:string_sel.index('-') - 1]
        self.currSearch = key_sel
        print(key_sel)

        self.keyword_list_display.delete(0, tk.END)
        for val, index in enumerate(self.keyword_occurrence[key_sel]):
            targetLink = ''
            try:
                targetLink = self.links[index]
            except IndexError:
                print('OOR!')

            news_target_title = self.genTarget(targetLink)
            self.keyword_list_display.insert(val + 1, self.titles[index] + " " + news_target_title)

        self.generate_button.pack_forget()
        self.return_to_keyword_button.pack(fill=tk.BOTH, expand=True)
        self.keyword_list_display.bind('<<ListboxSelect>>', self.on_link_selection)

    def gen_prev_state_with_key(self):
        for val, index in enumerate(self.keyword_occurrence[self.currSearch]):
            targetLink = ''
            try:
                targetLink = self.links[index]
            except IndexError:
                print('OOR!')

            news_target_title = self.genTarget(targetLink)
            self.keyword_list_display.insert(val + 1, self.titles[index] + " " + news_target_title)

        self.generate_button.pack_forget()
        self.return_to_keyword_button.pack(fill=tk.BOTH, expand=True)
        self.keyword_list_display.bind('<<ListboxSelect>>', self.on_link_selection)

    def on_link_selection(self, event):
        self.transition_to_summary()
        try:
            selection = self.keyword_occurrence[self.currSearch][self.keyword_list_display.curselection()[0]]
            summary_frame_gen = summaryFrame_Key(self.master, selection, self.links, self.titles, self.sred_dict,
                                                 self.keyword_occurrence, self.currSearch)
            summary_frame_gen.getSmryCustom()
        except IndexError:
            print('OOR!')


class summaryFrame_Key:
    # self, master, index, links, titles, sred_dict, keyword_occurrence, currSearch
    def __init__(self, *args):
        self.currMaster = args[0]
        print(self.currMaster)

        self.prog1 = Frame(self.currMaster, bg="khaki3")  # Frame for Entry, Textbox and their labels
        self.prog2 = Frame(self.currMaster, bg='khaki3')  # Frame for RESET Button
        self.prog3 = Frame(self.currMaster, bg='khaki3')  # Frame for length slider
        self.url = ''
        self.uptitle = ''

        if len(args) == 7:
            self.index_sel = args[1]
            self.currlinks = args[2]
            self.currtitles = args[3]
            self.sorted_keyword_dict = args[4]
            self.keyword_occurrence = args[5]
            self.currSearch = args[6]

            self.url = self.currlinks[self.index_sel]
            self.uptitle = self.currtitles[self.index_sel]

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
        print(self.currMaster)
        print(type(self.currMaster))
        fpl = keywordFrame(self.currMaster, self.currlinks, self.currtitles, self.sorted_keyword_dict,
                           self.keyword_occurrence, self.currSearch)

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

wrap = Frame(root, bg='khaki3')
kf = keywordFrame(wrap)
wrap.pack(expand=True, fill=tk.BOTH)
root.geometry("1400x800")
root.resizable(0,0)

root.mainloop()
'''
