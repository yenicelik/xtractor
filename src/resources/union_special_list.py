"""
    Imports the Union Special Parts list
"""
import pandas as pd
pd.set_option('display.max_columns', 100)

import Levenshtein


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

        # Create duplicates where we have a "TP" "SP" after the price, with a
        def _status_to_meaning(char):
            if char == 'A':
                return 'active'
            elif char == 'C':
                return 'avail/price must be checked'
            elif char == 'G':
                return 'not available or replaced'
            elif char == 'R':
                return 'parts on request'
            elif char == 'T':
                return 'dead part'
            else:
                return "-"

        # Remove all whitespaces from the partno
        df['Partnumber'] = df['Partnumber'].apply(lambda x: x.strip())
        # df['Partnumber'] = df['Partnumber'].apply(lambda x: x.replace(' ', ""))
        df['Price'] = df['Price'].apply(lambda x: float(x))
        print("Listprice is:")
        print(df['Price'])
        # Drop all where the listprice is not available
        # Perhaps make sense to put the warnings into the e-mail
        df['Replaced'] = df['Replaced'].apply(lambda x: str(x).strip())
        df['Replaced'] = df['Replaced'].fillna(" ")
        df['Status'] = df['Status'].apply(lambda x: str(x).strip())
        # df['Status'] = df['Status'].apply(_status_to_meaning)

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
        # "-" instead of " " (and vice-verca)
        # remove all whitespaces
        # Should probably populate initial dataframe with these items

        # Return a single JSON with the given items
        out = self.pricelist[self.pricelist['Partnumber'] == part_no]
        if len(out) != 0:
            return out.to_dict(orient='records')[0]
        print("No items found, using levenshtein 1")
        # Else, calculate the hamming distance for all partnumber items, and return the minimum one
        # (if we have hamming-distance less than 3!)
        levenshtein_distances = self.pricelist['Partnumber'].apply(lambda x: Levenshtein.distance(part_no, x)) == 0
        out = self.pricelist[levenshtein_distances == 1]
        print("No items found, using levenshtein 2")
        print(out)
        if len(out) != 0:
            return out.to_dict(orient='records')[0]
        # Not sure if we should allow this
        out = self.pricelist[levenshtein_distances == 2]
        # Return first find
        return out.to_dict(orient='records')[0]

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