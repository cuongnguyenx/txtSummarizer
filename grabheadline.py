import bs4 as bs
from urllib.request import Request, urlopen
import urllib3
import urllib.error
import re
import lxml
import nltk


def grabfront(link):
    try:
        # https://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden
        hdr = {'User-Agent': 'Mozilla/5.0'}
        if 'npr.org' in link:
            hdr['Cookies'] = "choiceVersion=1, trackingChoice=true"
        req = Request(link, headers=hdr)
        scraped_data = urlopen(req)  # Try grabbing the source code of the page
    except urllib.error.URLError:  # In the case there's no Internet, or the link is invalid
        print('invalid')
        return [], [], []

    # Parse the HTML to be analyzable
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    # print(parsed_article)

    # Ignore link with any of these following words
    verboten = ['crossword', 'podcast', 'graphics', 'photography', 'interactive', 'av', 'food', 'newsletter', 'live',
                'videos', 'programmes', 'bbcthree', 'britbox', 'topgear', 'slideshow', 'tips', 'video']
    links = []  # Contains the links to pages on the FrontPageList, to be used for urllib
    titles = []  # Contains the titles to the corresponding links
    categories = []

    # A lot of the following are custom rules discovered by me, and they work as is currently
    if 'nytimes.com' in link:
        # print(parsed_article)
        headlines = parsed_article.find_all('article', {'class': ['css-8atqhb']})
        for xx in headlines[:-1]:
            try:
                sublink = xx.find('a')['href']
            except AttributeError:
                print('ERROR LINK')
                continue

            try:
                title_tag = xx.find('h2')  # Title of article
            except AttributeError:
                print('ERROR TITLE')
                continue

            try:
                if title_tag.find('span'):
                    title = title_tag.find('span').text
                else:
                    title = title_tag.text
            except AttributeError:
                print('ERROR TEXT')
                continue

            if not any([x in sublink for x in verboten]):
                if 'http' not in sublink:
                    finall = link + sublink
                else:
                    finall = sublink

                links.append(finall)  # Link of article

                link_toks = finall.split('/')
                temp = []
                for toks in link_toks[-2::-1]:
                    if str.isnumeric(toks):
                        break
                    temp.append(toks.title())
                categories.append('/'.join(reversed(temp)))  # Section of article

                titles.append(title)
                # print(link + sublink)
                # print(title)
                # print('/'.join(reversed(temp)))

            else:
                continue

            # print('\n')

    if 'washingtonpost.com' in link:
        headlines = parsed_article.find_all('div', {'class': ["headline x-small normal-style text-align-inherit ",
                                                              "headline xx-small normal-style text-align-inherit ",
                                                              "headline small normal-style text-align-inherit ",
                                                              "headline x-small normal-style text-align-inherit",
                                                              "headline xx-small normal-style text-align-inherit",
                                                              "headline small normal-style text-align-inherit"]})

        # print(headlines)
        for xx in headlines[:-1]:
            sublink = xx.find('a')['href']
            if 'gallery' in sublink:
                continue
            title = xx.text

            if not any([x in sublink for x in verboten]):
                links.append(sublink)
                titles.append(title)
                link_toks = sublink.split('/')
                temp = []
                for toks in link_toks[3:]:
                    if str.isnumeric(toks) or len(toks) > 30:
                        break
                    temp.append(toks.title())
                categories.append('/'.join(temp))  # Section of article
            else:
                continue
            # print(sublink)
            # print(title)
            # print('/'.join(temp))
            # print('\n')

    if 'reuters.com' in link:
        headlines_1 = parsed_article.find_all('div', {'class': ['story-content', 'feature']})
        for xx in headlines_1[:-1]:
            if xx.find('a'):
                atag = xx.find('a')
                sublink = atag['href']
                # Not Text Article
                if 'tv' in sublink:
                    continue

                if 'reuters' not in sublink:
                    sublink = link + sublink
                elif 'https:' not in sublink:
                    sublink = 'https:' + sublink

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
            title = re.sub(r'[\t\n]+', r"", title)
            links.append(sublink)
            titles.append(title)

    if 'bbc.com' in link:
        headlines_1 = parsed_article.find_all('div',
                                              {'class': ['media__content', 'story-body sp-story-body gel-body-copy']})
        for xx in headlines_1[:-1]:
            sublink = ''
            '''
            if not xx.find('p'):
                continue
            '''

            if xx.find('a'):
                atag = xx.find('a', {'class': 'media__link'})

                if 'video' in atag['rev'][0] or 'pictures' in atag['rev'][0]:
                    continue

                if not any([x in atag['href'] for x in verboten]):
                    if 'bbc' not in atag['href']:
                        sublink = link + atag['href']
                    else:
                        sublink = atag['href']
                    title = re.sub(r'[\s]+', r" ", atag.text)
                    links.append(sublink)

                    link_toks = sublink.split('/')
                    temp = []
                    for toks in link_toks[3:]:
                        if toks == link_toks[-1]:
                            tt = toks.split('-')
                            if str.isnumeric(tt[0]):
                                continue
                            else:
                                for subtok in tt[:-1]:
                                    temp.append(subtok.title())

                        elif toks != 'news' and toks != 'story':
                            temp.append(toks.title())
                        else:
                            continue
                    categories.append(' '.join(reversed(temp)))  # Section of article

                    titles.append(title)

                    # print(sublink)
                    # print(title)
                    # print('/'.join(temp))
                    # print('\n')
                else:
                    continue
            else:
                continue

            # print(sublink)
            # print(re.sub(r'[\s]+', r" ", title) + "\n")

    if 'theguardian.com' in link:
        sections = parsed_article.find_all('section', {'id': ['headlines', 'opinion', 'spotlight']})
        for section in sections:
            headlines = section.find_all('h3', {'class': 'fc-item__title'})
            for xx in headlines[:-1]:
                sublink = xx.find('a')['href']
                if any([x in sublink for x in verboten]):
                    continue
                title = xx.find('span', {'class': 'js-headline-text'}).text
                if 'video' in sublink:
                    continue

                links.append(sublink)
                categories.append(sublink.split('/')[3].replace('-', ' ').title())
                titles.append(title)

                # print(sublink)
                # print(title)
                # print(sublink.split('/')[3].replace('-', ' ').title()+"\n")

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

            # print(sublink)
            # print(title + "\n")

    if 'apnews.com' in link:
        # print(parsed_article)
        headlines = parsed_article.find_all('div', {'class': re.compile(r'CardHeadline.*')})
        for xx in headlines[:-1]:
            print(xx)
            atag = xx.find('a', {'class': ['headline']})
            try:
                sublink = link + atag['href']
            except TypeError:
                continue
            title = atag.find('h1').text

            if sublink not in links:
                links.append(sublink)
            else:
                continue
            titles.append(title)

        # print(sublink)
        # print(title + "\n")

    if 'latimes.com' in link:
        headlines = parsed_article.find_all('a', {'data-pb-field': "headlines.basic"})
        for xx in headlines[:-1]:
            if 'http' not in xx['href']:
                sublink = link + xx['href']
            else:
                sublink = xx['href']

            title = xx.text
            category = []
            for toks in xx['href'].split('/')[0:-1]:
                category.append(toks.title())

            links.append(sublink)
            titles.append(title)
            if len(category) > 1:
                categories.append('/'.join(category)[1:])
            else:
                categories.append('Others')

    if 'npr.org' in link:
        headlines = parsed_article.find_all('div', {'class': "story-text"})
        for xx in headlines[:-1]:
            category = xx.find('a', {'data-metrics': '{"action":"Click Slug"}'})
            if category is None:
                cate_text = "Others"
            else:
                cate_text = re.sub(r'[\s]+', r" ", category.text)
            # print(cate_text)

            if xx.find('a', {'data-metrics': True}) is not None:
                sublink = xx.find('h3', {'class': 'title'}).parent['href']
                title = xx.find('h3', {'class': 'title'}).text
            else:
                continue

            links.append(sublink)
            titles.append(title)
            categories.append(cate_text)

    if 'huffpost' in link:
        headlines = parsed_article.find_all('a', {'class': 'card__link yr-card-headline'})
        for xx in headlines[:-1]:
            sublink = xx['href']
            if any([x in sublink for x in verboten]):
                continue
            title = xx.find('div').text
            if str.isupper(title):
                continue

            links.append(sublink)
            titles.append(title)

    if 'newsweek' in link:
        pattern = re.compile(r'Opinion')
        headlines_1 = parsed_article.find_all('article', {'class': [False, 'col-sm-6 col-md-3']})
        headlines_2 = parsed_article.find('div', {'class': 'feature2 subfeature2'}).find_all('li', {'class': 'flex-xs'})
        headlines_3 = parsed_article.find_all('article', {'class': 'clearfix'})

        for sections in headlines_1[:-1]:
            category = sections.find('div', {'class': 'category'}).text
            h3_tag = sections.find('h3')
            sublink = h3_tag.find('a')['href']
            title = h3_tag.find('a').text

            links.append(link + sublink)
            titles.append(title)
            categories.append(category)

        for sections in headlines_2[:-1]:
            div_tag = sections.find('div', {'class': 'info'})
            sublink = div_tag.find('a')['href']
            title = div_tag.find('a').text

            links.append(link + sublink)
            titles.append(title)
            categories.append('Opinion')

        for sections in headlines_3[:-1]:
            h4_tag = sections.find('h4')
            sublink = h4_tag.find('a')['href']
            title = h4_tag.find('a').text

            links.append(link + sublink)
            titles.append(title)
            categories.append('More Stories')

    if 'politico' in link:
        headlines = parsed_article.find_all('h1', {'class': 'headline '})
        for xx in headlines[:-1]:
            sublink = xx.find('a')['href']
            if any([x in sublink for x in verboten]):
                continue
            title = xx.find('a').text

            links.append(sublink)
            titles.append(title)

    if 'bloomberg' in link:
        headlines_1 = parsed_article.find('section', {'class': 'single-story-module__info'})
        print(headlines_1)
        category_1 = headlines_1.find('a', {'class': 'single-story-module__eyebrow-link'})

        headlines_2 = parsed_article.find_all('article', {'class': "story-package-module__story"})

        for xx in headlines_1.find_all('a', {
            'class': ['single-story-module__headline-link', 'single-story-module__related-story-link']})[:-1]:
            sublink = xx['href']
            title = xx.text

            links.append(link + sublink)
            titles.append(title)
            categories.append(category_1)

        for xx in headlines_2[:-1]:
            if xx.find('section', {'class': 'story-package-module__story__eyebrow'}):
                category_2 = xx.find('section', {'class': 'story-package-module__story__eyebrow'}).text
            else:
                category_2 = 'Opinion'

            if xx.find('a', {'class': 'story-package-module__story__headline-link'}):
                atag = xx.find('a', {'class': 'story-package-module__story__headline-link'})
                sublink = atag['href']
                title = atag.text

                links.append(link + sublink)
                titles.append(title)
                categories.append(category_2)
            else:
                continue
    if 'verge' in link:
        headlines = parsed_article.find_all('h2', {'class': 'c-entry-box--compact__title'})
        for xx in headlines[:-1]:
            atag = xx.find('a')
            if atag['data-analytics-link'] != 'article':
                continue
            sublink = atag['href']
            if any([x in sublink for x in verboten]):
                continue
            title = atag.text

            links.append(sublink)
            titles.append(title)


    return links, titles, categories
