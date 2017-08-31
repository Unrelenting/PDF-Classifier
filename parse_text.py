from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
import string
import os
import re
import unicodedata
from OCR import *


stemmer = PorterStemmer()


def get_docs(filename):
    ''' Returns a cleaned text document. '''
    with open(filename, 'r') as f:
        text = f.read()
        lowers = text.lower()
        replace = lowers.replace('\n', ' ')
        replace = replace.replace('\t', ' ')
        replace = re.sub('[^A-Za-z0-9]+', ' ', replace)
        no_punctuation = replace.translate(None, string.punctuation)
        return no_punctuation


def remove_stopwords(tokens):
    stop = set(stopwords.words('english'))
    filtered = [word for word in tokens if word not in stop]
    return filtered


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def strip_blank(txtDir):
    '''
    Deletes any blank text documents created when pdfminer could not pull the text.
    ex: list_to_OCR = strip_blank('/Users/matthewwong/dsi-capstone/Text/')
    Returns a list of the blank documents that were deleted and need be pulled with
    OCR.
    '''
    blank_docs = []
    list_to_OCR = []
    # gets clients
    for client in os.listdir(txtDir):
        if not client.startswith('.'):
            # gets folders
            for folder in os.listdir(txtDir + client):
                if not folder.startswith('.'):
                    # gets textfiles
                    docs_list = []
                    for textfile in os.listdir(txtDir + client + '/' + folder):
                        textfilepath = txtDir + client + '/' + folder + '/' + textfile
                        # refers to any document smaller than size 25 as blank
                        if os.stat(textfilepath).st_size < 25:
                            blank_docs.append(textfilepath)
                            os.remove(textfilepath)
    for filename in blank_docs:
        # [5:] refers to the index starting with the client folder (ex: A1)
        list_to_OCR.append('/'.join(filename.split('/')[5:]))
    return list_to_OCR


def fill_one(filename):
    '''
    Use to replace a text document that pdfminer could not pull the text from.
    ex: fill_one('V1/Insurance/Villarin - Insurance - Current HO6 - Allstate - \
        EXP 2018-04-17 - 562.00.pdf')
    '''
    pdfDir = '/Users/matthewwong/dsi-capstone/PDFs/decrypted/'
    txtDir = '/Users/matthewwong/dsi-capstone/Text/'
    final_text = get_text(pdfDir + filename)
    text_file = open(txtDir + filename, 'w')
    for page in final_text:
        text_file.write(page.encode('ascii','ignore'))
    text_file.close()


def fill_blanks(list_to_OCR):
    '''
    Use to replace text documents that pdfminer could not pull any text from.
    ex: fill_blanks(list_to_OCR)
    '''
    pdfDir = '/Users/matthewwong/dsi-capstone/PDFs/decrypted/'
    txtDir = '/Users/matthewwong/dsi-capstone/Text/'
    for filename in list_to_OCR:
        print 'Converting file: {}'.format(filename)
        new_filename = string.replace(filename, '.txt', '.pdf')
        final_text = get_text(pdfDir + new_filename)
        text_file = open(txtDir + filename, 'w')
        for page in final_text:
            text_file.write(page.encode('ascii','ignore'))
        text_file.close()


def get_dict(txtDir):
    '''
    Returns a dictionary where the keys are in the form index-client-folder, and
    the value are all the cleaned documents in those folders.
    ex: get_dict('/Users/matthewwong/dsi-capstone/Text/')
    ex key: '0-A1-Appraisal'
    ex value: [doc1, doc2, doc3, doc4, doc5]
    '''
    idx = 0
    token_dict = OrderedDict()
    # gets clients
    for client in os.listdir(txtDir):
        if not client.startswith('.'):
            # gets folders
            for folder in os.listdir(txtDir + client):
                if not folder.startswith('.'):
                    # gets textfiles
                    docs_list = []
                    for textfile in os.listdir(txtDir + client + '/' + folder):
                        textfilepath = txtDir + client + '/' + folder + '/' + textfile
                        doc = get_docs(textfilepath)
                        docs_list.append(doc)
                    token_dict[str(idx) + '-' + client + '-' + folder] = docs_list
                    idx += 1
    return token_dict


def seperate(token_dict):
    ''' Seperates the data into raw_docs and doc_labels. '''
    raw_docs = []
    doc_labels = []
    for key in token_dict.keys():
        for doc in token_dict[key]:
            raw_docs.append(doc)
            doc_labels.append(key.split('-')[2])
    return raw_docs, doc_labels


def categories(token_dict):
    ''' Gets all the unique categories of documents. '''
    categories = []
    for key in token_dict.keys():
        categories.append(key.split('-')[2])
    return set(categories)


def category_dicts(token_dict, categories):
    '''
    Returns a list of dictionaries where the keys are each unique category
    and the values are documents in that category.
    '''
    sep_dicts = []
    for category in categories:
        category_dict = dict((k, v) for k, v in token_dict.iteritems() if \
                        k.split('-')[1] == category)
        sep_dicts.append(category_dict)
    return sep_dicts


def cosine_similarity(doc1, doc2):
    '''
    Compares the cosine similarity between two documents.
    tfidfed = tfidf.fit_transform(training_docs)
    tfidfed1 = tfidf.transform(test_docs)
    ex: cos = cosine_similarity(tfidfed1, tfidfed)
    cos is a numpy.ndarray where each element is another numpy.ndarray with the
    corresponding cosine similarity to each document in the training set
    '''
    cosine_similarities = linear_kernel(doc1, doc2)
    return cosine_similarities
