class ShippingContainer(object):
    def __init__(self, carrier_company, container_num, arrival_date):
        self.po_num = 'None'
        self.company = 'None'
        self.item_contents = 'None'
        self.carrier_company = carrier_company
        self.container_num = container_num
        self.arrival_date = arrival_date
        self.date_cell_highlight = 'None'
        self.cell_location = 'None'
        self.cell_sheet_name = 'None'
    '''
    @po_num.setter
    def po_num(self, po_num):
        self.po_num = po_num

    @property
    def po_num(self):
        return self.po_num

    @company.setter
    def company(self, company):
        self.company = company

    @property
    def company(self):
        return self.company

    @item_contents.setter
    def item_contents(self, item_contents):
        self.item_contents = item_contents

    @property
    def item_contents(self):
        return self.item_contents

    @carrier_company.setter
    def carrier_company(self, carrier_company):
        self.carrier_company = carrier_company

    @property
    def carrier_company(self):
        return self.carrier_company

    @container_num.setter
    def container_num(self, container_num):
        self.container_num = container_num

    @property
    def container_num(self):
        return self.container_num

    @arrival_date.setter
    def arrival_date(self, arrival_date):
        self.arrival_date = arrival_date

    @property
    def arrival_date(self):
        return self.arrival_date

    @date_cell_highlight.setter
    def date_cell_highlight(self, date_cell_highlight):
        self.date_cell_highlight = date_cell_highlight

    @property
    def date_cell_highlight(self):
        return self.date_cell_highlight

    @cell_location.setter
    def cell_location(self, cell_location):
        self.cell_location = cell_location

    @property
    def cell_location(self):
        return self.cell_location

    @cell_sheet_name.setter
    def cell_sheet_name(self, cell_sheet_name):
        self.cell_sheet_name = cell_sheet_name

    @property
    def cell_sheet_name(self):
        return self.cell_sheet_name
    '''

