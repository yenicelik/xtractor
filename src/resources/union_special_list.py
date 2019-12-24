"""
    Imports the Union Special Parts list
"""
import pandas as pd
pd.set_option('display.max_columns', 100)

class USPriceList:

    def _load_pricelist(self):
        filepath = "/Users/david/xtractor/data/UnionSpecial/Spare Parts EDC with Stock_11_2019.xls"
        df = pd.read_excel(filepath)
        print(df.head())
        df = df[[
            'Partnumber',
            'Beschreibung',
            'Description',
            'Status',
            'Price €',
            'Stock',
            'Weight in g',
            'Replaced by',
            'Changes',
            'Shortcut',
            'HS Code'
        ]]
        print(df.head())
        df = df.rename(columns={'Price €': 'Price', 'Weight in g': 'Weight', 'Replaced by': 'Replaced', 'HS Code': 'HSCode'})
        df = df[3:]
        print(df.head())

        # Remove all whitespaces from the partno
        df['Partnumber'] = df['Partnumber'].apply(lambda x: x.strip())
        # df['Replaced'] = df['Replaced'].apply(lambda x: str(x).strip())
        # Remove all whitespaces from HSCode

        return df

    def __init__(self):
        self.pricelist = self._load_pricelist()

    def get_partnumber_json(self, part_no):
        """
            Retrieves the part number from the stock list
        :param part_no:
        :return:
        """
        return self.pricelist[self.pricelist['Partnumber'] == part_no]

    @property
    def get_partlist(self):
        return self.pricelist['Partnumber']

    @property
    def get_partlist_as_set(self):
        return set(self.pricelist['Partnumber'])

usp_price_list = USPriceList()

if __name__ == "__main__":
    print("Import the Stock Control List from Union Special")
    stock = USPriceList()
    print("Stock object is: ")
    print(stock.get_partnumber_json(part_no="10005B"))