from bs4 import BeautifulSoup
import requests
import re


def parse_doc(html):
    f = open(html)
    soup = BeautifulSoup(f)

    address = soup.find('div', style='position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:134px; top:312px; width:115px; height:61px;').text
    value = soup.find('div', style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:319px; top:612px; width:35px; height:13px;").text
    print address
    print value

    f.close()

if __name__ == '__main__':
    parse_doc('/Users/matthewwong/Desktop/test.html')
