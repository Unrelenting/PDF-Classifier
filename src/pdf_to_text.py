from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from OCR import *
import string
import pdfminer
import os
import sys, getopt


'''
To fix unichr() arg not in range(0x10000) (narrow Python build)
https://github.com/euske/pdfminer/pull/148/commits/cea7eefde6301e377bb4a3a499fb2e2ace8c2a78

To fix AttributeError: 'FileUnicodeMap' object has no attribute 'add_code2cid'
https://github.com/euske/pdfminer/commit/6b6fc264ffd58cd1c305e8c23990b85e846964e9
'''


def convert_one(filename, pages=None):
    '''
    Converts a PDF and returns its contents as a string using PDFminer.
    ex: text = convert_one('/Users/matthewwong/dsi-capstone/PDFs/decrypted/A1/Appraisal/Certificate.pdf')
    '''
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


def convert_multiple(pdfDir, txtDir):
    '''
    Converts all PDFs in a specific folder to the Text directory using PDFminer.
    ex: convert_multiple(pdfDir, txtDir + pdfDir.split('/')[-1])
    '''
    text_file = "/Users/matthewwong/dsi-capstone/Text/"
    if pdfDir == "": pdfDir = os.getcwd() + "\\" # if no pdfDir passed in
    for pdf in os.listdir(pdfDir): # iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf" or fileExtension == "PDF":
            pdfFilename = pdfDir + '/' + pdf
            text = convert_one(pdfFilename) # get string of text content of pdf
            # makes folder for client if none exists in text folder
            if not os.path.exists(text_file + pdfDir.split('/')[-2]):
                os.makedirs(text_file + pdfDir.split('/')[-2])
            if not os.path.exists(text_file + pdfDir.split('/')[-2] + '/' + pdfDir.split('/')[-1]):
                os.makedirs(text_file + pdfDir.split('/')[-2] + '/' + pdfDir.split('/')[-1])
            # textFilename = txtDir + '/' + pdf.split('.')[0] + ".txt"
            textFilename = txtDir + '/' + string.replace(pdf, '.pdf', '.txt')
            textFile = open(textFilename, "w") # make text file
            textFile.write(text) # write text to text file


def convert(Dir):
    '''
    Converts one client's folder with PDFs into text documents in the Text directory
    using PDFminer.
    ex: convert('A1')
    '''
    # filepath to decrypted pdfs folder and text directory
    pdfDir = "/Users/matthewwong/dsi-capstone/PDFs/decrypted_test/"
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
    '''
    Simple command line function that will convert every client in the decrypted
    directory into the text directory using PDFminer.
    ex: convert_pdfDir()
    '''
    pdfDir = "/Users/matthewwong/dsi-capstone/PDFs/decrypted_test/"
    for client in os.listdir(pdfDir):
        if not client.startswith('.'):
            print 'Converting: {}'.format(client)
            convert(client)


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
    pdfDir = '/Users/matthewwong/dsi-capstone/PDFs/decrypted_test/'
    txtDir = '/Users/matthewwong/dsi-capstone/Test/'
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
    pdfDir = '/Users/matthewwong/dsi-capstone/PDFs/decrypted_test/'
    txtDir = '/Users/matthewwong/dsi-capstone/Test/'
    for filename in list_to_OCR:
        print 'Converting file: {}'.format(filename)
        new_filename = string.replace(filename, '.txt', '.pdf')
        final_text = get_text(pdfDir + new_filename)
        text_file = open(txtDir + filename, 'w')
        for page in final_text:
            text_file.write(page.encode('ascii','ignore'))
        text_file.close()


def OCR_convert(pdfDir, txtDir):
    '''
    Uses OCR to convert all PDF documents from one directory into another.
    ex: OCR_convert('/Users/matthewwong/dsi-capstone/PDFs/decrypted_test/', \
                    '/Users/matthewwong/dsi-capstone/OCR_text_subset/')
    '''
    for client in os.listdir(pdfDir)[1:]:
        print 'Converting: {}'.format(client)
        # makes client folders if they do not exist
        if not os.path.exists(txtDir + client):
            os.makedirs(txtDir + client)
        for folder in os.listdir(pdfDir + client)[1:]:
            # makes category folders if they do not exist
            if not os.path.exists(txtDir + client + '/' + folder):
                os.makedirs(txtDir + client + '/' + folder)

            for pdf in os.listdir(pdfDir + client + '/' + folder):
                fileExtension = pdf.split('.')[-1]
                if fileExtension == 'pdf' or fileExtension == 'PDF':
                    final_text = get_text(pdfDir + client + '/' + folder + '/' + pdf)

                    new_filename = string.replace(pdf, '.pdf', '.txt')
                    new_filename = string.replace(new_filename, '.PDF', '.txt')

                    text_file = open(txtDir + client + '/' + folder + '/' + new_filename, 'w')
                    for page in final_text:
                        text_file.write(page.encode('ascii','ignore'))
                    text_file.close()
