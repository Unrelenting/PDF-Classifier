import os
import subprocess
import glob
import string


def format_filename(filename):
    '''
    Changes filenames and gets rid of any characters that might break the code.
    '''
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(char for char in filename if char in valid_chars)
    return filename


def clean_folder(client_folder):
    '''
    Goes through each folder and checks if the filenames are acceptable.
    ex: clean_folder('/Users/matthewwong/Desktop/A1')
    '''
    for folder in os.listdir(client_folder):
        filepath = client_folder + '/' + folder
        if not folder.startswith('.'):
            for filename in os.listdir(filepath):
                os.rename(filepath + '/' + filename, \
                    filepath + '/' + format_filename(filename))


def decrypt_pdf(filename):
    '''
    Decrypts a PDF so they can be run through PDFminer to extract the text.
    Also makes folders for client if none exists.
    ex: decrypt_pdf('/Users/matthewwong/Desktop/Insurance.pdf')
    Subprocess example:
    subprocess.call(["qpdf", "--password=''", "--decrypt", "input_file", "output_file"])
    '''
    decrypted_file = "/Users/matthewwong/dsi-capstone/PDFs/decrypted/"
    client_folder = filename.split('/')[-3]
    folder = filename.split('/')[-2]
    pdf = filename.split('/')[-1]
    if not os.path.exists(decrypted_file + client_folder):
        os.makedirs(decrypted_file + client_folder)
    if not os.path.exists(decrypted_file + client_folder + '/' + folder):
        os.makedirs(decrypted_file + client_folder + '/' + folder)
    lst = ["qpdf", "--password=''", "--decrypt", filename, \
        decrypted_file + client_folder + '/' + folder + '/' + pdf]
    subprocess.call(' '.join(map(lambda x: x.replace(' ', '\ '), lst)),
                    shell=True)


def decrypt_folder(client_folder):
    '''
    Decrypts a folder so the PDFs can be run through PDFminer to extract text.
    ex: decrypt_folder('/Users/matthewwong/Desktop/A1')
    '''
    # looks at all the folders in the client folder
    for folder in os.listdir(client_folder):
        filepath = str(client_folder) + '/' + folder
        if not folder.startswith('.'):
            # looks at the files in those folders
            for filename in os.listdir(filepath):
                # list of all the pdfs
                pdfs = glob.glob(filepath + '/' + '*.pdf')
                # adds files ending with caps
                if filename.endswith('PDF'):
                    pdfs.append(filepath + '/' + filename)
                for pdf in pdfs:
                    decrypt_pdf(pdf)


def decrypt(client_folder):
    '''
    Decrypts a client's entire folder.
    ex: decrypt('/Users/matthewwong/Desktop/A1')
    '''
    clean_folder(client_folder)
    decrypt_folder(client_folder)
