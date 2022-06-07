from datetime import datetime
import random
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from os import listdir
from os.path import isfile, join
from openpyxl.styles import PatternFill, Alignment 
from openpyxl import load_workbook
from dateutil import parser
from ShippingContainer import *
from Cosco import CoscoSearch
from ONE import ONESearch
from HapagLloyd import HapagSearch
from Maersk import MaerskSearch
from CMA import CMASearch
from Evergreen import EvergreenSearch
from HMM import HMMSearch

#Global lists of all modified cells in each sheet
modified_custom_cells_list = list()
modified_rest_cells_list = list()
    
def replace_values(date_dict,df, sheet_name):
    #gets all containers for the sheet
    dict_keys = [*date_dict]

    #opening workbook and setting up modifications
    workbook = load_workbook(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')
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


        workbook.save(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')


def main():
    #prompt to update uc chrome and regular chrome if needed, maybe do manually?

    cont = ShippingContainer('1','1','1')
    cont.container_num = '2'

    #Setting up all the lists for each 
    custom_cosco_list = list()
    rest_cosco_list = list()

    custom_one_list = list()
    rest_one_list = list()

    custom_hapag_list = list()
    rest_hapag_list = list()

    custom_maersk_list = list()
    rest_maersk_list = list()

    custom_cma_list = list()
    rest_cma_list = list()
    
    custom_evergreen_list = list()
    rest_evergreen_list = list()

    custom_hmm_list = list()
    rest_hmm_list = list()

    #getting data to pull from for both sheets
    customsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'custom')
    restsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'Rest')

    #populating lists for the custom sheet
    for index,row in customsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            custom_cosco_list.append(row['Container Number'])
        elif row['Carrier'] == 'ONE':
            custom_one_list.append(row['Container Number'])
        elif row['Carrier'] == 'Hapag-Lloyd':
            custom_hapag_list.append(row['Container Number'])
        elif row['Carrier'] == 'Maersk':
            custom_maersk_list.append(row['Container Number'])
        elif row['Carrier'] == 'CMA CGM':
            custom_cma_list.append(row['Container Number'])
        elif row['Carrier'] == 'Evergreen':
            custom_evergreen_list.append(row['Container Number'])
        elif row['Carrier'] == 'HMM':
            custom_hmm_list.append(row['Container Number'])

    print('\n[Driver Alert] Custom sheet processed\n')

    #populating lists for the rest sheet
    for index, row in restsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            rest_cosco_list.append(row['Container Number'])
        elif row['Carrier'] == 'ONE':
            rest_one_list.append(row['Container Number'])
        elif row['Carrier'] == 'Hapag-Lloyd':
            rest_hapag_list.append(row['Container Number'])
        elif row['Carrier'] == 'Maersk':
            rest_maersk_list.append(row['Container Number'])
        elif row['Carrier'] == 'CMA CGM':
            rest_cma_list.append(row['Container Number'])
        elif row['Carrier'] == 'Evergreen':
            rest_evergreen_list.append(row['Container Number'])
        elif row['Carrier'] == 'HMM':
            rest_hmm_list.append(row['Container Number'])

    print('\n[Driver Alert] Rest sheet processed\n')
        
    #dictionary creation to hold all dates pulled for custom sheet containers
    cosco_custom_dates_dict = {}
    one_custom_dates_dict = {}
    hapag_custom_dates_dict = {}
    maersk_custom_dates_dict = {}
    cma_custom_dates_dict = {}  
    evergreen_custom_dates_dict = {}  
    hmm_custom_dates_dict = {}

    #dictionary creation to hold all dates pulled for rest sheet containers
    cosco_rest_dates_dict = {}
    one_rest_dates_dict = {}
    hapag_rest_dates_dict = {}
    maersk_rest_dates_dict = {}
    cma_rest_dates_dict = {}
    evergreen_rest_dates_dict = {} 
    hmm_rest_dates_dict = {}

    #---------------------------------------- All searches for each website----------------------------------------
    
    cosco = CoscoSearch(custom_cosco_list)
    
    #Searching for all cosco containers from the custom sheet
    if len(custom_cosco_list) != 0:
        cosco_custom_dates_dict = cosco.search(custom_cosco_list)
        if len(cosco_custom_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Cosco Search Again (Custom Sheet)\n')
                cosco_custom_dates_dict = cosco.search(custom_cosco_list)
                if len(cosco_custom_dates_dict) != 0:
                    break
        if len(cosco_custom_dates_dict) == 0:
            print('\n[Driver Alert] Cosco Search Fatal Error (Custom Sheet)\n')
            #highlight all cosco custom sheet items red

    cosco = CoscoSearch(rest_cosco_list)

    #Searching for all cosco containers from the rest sheet
    if len(rest_cosco_list) != 0:
        cosco_rest_dates_dict = cosco.search(rest_cosco_list)
        if len(cosco_rest_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Costco Search Again (Rest Sheet)\n')
                cosco_rest_dates_dict = cosco.search(rest_cosco_list)
                if len(cosco_rest_dates_dict) != 0:
                    break
        if len(cosco_rest_dates_dict) == 0:
            print('\n[Driver Alert] Cosco Search Fatal Error (Rest Sheet)\n')
            #highlight all cosco rest sheet items red

    one = ONESearch(custom_one_list)

    #Searching for all ONE containers from the custom sheet
    if len(custom_one_list) != 0:
        one_custom_dates_dict = one.search(custom_one_list)
        if len(one_custom_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying ONE Search Again (Custom Sheet)\n')
                one_custom_dates_dict = one.search(custom_one_list)
                if len(one_custom_dates_dict) != 0:
                    break
        if len(one_custom_dates_dict) == 0:
            print('\n[Driver Alert] ONE Search Fatal Error (Custom Sheet)\n')
            #highlight all ONE custom sheet items red

    one = ONESearch(rest_one_list)

    #Searching for all ONE containers from the rest sheet
    if len(rest_one_list) != 0:
        one_rest_dates_dict = one.search(rest_one_list)
        if len(one_rest_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying ONE Search Again (rest Sheet)\n')
                one_rest_dates_dict = one.search(rest_one_list)
                if len(one_rest_dates_dict) != 0:
                    break
        if len(one_rest_dates_dict) == 0:
            print('\n[Driver Alert] ONE Search Fatal Error (rest Sheet)\n')
            #highlight all ONE rest sheet items red
    
    #Searching for all Maersk containers from the Custom sheet
    if len(custom_maersk_list) != 0:
        for container_num in custom_maersk_list:

            maersk = MaerskSearch(container_num)

            maersk_custom_dates_dict[container_num] = maersk.search(container_num)
        if len(custom_maersk_list) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Maersk Search Again (Custom Sheet)\n')
                for container_num in custom_maersk_list:
                    maersk_custom_dates_dict[container_num] = maersk.search(container_num)
                if len(maersk_rest_dates_dict) != 0:
                    break
        if len(maersk_custom_dates_dict) == 0:
            print('\n[Driver Alert] Maersk Search Fatal Error (Custom Sheet)\n')
            #highlight all maersk Custom sheet items red


    #Searching for all Maersk containers from the rest sheet
    if len(rest_maersk_list) != 0:
        for container_num in rest_maersk_list:

            maersk = MaerskSearch(container_num)

            maersk_rest_dates_dict[container_num] = maersk.search(container_num)
        if len(rest_maersk_list) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Maersk Search Again (Rest Sheet)\n')
                for container_num in rest_maersk_list:
                    maersk_rest_dates_dict[container_num] = maersk.search(container_num)
                if len(maersk_rest_dates_dict) != 0:
                    break
        if len(maersk_rest_dates_dict) == 0:
            print('\n[Driver Alert] Maersk Search Fatal Error (Rest Sheet)\n')
            #highlight all maersk rest sheet items red
    
    #Searching for all Evergreen containers from the custom sheet

    evergreen = EvergreenSearch(custom_evergreen_list)

    if len(custom_evergreen_list) != 0:
        evergreen_custom_dates_dict = evergreen.search(custom_evergreen_list)
        if len(evergreen_custom_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Evergreen Search Again (Custom Sheet)\n')
                evergreen_custom_dates_dict = evergreen.search(custom_evergreen_list)
                if len(evergreen_custom_dates_dict) != 0:
                    break
        if len(evergreen_custom_dates_dict) == 0:
            print('\n[Driver Alert] Evergreen Search Fatal Error (Custom Sheet)\n')
            #highlight all evergreen custom sheet items red

    evergreen = EvergreenSearch(rest_evergreen_list)

    #Searching for all Evergreen containers from the rest sheet
    if len(rest_evergreen_list) != 0:
        evergreen_rest_dates_dict = evergreen.search(rest_evergreen_list)
        if len(evergreen_rest_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Evergreen Search Again (Rest Sheet)\n')
                evergreen_rest_dates_dict = evergreen.search(rest_evergreen_list)
                if len(evergreen_rest_dates_dict) != 0:
                    break
        if len(evergreen_rest_dates_dict) == 0:
            print('\n[Driver Alert] Evergreen Search Fatal Error (Rest Sheet)\n')
            #highlight all evergreen rest sheet items red

    
    #Searching for all HMM containers from the Custom sheet
    if len(custom_hmm_list) != 0:
        for container_num in custom_hmm_list:

            hmm = HMMSearch(container_num)

            hmm_custom_dates_dict[container_num] = hmm.search(container_num)
        if len(custom_hmm_list) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying HMM Search Again (Custom Sheet)\n')
                for container_num in custom_hmm_list:
                    hmm_custom_dates_dict[container_num] = hmm.search(container_num)
                if len(hmm_rest_dates_dict) != 0:
                    break
        if len(hmm_custom_dates_dict) == 0:
            print('\n[Driver Alert] hmm Search Fatal Error (Custom Sheet)\n')
            #highlight all hmm Custom sheet items red
    
    #Searching for all HMM containers from the rest sheet
    if len(rest_hmm_list) != 0:
        for container_num in rest_hmm_list:

            hmm = HMMSearch(container_num)

            hmm_rest_dates_dict[container_num] = hmm.search(container_num)
        if len(rest_hmm_list) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying HMM Search Again (Rest Sheet)\n')
                for container_num in rest_hmm_list:
                    hmm_rest_dates_dict[container_num] = hmm.search(container_num)
                if len(hmm_rest_dates_dict) != 0:
                    break
        if len(hmm_rest_dates_dict) == 0:
            print('\n[Driver Alert] hmm Search Fatal Error (Rest Sheet)\n')
            #highlight all hmm rest sheet items red
    '''
    cma = CMASearch(custom_cma_list)

    #Searching for all CMA CGM containers from the Custom sheet
    if len(custom_cma_list) != 0:
        cma_custom_dates_dict = cma.search(custom_cma_list)
        if len(cma_custom_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying CMA CGM Search Again (Custom Sheet)\n')
                cma_custom_dates_dict = cma.search(custom_cma_list)
                if len(cma_custom_dates_dict) != 0:
                    break
        if len(cma_custom_dates_dict) == 0:
            print('\n[Driver Alert] CMA CGM Search Fatal Error (Custom Sheet)\n')
            #highlight all cma Custom sheet items red

    cma = CMASearch(rest_cma_list)

    #Searching for all CMA CGM containers from the rest sheet
    if len(rest_cma_list) != 0:
        cma_rest_dates_dict = cma.search(rest_cma_list)
        if len(cma_rest_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying CMA CGM Search Again (Rest Sheet)\n')
                cma_rest_dates_dict = cma.search(rest_cma_list)
                if len(cma_rest_dates_dict) != 0:
                    break
        if len(cma_rest_dates_dict) == 0:
            print('\n[Driver Alert] CMA CGM Search Fatal Error (Rest Sheet)\n')
            #highlight all cma rest sheet items red
   
    '''
    hapag = HapagSearch(custom_hapag_list)

    #Searching for all Hapag-Loyd containers from the custom sheet
    if len(custom_hapag_list) != 0:
        hapag_custom_dates_dict = hapag.search(custom_hapag_list)
        if len(hapag_custom_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Hapag-Loyd Search Again (Custom Sheet)\n')
                hapag_custom_dates_dict = hapag.search(custom_hapag_list)
                if len(hapag_custom_dates_dict) != 0:
                    break
        if len(hapag_custom_dates_dict) == 0:
            print('\n[Driver Alert] Hapag-Loyd Search Fatal Error (Custom Sheet)\n')
            #highlight all hapag custom sheet items red
    
    hapag = HapagSearch(rest_hapag_list)

    #Searching for all Hapag-Loyd containers from the rest sheet
    if len(rest_hapag_list) != 0:
        hapag_rest_dates_dict = hapag.search(rest_hapag_list)
        if len(hapag_rest_dates_dict) == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Hapag-Loyd Search Again (Rest Sheet)\n')
                hapag_rest_dates_dict = hapag.search(rest_hapag_list)
                if len(hapag_rest_dates_dict) != 0:
                    break
        if len(hapag_rest_dates_dict) == 0:
            print('\n[Driver Alert] Hapag-Loyd Search Fatal Error (Rest Sheet)\n')
            #highlight all hapag rest sheet items red
    #------------------------------------------------------------------------------------------------------------

    #Creates dictionaries to hold all dates found from searches, separated by sheet
    rest_total_dict = cosco_rest_dates_dict | one_rest_dates_dict | hapag_rest_dates_dict | maersk_rest_dates_dict | cma_rest_dates_dict | evergreen_rest_dates_dict | hmm_rest_dates_dict
    custom_total_dict =  cosco_custom_dates_dict | one_custom_dates_dict | hapag_custom_dates_dict | maersk_custom_dates_dict | cma_custom_dates_dict | evergreen_custom_dates_dict | hmm_custom_dates_dict

    #Calls function to check and replace all values on each sheet
    replace_values(rest_total_dict, restsheet_data, 'Rest')
    replace_values(custom_total_dict, customsheet_data, 'custom')

if __name__ == '__main__': 
    main()


'''
Storage for possibly future used variables

custom_yangming_list = list()
rest_yangming_list = list()
custom_msc_list = list()
rest_msc_list = list()
custom_oocl_list = list()
rest_oocl_list = list()
oocl_rest_dates_dict = dict()
msc_rest_dates_dict = dict()
yangming_rest_dates_dict = dict()
oocl_custom_dates_dict = dict()
msc_custom_dates_dict = dict()
yangming_custom_dates_dict = dict(

custom_hapag_list.append('HLXU1143116')
custom_hapag_list.append('HLXU5257457')
custom_yangming_list.append('YMLU8268863')
custom_yangming_list.append('YMLU5426986')
custom_maersk_list.append('MSKU9342870')
custom_maersk_list.append('MRKU8485175')
custom_cma_list.append('CMAU0459057')
custom_cma_list.append('CMAU1999430')
custom_msc_list.append('MSCU6919130')
custom_msc_list.append('MSCU6919130')

custom_unadded_containers_list = list()
rest_unadded_containers_list = list()

def yangming_search(container_num): #has an api
    print('No yangming')

def msc_search(container_num): #has an api
    print('no msc')

def oocl_search(container_num): #has an api
    print('no oocl')

'''