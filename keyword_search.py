import grabheadline
import lxrTest
import time
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import tkinter as tk
from tkinter import ttk


def graball():
    # Takes around 160-180s for 200 articles, way too slow
    prev = time.time()
    list_news = ['https://nytimes.com', 'https://reuters.com', 'https://bbc.com',
                 'https://www.theguardian.com/international', 'https://apnews.com',
                 'https://latimes.com', 'http://huffpost.com', 'https://www.npr.org/']
    links = []
    titles = []
    categories = []
    bags_key = [[]]
    keywords = dict()
    for source in list_news:
        prevt = time.time()
        templinks, temptitles, tempcategories = grabheadline.grabfront(source)
        # print(templinks)
        links.extend(templinks)
        titles.extend(temptitles)
        categories.extend(tempcategories)
        print(time.time() - prevt)

    for link in links:
        print(link)
        prevt = time.time()
        currkeys = lxrTest.generateKeywords(link)
        bags_key.append(currkeys)
        # print(type(currkeys))
        for key in currkeys:
            if key in keywords.keys():
                keywords[key] = keywords[key] + 1
            else:
                keywords[key] = 1
        print(time.time() - prevt)
    sred = sorted(keywords.items(), key=lambda value: value[1], reverse=True)
    bags_key = bags_key[1:]
    print(sred)
    print(time.time() - prev)


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
        results_prelim = [pool_prelim.apply_async(grabfront_wrapper, args=(source, val)) for val, source in
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
        results_final = [pool_final.apply_async(build_dictionary, args=(link, val)) for val, link in enumerate(links)]
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
        sred = sorted(keywords.items(), key=lambda value: value[1], reverse=True)

        print(bags_key[1:])
        print(sred)
        print(time.time() - prev)


graball_better()
