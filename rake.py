import re
import inflect
import numpy as np
import time
import nltk


# https://github.com/aneesha/RAKE/blob/master/rake.py
# Split text into separate lexical clauses (so not just sentences but also sub-clauses within a sentence)
# Takes in the original text of the article, and return the list of lexical clauses
def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences_list = sentence_delimiters.split(text)
    return sentences_list


def split_words(sentences):
    pp = inflect.engine()
    stoplist = open('stopwords_en.txt', 'r', encoding='utf-8')
    stops = []
    for words in stoplist.readlines():
        stops.append(words.strip('\n'))

    bag_words = []
    word_dict = dict()
    inverse_word_dict = dict()
    val = 0

    curr_key = ''
    for sentence in sentences:
        default = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(default)
        # print(tagged)

        val_temp = 0

        for elements in tagged:
            if 'NN' not in elements[1]:
                default.pop(val_temp)
                val_temp = val_temp - 1
            val_temp = val_temp + 1

        # print(default)

        temp = []

        if curr_key != '':
            temp.append(curr_key[1:])
        curr_key = ''

        for words in default:
            if not any([stop == words.lower() for stop in stops]) and len(words) > 4:
                low = words.lower()
                # out = pp.singular_noun(low)

                curr_key += ' ' + low
                if low not in word_dict.keys():
                    word_dict[low] = val
                    inverse_word_dict[val] = low
                    val = val + 1

            else:
                if curr_key != '':
                    temp.append(curr_key[1:])
                curr_key = ''

        if len(temp) > 0:
            bag_words.append(temp)
    return bag_words, word_dict, inverse_word_dict


def calc_score(bag_words, word_dict, inverse_word_dict):
    lll = len(word_dict.keys())
    coor_mat = np.zeros((lll, lll))
    keywords = set()
    for bag in bag_words:
        # print(bag)
        for phrases in bag:
            keywords.add(phrases)
            curr_list = phrases.split(' ')
            for word_src in curr_list:
                for word_tgt in curr_list:
                    ind_src = word_dict[word_src]
                    ind_tgt = word_dict[word_tgt]
                    coor_mat[ind_src, ind_tgt] += 1

    # print(keywords)

    score_list = []
    for i in range(lll):
        # print(inverse_word_dict[i])
        deg = np.sum(coor_mat[i])
        freq = coor_mat[i, i]
        # print(deg)
        # print(freq)
        score_list.append(deg)

    keyword_score = dict()
    for keyword in keywords:
        currScore = 0
        for word in keyword.split(' '):
            currScore += score_list[word_dict[word]]
        keyword_score[keyword] = currScore

    return keyword_score


def getHighestKeywords(keyword_score, num_keys):
    sred = sorted(keyword_score.items(), key=lambda value: value[1] / (len(value[0].split(' ')) ** 1), reverse=True)
    # print(sred)
    keys_out = 0
    taken_keys = []
    key_array = []
    long_lim = 5
    curr_lim = 2

    for keys in sred:
        splitted = keys[0].split()
        if len(keys[0]) < 5:
            continue

        if len(keys[0].split()) <= curr_lim:
            status = True
            check_dup = set()
            for token in splitted:
                if any([token == key.lower() for key in taken_keys]):
                    status = False
                    break
                check_dup.add(token)
            if status:
                key_array.append(' '.join(check_dup))
                if len(splitted) >= 2:
                    long_lim = long_lim - 1
                if long_lim == 0:
                    curr_lim = 1

                taken_keys.extend(splitted)
                keys_out = keys_out + 1
        if keys_out == num_keys:
            return key_array
        # print(keys)


def open_file(direc):
    raw = open(direc, 'r', encoding='utf-8')
    inp = ''
    for lines in raw.readlines():
        inp += lines.replace('\n', ' ')
    generate_from_article(inp)


def generate_from_article(text):
    bag_words, word_dict, inverse_word_dict = split_words(split_sentences(text))
    return getHighestKeywords(calc_score(bag_words, word_dict, inverse_word_dict), 10)
