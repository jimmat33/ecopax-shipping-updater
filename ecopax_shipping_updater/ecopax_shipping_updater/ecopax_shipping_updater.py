from asyncio.windows_events import NULL
from calendar import c
from datetime import datetime
from http.server import executable
from pickle import NONE
import tarfile
from typing import Container
import numpy
import sys
import pprint
import time
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strptime
from datetime import datetime, date
from openpyxl import load_workbook
import xlwt
import xlrd
from xlutils.copy import copy

chrome_options = Options()
chrome_options.headless = True
modified_custom_cells_list = list()
modified_rest_cells_list = list()

def get_month_num(month):
    if month == 'January' or month == 'JAN':
        return '01'
    elif month == 'February' or month == 'FEB':
        return '02'
    elif month == 'March' or month == 'MAR':
        return '03'
    elif month == 'April' or month == 'APR':
        return '04'
    elif month == 'May' or month == 'MAY':
        return '05'
    elif month == 'June' or month == 'JUN':
        return '06'
    elif month == 'July' or month == 'JUL':
        return '07'
    elif month == 'August' or month == 'AUG':
        return '08'
    elif month == 'September' or month == 'SEP':
        return '09'
    elif month == 'October' or month == 'OCT':
        return '10'
    elif month == 'November' or month == 'NOV':
        return '11'
    else:
        return '12'

def replace_values(date_dict,sheet_name, df):
    dict_keys = [*date_dict]
    #workbook = load_workbook(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')
    sheet = sheet_name


    for key in dict_keys:
        container_num = key
        container_arrival_date = date_dict[key]

        formatted_date = container_arrival_date[2] + '-' + container_arrival_date[0] + '-' + container_arrival_date[1]
        index_list = df[df == container_num].stack().index.tolist()

        if sheet_name == 'custom':
            old_date = str(df.iat[index_list[0][0], 6])

            old_formatted_date = old_date[0:10]

            if old_date == 'arrived':
                print('already arrived')
            elif old_formatted_date == formatted_date:
                sheet_index = 'G' + str(index_list[0][0])
                sheet[sheet_index] = 'arrived'
                
                modified_custom_cells_list.append(container_num)
            else:
                sheet_index = 'G' + str(index_list[0][0])
                sheet[sheet_index] = datetime(int(container_arrival_date[2]), int(container_arrival_date[0]), int(container_arrival_date[1]), 0 ,0)

                modified_custom_cells_list.append(container_num)
        else:
            old_date = str(df.iat[index_list[0][0], 7])
            old_formatted_date = old_date[0:10]

            if old_date == 'arrived':
                print('already arrived')
            elif old_formatted_date == formatted_date:
                sheet_index = 'H' + str(index_list[0][0])
                sheet[sheet_index] = 'arrived'

                modified_rest_cells_list.append(container_num)
            else:
                sheet_index = 'G' + str(index_list[0][0])
                sheet[sheet_index] = datetime(int(container_arrival_date[2]), int(container_arrival_date[0]), int(container_arrival_date[1]), 0 ,0)

                modified_rest_cells_list.append(container_num)


        #workbook.save(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')

def cosco_search(container_num_list):
    '''
    This function searches the cosco site for the estimated arrival date of a crate
    '''
    return_dict = dict()

    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    cosco_link = 'https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=CONTAINER&number='

    if len(container_num_list)!= 0:
        cosco_link = cosco_link + container_num_list[0]
    else:
        return

    driver.implicitly_wait(0.5)
    driver.get(cosco_link)

    #clicking past the TOS popup
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button').click()

    #finding estimated arrival date in website table
    web_date = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]/p[2]')

    #waiting to get date from page and pulling data
    time.sleep(0.5) 
    str_date = web_date.get_attribute('textContent')

    #formatting date properly
    year = str_date[0:4]
    month = str_date[5:7]
    day = str_date[8:10]

    return_dict[container_num_list[0]] = [month, day, year]

    i = 1

    while i < len(container_num_list):
        textbox = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[1]/div/div[2]/form/div/div[1]/div/div/div/input')
        textbox.clear()

        textbox.send_keys(container_num_list[i])
        driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[1]/div/div[2]/form/div/div[2]/button').click()
        time.sleep(1)

        str_date = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]/p[2]'))).get_attribute('textContent')

        #formatting date properly
        year = str_date[0:4]
        month = str_date[5:7]
        day = str_date[8:10]

        return_dict[container_num_list[i]] = [month, day, year]

        i += 1


    driver.close()
    return return_dict

def main():
    #Setting up all the lists for each 
    custom_cosco_list = list()
    rest_cosco_list = list()
    custom_unadded_containers_list = list()
    rest_unadded_containers_list = list()
    

    #getting data to pull from for both sheets
    customsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'custom')
    restsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'Rest')

    for index,row in customsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            custom_cosco_list.append(row['Container Number'])
    for index, row in restsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            rest_cosco_list.append(row['Container Number'])

    cosco_custom_dates_dict = cosco_search(custom_cosco_list)
    cosco_rest_dates_dict = cosco_search(rest_cosco_list)
    replace_values(cosco_custom_dates_dict, customsheet_data, 'custom')

if __name__ == '__main__': 
    main()