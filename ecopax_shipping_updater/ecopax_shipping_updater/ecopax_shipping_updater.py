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
    workbook = load_workbook(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')
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


        workbook.save(filename=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')




        '''
        index_list = df[df == container_num].stack().index.tolist()

        formatted_date = container_arrival_date[2] + '-' + container_arrival_date[0] + '-' + container_arrival_date[1]

        if sheet_name == 'custom':
            old_date = str(df.iat[index_list[0][0], 6])

            old_formatted_date = old_date[0:10]

            if old_date == 'arrived':
                print('already arrived')
            elif old_formatted_date == formatted_date:
                df.iat[index_list[0][0], 6] = 'arrived'

                modified_custom_cells_list.append(container_num)
            else:
                df.iat[index_list[0][0], 6] = datetime(int(container_arrival_date[2]), int(container_arrival_date[0]), int(container_arrival_date[1]), 0 ,0)

                modified_custom_cells_list.append(container_num)
        else:
            old_date = str(df.iat[index_list[0][0], 7])
            old_formatted_date = old_date[0:10]

            if old_date == 'arrived':
                print('already arrived')
            elif old_formatted_date == formatted_date:
                df.iat[index_list[0][0], 7] = 'arrived'

                modified_rest_cells_list.append(container_num)
            else:
                df.iat[index_list[0][0], 7] = datetime(int(container_arrival_date[2]), int(container_arrival_date[0]), int(container_arrival_date[1]), 0 ,0)

                modified_rest_cells_list.append(container_num)
    '''

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

def one_search(container_num):
    '''
    one_link = 'https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking'
    driver.implicitly_wait(0.5)
    driver.get(one_link)
    #time.sleep(15)
    #cannot find dropdown, try again later
    #dropdown = driver.find_element_by_class_name('select')
    #dropdown.select_by_visible_text('Container No.')
    '''
    return 

def hapag_search(container_num):
    '''
    This function searches the hapag-lloyd site for the estimated arrival date of a crate (May be buggy)
    
    driver = uc.Chrome(options=chrome_options)
    hapag_link = 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html'
    driver.implicitly_wait(0.5)
    driver.get(hapag_link)
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[2]/div[3]/div[1]/button[2]'))).click()
    except:
        driver.find_element(By.ID, "accept-recommended-btn-handler").click()

    time.sleep(0.5)

    textbox = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input')
    textbox.clear()
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/button').click()
    
    time.sleep(0.5)
    
    table_text = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table')
    str_text = table_text.get_attribute('textContent')
    index = str_text.find("Vessel arrival")

    target_text = str_text[269:]
    date_text = target_text[(target_text.find("20")):]
    print(f'\n\n{date_text}')
    

    year = date_text[0:4]
    month = date_text[5:7]
    day = date_text[8:10]

    driver.close()
    '''
    return

def yangming_search(container_num):
    '''
    yangming_link = 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(yangming_link)

    #time.sleep(15)
    '''
    return

def maersk_search(container_num):
    '''
    This function searches the maersk site for the estimated arrival date of a crate
    
    maersk_link = 'https://www.maersk.com/tracking/'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)

    maersk_link = maersk_link + container_num

    driver.implicitly_wait(0.5)
    driver.get(maersk_link)


    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/button[3]'))).click()
    except:
        driver.find_elements_by_class_name('coi-banner__accept--fixed-margin').click()

    str_text = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/div[3]/dl/dd[1]'))).get_attribute('textContent')

    year = str_text[-4:]

    month = str((str_text[3:-5]).strip())
    month_num = get_month_num(month)

    day = str_text[0:3]
    '''
    return
   
def cma_search(container_num):
    '''
    cma_link = 'https://www.cma-cgm.com/ebusiness/tracking'
    driver = uc.Chrome(options=chrome_options)
    driver.get(cma_link)
    #text_to_speech_driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    #text_to_speech_driver.implicitly_wait(0.5)
    
    ------------------ Audio Bypass -----------------------------------------------------------------------------------------------------------------------------
    
    delayTime = 2
    audioToTextDelay = 10

    filename = 'captcha-audio.mp3'
    bypass_url = 'https://www.cma-cgm.com/ebusiness/tracking'
    text_to_speech_url = 'https://speech-to-text-demo.ng.bluemix.net/'

    driver.get(bypass_url)

    time.sleep(7)
    captcha_button = driver.find_element_by_class_name('geetest_logo')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(captcha_button, 5, 5)
    action.click()
    action.perform()



    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')))
    except:
        textbox = driver.find_elements_by_class_name('o-button primary')

    textbox = driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/p/button').click()
    #time.sleep(10)
    '''
    return

def msc_search(container_num):
    #msc_link = 'https://www.msc.com/en/track-a-shipment'
    return

def evergreen_search(container_num):
    '''
    evergreen_link = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(evergreen_link)

    driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input').click()

    textbox = driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]')
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]').click()

    str_date = driver.find_element_by_xpath('/html/body/div[5]/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td').get_attribute('textContent')

    month = str_date[28:31]
    day = str_date[32:34]
    year = str_date[35:]

    month_num = get_month_num(month)
    '''
    return

def oocl_search(container_num):
    '''
    oocl_link = 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe')
    driver.implicitly_wait(0.5)
    driver.get(oocl_link)

    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/form/button'))).click()
    except:
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/form/button').click()

    time.sleep(10)
    #human bypass needed
    '''
    return

def hmm_search(container_num):
    return

def main():
    #Setting up all the lists for each 
    custom_cosco_list = list()
    rest_cosco_list = list()

    custom_one_list = list()
    rest_one_list = list()

    custom_hapag_list = list()
    rest_hapag_list = list()

    custom_yangming_list = list()
    rest_yangming_list = list()

    custom_maersk_list = list()
    rest_maersk_list = list()

    custom_cma_list = list()
    rest_cma_list = list()

    custom_msc_list = list()
    rest_msc_list = list()
    
    custom_evergreen_list = list()
    rest_evergreen_list = list()

    custom_oocl_list = list()
    rest_oocl_list = list()

    custom_hmm_list = list()
    rest_hmm_list = list()

    custom_unadded_containers_list = list()
    rest_unadded_containers_list = list()
    
    excel_filepath = r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx'

    #getting data to pull from for both sheets
    customsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'custom')
    restsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx', sheet_name = 'Rest')

    for index,row in customsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            custom_cosco_list.append(row['Container Number'])
        elif row['Carrier'] == 'ONE':
            custom_one_list.append(row['Container Number'])
        elif row['Carrier'] == 'Hapag-Lloyd':
            custom_hapag_list.append(row['Container Number'])
        elif row['Carrier'] == 'Yangming':
            custom_yangming_list.append(row['Container Number'])
        elif row['Carrier'] == 'Maersk':
            custom_maersk_list.append(row['Container Number'])
        elif row['Carrier'] == 'CMA CGM':
            custom_cma_list.append(row['Container Number'])
        elif row['Carrier'] == 'MSC':
            custom_msc_list.append(row['Container Number'])
        elif row['Carrier'] == 'Evergreen':
            custom_evergreen_list.append(row['Container Number'])
        elif row['Carrier'] == 'OOCL':
            custom_oocl_list.append(row['Container Number'])
        elif row['Carrier'] == 'HMM':
            custom_hmm_list.append(row['Container Number'])
        else:
            if isinstance(row['Container Number'], str) != False:
                custom_unadded_containers_list.append(row['Container Number'])

    for index, row in restsheet_data.iterrows():
        if row['Carrier'] == 'Cosco':
            rest_cosco_list.append(row['Container Number'])
        elif row['Carrier'] == 'ONE':
            rest_one_list.append(row['Container Number'])
        elif row['Carrier'] == 'Hapag-Lloyd':
            rest_hapag_list.append(row['Container Number'])
        elif row['Carrier'] == 'Yangming':
            rest_yangming_list.append(row['Container Number'])
        elif row['Carrier'] == 'Maersk':
            rest_maersk_list.append(row['Container Number'])
        elif row['Carrier'] == 'CMA CGM':
            rest_cma_list.append(row['Container Number'])
        elif row['Carrier'] == 'MSC':
            rest_msc_list.append(row['Container Number'])
        elif row['Carrier'] == 'Evergreen':
            rest_evergreen_list.append(row['Container Number'])
        elif row['Carrier'] == 'OOCL':
            rest_oocl_list.append(row['Container Number'])
        elif row['Carrier'] == 'HMM':
            rest_hmm_list.append(row['Container Number'])
        else:
            if isinstance(row['Container Number'], str) != False:
                rest_unadded_containers_list.append(row['Container Number'])
        

    cosco_custom_dates_dict = cosco_search(custom_cosco_list)
    cosco_rest_dates_dict = cosco_search(rest_cosco_list)
 
    one_custom_dates_dict = one_search(custom_one_list)
    one_rest_dates_dict = one_search(rest_one_list)
    
    hapag_custom_dates_dict = hapag_search(custom_hapag_list)
    hapag_rest_dates_dict = hapag_search(rest_hapag_list)
    
    yangming_custom_dates_dict = yangming_search(custom_yangming_list)
    yangming_rest_dates_dict = yangming_search(rest_yangming_list)

    maersk_custom_dates_dict = maersk_search(custom_maersk_list)
    maersk_rest_dates_dict = maersk_search(rest_maersk_list)

    cma_custom_dates_dict = cma_search(custom_cma_list)
    cma_rest_dates_dict = cma_search(rest_cma_list)

    msc_custom_dates_dict = msc_search(custom_msc_list)
    msc_rest_dates_dict = msc_search(rest_msc_list)

    evergreen_custom_dates_dict = evergreen_search(custom_evergreen_list)
    evergreen_rest_dates_dict = evergreen_search(rest_evergreen_list)

    oocl_custom_dates_dict = oocl_search(custom_oocl_list)
    oocl_rest_dates_dict = oocl_search(rest_oocl_list)

    hmm_custom_dates_dict = hmm_search(custom_hmm_list)
    hmm_rest_dates_dict = hmm_search(rest_hmm_list)
    
    #value = hapag_search('HLXU1143116')
    #value = maersk_search('MSKU9342870')
    #value = evergreen_search('TCNU3811162')

    #replace_values(cosco_custom_dates_dict, customsheet_data, 'custom')
    rest_total_dict = cosco_rest_dates_dict + one_rest_dates_dict + hapag_rest_dates_dict + yangming_rest_dates_dict + maersk_rest_dates_dict + cma_rest_dates_dict + msc_rest_dates_dict + evergreen_rest_dates_dict + oocl_rest_dates_dict + hmm_rest_dates_dict

    custom_total_dict =  cosco_custom_dates_dict + one_custom_dates_dict + hapag_custom_dates_dict + yangming_custom_dates_dict + maersk_custom_dates_dict + cma_custom_dates_dict + msc_custom_dates_dict + evergreen_custom_dates_dict + oocl_custom_dates_dict + hmm_custom_dates_dict

    replace_values(rest_total_dict, 'Rest', restsheet_data)
    #replace_values(custom_total_dict, 'custom', customsheet_data)

    #modified_custom_cells_list = list()
    #modified_rest_cells_list = list()


if __name__ == '__main__': 
    main()