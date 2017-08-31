from __future__ import print_function
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io


def get_text(filepath):
    '''
    Uses OCR to get the text from a pdf.
    Returns a list where each element is the text of a single page of that pdf.
    ex: final_text = get_text('/Users/matthewwong/dsi-capstone/PDFs/decrypted/
        A1/Certifications/Certificates Flood Cert.txt')
    '''
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]

    req_image = []
    final_text = []

    image_pdf = Image(filename=filepath, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)

    return final_text
