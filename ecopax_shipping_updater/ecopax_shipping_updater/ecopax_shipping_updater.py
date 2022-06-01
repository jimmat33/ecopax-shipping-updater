from datetime import datetime
from http.server import executable
import tarfile
from unittest import registerResult
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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import os, sys
import time,requests
from bs4 import BeautifulSoup
import random


chrome_options = Options()
#chrome_options.headless = True

def get_month_num(month):
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
        return '-------ERROR-------'

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

def one_search(container_num_list):
    return_dict = dict()

    one_link = 'https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(one_link)

    frame = driver.find_element_by_css_selector('#__next > main > div > div.MainLayout_one-container__4HS_a > div > div.IframeCurrentEcom_wrapper__qvnCe > iframe')
    driver.switch_to.frame(frame)
    select = Select(driver.find_element_by_name('searchType'))
    select.select_by_visible_text('Container No.')

    textbox = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/form/table/tbody/tr/td/div/textarea')
    textbox.clear()
    textbox.send_keys(container_num_list[0])

    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/form/div[1]/div[1]/button/span').click()

    time.sleep(0.5)

    arrival_text = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/form/div[8]/table/tbody/tr[10]/td[4]').get_attribute('textContent')

    month = arrival_text[-11:-9]
    day = arrival_text[-8:-6]
    year = arrival_text[-16:-12]

    return_dict[container_num_list[0]] = [month, day, year]

    i = 1

    while i < len(container_num_list):
        textbox = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/form/table/tbody/tr/td/div/textarea')
        textbox.clear()

        textbox.send_keys(container_num_list[i])
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/form/div[1]/div[1]/button/span').click()
        time.sleep(0.5)

        arrival_text = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/div[8]/table/tbody/tr[10]/td[4]'))).get_attribute('textContent')

        #formatting date properly
        month = arrival_text[-11:-9]
        day = arrival_text[-8:-6]
        year = arrival_text[-16:-12]

        return_dict[container_num_list[i]] = [month, day, year]

        i += 1


    driver.close()
    return return_dict
    
def hapag_search(container_num_list):
    '''
    This function searches the hapag-lloyd site for the estimated arrival date of a crate (May be buggy)
    '''
    return_dict = dict()

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
    textbox.send_keys(container_num_list[0])

    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/button').click()
    
    time.sleep(0.5)
    
    table_text = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table')
    str_text = table_text.get_attribute('textContent')
    index = str_text.find("Vessel arrival")

    target_text = str_text[269:]
    date_text = target_text[(target_text.find("20")):]

    year = date_text[0:4]
    month = date_text[5:7]
    day = date_text[8:10]

    return_dict[container_num_list[0]] = [month, day, year]

    i = 1

    while i < len(container_num_list):
        textbox = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input')
        textbox.clear()

        textbox.send_keys(container_num_list[i])
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/button').click()
        time.sleep(0.5)

        time.sleep(0.5)
    
        table_text = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table')
        str_text = table_text.get_attribute('textContent')
        index = str_text.find("Vessel arrival")

        target_text = str_text[269:]
        date_text = target_text[(target_text.find("20")):]

        year = date_text[0:4]
        month = date_text[5:7]
        day = date_text[8:10]

        return_dict[container_num_list[i]] = [month, day, year]

        i += 1

    driver.close()
    return return_dict

def yangming_search(container_num): #needs human verification, can do up to 12 containers at a time
    '''
    Can't find any estimated date on website, also needs manual verification
    '''
    yangming_link = 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    #driver.get(yangming_link)
    return

def maersk_search(container_num):
    '''
    This function searches the maersk site for the estimated arrival date of a crate
    '''
    return_dict = dict()

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

    year = str_text[-5:-1]

    month = str((str_text[3:-5]).strip())
    month_num = get_month_num(month)

    day = str_text[0:3]

    return [month_num, day, year]
   
def cma_search(container_num):#Ask about verification here
    cma_link = 'https://www.cma-cgm.com/ebusiness/tracking'
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1100,1000")

    driver = uc.Chrome(options=options)

    time_to_sleep = random.randint(2,5)
    time.sleep(time_to_sleep)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    time_to_sleep = random.randint(2,5)
    time.sleep(time_to_sleep)

    driver.get(cma_link)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    '''
    ------------------ Audio Bypass -----------------------------------------------------------------------------------------------------------------------------
    
    --------------------------------------------------------------------------------------------------------------------------------------------------------------
    '''
    time_to_sleep = random.randint(2,5)
    time.sleep(time_to_sleep) # sleep b/w 5 to 10 seconds

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')))
    except:
        textbox = driver.find_elements_by_class_name('o-button primary')

    textbox = driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/p/button').click()
    
    time.sleep(100)

def msc_search(container_num):# no way to see eta
    msc_link = 'https://www.msc.com/en/track-a-shipment'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(msc_link)

