'''
Module that contains the ShippingContainer class
'''


class ShippingContainer():
    '''
    An object that is a shipping container and contains all pertinent properties

    Parameters
    ---------
    container_num : str
        A container num
    carrier_company : str
        A valid shipping company
    arrival_date : str
        A due to dock date
    wb_file_path : str or list
        A set of excel workbook filepaths that the container is on
    wb_sheet : str or list
        A set of excel sheets the container is on
    container_num_cell_location : str or list
        A str or list of container num cell addresses on each wb_sheet
    date_cell_location : str or list
        A str or list of arrival date cell addresses on each wb_sheet
    '''

    def __init__(self, container_num, carrier_company, arrival_date, wb_file_path, wb_sheet,
                 container_num_cell_location, date_cell_location):
        self._wb_file_path = wb_file_path
        self._wb_sheet = wb_sheet
        self._carrier_company = carrier_company
        self._container_num = container_num
        self._arrival_date = arrival_date
        self._container_num_cell_location = container_num_cell_location
        self._date_cell_location = date_cell_location


    @property
    def carrier_company(self):
        '''
        carrier_company getter
        '''
        return self._carrier_company

    @carrier_company.setter
    def carrier_company(self, new_carrier_company):
        '''
        carrier_company setter
        '''
        self._carrier_company = new_carrier_company

    @property
    def wb_file_path(self):
        '''
        wb_file_path getter
        '''
        return self._wb_file_path

    @wb_file_path.setter
    def wb_file_path(self, new_wb_file_path):
        '''
        wb_file_path setter
        '''
        self._wb_file_path = new_wb_file_path

    @property
    def container_num(self):
        '''
        container_num getter
        '''
        return self._container_num

    @container_num.setter
    def container_num(self, new_container_num):
        '''
        container_num setter
        '''
        self._container_num = new_container_num

    @property
    def arrival_date(self):
        '''
        arrival_date getter
        '''
        return self._arrival_date

    @arrival_date.setter
    def arrival_date(self, new_arrival_date):
        '''
        arrival_date setter
        '''
        self._arrival_date = new_arrival_date


    @property
    def container_num_cell_location(self):
        '''
        container_num_cell_location getter
        '''
        return self._container_num_cell_location

    @container_num_cell_location.setter
    def container_num_cell_location(self, new_container_num_cell_location):
        '''
        container_num_cell_location setter
        '''
        self._container_num_cell_location = new_container_num_cell_location

    @property
    def wb_sheet(self):
        '''
        wb_sheet getter
        '''
        return self._wb_sheet

    @wb_sheet.setter
    def wb_sheet(self, new_wb_sheet):
        '''
        wb_sheet setter
        '''
        self._wb_sheet = new_wb_sheet

    @property
    def date_cell_location(self):
        '''
        date_cell_location getter
        '''
        return self._date_cell_location

    @date_cell_location.setter
    def date_cell_location(self, new_date_cell_location):
        '''
        date_cell_location setter
        '''
        self._date_cell_location = new_date_cell_location

    def get_properties(self):
        '''
        Gets all container properties

        This method uses all the getters of the object to return a list
        of all of the properties of the object

        Parameters
        ---------
        None

        Returns
        -------
        list
            A list of all container object instance properties
        '''
        return [self.container_num, self.carrier_company, self.arrival_date, self.wb_file_path,
                self.wb_sheet, self.container_num_cell_location, self.date_cell_location]
