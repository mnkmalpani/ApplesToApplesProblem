from typing import Tuple
from src.pojo.buyer import Buyer
from src.pojo.supplier import Supplier
import difflib
import sys
import datetime
"""
Chain of responsiblity
"""

class Match:

    def __init__(self):
        self.diff = 0
        self.partial_match = True

    def compare_alfa_numeric(self, alfa1, alfa2) -> int:
        diff = 0
        if len(alfa1) == 0 or len(alfa2) == 0:
            return 1
        for i, s in enumerate(difflib.ndiff(alfa1.lower(), alfa2.lower())):
            if s[0] == ' ':
                continue
            elif s[0] == '-':
                diff = diff + 1
            elif s[0] == '+':
                diff = diff + 1

        return diff

    def clean_date(self, date: str):
        if '-' in date:
            return date
        elif '/' in date:
            d = datetime.datetime.strptime(date, "%d/%m/%y")
            return datetime.date.strftime(d, '%d-%m-%Y')

    def clean_int(self, int_str: str) -> int:
        _int_str = int_str.replace(',', '')
        return int(float(_int_str))

    def find_difference(self, obj1: Buyer, obj2: Supplier) -> Tuple[int, str]:
        # TODO can be done with a same funtion
        self.diff = 0
        self.diff, self.partial_match = self.compare_bill_num(obj1.bill_no, obj2.bill_no, self.diff)
        if self.partial_match is False:
            return sys.maxsize, "No Match"
        self.diff, self.partial_match = self.compare_gsdin(obj1.gstin, obj2.gstin, self.diff)
        if self.partial_match is False:
            return sys.maxsize, "No Match"
        self.diff, self.partial_match = self.compare_date(obj1.date, obj2.date, self.diff)
        if self.partial_match is False:
            return self.diff, "No Match"

        self.diff = self.compare_ints(obj1.gst_rate, obj2.gst_rate, self.diff)
        self.diff = self.compare_ints(obj1.taxable_value, obj2.taxable_value, self.diff)
        self.diff = self.compare_ints(obj1.igst, obj2.igst, self.diff)
        self.diff = self.compare_ints(obj1.cgst, obj2.cgst, self.diff)
        self.diff = self.compare_ints(obj1.sgst, obj2.sgst, self.diff)
        self.diff = self.compare_ints(obj1.total, obj2.total, self.diff)

        if self.diff == 0:
            return self.diff, "EXACT"

        return self.diff, "PARTIAL"

    def compare_bill_num(self, bill_no1, bill_no2, diff):
        change = self.compare_alfa_numeric(bill_no1, bill_no2)
        if change > 2:
            return diff + change, False

        return diff + change, True

    def compare_gsdin(self, gstin1, gstin2, diff):
        change = self.compare_alfa_numeric(gstin1, gstin2)
        if change > 2:
            return diff + change, False

        return diff + change, True

    def compare_date(self, date1, date2, diff):
        if len(date1) == 0 and len(date2) == 0:
            return diff
        elif len(date1) == 0 or len(date2) == 0:
            return diff + 1
        mdate = self.clean_date(date1)
        rdate = self.clean_date(date2)
        mdate1 = datetime.datetime.strptime(mdate, "%d-%m-%Y").date()
        rdate1 = datetime.datetime.strptime(rdate, "%d-%m-%Y").date()
        delta = (mdate1 - rdate1).days

        if delta > 7:
            return diff + delta, False

        return diff + delta, True

    def compare_ints(self, int1: str, int2: str, diff) -> int:
        if len(int1) == 0 and len(int2) == 0:
            return diff
        elif len(int1) == 0 or len(int2) == 0:
            return diff + 1

        _int1 = self.clean_int(int1)
        _int2 = self.clean_int(int2)

        return diff + abs(_int1 - _int2)
