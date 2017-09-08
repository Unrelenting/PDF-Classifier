# Examples for Models



# Running the PDFminer model:

dictionary = get_dict('/Users/matthewwong/dsi-capstone/miner_Text/')
docs, labels = seperate(dictionary)
training_docs, test_docs, training_labels, test_labels = train_test_split(\
   docs, labels, stratify=labels, test_size=0.25)
categories = categories(dictionary)
tfidfed = tfidf.fit_transform(training_docs)


nb_predictions = classify_nb(test_docs, tfidfed, training_labels)
cos_predictions = classify_avg_cos(categories, test_docs, tfidfed, training_labels)
knn_predictions = classify_knn_cos(test_docs, tfidfed, training_labels)



# Running the PDFminer and PyOCR model:

dictionary = get_dict('/Users/matthewwong/dsi-capstone/Text/')
docs, labels = seperate(dictionary)
training_docs, test_docs, training_labels, test_labels = train_test_split(\
   docs, labels, stratify=labels, test_size=0.25)
categories = categories(dictionary)
tfidfed = tfidf.fit_transform(training_docs)


nb_predictions = classify_nb(test_docs, tfidfed, training_labels)
cos_predictions = classify_avg_cos(categories, test_docs, tfidfed, training_labels)
knn_predictions = classify_knn_cos(test_docs, tfidfed, training_labels)



# Running the PyOCR model:

dictionary = get_dict('/Users/matthewwong/dsi-capstone/OCR_Text/')
docs, labels = seperate(dictionary)
training_docs, test_docs, training_labels, test_labels = train_test_split(\
   docs, labels, stratify=labels, test_size=0.25)
categories = categories(dictionary)
tfidfed = tfidf.fit_transform(training_docs)


nb_predictions = classify_nb(test_docs, tfidfed, training_labels)
cos_predictions = classify_avg_cos(categories, test_docs, tfidfed, training_labels)
knn_predictions = classify_knn_cos(test_docs, tfidfed, training_labels)
