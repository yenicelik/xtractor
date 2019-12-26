"""
    Extracts the fulltext form the XLS
"""

import tempfile

from xlrd import open_workbook


class XLS2Text:

    def __init__(self):
        pass

    def xls_bytestring_to_text(self, bytestr):

        # Create the xlrd object

        # Iterate through all sheets

        fulltext = []

        # Otherwise we can also save and load from disk
        # if this is not successful...

        # Put the entire text into the fulltext
        workbook = open_workbook(file_contents=bytestr)
        # )xlsx_file.read().decode(encoding="utf-8", errors='replace'))

        # save the bytestr to a temporary location...
        fulltext = []

        for sheets in workbook.sheets():
            for col in range(sheets.ncols):
                for rows in range(sheets.nrows):
                    # Try to extract the value here,
                    # should probably place try-errors after some first successful tries...
                    fulltext.append(str(sheets.cell(rows, col).value))

        fulltext = "\n".join(fulltext).strip()
        # Remove all newlines
        fulltext = fulltext.replace("\n", " ")

        return fulltext
