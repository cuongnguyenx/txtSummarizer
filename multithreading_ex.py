import threading
import time

import multiprocessing as mp
import random
import string
import grabheadline
import lxrTest


def grabfront_wrapper(source, pos):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    templinks, temptitles, tempcategories = grabheadline.grabfront(source)
    print(templinks)
    print(pos)
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
    pool_prelim = mp.Pool(processes=4)
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
    '''
    for i in range(int(len(links)/20) + 1):
        output = mp.Queue()
        curr_batch = []
        print('Staring Batch %s' % i)
        if len(link) - curr_count >= 5:
            for val, link in enumerate(links[curr_count:curr_count+5]):
                curr_batch.append(mp.Process(target=build_dictionary, args=(link, val, output)))
        else:
            for val, link in enumerate(links[curr_count:len(links)]):
                curr_batch.append(mp.Process(target=build_dictionary, args=(link, val, output)))

        for p in curr_batch:
            p.start()
        results_temp = [output.get() for p in curr_batch]

        for p in curr_batch:
            print('Ending Process')
            print(p)
            p.join()
            p.close()
        curr_count = curr_count + 5
        results_final.extend(results_temp)
    '''
    pool_final = mp.Pool(processes=8)
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

# print('sdasd')
# print(output)
# Get process results from the output queue
# print(time.time()-prev)

# print(results)

'''
def cube(x):
    return x**3


prev = time.time()


if __name__ == '__main__':
    pool = mp.Pool(processes=1)
    results = [pool.apply(cube, args=(x,)) for x in range(1, 1000)]
    # print(results)
    print(time.time()-prev)
'''

'''
Alternative Function
pool = mp.Pool(processes=4)
results = pool.map(cube, range(1,7))
print(results)
'''

'''
MP Queue + Process
# Define an output queue
output = mp.Queue()


# define a example function
def rand_string(length, pos, output):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    rand_str = ''.join(random.choice(
                        string.ascii_lowercase
                        + string.ascii_uppercase
                        + string.digits)
                   for i in range(length))
    output.put((pos, rand_str))


# Setup a list of processes that we want to run
processes = [mp.Process(target=rand_string, args=(5, x, output)) for x in range(4)]


if __name__ == '__main__':
    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = [output.get() for p in processes]

    print(results)
'''

'''
# Ten thread example
exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.count = count

    def run(self):
        print("Starting " + self.name)
        print_array(self.name, self.count, self.counter)
        print("Exiting " + self.name)


def print_array(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s\n" % (threadName, counter))
        counter -= 1


prev = time.time()
# Create new threads
thread1 = myThread(1, "Thread-1", 1, 10)
thread2 = myThread(2, "Thread-2", 1, 20)
thread3 = myThread(3, "Thread-3", 1, 30)
thread4 = myThread(4, "Thread-4", 1, 40)
thread5 = myThread(5, "Thread-5", 1, 50)
thread6 = myThread(6, "Thread-6", 1, 60)
thread7 = myThread(7, "Thread-7", 1, 70)
thread8 = myThread(8, "Thread-8", 1, 80)
thread9 = myThread(9, "Thread-9", 1, 90)
thread10 = myThread(10, "Thread-10", 1, 100)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()

print("Exiting Main Thread")
'''
