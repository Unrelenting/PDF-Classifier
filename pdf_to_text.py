from cStringIO import StringIO
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt


'''
To fix unichr() arg not in range(0x10000) (narrow Python build)
https://github.com/euske/pdfminer/pull/148/commits/cea7eefde6301e377bb4a3a499fb2e2ace8c2a78

To fix AttributeError: 'FileUnicodeMap' object has no attribute 'add_code2cid'
https://github.com/euske/pdfminer/commit/6b6fc264ffd58cd1c305e8c23990b85e846964e9
'''


# converts pdf and returns its text content as a string
def convert_one(filename, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(filename, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


# converts all pdfs in directory pdfDir and saves all resulting text files to txtdir
def convert_multiple(pdfDir, txtDir):
    text_file = "/Users/matthewwong/dsi-capstone/Text/"
    if pdfDir == "": pdfDir = os.getcwd() + "\\" # if no pdfDir passed in
    for pdf in os.listdir(pdfDir): # iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + '/' + pdf
            text = convert_one(pdfFilename) # get string of text content of pdf
            # makes folder for client if none exists in text folder
            if not os.path.exists(text_file + pdfDir.split('/')[-2]):
                os.makedirs(text_file + pdfDir.split('/')[-2])
            if not os.path.exists(text_file + pdfDir.split('/')[-2] + '/' + pdfDir.split('/')[-1]):
                os.makedirs(text_file + pdfDir.split('/')[-2] + '/' + pdfDir.split('/')[-1])
            textFilename = txtDir + '/' + pdf.split('.')[0] + ".txt"
            textFile = open(textFilename, "w") # make text file
            textFile.write(text) # write text to text file


def convert(Dir):
    # filepath to decrypted pdfs folder and text directory
    pdfDir = "/Users/matthewwong/dsi-capstone/PDFs/decrypted/"
    txtDir = "/Users/matthewwong/dsi-capstone/Text/"
    # changes pdfDir and txtDir to reflect which folder you want to convert
    pdfDir = pdfDir + Dir
    txtDir = txtDir + pdfDir.split('/')[-1]
    # goes through all the folders in that client's files and converts them to text
    for folder in os.listdir(pdfDir):
        if not folder.startswith('.'):
            pdfDir1 = pdfDir + '/' + folder
            txtDir1 = txtDir + '/' + folder
            convert_multiple(pdfDir1, txtDir1)


def convert_pdfDir():
    pdfDir = "/Users/matthewwong/dsi-capstone/PDFs/decrypted/"
    for client in os.listdir(pdfDir):
        if not client.startswith('.'):
            print client
            convert(client)


# if __name__ == '__main__':
    # text = convert('/Users/matthewwong/dsi-capstone/pdf_to_text/PDFs/test1.pdf')
    # convert_multiple(pdfDir, txtDir + pdfDir.split('/')[-1])
    # convert('A1')
