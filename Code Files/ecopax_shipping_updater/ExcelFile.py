from pyexpat import native_encoding
import re
import shutil
import string
from datetime import datetime
import openpyxl
import pandas as pd
from ShippingContainerDB import db_add_excel_file, db_get_excel_file_info, db_add_container
from ShippingContainer import *
import os

class ExcelFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.sheet_names = self.get_sheet_names()
        self.container_num_pattern = re.compile("[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]+(?s).*$")
        self.accepted_container_carriers = ['Cosco', 'ONE', 'Hapag-Lloyd', 'Maersk', 'CMA CGM', 'Evergreen', 'HMM']
        self.get_wb_columns = self.validate_column_types()
        self.save_file_copy()


    def save_file_copy(self):
        copy_fp = os.path.abspath('Excel File Cache')
        fp_list = self.file_path.split('\\')

        orig_filename = fp_list[-1].split('.')[0]
        new_fn = str(orig_filename) + '-copy-' + datetime.now().strftime('%m-%d-%y-%H-%M-%S') + '.xlsx'
        
        fp_list[-1] = new_fn
        
        old_filepath_str = ''

        for part in fp_list:
            if part == fp_list[0]:
                old_filepath_str = old_filepath_str + part
            else:
                old_filepath_str = old_filepath_str + '\\' + part


        shutil.copy(self.file_path, old_filepath_str)

        shutil.move(old_filepath_str, copy_fp)



    def parse_carrier(self, carrier_str): #add all possible entries here

        if not isinstance(carrier_str, str):
            return 'ERROR'
        
        check_str = carrier_str.lower().strip()

        if check_str.find('cosco') != -1:
            return 'Cosco'
        elif check_str.find('one') != -1:
            return 'ONE'
        elif check_str.find('h') != -1 and check_str.find('p') != -1 and check_str.find('l') != -1:
            return 'Hapag-Lloyd'
        elif check_str.find('m') != -1 and check_str.find('s') != -1 and check_str.find('k') != -1:
            return 'Maersk'
        elif check_str.find('cma') != -1:
            return 'CMA CGM'
        elif check_str.find('e') != -1 and check_str.find('v') != -1 and check_str.find('g') != -1:
            return 'Evergreen'
        elif check_str.find('hmm') != -1:
            return 'HMM'
        elif check_str.find('emc') != -1:
            return 'Valid, No Search'
        elif check_str.find('zim') != -1:
            return 'Valid, No Search'
        elif check_str.find('whl') != -1:
            return 'Valid, No Search'
        elif check_str.find('sml') != -1:
            return 'Valid, No Search'
        elif check_str.find('pil') != -1:
            return 'Valid, No Search'
        elif check_str.find('apl') != -1:
            return 'Valid, No Search'
        elif check_str.find('msc') != -1:
            return 'Valid, No Search'
        elif check_str.find('y') != -1 and check_str.find('n') != -1 and check_str.find('g') != -1:
            return 'Valid, No Search'
        elif check_str.find('oocl') != -1:
            return 'Valid, No Search'
        elif check_str.find('hsd') != -1:
            return 'Valid, No Search'
        elif check_str.find('sm') != -1:
            return 'Valid, No Search'
        else:
            return 'ERROR'


    def get_sheet_names(self):
        xls = openpyxl.load_workbook(self.file_path)
        sheets_list = xls.sheetnames

        return sheets_list

    def get_date_column_list(self, column_type_dict, search_len):
        column_check_percent_list = []
        dict_keys = [*column_type_dict]

        for key in dict_keys:
            percentage_check = ((column_type_dict[key].count('Date')) / search_len) * 100
            column_check_percent_list.append(percentage_check)

        return column_check_percent_list


    def get_container_num_column(self, column_type_dict, search_len):
        column_check_percent_list = []
        dict_keys = [*column_type_dict]

        for key in dict_keys:
            percentage_check = ((column_type_dict[key].count('Container Num')) / search_len) * 100
            column_check_percent_list.append(percentage_check)

        max_percent = max(column_check_percent_list)

        return [(column_check_percent_list.index(max_percent) + 1), max_percent]


    def get_carrier_column(self, column_type_dict, search_len):
        column_check_percent_list = []
        dict_keys = [*column_type_dict]

        for key in dict_keys:
            percentage_check = ((column_type_dict[key].count('Carrier')) / search_len) * 100
            column_check_percent_list.append(percentage_check)

        max_percent = max(column_check_percent_list)

        return column_check_percent_list.index(max_percent) + 1

    
    def validate_column_types(self):
        for sheet_name in self.sheet_names:

            column_type_dict = dict()
            sheet_data = pd.read_excel(self.file_path, sheet_name = sheet_name)
            sheet_data.astype('str')

            for val in range(len(sheet_data.columns)):
                column_type_dict[val] = []

            search_len = 0
            i = 0

            if len(sheet_data.index) < 200:
                search_len = len(sheet_data.index)
            else:
                search_len = 200

            for i in range(search_len):
                check_row = sheet_data.iloc[i]
                if isinstance(check_row, int) == False and isinstance(check_row, float) == False:
                    values_list = check_row.values
                    j = 0

                    while j < len(values_list):
                        if isinstance(values_list[j], str) or isinstance(values_list[j], datetime):
                            try:
                                if values_list[j] == 'arrived' or values_list[j] == 'Date Error' or isinstance(values_list[j], datetime) or bool(datetime.strptime(values_list[j], '%m/%d/%Y')):
                                    column_type_dict[j].append('Date')
                            except Exception:
                                pass

                            if isinstance(values_list[j], datetime) == False:
                                if self.container_num_pattern.match(values_list[j]):
                                    column_type_dict[j].append('Container Num')
                                elif self.parse_carrier(values_list[j]) != 'ERROR':
                                    
                                    if self.parse_carrier(values_list[j]) in self.accepted_container_carriers:
                                        [column_type_dict[j].append('Carrier') for k in range(2)]

                                    column_type_dict[j].append('Carrier')

                        j += 1

            date_column_list = self.get_date_column_list(column_type_dict, search_len)
            container_num_column = self.get_container_num_column(column_type_dict, search_len)
            carrier_column = self.get_carrier_column(column_type_dict, search_len)

            sorted_date_list = sorted(date_column_list)

            if max(date_column_list) > container_num_column[1] and sorted_date_list[-2] != 0:
                date_column = date_column_list.index(sorted_date_list[-2]) + 1
            else:
                date_column = date_column_list.index(sorted_date_list[-1]) + 1 

            excel_db_properties = [self.file_path, sheet_name, date_column, container_num_column[0], carrier_column]

            db_add_excel_file(excel_db_properties)


    def parse_workbook(self):
        i = 0

        while i < len(self.sheet_names):

            sheet_data = pd.read_excel(self.file_path, sheet_name = self.sheet_names[i])

            excel_data_list = db_get_excel_file_info(self.file_path, self.sheet_names[i])
            excel_data = excel_data_list[0]

            date_column = int(excel_data[0])
            carrier_column = int(excel_data[2])
            container_num_column = int(excel_data[1])

            j = 0

            while j < len(sheet_data.index):
                row = sheet_data.iloc[j].values
                if isinstance(row[container_num_column - 1], str) and self.container_num_pattern.match(row[container_num_column - 1]):
                    
                    obj_container_num = row[container_num_column - 1]
                    if len(obj_container_num) > 11:
                        obj_container_num = obj_container_num[0:11]

                    obj_carrier_company = self.parse_carrier(row[carrier_column - 1])

                    if isinstance(row[date_column - 1], datetime) and str(row[date_column - 1]) != 'NaT': 
                        obj_arrival_date = row[date_column - 1].strftime('%m/%d/%Y')
                    else:
                        obj_arrival_date = str(row[date_column - 1])

                    obj_container_num_column = string.ascii_uppercase[container_num_column - 1]
                    obj_arrival_date_column = string.ascii_uppercase[date_column - 1]
                    obj_container_num_location = obj_container_num_column + str(j + 2)
                    obj_arrival_date_location = obj_arrival_date_column + str(j + 2)

                    if obj_carrier_company in self.accepted_container_carriers:
                        new_shipping_cont = ShippingContainer(obj_container_num, obj_carrier_company, obj_arrival_date, self.file_path, self.sheet_names[i], obj_container_num_location, obj_arrival_date_location)
                        db_add_container(new_shipping_cont, 'reg')
                    else:
                        no_search_cont = [obj_container_num, self.file_path, self.sheet_names[i], obj_container_num_location]
                        db_add_container(no_search_cont, 'no-search')

                j += 1
        
            i += 1


    def replace_values():
        pass
        '''
        #gets all containers for the sheet
        dict_keys = [*date_dict]

        #opening workbook and setting up modifications
        #workbook = load_workbook(filename=r'')
        sheet = workbook.get_sheet_by_name(sheet_name)
        greenFill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
        redFill = PatternFill(start_color='FF7F7F', end_color='FF7F7F', fill_type='solid')
        yellowFill = PatternFill(start_color='F1EB9C', end_color='F1EB9C', fill_type='solid')

        for key in dict_keys:
            #mapping proper fields
            container_num = key
            container_arrival_date = date_dict[key]

            #getting both the dates to use for formatting
            formatted_date = container_arrival_date[2] + '-' + container_arrival_date[0] + '-' + container_arrival_date[1]
            excel_date = container_arrival_date[0] + '/' + container_arrival_date[1] + '/' + container_arrival_date[2]

            #getting index of cell
            index_list = df[df == container_num].stack().index.tolist()

            #validating dates and highlighting all searches that returned invalid dates yellow
            try:
                is_valid_date = bool(parser.parse(formatted_date))
            except Exception:
                is_valid_date = False

            if is_valid_date == False:
                if sheet_name == 'custom':
                    sheet_index = 'G' + str(index_list[0][0] + 2)
                    sheet[sheet_index] = 'Date Error'
                    sheet[sheet_index].fill = yellowFill
                    sheet[sheet_index].alignment = Alignment(horizontal='right')

                    modified_custom_cells_list.append(container_num)
                else:
                    sheet_index = 'H' + str(index_list[0][0] + 2)
                    sheet[sheet_index] = 'Date Error'
                    sheet[sheet_index].fill = yellowFill
                    sheet[sheet_index].alignment = Alignment(horizontal='right')

                    modified_rest_cells_list.append(container_num)
            else:

                #custom sheet modifications
                if sheet_name == 'custom':

                    #getting prexisiting date in sheet
                    old_date = str(df.iat[index_list[0][0], 6])
                    old_formatted_date = old_date[0:10]

                    new_date_datetime = datetime.strptime(formatted_date, "%Y-%m-%d")
                    today_date = datetime.today()

                    if old_date == 'arrived':
                        print('already arrived')

                    #if date pulled has already passed
                    elif old_formatted_date == formatted_date or new_date_datetime < today_date:
                        #getting location of cell in sheet and making it say arrived and highlighted green
                        sheet_index = 'G' + str(index_list[0][0] + 2)
                        sheet[sheet_index] = 'arrived'
                        sheet[sheet_index].fill = greenFill
                        sheet[sheet_index].alignment = Alignment(horizontal='right')
                
                        modified_custom_cells_list.append(container_num)
                    else:
                        #getting location of cell in sheet and changing the arrival date
                        sheet_index = 'G' + str(index_list[0][0] + 2)
                        sheet[sheet_index] = excel_date
                        sheet[sheet_index].alignment = Alignment(horizontal='right')

                        modified_custom_cells_list.append(container_num)
                else:
                    #getting pre-exisiting date in sheet
                    old_date = str(df.iat[index_list[0][0], 7])
                    old_formatted_date = old_date[0:10]

                    if old_date == 'arrived':
                        print('already arrived')

                     #if date pulled has already passed
                    elif old_formatted_date == formatted_date:
                         #getting location of cell in sheet and making it say arrived and highlighted green
                        sheet_index = 'H' + str(index_list[0][0] + 2)
                        sheet[sheet_index] = 'arrived'
                        sheet[sheet_index].fill = greenFill
                        sheet[sheet_index].alignment = Alignment(horizontal='right')

                        modified_rest_cells_list.append(container_num)
                    else:
                        #getting location of cell in sheet and changing the arrival date
                        sheet_index = 'H' + str(index_list[0][0] + 2)
                        sheet[sheet_index] = excel_date
                        sheet[sheet_index].alignment = Alignment(horizontal='right')

                        modified_rest_cells_list.append(container_num)

       
        for index,row in df.iterrows():
            if row['Container Number'] not in modified_custom_cells_list and row['Container Number'] not in modified_rest_cells_list:
                container_num = row['Container Number']
                index_list = df[df == container_num].stack().index.tolist()
            
                try:
                    if sheet_name == 'custom':
                        sheet_index = 'G' + str(index_list[0][0] + 2)
                    else:
                        sheet_index = 'H' + str(index_list[0][0] + 2)
            
                    sheet[sheet_index].fill = redFill
                except:
                    #do nothing, value is empty
                    container_num = 0


            #workbook.save(filename='')
        '''

