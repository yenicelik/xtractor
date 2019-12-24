"""
    Trying out table-extraction using OCR software
"""

import camelot
import pandas as pd

pd.set_option('display.max_columns', 100)


def run_analysis(filepath):
    tables = camelot.read_pdf(filepath)
    print(tables)

    for table in tables:
        print(table)
        print(table.parsing_report)
        print(table.df)  # get a pandas DataFrame!
        print(table.df.columns)  # get a pandas DataFrame!

    # Replace all \n by space

    # Find within the entire

    # Apply all character recognition to just do NER and find all parts that are also in the database of product cataglogues


if __name__ == "__main__":
    print("Trying to get tables from PDFs and excels etc.")
    filepaths = [
        '/Users/david/xtractor/data/RFP/sample2.pdf',
        # '/Users/david/xtractor/data/RFP/sample1.pdf'
    ]
    for filepath in filepaths:
        run_analysis(filepath)
