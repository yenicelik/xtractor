"""
    Playing around with reading a PDF (extracting rawtext)
"""

# importing required modules
import textract

if __name__ == "__main__":
    filename = '/Users/david/xtractor/data/UnionSpecial/GulsanTeklif.pdf'

    text = textract.process(filename).decode("utf-8")

    # text = text.split("\n")

    print("Text is: ", text)

    # Find within the text

    # Using a dictionary, we try to find the

    # print("Reading in the 'RFP' document")
    #
    # # creating a pdf file object
    # pdfFileObj = open('/Users/david/xtractor/data/UnionSpecial/GulsanTeklif.pdf', 'rb')
    #
    # # creating a pdf reader object
    # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #
    # # printing number of pages in pdf file
    # print(pdfReader.numPages)
    #
    # # creating a page object
    # pageObj = pdfReader.getPage(0)
    #
    # # extracting text from page
    # print(pageObj.extractText().encode('utf-8'))
    #
    # # closing the pdf file object
    # pdfFileObj.close()

    # fd = open(filename, "rb")
    # viewer = SimplePDFViewer(fd)
