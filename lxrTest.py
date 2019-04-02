import lexy
import bs4 as bs
from urllib.request import Request, urlopen
import urllib.error
import re
import lxml
import nltk
import time
import rake

nltk.data.path.append('./nltk_data')


def parseText(link):
    article_content = ''
    title = ''
    lang = 'en'
    paragraphs = ''
    keywords = []
    status = -1

    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(link, headers=hdr)
        scraped_data = urlopen(req)  # Try grabbing the source code of the page
        status = 0
    except ValueError:  # Invalid link
        status = -69
        return status, lang, title, paragraphs
    except urllib.error.URLError:  # Unable to open link (Internet down?)
        status = -404
        return status, lang, title, paragraphs

    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')

    paragraphs = parsed_article.find_all('p')

    try:
        # Right now, only supports English and Vietnamese
        lang = parsed_article.find('html')['lang']  # Get language of article. If unable, default to english
        if 'en' in lang:
            lang = 'en'

    except KeyError:
        lang = 'en'
    except TypeError:
        lang = 'en'

    try:
        title = parsed_article.find('head').find('title')
    except AttributeError:
        status = -69
        return status, lang, title, paragraphs

    # Find all sections within the html that contains the main article body
    if 'nytimes.com' in link:
        article_content = parsed_article.find('section', {'name': "articleBody"})
        paragraphs = article_content.find_all('p', {'class': ["css-1ygdjhk evys1bk0", "css-1e7dx92 evys1bk0"]})
        title = parsed_article.find('head').find('title', {'data-rh': "true"})

    if 'bbc.com' in link:
        try:
            article_content = parsed_article.find('div', {'class': ['story-body__inner', 'story-body', 'body-content',
                                                                    'vxp-media__summary', 'LongArticle-bodyItem',
                                                                    '   story-body sp-story-body gel-body-copy',
                                                                    'gallery-list-wrapper']})
        except AttributeError:
            print('error')

        try:
            paragraphs = article_content.find_all('p')
            # print(type(paragraphs))
        except AttributeError:
            status = -69
            print('error')

    if 'washingtonpost.com' in link:
        article_content = parsed_article.find('article', {'itemprop': 'articleBody'})
        paragraphs = article_content.find_all('p', {'class': False})
        title = parsed_article.find('title')

    if 'time.com' in link:
        article_content = parsed_article.find('div', {'id': 'article-body'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'theguardian.com' in link:
        article_content = parsed_article.find('div', {'class': 'content__article-body from-content-api js-article__body'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'wsj.com' in link:
        article_content = parsed_article.find('div', {'class': 'article-content'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'huffpost.com' in link:
        paragraphs = parsed_article.find_all('div', {'class': 'content-list-component yr-content-list-text text'})
        # print(paragraphs)

    if 'arstechnica' in link:
        article_content = parsed_article.find('section', {'class': 'article-guts'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'reuters.com' in link:
        article_content = parsed_article.find('div', {'class': 'StandardArticleBody_body'})
        try:
            paragraphs = article_content.find_all('p', {'class': False})
        except AttributeError:
            status = -69
            print('error')

    if 'politico' in link:
        article_content = parsed_article.find('div', {'class': 'content-group story-core'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'vnexpress.net' in link:
        paragraphs = parsed_article.find_all('p', {'class': 'Normal'})
        title = parsed_article.find('head').find('title')

    if 'tuoitre.com' in link:
        article_content = parsed_article.find('div', {'id': 'main-detail-body'})
        paragraphs = article_content.find_all('p', {'class': ""})
        title = parsed_article.find('head').find('title')

    if 'latimes' in link:
        paragraphs = parsed_article.find_all('div', {'class': "card collection-item", 'data-type': 'text'})
        title = parsed_article.find('head').find('title')

    return status, lang, title, paragraphs


def generateKeywords(link):
    print('[INFO] Currently Generating Keywords For ' + link)
    sentences = ""
    status, lang_name, ttl, paragraphs = parseText(link)

    if status == 0:
        # Append the text into one string, for NTLK sentence tokenizing
        for p in paragraphs:
            # Ignore if paragraph is too short
            if len(p.text) < 10:
                continue
            # Ignore if paragraph is of the form [....xyzabc...]
            if p.text[0] == '[' and p.text[-1] == ']':
                continue

            # Remove the whitespace at the end of sentence
            if p.text[-1] == ' ':
                sentences += p.text[:-1]
            else:
                sentences += p.text

            # <NNN> indicates the end of a paragraph. This is very important as we want to preserve paragraph boundaries
            if p.text[-1] in ['.', '!', '?']:
                sentences += " "
        # Scrub sentences of fluff (Mostly Refenrences in Square Brackets)

        sentences = re.sub(r'\[[0-9]*\]', ' ', sentences)
        sentences = re.sub(r'\s+', ' ', sentences)
        # sentences = re.sub(r'\.([A-Z0-9])', r'. \1', sentences)
        sentences = re.sub(r'\."([A-Z0-9])', r'". \1', sentences)
        sentences = re.sub(r'(Mr\.|Ms\.|Dr\.|Mrs\.|[A-Z]\.) ', r'\1', sentences)
        sentences = re.sub(r'([0-9])\.([0-9])', r'\1\2', sentences)
        # formatted_article_text = re.sub('[^a-zA-Z]', ' ', sentences)
        # print(sentences)
        keywords = rake.generate_from_article(sentences, 999)
        # print(keywords)
        return keywords
    else:
        print('OUT!')
        return []


def generateSummary(link, typ):
    print(link)
    prev = time.time()
    sentences = ""
    status, lang_name, ttl, paragraphs = parseText(link)

    if status == 0:
        # Append the text into one string, for NTLK sentence tokenizing
        for p in paragraphs:
            # Ignore if paragraph is too short
            if len(p.text) < 10:
                continue
            # Ignore if paragraph is of the form [....xyzabc...]
            if p.text[0] == '[' and p.text[-1] == ']':
                continue

            # Remove the whitespace at the end of sentence
            if p.text[-1] == ' ':
                sentences += p.text[:-1]
            else:
                sentences += p.text

            # <NNN> indicates the end of a paragraph. This is very important as we want to preserve paragraph boundaries
            sentences += '<NNN>. '
            if p.text[-1] in ['.', '!', '?']:
                sentences += " "
        if not isinstance(ttl, str):
            title = ttl.text
        else:
            title = ttl
        # Scrub sentences of fluff (Mostly Refenrences in Square Brackets)

        sentences = re.sub(r'\[[0-9]*\]', ' ', sentences)
        sentences = re.sub(r'\s+', ' ', sentences)
        # sentences = re.sub(r'\.([A-Z0-9])', r'. \1', sentences)
        sentences = re.sub(r'\."([A-Z0-9])', r'". \1', sentences)
        sentences = re.sub(r'(Mr\.|Ms\.|Dr\.|Mrs\.|[A-Z]\.) ', r'\1', sentences)
        sentences = re.sub(r'([0-9])\.([0-9])', r'\1\2', sentences)
        # formatted_article_text = re.sub('[^a-zA-Z]', ' ', sentences)
        print(sentences)
        keywords = rake.generate_from_article(sentences, 10)

        sentence_list = []
        vi_token = nltk.data.load('vi.pickle')

        if 'en' in lang_name:
            sentence_list = nltk.sent_tokenize(sentences)
        elif lang_name == 'vi':
            sentence_list = vi_token.tokenize(sentences)

        new_sent_list = []
        paragraph_bound = [-1]
        # Some sentences might end with a quote, which NLTK does not detect. Added a proper period after quotes for NLTK
        for sents in sentence_list:
            temp = []
            if '<NNN>' not in sents:
                sents = re.sub(r'([!?.][\"\”])', r'\1. ', sents)
            if lang_name == 'en':
                temp = nltk.sent_tokenize(sents)
            elif lang_name == 'vi':
                temp = vi_token.tokenize(sents)
            for new_sent in temp:
                if new_sent != '<NNN>.':
                    new_sent_list.append(new_sent)

        for val, sents in enumerate(new_sent_list):
            # print(sents)
            if '<NNN>' in sents:
                if sents == '<NNN>.':
                    paragraph_bound.append(val - 1)
                else:
                    paragraph_bound.append(val)
                sents = sents.replace('<NNN>.', '')
            new_sent_list[val] = sents

            if len(sents) > 3 and sents[-3:] in ['.\".', '?\".', '!\".']:
                new_sent_list[val] = sents[:-2]

        # print(time.time() - prev)
        # Generate the summary using LexRank, @summary_size = number of sentences
        # @threshold = only count connections above threshold

        if typ == 'default':
            summary = lexy.get_summary(sentence_list, lang_name, summary_size=10, threshold=0.1)
            rtn = ""
            for val, s in enumerate(summary):
                rtn += str(val + 1) + ".  " + s + "\n\n"
            print(time.time() - prev)
            return status, title, rtn

        elif typ == 'custom':
            summary = lexy.get_summary_with_user(new_sent_list, lang_name, threshold=0.1)
            # @status == (int), @title == (str), @new_sent_list == (list), @summary = np array, @ paragraph_bound = (list)
            return status, title, new_sent_list, summary, paragraph_bound, keywords
    else:
        if typ == 'default':
            return status, '', ''
        elif typ == 'custom':
            return status, '', [], [], [], []


# parseText('https://www.nytimes.com/2019/02/06/opinion/state-of-the-union-abortion-trump.html')
# output = generateSummary("https://nytimes.com/2019/03/06/opinion/jared-kushner-trump.html", 'default')
# for ss in output:
# print(ss)
