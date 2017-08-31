from __future__ import division
from parse_text import *
from collections import Counter
from copy import *
import parse_text
import os
import numpy as np


def classify_knn_cos(TestDir, n=6):
    '''
    Classifies new documents by finding their cosine similarity to each document
    in the training data.  Then returns a prediction based on majority of the
    labels for the top n-1 cosine values.
    ex: knn_predictions = classify_knn_cos('/Users/matthewwong/dsi-capstone/Test/')
    '''
    test_dict = get_dict(TestDir)
    test_docs, test_labels = seperate(test_dict)
    tfidfed1 = tfidf.transform(test_docs)
    cos = cosine_similarity(tfidfed1, tfidfed)

    knn_predictions = []
    for test_doc in xrange(len(cos)):
        count = []
        top_n_idx = []
        top_n_pred = []
        copy = deepcopy(cos[test_doc])
        copy.sort()
        # takes the n-1 highest cosine similarities
        top_n = copy[:-n:-1]
        # finds the index for each of those cosine similarities
        for doc_cos_sim in top_n:
            idx = np.where(cos[test_doc] == doc_cos_sim)
            top_n_idx.append(idx[0][0])
        # finds the labels for each of those indices
        for idx in top_n_idx:
            top_n_pred.append(training_labels[idx])
        # takes the majority votex
        top_n_dict = Counter(top_n_pred)
        for k, v in top_n_dict.iteritems():
            count.append((v, k))
        count.sort(reverse=True)
        knn_predictions.append(count[0][1])
    return knn_predictions


def knn_accuracy(knn_predictions, test_labels, display=False):
    '''
    Calculates the accuracy of the knn_cos prediction model.
    ex: knn_accuracy(knn_predictions, test_labels)
    '''
    accuracy = []
    for i in xrange(len(labels)):
        accuracy.append(knn_predictions[i] == labels[i])
        if display == True:
            print (knn_predictions[i], labels[i])
    result = sum(accuracy) / len(accuracy)
    print '-------------------------'
    print 'Total Accuracy: {}'.format(sum(accuracy) / len(accuracy))


def classify_avg_cos(TestDir, threshold=1.5):
    '''
    Classifies new documents by finding their average cosine similarity to each
    of the different categories.  The average cosine similarity is calculated
    by the sum of all cosine similarities in that category divided by the total
    number of documents in that category.  If the highest average cosine similarity
    is above the threshold level, then it returns that prediction.  If it is within
    the threshold then it returns the top 3 categories with their average cosine
    similarities.  Base threshold is set at 1.5 times the second greatest category.
    ex: cos_predictions = classify_avg_cos('/Users/matthewwong/dsi-capstone/Test/')
    '''
    test_dict = get_dict(TestDir)
    test_docs, test_labels = seperate(test_dict)
    tfidfed1 = tfidf.transform(test_docs)
    cos = cosine_similarity(tfidfed1, tfidfed)

    cos_predictions = []
    for test_doc in xrange(len(test_docs)):
        avg_predictions = []
        # goes through every category
        for category in categories:
            cos_sum = 0
            # gets all the indices in the training data that match that category
            indices = [idx for idx, label in enumerate(training_labels) if label == category]
            # adds all the cosine similarities together and takes the average
            for idx in indices:
                cos_sum += cos[test_doc][idx]
            avg_cos = cos_sum / len(indices)
            avg_predictions.append((avg_cos, category))
        # sorts avg_predictions from highest to lowest
        avg_predictions.sort(reverse=True)
        # adds prediction or options based on confidence
        if avg_predictions[0][0] > threshold * avg_predictions[1][0]:
            cos_predictions.append(avg_predictions[0][1])
        else:
            cos_predictions.append(avg_predictions[:3])
    return cos_predictions


def cos_accuracy(cos_predictions, test_labels, display=False):
    '''
    Calculates the accuracy of the avg_cos prediction model.
    ex: cos_accuracy(cos_predictions, test_labels)
    '''
    accuracy = []
    for i in xrange(len(labels)):
        # accounts for the predictions where there are options
        if type(predictions[i]) == list:
            accuracy.append(predictions[i][0][1] == labels[i])
            if display == True:
                print 'Review: {}'.format(predictions[i])
                print 'Prediction: {}'.format((predictions[i][0][1], labels[i]))
        # accounts for predictions where there is a clear decision
        else:
            accuracy.append(predictions[i] == labels[i])
            if display == True:
                print 'Prediction: {}'.format((predictions[i], labels[i]))
    result = sum(accuracy) / len(accuracy)
    print '-------------------------'
    print 'Total Accuracy: {}'.format(sum(accuracy) / len(accuracy))


def classify_nb(TestDir):
    '''
    Classifies new documents using a Naive Bayes model.
    ex: nb_predictions = classify_nb('/Users/matthewwong/dsi-capstone/Test/')
    '''
    test_dict = get_dict(TestDir)
    test_docs, test_labels = seperate(test_dict)
    # reshape training_labels to a column vector
    reshape_labels = np.asarray(training_labels)
    reshape_labels.reshape(len(training_labels), 1)
    # nb.fit takes in (X_train as sparse_matrix, y_train as array_like)
    nb.fit(tfidfed, reshape_labels)
    tfidfed1 = tfidf.transform(test_docs)
    nb_predictions = nb.predict(tfidfed1)
    return nb_predictions


def nb_accuracy(predictions, labels, display=False):
    '''
    Calculates the accuracy of the Naive Bayes model.
    ex: nb_accuracy(nb_predictions, test_labels)
    '''
    accuracy = []
    predictions = predictions.tolist()
    for i in xrange(len(labels)):
        accuracy.append(predictions[i] == labels[i])
        if display == True:
            print (predictions[i], labels[i])
    result = sum(accuracy) / len(accuracy)
    print '-------------------------'
    print 'Total Accuracy: {}'.format(sum(accuracy) / len(accuracy))


def compare(knn_predictions, cos_predictions, nb_predictions, test_labels):
    '''
    Compares the predictions of the 3 different models.
    ex: compare(knn_predictions, cos_predictions, nb_predictions, test_labels)
    '''
    for i in xrange(len(knn_predictions)):
        if type(cos_predictions[i]) == list:
            print (knn_predictions, cos_predictions[i][0][1], \
                    nb_predictions[i], test_labels[i])
        else:
            print (knn_predictions, cos_predictions[i], \
                    nb_predictions[i], test_labels[i])


if __name__ == '__main__':
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    nb = MultinomialNB()

    # deletes documents with no text in them
    # list_to_OCR = strip_blank('/Users/matthewwong/dsi-capstone/Text/')
    # list_to_OCR1 = strip_blank('/Users/matthewwong/dsi-capstone/Test/')

    training_dict = get_dict('/Users/matthewwong/dsi-capstone/Text/')
    training_docs, training_labels = seperate(training_dict)
    categories = categories(training_dict)
    tfidfed = tfidf.fit_transform(training_docs)

    test_dict = get_dict('/Users/matthewwong/dsi-capstone/Test/')
    test_docs, test_labels = seperate(test_dict)
    # tfidfed1 = tfidf.transform(test_docs)
    #
    # cos = cosine_similarity(tfidfed1, tfidfed)
