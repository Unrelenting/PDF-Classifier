from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
import string
import os


stemmer = PorterStemmer()


def get_docs(filename):
    with open(filename, 'r') as f:
        text = f.read()
        lowers = text.lower()
        replace = lowers.replace('\n', ' ')
        replace = replace.replace('\t', ' ')
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


def train_data():
    # keys are the documents client_folder and values are the words
    idx = 0
    token_dict = OrderedDict()
    txtDir = "/Users/matthewwong/dsi-capstone/Text/"
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
    for key in token_dict.keys():
        cos_sum = 0
        avg_cos = 0
        num_docs = 0
        for doc_num in xrange(len(token_dict[key])):
            cos_sum += cos[total_num_docs]
            num_docs += 1
            total_num_docs += 1
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
            if category == folder.split('-')[2]:
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

    token_dict = train_data()
    raw_docs, doc_labels = get_raw_docs(token_dict)
    categories = categories(token_dict)

    tfidfed = tfidf.fit_transform(raw_docs)

    # Naive Bayes example
    # mnb = MultinomialNB()
    # mnb.fit(X_train, y_train)
    # print 'Accuracy:', mnb.score(X_test, y_test)
    # sklearn_predictions = mnb.predict(X_test)

    nb = MultinomialNB()

    # test = get_docs('/Users/matthewwong/dsi-capstone/Text/A1/Appraisal/Certificate.txt')
    # test1 = []
    # test2 = test1.append(test)
    #
    # tfidfed1 = tfidf.transform(test1)
    # cos = cosine_similarity(tfidfed, tfidfed1)
    #
    # client_folder = summarize(token_dict, cos)
    # result = categorize(token_dict, client_folder, categories)
