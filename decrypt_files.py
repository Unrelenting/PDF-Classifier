import os
import subprocess
import glob
import string


# does not yet deal with an extra layer of folders in client subfolders


def format_filename(filename):
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(char for char in filename if char in valid_chars)
    return filename


def clean_folder(folder):
    for subfolder in os.listdir(folder):
        filepath = str(folder) + '/' + subfolder
        if not subfolder.startswith('.'):
            for filename in os.listdir(filepath):
                os.rename(filepath + '/' + filename, \
                    filepath + '/' + format_filename(filename))


def decrypt_pdf(filename):
    # makes folder for client if none exists in decrypted folder
    # filename.split('/')[-3] refers to the client's folder
    # filename.split('/')[-2] refers to the subfolders
    decrypted_file = "/Users/matthewwong/dsi-capstone/PDFs/decrypted/"
    client_folder = filename.split('/')[-3]
    subfolder = filename.split('/')[-2]
    pdf_file = filename.split('/')[-1]
    # cleaned = format_filename(pdf_file)
    # filename = decrypted_file + subfolder + cleaned

    if not os.path.exists(decrypted_file + filename.split('/')[-3]):
        os.makedirs(decrypted_file + filename.split('/')[-3])
    if not os.path.exists(decrypted_file + filename.split('/')[-3] + '/' + filename.split('/')[-2]):
        os.makedirs(decrypted_file + filename.split('/')[-3] + '/' + filename.split('/')[-2])
    # subprocess.call(["qpdf", "--password=''", "--decrypt", "input_file", "output_file"])
    lst = ["qpdf", "--password=''", "--decrypt", filename, \
        decrypted_file + client_folder + '/' + subfolder + '/' + pdf_file]
    subprocess.call(' '.join(map(lambda x: x.replace(' ', '\ '), lst)),
                    shell=True)


def decrypt_folder(folder):
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
    clean_folder(folder)
    decrypt_folder(folder)


# if __name__ == '__main__':
    # decrypt_pdf('/Users/matthewwong/Desktop/Insurance.pdf')
    # decrypt_folder('/Users/matthewwong/Desktop/A1')
