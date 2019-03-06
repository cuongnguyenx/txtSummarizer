import bs4 as bs
import urllib.request
import urllib.error
import re
import tkinter as tk
import lxml
import nltk


def grabfront(link):
    try:
        scraped_data = urllib.request.urlopen(link)
    except urllib.error.URLError:
        return [], []

    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    verboten = ['crossword', 'podcast', 'graphics', 'photography']
    links = []
    titles = []

    if 'nytimes.com' in link:
        headlines = parsed_article.find_all('article', {'class': 'css-8atqhb'})
        for xx in headlines[:-1]:
            sublink = xx.find('a')['href']
            title = xx.find('h2').text

            if not any([x in sublink for x in verboten]):
                links.append(link + sublink)
            else:
                continue
            titles.append(title)
            print(link + sublink)
            print(title)
            print('\n')

    if 'washingtonpost.com' in link:
        print('{INFO] WAPO')
        headlines = parsed_article.find_all('div', {'class': ["headline x-small normal-style text-align-inherit",
                                                              "headline xx-small normal-style text-align-inherit",
                                                              "headline small normal-style text-align-inherit"]})
        print(headlines)
        for xx in headlines[:-1]:
            sublink = xx.find('a')['href']
            title = xx.text

            if not any([x in sublink for x in verboten]):
                links.append(sublink)
            else:
                continue
            titles.append(title)
            print(sublink)
            print(title)
            print('\n')

    if 'reuters.com' in link:
        headlines_1 = parsed_article.find_all('div', {'class': ['story-content', 'feature']})
        for xx in headlines_1[:-1]:
            if xx.find('a'):
                atag = xx.find('a')
                sublink = atag['href']
            else:
                continue
            if atag.find('h3'):
                tt = atag.find('h3')
                if tt['class'] == 'article-heading':
                    continue
                title = tt.text
                # print(re.sub(r'[\t\n]+', r"", title) + "\n")
            elif atag.find('h2'):
                title = atag.find('h2').text
                # print(re.sub(r'[\t\n]+', r"", title) + "\n")
            else:
                continue
            links.append(sublink)
            titles.append(re.sub(r'[\t\n]+', r"", title))

    if 'bbc.com' in link:
        headlines_1 = parsed_article.find_all('div', {'class': ['media__content']})
        for xx in headlines_1[:-1]:
            sublink = ''
            if not xx.find('p'):
                continue

            if xx.find('a'):
                atag = xx.find('a')
                if 'bbc.com' not in atag['href']:
                    sublink = link + atag['href']
                else:
                    sublink = atag['href']
                title = atag.text

            else:
                continue
            links.append(sublink)
            titles.append(re.sub(r'[\s]+', r" ", title))

            print(sublink)
            print(re.sub(r'[\s]+', r" ", title) + "\n")

    if 'theguardian.com' in link:
        sections = parsed_article.find_all('section', {'id': ['headlines', 'opinion', 'spotlight']})
        for section in sections:
            headlines = section.find_all('h3', {'class': 'fc-item__title'})
            for xx in headlines[:-1]:
                sublink = xx.find('a')['href']
                title = xx.find('span', {'class': 'js-headline-text'}).text
                links.append(sublink)
                titles.append(title)

                print(sublink)
                print(title + "\n")

    if 'wsj.com' in link:
        headlines = parsed_article.find_all('h3', {'class': ['wsj-headline dj-sg wsj-card-feature heading-1',
                                                             'wsj-headline dj-sg wsj-card-feature heading-2',
                                                             'wsj-headline dj-sg wsj-card-feature heading-3',
                                                             'wsj-headline dj-sg wsj-card-feature heading-6']})
        for xx in headlines[:-1]:
            sublink = xx.find('a')['href']
            title = xx.find('a').text
            links.append(sublink)
            titles.append(title)

            print(sublink)
            print(title + "\n")

    return links, titles
