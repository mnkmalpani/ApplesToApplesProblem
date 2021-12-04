"""
Assumptions:
1. One Row in buyer will have one match in supplier, if it is Exact or Partial.
    Note: In partial we will find the best suit then club them.
"""
import csv
from src.pojo.buyer import Buyer
from src.pojo.supplier import Supplier
from src.match import Match
import copy
import sys


class Classify:

    def __init__(self, file1, file2=None):
        self.file1 = file1
        self.file2 = file2
        self.buyers = []
        self.suppliers = []
        self.results = []
        self.match_obj = Match()

    def read_files(self):
        with open(self.file1, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                # print(row)
                self.buyers.append(Buyer(row['GSTIN'],
                                         row['Date'],
                                         row['Bill no'],
                                         row['GST rate(%)'],
                                         row['Taxable value'],
                                         row['IGST'],
                                         row['CGST'],
                                         row['SGST'],
                                         row['Total']))

        with open(self.file2, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                # print(row)
                self.suppliers.append(Supplier(row['GSTIN'],
                                               row['Date'],
                                               row['Bill no'],
                                               row['GST rate(%)'],
                                               row['Taxable value'],
                                               row['IGST'],
                                               row['CGST'],
                                               row['SGST'],
                                               row['Total']))

    def try_match(self):

        min_diff = sys.maxsize
        partitial_supp = None
        temp_buyers = copy.copy(self.buyers)

        for buyer in temp_buyers:
            buyer_added = False
            temp_supp = copy.copy(self.suppliers)

            for supp in temp_supp:
                diff, category = self.match_obj.find_difference(obj1=buyer, obj2=supp)
                # print(f"{diff}, buyer: {buyer.bill_no}, supp: {supp.bill_no}")
                if diff == 0 and category == 'EXACT':
                    min_diff = sys.maxsize
                    self.results.append([buyer, category, supp])
                    self.suppliers.remove(supp)
                    buyer_added = True
                    break
                elif diff < min_diff:
                    min_diff = diff
                    partitial_supp = supp

            if min_diff != sys.maxsize:
                min_diff = sys.maxsize
                self.results.append([buyer, "PARTIAL", partitial_supp])
                self.suppliers.remove(partitial_supp)
                buyer_added = True

            if buyer_added:
                self.buyers.remove(buyer)

        # add remaining
        for supp in self.suppliers:
            self.results.append([supp, "Only Suppliers"])

        # add remaining
        for buyer in self.buyers:
            self.results.append([buyer, "Only Buyers"])

    def print_result(self):

        for result in self.results:
            if isinstance(result[0], object):
                print(result[0].__dict__, end=" ")
            print(result[1], end=" ")
            if len(result) > 2:
                if isinstance(result[2], object):
                    print(result[2].__dict__, end=" ")
            print()


if __name__ == '__main__':
    result = []
    classify_obj = Classify(file1='/Users/mmalpani/Documents/personal/pythonProject/A4AProblem/data/Buyer.csv',
                            file2='/Users/mmalpani/Documents/personal/pythonProject/A4AProblem/data/Supplier.csv')
    classify_obj.read_files()
    classify_obj.try_match()
    classify_obj.print_result()
