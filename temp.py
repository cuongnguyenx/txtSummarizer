import threading
from functools import partial
from tkinter import *
from tkinter import messagebox
import asyncio
import random
import grabheadline
from tkinter import ttk
import time
import lxrTest
import aioprocessing


# Please wrap all this code in a nice App class, of course


def _run_aio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


aioloop = asyncio.new_event_loop()
t = threading.Thread(target=partial(_run_aio_loop, aioloop))
t.daemon = True  # Optional depending on how you plan to shutdown the app
t.start()

buttonT = None


def do_freezed():
    """ Button-Event-Handler to see if a button on GUI works. """
    messagebox.showinfo(message='Tkinter is reacting.')


def do_tasks():
    """ Button-Event-Handler starting the asyncio part. """
    buttonT.configure(state=DISABLED)
    asyncio.run_coroutine_threadsafe(do_urls(), aioloop)


async def one_url(url, val):
    """ One task. """
    templinks, temptitles, tempcategories = grabheadline.grabfront(url)
    return val, templinks, temptitles


async def one_url_2(url, val):
    currkeys = lxrTest.generateKeywords(url)
    temp_d = dict()
    for key in currkeys:
        if key in temp_d.keys():
            temp_d[key] = temp_d[key] + 1
        else:
            temp_d[key] = 1
    return val, currkeys, temp_d


async def do_urls():
    links = []
    titles = []

    prev = time.time()
    list_news = ['https://nytimes.com', 'https://reuters.com', 'https://bbc.com',
                 'https://www.theguardian.com/international', 'https://apnews.com',
                 'https://latimes.com', 'http://huffpost.com', 'https://www.npr.org/']
    """ Creating and starting 10 tasks. """
    tasks = [one_url(url, val) for val, url in enumerate(list_news)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]

    results.sort(key=lambda tup: tup[0])

    for elem in results:
        links.extend(elem[1])
        titles.extend(elem[2])
    print(links)
    print(titles)

    tasks = [one_url_2(url, val) for val, url in enumerate(links)]
    completed, pending = await asyncio.wait(tasks)
    results_2 = [task.result() for task in completed]

    buttonT.configure(state=NORMAL)  # Tk doesn't seem to care that this is called on another thread
    print(time.time() - prev)


if __name__ == '__main__':
    root = Tk()

    buttonT = Button(master=root, text='Asyncio Tasks', command=do_tasks)
    buttonT.pack()
    buttonX = Button(master=root, text='Freezed???', command=do_freezed)
    buttonX.pack()
    progress = ttk.Progressbar(master=root, orient='horizontal', mode='indeterminate')
    progress.start(50)
    progress.pack()

    root.mainloop()
