import math
from collections import Counter, defaultdict
import numpy as np
from nltk.corpus import stopwords
import os
import nltk
import string
import time
from underthesea import word_tokenize
import re

path_en = 'K:/bbc/combi'
path_vi = 'K:/vi_txt/Train_Full/Chinh tri Xa hoi'
documents = []


def get_summary(sentences, lang, summary_size, threshold):
    # prev = time.time()
    idf_score = calculate_idf(lang)
    # print(time.time() - prev)

    # prev = time.time()
    lex_scores = rank_sentences(idf_score, lang, sentences, threshold)  # Calculate LexRank
    # print(time.time() - prev)

    sorted_scores = np.argsort(lex_scores)[::-1]  # Sorting the score array in terms of index
    final_list = np.sort(sorted_scores[:summary_size])
    summary = [sentences[i] for i in final_list]  # Getting the summary based on summary length

    return summary


def get_summary_with_user(sentences, lang, threshold):
    # prev = time.time()
    idf_score = calculate_idf(lang)
    # print(time.time() - prev)

    # prev = time.time()
    lex_scores = rank_sentences(idf_score, lang, sentences, threshold)  # Calculate LexRank
    # print(time.time() - prev)

    sorted_scores = np.argsort(lex_scores)[::-1]  # Sorting the score array in terms of index
    return sorted_scores


def load_stop_vi(direc):
    ret = []
    ff = open(direc, 'r', encoding='utf-8')
    for stops in ff.readlines():
        ret.append(stops)
    return ret


def rank_sentences(idf_sc, lang, sentences, threshold=0.1):
    tf_scores = [Counter(tokenize_words(sentence, lang)) for sentence in sentences]
    sim_matrix = calculate_sim_matrix(idf_sc, tf_scores)
    markov_matrix = transform_markov_matdis(sim_matrix, threshold)
    scores = power_method(markov_matrix)
    return scores


#  Load all documents, turning them into an array (list of documents) of arrays (list of sentences)
# Used for calculating IDF Score
'''
def load_en(direc):
    listd = os.listdir(direc)
    docs = [['dummy']]
    for files in listd:
        text = ''
        file = open(direc+"/"+files, 'r', encoding='cp1252')
        for lines in file.readlines():
            text += lines.strip('\n')
        docs.append(nltk.sent_tokenize(text, 'english'))
    docs.pop(0)
    return docs


def load_vi(direc):
    print("I'm in!")
    ll = os.listdir(direc)
    docs = [['dummy']]
    nltk_token = nltk.data.load('vi.pickle')
    for val, files in enumerate(ll):
        text = ''
        ff = open(direc+"/"+files, 'r', encoding='utf_16_le')
        listsen = ff.readlines()
        for li in listsen:
            li = re.sub(r'([0-9])\.([0-9])', r'\1\2', li)
            li += " "
            if li[0] == ' ':
                li = li[1:]
            text += li.strip('\n').replace('\ufeff', '')
        out = nltk_token.tokenize(text)
        docs.append(out)
    docs.pop(0)
    return docs
'''


# Tokenize sentence into distinct words using the Punkt Sentence Tokenizer package in NLTK
def tokenize_words(sentence, lang):
    if lang == 'en':
        stop = stopwords.words('english') + list(string.punctuation)  # Common words that are not informative
        return [i for i in nltk.word_tokenize(sentence.lower(), 'english') if i not in stop and str.isalpha(i)]
    elif lang == 'vi':
        stop = load_stop_vi('stopwords_vi.txt') + list(string.punctuation)
        sent = word_tokenize(sentence.lower())
        return [i for i in sent if i not in stop and str.isalpha(i)]


