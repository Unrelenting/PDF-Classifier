from __future__ import division
from parse_text import *
import parse_text
import os
import numpy as np


# TestDir = '/Users/matthewwong/dsi-capstone/Test'


def classify_cos(TestDir):
    predictions = []
    labels = []
    for client in os.listdir(TestDir):
        if not client.startswith('.'):
            category_path = TestDir + '/' + client
            for category in os.listdir(category_path):
                if not category.startswith('.'):
                    pdf_path = TestDir + '/' + client + '/' + category
                    for pdf in os.listdir(pdf_path):
                        lst = []
                        # labels for the test documents
                        labels.append(category)
                        # cleans the test document
                        new_pdf = get_docs(pdf_path + '/' + pdf)
                        # takes new pdf in a list so it is able to be transformed
                        lst.append(new_pdf)
                        # returns term-document matrix
                        tfidfed1 = tfidf.transform(lst)
                        # calculates cos_similarity between training set and new document
                        cos = cosine_similarity(tfidfed, tfidfed1)
                        # averages the cosine similarities for client_folders
                        client_folder = summarize(token_dict, cos)
                        # averages the cosine similarities for categories
                        result = categorize(token_dict, client_folder, categories)
                        # predicts which category the document should fit in
                        prediction = predict(result)
                        predictions.append(prediction)
    return predictions, labels


def cos_accuracy(predictions, labels, display=False):
    accuracy = []
    for i in xrange(len(labels)):
        accuracy.append(predictions[i] == labels[i])
        if display == True:
            print (predictions[i], labels[i])
    result = sum(accuracy) / len(accuracy)
    print '-------------------------'
    print 'Total Accuracy: {}'.format(sum(accuracy) / len(accuracy))


def classify_nb(TestDir):
    X_test = []
    y_test = []
    for client in os.listdir(TestDir):
        if not client.startswith('.'):
            category_path = TestDir + '/' + client
            for category in os.listdir(category_path):
                if not category.startswith('.'):
                    pdf_path = TestDir + '/' + client + '/' + category
                    for pdf in os.listdir(pdf_path):
                        # cleans documents
                        new_pdf = get_docs(pdf_path + '/' + pdf)
                        # X_test is a list where each entry is a document
                        X_test.append(new_pdf)
                        # y_test is the label for each document
                        y_test.append(category)
    # reshapes y_test because nb takes array_like not a list
    reshape_labels = np.asarray(labels)
    reshape_labels.reshape(len(labels), 1)
    # nb.fit takes in (X_train as sparse_matrix, array_like)
    nb.fit(tfidfed, reshape_labels)
    # changes X_test into a sparse_matrix
    tfidfed1 = tfidf.transform(X_test)
    # predicts X_test
    pred = nb.predict(tfidfed1)
    return pred, y_test


def nb_accuracy(labels, predictions, display=False):
    accuracy = []
    predictions = predictions.tolist()
    for i in xrange(len(labels)):
        accuracy.append(predictions[i] == labels[i])
        if display == True:
            print (predictions[i], labels[i])
    result = sum(accuracy) / len(accuracy)
    print '-------------------------'
    print 'Total Accuracy: {}'.format(sum(accuracy) / len(accuracy))


if __name__ == '__main__':
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')

    token_dict = train_data()
    raw_docs, doc_labels = get_raw_docs(token_dict)
    categories = categories(token_dict)

    tfidfed = tfidf.fit_transform(raw_docs)

    nb = MultinomialNB()

# predictions, labels = classify_cos('/Users/matthewwong/dsi-capstone/Test')
# cos_accuracy(predictions, labels)
# predictions, labels = classify_nb('/Users/matthewwong/dsi-capstone/Test')
# nb_accuracy(predictions, labels)
