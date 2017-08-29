try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

'''
pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

print(pytesseract.image_to_string(Image.open('test.png')))
print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
'''


pytesseract.pytesseract.tesseract_cmd = \
'/Users/matthewwong/dsi-capstone/PDFs/decrypted/Z2/Zhang - Payoffs - Quicken thru 2017-07-01.pdf'

print(pytesseract.image_to_string(Image.open('/Users/matthewwong/dsi-capstone/PDFs/decrypted/Z2/Zhang - Payoffs - Quicken thru 2017-07-01.pdf')))
