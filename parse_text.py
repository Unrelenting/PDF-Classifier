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


# txtDir = '/Users/matthewwong/dsi-capstone/Text/'
def strip_blank(txtDir):
    # list of documents that pdfminer could not convert to text
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
                        if os.stat(textfilepath).st_size < 25:
                            blank_docs.append(textfilepath)
                            os.remove(textfilepath)
    for filename in blank_docs:
        # [5:] should refer to the index starting with the client folder (ex: A1)
        list_to_OCR.append('/'.join(filename.split('/')[5:]))
    return list_to_OCR


def fill_blank(list_to_OCR):
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


# txtDir = '/Users/matthewwong/dsi-capstone/Text/'
def train_data(txtDir):
    # keys are the documents client_folder and values are the words
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


def get_raw_docs(token_dict):
    raw_docs = []
    doc_labels = []
    for key in token_dict.keys():
        for doc in token_dict[key]:
            raw_docs.append(doc)
            doc_labels.append(key.split('-')[2])
    return raw_docs, doc_labels


def categories(token_dict):
    # returns all the unique categories of folders
    categories = []
    for key in token_dict.keys():
        categories.append(key.split('-')[2])
    return set(categories)


# not used
def category_dicts(token_dict, categories):
    # returns a list where each element are dictionaries that are of the same category
    sep_dicts = []
    for category in categories:
        category_dict = dict((k, v) for k, v in token_dict.iteritems() if k.split('-')[1] == category)
        sep_dicts.append(category_dict)
    return sep_dicts


# gets the average of the sums of the cosine similarities for client_folders
def summarize(token_dict, cos):
    client_folder = OrderedDict()
    num_client_folder = 0
    total_num_docs = 0
    # goes through all the client_folders and counts the subfolders
    for key in token_dict.keys():
        cos_sum = 0
        avg_cos = 0
        num_docs = 0
        # goes through all the documents in each subfolder
        # only increments if subfolders are not empty
        for doc_num in xrange(len(token_dict[key])):
            cos_sum += cos[total_num_docs]
            num_docs += 1
            total_num_docs += 1
        # avg_cos would be 0 for subfolders that are empty
        if num_docs > 0:
            avg_cos = cos_sum / num_docs
        client_folder[num_client_folder] = avg_cos
        num_client_folder += 1
    return client_folder


# gets the average cosine similarity for each category
def categorize(token_dict, client_folder, categories):
    result = {}
    for category in categories:
        category_avg = 0
        num_folders = 0
        for folder in token_dict.keys():
            # finds every subfolder in that category and sums their cos_similarity
            if category == folder.split('-')[2]:
                if type(client_folder[int(folder.split('-')[0])]) != int:
                    category_avg += client_folder[int(folder.split('-')[0])][0]
                    num_folders += 1
        category_avg = category_avg / num_folders
        result[category] = category_avg
    return result


def predict(result):
    prediction = ''
    similarity = 0
    for key, value in result.iteritems():
        if value > similarity:
            similarity = value
            prediction = key
    return prediction


def cosine_similarity(doc1, doc2):
    cosine_similarities = linear_kernel(doc1, doc2)
    return cosine_similarities


if __name__ == '__main__':
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    nb = MultinomialNB()

    # list_to_OCR = strip_blank('/Users/matthewwong/dsi-capstone/Text/')
    # fill_blank(list_to_OCR)
    # token_dict = train_data('/Users/matthewwong/dsi-capstone/Text/')
    # raw_docs, doc_labels = get_raw_docs(token_dict)
    # categories = categories(token_dict)
    #
    # tfidfed = tfidf.fit_transform(raw_docs)
