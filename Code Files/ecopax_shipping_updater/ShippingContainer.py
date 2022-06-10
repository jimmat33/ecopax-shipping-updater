class ShippingContainer(object):

    def __init__(self, container_num, carrier_company, arrival_date, wb_file_path, wb_sheet, container_num_cell_location, date_cell_location):
        self._wb_file_path = wb_file_path
        self._wb_sheet = wb_sheet
        self._carrier_company = carrier_company
        self._container_num = container_num
        self._arrival_date = arrival_date
        self._container_num_cell_location = container_num_cell_location
        self._date_cell_location = date_cell_location


    @property
    def carrier_company(self):
        return self._carrier_company
    
    @carrier_company.setter
    def carrier_company(self, new_carrier_company):
        self._carrier_company = new_carrier_company

    @property
    def wb_file_path(self):
        return self._wb_file_path
    
    @wb_file_path.setter
    def wb_file_path(self, new_wb_file_path):
        self._wb_file_path = new_wb_file_path
    

    @property
    def container_num(self):
        return self._container_num
    
    @container_num.setter
    def container_num(self, new_container_num):
        self._container_num = new_container_num
    

    @property
    def arrival_date(self):
        return self._arrival_date
    @arrival_date.setter
    def arrival_date(self, new_arrival_date):
        self._arrival_date = new_arrival_date


    @property
    def container_num_cell_location(self):
        return self._container_num_cell_location
    
    @container_num_cell_location.setter
    def container_num_cell_location(self, new_container_num_cell_location):
        self._container_num_cell_location = new_container_num_cell_location
    

    @property
    def wb_sheet(self):
        return self._wb_sheet
    
    @wb_sheet.setter
    def wb_sheet(self, new_wb_sheet):
        self._wb_sheet = new_wb_sheet
    

    @property
    def date_cell_location(self):
        return self._date_cell_location
    
    @date_cell_location.setter
    def date_cell_location(self, new_date_cell_location):
        self._date_cell_location = new_date_cell_location


    def get_properties(self):
        return [self.container_num, self.carrier_company, self.arrival_date, self.wb_file_path, self.wb_sheet, self.container_num_cell_location, self.date_cell_location]
    


