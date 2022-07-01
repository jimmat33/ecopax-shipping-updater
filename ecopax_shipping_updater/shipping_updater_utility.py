import time
import random
from shipping_container_db import db_get_cont_by_carrier
import numpy as np
from openpyxl.styles import PatternFill, Alignment 
from openpyxl import *


def random_sleep():
    sleep_time = random.uniform(0.25, 1.25)
    time.sleep(sleep_time)


def get_month_num(month):
    '''
    This function takes a month as a word and returns it as the respective number of the month for
    proper date formatting
    '''
    if month == 'January' or month == 'JAN' or month == 'Jan':
        return '01'
    elif month == 'February' or month == 'FEB' or month == 'Feb':
        return '02'
    elif month == 'March' or month == 'MAR' or month == 'Mar':
        return '03'
    elif month == 'April' or month == 'APR' or month == 'Apr':
        return '04'
    elif month == 'May' or month == 'MAY' or month == 'May':
        return '05'
    elif month == 'June' or month == 'JUN' or month == 'Jun':
        return '06'
    elif month == 'July' or month == 'JUL' or month == 'Jul':
        return '07'
    elif month == 'August' or month == 'AUG' or month == 'Aug':
        return '08'
    elif month == 'September' or month == 'SEP' or month == 'Sep':
        return '09'
    elif month == 'October' or month == 'OCT' or month == 'Oct':
        return '10'
    elif month == 'November' or month == 'NOV' or month == 'Nov':
        return '11'
    elif month == 'December' or month == 'DEC' or month == 'Dec':
        return '12'
    else:
        return 'ERROR'


def get_date_from_cma(given_str):
    '''
    This function is specifically used for CMA CGM, it takes the raw data from their website and
    returns a string that can be used to create the proper date for adding to the container's
    dictionary entry
    '''
    start_index = 0

    #This if block is checking for the days of the week and then using that as a basis for the starting index of the date
    if given_str.find("Sunday") != -1:
        start_index = given_str.find("Sunday") + len("Sunday") + 1
    elif given_str.find("Monday") != -1:
        start_index = given_str.find("Monday") + len("Monday") + 1
    elif given_str.find("Tuesday") != -1:
        start_index = given_str.find("Tuesday") + len("Tuesday") + 1 
    elif given_str.find("Wednesday") != -1:
        start_index = given_str.find("Wednesday") + len("Wednesday") + 1
    elif given_str.find("Thursday") != -1:
        start_index = given_str.find("Thursday") + len("Thursday") + 1
    elif given_str.find("Friday") != -1:
        start_index = given_str.find("Friday") + len("Friday") + 1
    elif given_str.find("Saturday") != -1:
        start_index = given_str.find("Saturday") + len("Saturday") + 1
    elif given_str.find("Sunday") != -1:
        start_index = given_str.find("Sunday") + len("Sunday") + 1
    else:
        return 'ERROR'

    actual_date = given_str[start_index:(start_index + 11)]

    return actual_date


def get_divided_containers_by_carrier(carrier_company):
    total_list = db_get_cont_by_carrier(carrier_company)
    ret_list = np.array_split(total_list, 3)

    return ret_list


def modify_sheets():
    green_fill = PatternFill(start_color='8FB547', end_color='8FB547', fill_type='solid')
    red_fill = PatternFill(start_color='FF7F7F', end_color='FF7F7F', fill_type='solid')
    yellow_fill = PatternFill(start_color='F1EB9C', end_color='F1EB9C', fill_type='solid')
    blue_fill = PatternFill(start_color='84C4E4', end_color='84C4E4', fill_type='solid')
    no_fill = PatternFill(fill_type=None)

    cont_list = db_get_all_containers()
    no_search_list = db_get_no_search_cont()
    excel_file_list = db_get_all_excel_files()
    unmod_cont_list= db_get_all_unmod_containers()


    for xcel_sheet in excel_file_list:

        workbook = load_workbook(filename=xcel_sheet[0])
        sheet = workbook[xcel_sheet[1]]
        if type(cont_list) == list:
            
            for cont in cont_list:

                if sheet.title in cont.wb_sheet:
                    cont_sheet_index = cont.wb_sheet.index(sheet.title)
                    date_cell_loc = cont.date_cell_location[cont_sheet_index]

                    if cont.arrival_date == 'arrived':
                        sheet[date_cell_loc] = 'arrived'
                        sheet[date_cell_loc].fill = green_fill
                        sheet[date_cell_loc].alignment = Alignment(horizontal='right')
                    elif cont.arrival_date == 'Date Error':
                        sheet[date_cell_loc] = 'Date Error'
                        sheet[date_cell_loc].fill = yellow_fill
                        sheet[date_cell_loc].alignment = Alignment(horizontal='right')
                    else:
                        sheet[date_cell_loc] = cont.arrival_date
                        sheet[date_cell_loc].fill = blue_fill
                        sheet[date_cell_loc].alignment = Alignment(horizontal='right')


            for ns_cont in no_search_list:
                if sheet.title in ns_cont.wb_sheet:
                    cont_sheet_index = ns_cont.wb_sheet.index(sheet.title)
                    cont_num_cell_loc = ns_cont.container_num_cell_location[cont_sheet_index]
                    sheet[cont_num_cell_loc].fill = red_fill


            for cont in unmod_cont_list:

                if sheet.title in cont.wb_sheet:
                    cont_sheet_index = cont.wb_sheet.index(sheet.title)
                    date_cell_loc = cont.date_cell_location[cont_sheet_index]

                    if cont.arrival_date != 'arrived':
                        sheet[date_cell_loc].fill = no_fill

        workbook.save(xcel_sheet[0])





