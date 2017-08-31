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


def clean_folder(folder):
    '''
    Goes through each folder and checks if the filenames are acceptable.
    '''
    for subfolder in os.listdir(folder):
        filepath = str(folder) + '/' + subfolder
        if not subfolder.startswith('.'):
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
    subfolder = filename.split('/')[-2]
    pdf_file = filename.split('/')[-1]
    if not os.path.exists(decrypted_file + client_folder):
        os.makedirs(decrypted_file + client_folder)
    if not os.path.exists(decrypted_file + client_folder + '/' + subfolder):
        os.makedirs(decrypted_file + client_folder + '/' + subfolder)
    lst = ["qpdf", "--password=''", "--decrypt", filename, \
        decrypted_file + client_folder + '/' + subfolder + '/' + pdf_file]
    subprocess.call(' '.join(map(lambda x: x.replace(' ', '\ '), lst)),
                    shell=True)


def decrypt_folder(folder):
    '''
    Decrypts a folder so the PDFs can be run through PDFminer to extract text.
    ex: decrypt_folder('/Users/matthewwong/Desktop/A1')
    '''
    # looks at all the folders in the client folder
    for subfolder in os.listdir(folder):
        filepath = str(folder) + '/' + subfolder
        if not subfolder.startswith('.'):
            # looks at the files in those folders
            for filename in os.listdir(filepath):
                # list of all the pdfs
                pdfs = glob.glob(filepath + '/' + '*.pdf')
                # adds files ending with caps
                if filename.endswith('PDF'):
                    pdfs.append(filepath + '/' + filename)
                for pdf in pdfs:
                    decrypt_pdf(pdf)


def decrypt(folder):
    '''
    Decrypts a client's entire folder.
    ex: decrypt('A1')
    '''
    clean_folder(folder)
    decrypt_folder(folder)