'''
# Calculate the Inverse Document Frequency of all words in document, not needed if you have a dict file
def calculate_idf(docs, lang):
    bags_of_words = []
    for document in docs:
        b_words = set()
        for sentences in document:
            if len(sentences) < 10:
                continue
            # https://stackoverflow.com/questions/17390326/getting-rid-of-stop-words-and-document-tokenization-using-nltk
            sent_words = tokenize_words(sentences, lang)
            b_words.update(sent_words)
        if b_words:
            bags_of_words.append(b_words)

    doc_number_total = len(bags_of_words)
    default = math.log(doc_number_total+1)  # Default value for idf_score
    idf_score = defaultdict(lambda: default)

    # Combining all words in all sentences into a set (no repeats)
    for word in set.union(*bags_of_words):
        print(word)
        # If word is in a sentence(i.e bag-of-words containing that word), add 1 to @doc_word_amount
        doc_word_amount = sum(1 for bag in bags_of_words if word in bag)  # Number of instances of a word in corpus
        idf_score[word] = math.log(doc_number_total/doc_word_amount)  # https://www.quora.com/How-does-TF-IDF-work

    if lang == 'vi':
        idf_out = open('idf_vi.txt', 'w', encoding='utf_16_le')
    else:
        idf_out = open('idf_en.txt', 'w', encoding='utf_8')

    print(len(idf_score.keys()))
    for k in idf_score.keys():
        idf_out.write(str(k)+" !@# "+str(idf_score[k])+"\n")
    return idf_score
'''


# Calculate the IDF score using dictionary generated from a prepared corpus
def calculate_idf(lang):
    if lang == 'en':
        default = math.log(2226)  # Default value for idf_score
        file_en = open('idf_en.txt')
    else:
        default = math.log(5220)
        file_vi = open('idf_vi.txt', encoding='utf_16_le')

    idf_score = defaultdict(lambda: default)

    if lang == 'en':
        for words in file_en.readlines():
            sep = words.index(' !@# ')
            word = words[0:sep]
            score = float(words[sep + 5:])
            idf_score[word] = score

    elif lang == 'vi':
        for words in file_vi.readlines():
            sep = words.index(' !@# ')
            word = words[0:sep]
            score = float(words[sep + 5:])
            idf_score[word] = score
    return idf_score


# tfs is an array of two Counters, which is a dict of words and their occurrences in the sentences compared
def idf_modified_cosine(idf_sc, tfs, i, j):
    if i == j:
        return 1
    tf_i = tfs[i]  # TF score for the first sentence
    tf_j = tfs[j]

    words_i = set(tf_i.keys())
    words_j = set(tf_j.keys())

    if len(words_i) == 0 or len(words_j) == 0:
        return 0

    words = words_i.union(words_j)
    nominator = 0

    for word in words:
        nominator += tf_i[word]*tf_j[word]*(idf_sc[word]**2)

    if math.isclose(nominator, 0):
        return 0

    dem_x = 0
    for word in words_i:
        dem_x += (tf_i[word]*idf_sc[word])**2

    dem_y = 0
    for word in words_j:
        dem_y += (tf_j[word] * idf_sc[word]) ** 2

    cos_dis = nominator / math.sqrt(dem_x*dem_y)
    return cos_dis


'''
def sentence_similarity(idf_sc sent_1, sent_2):
    arr_1 = tokenize_words(sent_1)  # Tokenize sentences into words, also remove stopwords in process
    arr_2 = tokenize_words(sent_2)

    tf_1 = Counter(arr_1)
    tf_2 = Counter(arr_2)
    cos_simi = idf_modified_cosine(idf_sc, [tf_1, tf_2], 0, 1)
    return cos_simi
'''


def calculate_sim_matrix(idf_sc, tf_scores):
    length = len(tf_scores)
    # At location (i,j), store the cosine distance between sentence i and sentence j
    similarity_matrix = np.zeros([length] * 2, dtype=float)

    for i in range(length):
        for j in range(i, length):
            simi = idf_modified_cosine(idf_sc, tf_scores, i, j)
            if i == j:
                similarity_matrix[i, j] = 1
                similarity_matrix[j, i] = 1
                continue

            if simi:
                similarity_matrix[i, j] = simi
                similarity_matrix[j, i] = simi
    return similarity_matrix


# https://github.com/crabcamp/lexrank/blob/dev/lexrank/algorithms/summarizer.py#L125
def transform_markov_matdis(sim_matrix, threshold):
    np.set_printoptions(threshold=10000, linewidth=200)
    markov_matrix = np.zeros(sim_matrix.shape)  # Create probability matrix

    for i in range(len(sim_matrix)):
        add = 0
        columns = np.where(sim_matrix[i] > threshold)[0]
        markov_matrix[i, columns] = 1 / len(columns + add)  # LexRank paper, equation 4

    return markov_matrix


def power_method(mat):
    eigen = np.ones(len(mat))
    tranposed_mat = np.transpose(mat)
    while True:
        eigen_next = np.dot(tranposed_mat, eigen)
        if np.allclose(eigen, eigen_next):
            return eigen_next
        eigen = eigen_next











