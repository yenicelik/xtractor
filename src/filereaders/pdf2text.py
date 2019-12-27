"""
    Wrapper for logic to take in a PDF bytestring,
    and extract any existing text from the PDF
"""

import tempfile
import pytesseract
import cv2
from pdf2image import convert_from_path

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import tempfile

class PDF2Text:

    def __init__(self):
        pass

    def pdf_bytestring_to_text(self, bytestr):

        # save the bytestr to a temporary location...
        fulltext = []

        with tempfile.TemporaryDirectory() as path:
            # Save to file
            pdf_filepath = f"{path}/sample.pdf"
            with open(pdf_filepath, 'wb') as fp:
                fp.write(bytestr)
            # Must check if this is working properly with the save...

            images = convert_from_path(
                pdf_filepath,
                # dpi=300,
                output_folder=path,
                grayscale=True
            )
            print("Images from path")
            print(images)
            for i, img in enumerate(images):
                # fname = "image" + str(i) + ".png"
                # img.save(fname, "PNG")

                # Now with the image, do something!
                print('width =', img.width)
                print('height =', img.height)

                # Should we do some deblurring perhaps..?

                # print('pages = ', len(img.sequence))
                # print('resolution = ', img.resolution)

                # Resize for uniform treatment
                # Rotate the image four times, collect text from all items ...
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                for rotation_degree in [0, 90, 270]:

                    text = pytesseract.image_to_string(
                        img.rotate(rotation_degree),
                        config='-l eng' # --psm
                    )
                    fulltext.append(text)

        fulltext = "\n".join(fulltext).strip()
        # Remove all newlines
        fulltext = fulltext.replace("\n", " ")

        return fulltext
