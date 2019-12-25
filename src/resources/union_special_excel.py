"""
    Union special excel template
"""
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
            stock=None,
            status=None,
            weight=None,
            replaced=None
    ):

        assert isinstance(listprice, float) or isinstance(listprice, int) or isinstance(listprice, np.float64), (
            "Listprice is not of type float", listprice, type(listprice)
        )

        rowidx = self.rowcounter + self.rowoffset

        # Insert a row
        if self.rowcounter > 0:
            self.sheet.insert_rows(rowidx + 1) # Plus 1 because we insert above, not below the roindex

        # Copy the styles of the preivous cells

        # Insert "sira"
        style = copy(self.sheet[f'A{self.rowoffset}']._style)
        self.sheet[f'A{rowidx}'] = self.rowcounter + 1
        self.sheet[f'A{rowidx}']._style = style

        # Partnumber
        style = copy(self.sheet[f'D{self.rowoffset}']._style)
        self.sheet[f'D{rowidx}'] = partnumber
        self.sheet[f'D{rowidx}']._style = style

        # Description
        style = copy(self.sheet[f'E{self.rowoffset}']._style)
        self.sheet[f'E{rowidx}'] = description
        self.sheet[f'E{rowidx}']._style = style

        # Listprice
        style = copy(self.sheet[f'I{self.rowoffset}']._style)
        print("Row offset is: ", self.rowoffset)
        print("Style is: ", style)
        self.sheet[f'I{rowidx}'] = listprice
        self.sheet[f'I{rowidx}']._style = style

        # Replaced by
        style = copy(self.sheet[f'I{self.rowoffset}']._style)
        print("Row offset is: ", self.rowoffset)
        print("Style is: ", style)
        self.sheet[f'I{rowidx}'] = listprice
        self.sheet[f'I{rowidx}']._style = style

        # Weight
        style = copy(self.sheet[f'I{self.rowoffset}']._style)
        print("Row offset is: ", self.rowoffset)
        print("Style is: ", style)
        self.sheet[f'I{rowidx}'] = listprice
        self.sheet[f'I{rowidx}']._style = style

        # Stock
        if stock is not None:
            style = copy(self.sheet[f'L{self.rowoffset}']._style)
            print("Row offset is: ", self.rowoffset)
            print("Style is: ", style)
            self.sheet[f'L{rowidx}'] = stock
            self.sheet[f'L{rowidx}']._style = style

        # Status
        if status is not None:
            style = copy(self.sheet[f'K{self.rowoffset}']._style)
            print("Row offset is: ", self.rowoffset)
            print("Style is: ", style)
            self.sheet[f'K{rowidx}'] = status
            self.sheet[f'K{rowidx}']._style = style

        # Weight
        if weight is not None:
            style = copy(self.sheet[f'M{self.rowoffset}']._style)
            print("Row offset is: ", self.rowoffset)
            print("Style is: ", style)
            self.sheet[f'M{rowidx}'] = weight
            self.sheet[f'M{rowidx}']._style = style

        # Replaced
        if replaced is not None:
            style = copy(self.sheet[f'N{self.rowoffset}']._style)
            print("Row offset is: ", self.rowoffset)
            print("Style is: ", style)
            self.sheet[f'N{rowidx}'] = replaced
            self.sheet[f'N{rowidx}']._style = style

        # Increase counter by one...
        self.rowcounter += 1

        # Copy all equations which were not copied yet
        self.sheet[f'J{rowidx}'] = f'=I{rowidx} * 2.15'
        self.sheet[f'G{rowidx}'] = f'=F{rowidx}*B{rowidx}'
        self.sheet[f'F{rowidx}'] = f'=J{rowidx}'

    def save_to_disk(self):
        self.workbook.save("./test1.xlsx")


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
