class Buyer:

    def __init__(self, gstin, date, bill_no, gst_rate, taxable_value, igst, cgst, sgst, total):
        self.gstin = gstin
        self.date = date
        self.bill_no = bill_no
        self.gst_rate = gst_rate
        self.taxable_value = taxable_value
        self.igst = igst
        self.cgst = cgst
        self.sgst = sgst
        self.total = total