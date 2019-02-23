import lexy
import bs4 as bs
import urllib.request
import re
import lxml
import nltk
import time


def parseText(link):
    scraped_data = urllib.request.urlopen(link)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')

    article_content = ''
    title = ''
    paragraphs = parsed_article.find_all('p')
    lang = parsed_article.find('html')['lang']

    if 'nytimes.com' in link:
        article_content = parsed_article.find('section', {'name': "articleBody"})
        paragraphs = article_content.find_all('p', {'class': "css-1ygdjhk evys1bk0"})
        title = parsed_article.find('head').find('title', {'data-rh': "true"})

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

    if 'huffingtonpost.com' in link:
        paragraphs = parsed_article.find_all('div', {'class': 'content-list-component yr-content-list-text text'})

    if 'arstechnica' in link:
        article_content = parsed_article.find('section', {'class': 'article-guts'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'reuters.com' in link:
        article_content = parsed_article.find('div', {'class': 'StandardArticleBody_body'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'politico' in link:
        article_content = parsed_article.find('div', {'class': 'content-group story-core'})
        paragraphs = article_content.find_all('p', {'class': False})

    if 'vnexpress.net' in link:
        paragraphs = parsed_article.find_all('p', {'class': 'Normal'})
        title = parsed_article.find('head').find('title')

    if 'tuoitre' in link:
        article_content = parsed_article.find('div', {'id': 'main-detail-body'})
        paragraphs = article_content.find_all('p', {'class': ""})
        title = parsed_article.find('head').find('title')
    return lang, title, paragraphs


def generateSummary(link, typ):
    prev = time.time()
    sentences = ""
    lang_name, ttl, paragraphs = parseText(link)
    # Append the text into one string, for NTLK sentence tokenizing
    for p in paragraphs:
        if p.text[0] == '[' and p.text[-1] == ']':
            continue
        sentences += p.text
        sentences += '<EOP>. '
        if p.text[-1] in ['.', '!', '?']:
            sentences += " "
    title = ttl.text
    # Scrub sentences of fluff (Mostly Refenrences in Square Brackets)

    sentences = re.sub(r'\[[0-9]*\]', ' ', sentences)
    sentences = re.sub(r'\s+', ' ', sentences)
    # sentences = re.sub(r'\.([A-Z0-9])', r'. \1', sentences)
    sentences = re.sub(r'\."([A-Z0-9])', r'". \1', sentences)
    sentences = re.sub(r'(Mr\.|Ms\.|Dr\.|Mrs\.|[A-Z]\.) ', r'\1', sentences)
    sentences = re.sub(r'([0-9])\.([0-9])', r'\1\2', sentences)

    # formatted_article_text = re.sub('[^a-zA-Z]', ' ', sentences)

    sentence_list = []
    vi_token = nltk.data.load('vi.pickle')

    if lang_name == 'en':
        sentence_list = nltk.sent_tokenize(sentences)
    elif lang_name == 'vi':
        sentence_list = vi_token.tokenize(sentences)

    new_sent_list = []
    paragraph_bound = [-1]
    # Some sentences might end with a quote, which NLTK does not detect. Added a proper period after quotes for NLTK
    for sents in sentence_list:
        temp = []
        if '<EOP>' not in sents:
            sents = re.sub(r'([!?.][\"\”])', r'\1. ', sents)
        if lang_name == 'en':
            temp = nltk.sent_tokenize(sents)
        elif lang_name == 'vi':
            temp = vi_token.tokenize(sents)
        new_sent_list.extend(temp)

    for val, sents in enumerate(new_sent_list):
        # print(sents)
        if '<EOP>' in sents:
            paragraph_bound.append(val)
            sents = sents.replace('<EOP>.', '')
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
        return title, rtn
    elif typ == 'custom':
        summary = lexy.get_summary_with_user(new_sent_list, lang_name, threshold=0.1)
        return title, new_sent_list, summary, paragraph_bound


# parseText('https://www.nytimes.com/2019/02/06/opinion/state-of-the-union-abortion-trump.html')
# output = generateSummary("https://vnexpress.net/bong-da/messi-ghi-it-nhat-30-ban-trong-11-mua-lien-tiep-3882158.html")
# for ss in output:
# print(ss)