def evergreen_search(container_num_list):
    return_dict = dict()

    evergreen_link = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(evergreen_link)

    driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input').click()

    textbox = driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]')
    textbox.send_keys(container_num_list[0])

    driver.find_element_by_xpath('/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]').click()

    str_date = driver.find_element_by_xpath('/html/body/div[5]/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td').get_attribute('textContent')

    month = str_date[28:31]
    day = str_date[32:34]
    year = str_date[35:]

    month_num = get_month_num(month)
    
    return_dict[container_num_list[0]] = [month_num, day, year]

    i = 1

    while i < len(container_num_list):
        textbox = driver.find_element_by_xpath('/html/body/div[5]/center/table[1]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[2]/input[1]')
        textbox.clear()
        textbox.send_keys(container_num_list[i])

        driver.find_element_by_xpath('/html/body/div[5]/center/table[1]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[2]/input[2]').click()

        time.sleep(0.5)
        str_date = driver.find_element_by_xpath('/html/body/div[5]/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td').get_attribute('textContent')

        month = str_date[28:31]
        day = str_date[32:34]
        year = str_date[35:]

        month_num = get_month_num(month)
    
        return_dict[container_num_list[i]] = [month_num, day, year]

        i += 1

    driver.close()
    return return_dict

def oocl_search(container_num):
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

def hmm_search(container_num):
    return_dict = dict()

    hmm_link_part_1 = 'https://www.hmm21.com/cms/company/engn/index.jsp?type=2&number='
    hmm_link_part_2 = '&is_quick=Y&quick_params='
    driver = uc.Chrome()
    driver.implicitly_wait(0.5)

    hmm_search_link = hmm_link_part_1 + container_num + hmm_link_part_2

    driver.get(hmm_search_link)

    selector = Select(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/form/fieldset/p/span[1]/select'))
    selector.select_by_visible_text('Container No.')

    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/form/fieldset/p/span[3]/a').click()

    # Store the ID of the original window
    original_window = driver.current_window_handle

    wait = WebDriverWait(driver, 3)

    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    # Wait for the new tab to finish loading content
    wait.until(EC.title_is("HMM Customer Plus"))

    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/button[2]'))).click()
    except Exception:
        print('exception thrown')

    time.sleep(0.5)

    frame = driver.find_element_by_css_selector('#_frame1')
    driver.switch_to.frame(frame)

    str_date = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/form[1]/div/div[6]/table/tbody/tr[3]/td[5]/span'))).get_attribute('textContent')

    month = str_date[3:6]
    day = str_date[0:2]
    year = str_date[7:11:]

    month_num = get_month_num(month)
    
    driver.close()

    return [month_num, day, year]

def main():
    #put chrome driver version check and chrome version check, prompt to update if necessary


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
    
    #excel_filepath = r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx'

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
    '''
    cosco_custom_dates_dict = cosco_search(custom_cosco_list)
    cosco_rest_dates_dict = cosco_search(rest_cosco_list)
    
    one_custom_dates_dict = one_search(custom_one_list)
    one_rest_dates_dict = one_search(rest_one_list)
    
    hapag_custom_dates_dict = hapag_search(custom_hapag_list)
    hapag_rest_dates_dict = hapag_search(rest_hapag_list)
    
    yangming_custom_dates_dict = yangming_search(custom_yangming_list)
    yangming_rest_dates_dict = yangming_search(rest_yangming_list)
    
    maersk_custom_dates_dict = dict()
    maersk_rest_dates_dict = dict()

    
    for container_num in custom_maersk_list:
        maersk_custom_dates_dict[container_num] = maersk_search(container_num)

    for container_num in rest_maersk_list:
         maersk_rest_dates_dict[container_num] = maersk_search(container_num)
    
    cma_custom_dates_dict = cma_search(custom_cma_list)
    #cma_rest_dates_dict = cma_search(rest_cma_list)
    
    msc_custom_dates_dict = msc_search(custom_msc_list)
    #msc_rest_dates_dict = msc_search(rest_msc_list)
    
    #evergreen_custom_dates_dict = evergreen_search(custom_evergreen_list)
    evergreen_rest_dates_dict = evergreen_search(rest_evergreen_list)
    
    oocl_custom_dates_dict = oocl_search(custom_oocl_list)
    oocl_rest_dates_dict = oocl_search(rest_oocl_list)
    '''
    hmm_custom_dates_dict = dict()
    hmm_rest_dates_dict = dict()

    for container_num in custom_hmm_list:
        hmm_custom_dates_dict[container_num] = hmm_search(container_num)

    for container_num in rest_hmm_list:
         hmm_rest_dates_dict[container_num] = hmm_search(container_num)
    
    #value = evergreen_search('TCNU3811162')

    #replace_values(cosco_custom_dates_dict, customsheet_data, 'custom')
    rest_total_dict = cosco_rest_dates_dict + one_rest_dates_dict + hapag_rest_dates_dict + yangming_rest_dates_dict + maersk_rest_dates_dict + cma_rest_dates_dict + msc_rest_dates_dict + evergreen_rest_dates_dict + oocl_rest_dates_dict + hmm_rest_dates_dict

    custom_total_dict =  cosco_custom_dates_dict + one_custom_dates_dict + hapag_custom_dates_dict + yangming_custom_dates_dict + maersk_custom_dates_dict + cma_custom_dates_dict + msc_custom_dates_dict + evergreen_custom_dates_dict + oocl_custom_dates_dict + hmm_custom_dates_dict

    print("test")

if __name__ == '__main__': 
    main()