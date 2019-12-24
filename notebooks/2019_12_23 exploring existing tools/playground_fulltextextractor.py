"""
    We use the entire PDF or Excel to
    - (i) extract all of the text and
    - (ii) identify for any regex match with part-numbers
"""
# !/usr/bin/python
# coding: utf-8

from pdf2image import convert_from_path
from wand.image import Image

# from PIL import Image
import pytesseract

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from src.resources.union_special_excel import USExcelTemplate
from src.resources.union_special_list import usp_price_list

if __name__ == '__main__':
    print("Starting to extract text")

    print(usp_price_list.get_partlist_as_set)


    import tempfile

    fulltext = []

    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path('/Users/david/xtractor/data/RFP/sample2.pdf', output_folder=path)
        print("Images from path")
        print(images)
        for i, img in enumerate(images):
            fname = "image" + str(i) + ".png"
            img.save(fname, "PNG")

            # Now with the image, do something!
            print('width =', img.width)
            print('height =', img.height)

            # print('pages = ', len(img.sequence))
            # print('resolution = ', img.resolution)

            # Resize for uniform treatment
            text = pytesseract.image_to_string(img)
            # text = pytesseract.image_to_string(Image.open('image.jpg'))

            fulltext.append(text)

    fulltext = "\n".join(fulltext).strip()
    # Remove all newlines
    fulltext = fulltext.replace("\n", " ")
    fulltext = set(fulltext.split())

    print("Fulltext is")
    print(fulltext)

    print("\n\nIntersection is: ")

    # Now we could perhaps also run some simple NER to prune some of the options

    # Find intersection
    all_found_parts = fulltext.intersection(usp_price_list.get_partlist_as_set)

    # Create an excel with the given format (open, write, save to new)
    excel = USExcelTemplate()
    for part in all_found_parts:
        print("Getting part number")
        print(part)

        part_json = usp_price_list.get_partnumber_json(part_no=part)
        print("Part json is: ")



        # For each item in the intersection retrieve from the price list and retrieve the individual items
        print("Inserting example exel")
        excel.insert_item(
            partnumber=part_json['Partnumber'],
            description=part_json['Description'],
            listprice=part_json['Price'],
            stock=part_json['Stock'],
            status=part_json['Status'],
            weight=part_json['Weight'],
            replaced=part_json['Replaced']
        )

    exit(0)

    excel.save_to_disk()

    print("Opening Excel")

