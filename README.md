# PDF Classifier for a Mortgage Company

Often mortgage companies get hundreds of PDFs a day and many hours are spent by
employees to classify and file these PDFs.  This essentially costs businesses a
lot of money because employees need to spend time sorting and filing these PDFs
instead of completing other tasks essential to the business, so my goal was to
create a classifier that could address this issue and ultimately save both employees
time and the business money.  This pipeline contains scripts to decrypt these PDFs
to allow for text extraction, extract and analyze the text, and then predict
their classification based on various models.


# Prerequisites

1. QPDF
2. PDFminer
3. PyOCR

Tips to installing PDFminer:
https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf
Tips to installing PyOCR:
https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/


# Getting Started

Step One: Decrypt files so text extraction is possible.

Step Two: Convert PDFs to text files.  

PDFminer should work for forms, but you will need PyOCR for scanned PDFs.  For
the best results use the covert_pdfDir function first to extract text with PDFminer, then run the strip_blank function to delete any text files that were not converted,
and then use the fill_blank function to complete the rest of the documents with PyOCR.

Step Three: Train your model.

Step Four: Predict Classifications.


# Example Code

See examples.md
