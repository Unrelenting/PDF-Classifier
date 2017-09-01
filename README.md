# dsi-capstone


Steps:

1. Decrypt PDFs so that text extraction is possible
2. Covert PDFs to text files
  1. convert_pdfDir() - uses PDFminer to convert PDFs with forms or text layers
  2. strip_blank - gets rid of blank documents that PDFminer could not extract
      text from and uses OCR to complete those documents
3. Run models



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



# Notes on accuracy:

Just looking at kNN model:
Almost always predicts Conditions and Property labels wrong.
Of PDFs labelled as Closing_Docs, predicts 9/17 correct ~53% accuracy
Of PDFs labelled as Lock_Desk, predicts 8/10 correct ~ 80% accuracy
Of PDFs labelled as Disclosures, predicts 16/19 correct ~84% accuracy
Usually predicts other documents with ~95%+ accuracy
