"""
    Union special excel template
"""
import random

import numpy as np
from copy import copy
from openpyxl import load_workbook

def _write_value_to_cell(cell_identifier, style_cell_identifier, value):
    """
        Preserves style when writing to the cell
    :param cell_identifier:
    :param value:
    :return:
    """
    # new_cell.font = copy(cell.font)
    # new_cell.border = copy(cell.border)
    # new_cell.fill = copy(cell.fill)
    # new_cell.number_format = copy(cell.number_format)
    # new_cell.protection = copy(cell.protection)
    # new_cell.alignment = copy(cell.alignment)
    # self.sheet[f'A{rowidx}'] = self.rowcounter + 1
    # self.sheet[f'A{rowidx}'].style = style
    # new_cell.font = copy(cell.font)
    pass

class USExcelTemplate:

    def _load_template(self):
        filepath = "/Users/david/xtractor/data/Templates/UnionSpecial.xlsx"
        workbook = load_workbook(filepath)
        sheet = workbook.active
        print("Workbook is")
        print("Cell F11 is", sheet['F11'].internal_value)
        assert sheet['F11'].internal_value == "Ref:", (
            f"Correct cell not found! expected {sheet['F11'].internal_value} got {'Ref'}"
        )

        return workbook, sheet

    def __init__(self):
        self.workbook, self.sheet = self._load_template()
        # set the counter ...
        self.rowcounter = 0
        self.rowoffset = 17  # the enumeration of items starts at row 17

    def update_date(self):
        pass

    def insert_item(
            self,
            description,
            partnumber,
            listprice,
            requested_units,
            stock=None,
            status=None,
            weight=None,
            replaced=None
    ):

        assert isinstance(listprice, float) or isinstance(listprice, int) or isinstance(listprice, np.float64), (
            "Listprice is not of type float", listprice, type(listprice)
        )

        rowidx = self.rowcounter + self.rowoffset

        print("Row id is", rowidx)

        # Insert a row
        if self.rowcounter > 0:
            self.sheet.insert_rows(rowidx + 1) # Plus 1 because we insert above, not below the roindex
            previous_row = rowidx - 1
        else:
            previous_row = rowidx

        # Copy the styles of the preivous cells
        print("Row offset is: ", self.rowcounter)

        # Insert "sira"
        style = copy(self.sheet[f'A{previous_row}']._style)
        self.sheet[f'A{rowidx}'] = self.sheet[f'A{previous_row}'].value + 1 if self.rowcounter > 0 else 1
        self.sheet[f'A{rowidx}']._style = style

        # Partnumber
        style = copy(self.sheet[f'D{previous_row}']._style)
        self.sheet[f'D{rowidx}'] = partnumber
        self.sheet[f'D{rowidx}']._style = style

        # Description
        style = copy(self.sheet[f'E{previous_row}']._style)
        self.sheet[f'E{rowidx}'] = description
        self.sheet[f'E{rowidx}']._style = style

        # Listprice
        style = copy(self.sheet[f'I{previous_row}']._style)
        self.sheet[f'I{rowidx}'] = listprice
        self.sheet[f'I{rowidx}']._style = style

        style = copy(self.sheet[f'B{previous_row}']._style)
        self.sheet[f'B{rowidx}'] = requested_units
        self.sheet[f'B{rowidx}']._style = style

        # Stock
        if stock is not None:
            style = copy(self.sheet[f'L{previous_row}']._style)
            self.sheet[f'L{rowidx}'] = stock
            self.sheet[f'L{rowidx}']._style = style

        # Status
        if status is not None:
            style = copy(self.sheet[f'K{previous_row}']._style)
            self.sheet[f'K{rowidx}'] = status
            self.sheet[f'K{rowidx}']._style = style

        # Weight
        if weight is not None:
            style = copy(self.sheet[f'M{previous_row}']._style)
            self.sheet[f'M{rowidx}'] = weight
            self.sheet[f'M{rowidx}']._style = style

        # Replaced
        if replaced is not None:
            style = copy(self.sheet[f'N{previous_row}']._style)
            self.sheet[f'N{rowidx}'] = replaced
            self.sheet[f'N{rowidx}']._style = style

        # Copy all equations which were not copied yet

        style = copy(self.sheet[f'F{previous_row}']._style)
        self.sheet[f'F{rowidx}'] = f'=J{rowidx}'
        self.sheet[f'F{rowidx}']._style = style

        style = copy(self.sheet[f'J{previous_row}']._style)
        self.sheet[f'J{rowidx}'] = f'=I{rowidx} * 2.15'
        self.sheet[f'J{rowidx}']._style = style

        style = copy(self.sheet[f'H{previous_row}']._style)
        self.sheet[f'H{rowidx}'] = f'=F{rowidx}*B{rowidx}'
        self.sheet[f'H{rowidx}']._style = style

        # Copy cell style for "dead cells
        for deadcol in ['C', 'G']:
            style = copy(self.sheet[f'{deadcol}{previous_row}']._style)
            self.sheet[f'{deadcol}{rowidx}']._style = style

        print("Row id is", rowidx)

        self.sheet[f'H{rowidx + 3}'] = f'=SUM(H{self.rowoffset}: H{rowidx})'
        self.sheet[f'H{rowidx + 4}'] = f'=H{rowidx + 3}*25/100'
        self.sheet[f'H{rowidx + 5}'] = f'=H{rowidx + 3}-H{rowidx + 4}'

        # Increase counter by one...
        self.rowcounter += 1

    def save_to_disk(self):
        rnd_no = random.randint(10000, 99999)
        # self.workbook.save(f"./test{rnd_no}.xlsx")
        self.workbook.save(f"./test1.xlsx")

if __name__ == "__main__":
    print("Looking at the individual items")
    excel = USExcelTemplate()
    print("Inserting example exel")
    excel.insert_item(
        description="Item descr",
        partnumber="Part number",
        listprice=249
    )
    excel.insert_item(
        description="Item descrtoo",
        partnumber="FFF2",
        listprice=266
    )
    excel.save_to_disk()
