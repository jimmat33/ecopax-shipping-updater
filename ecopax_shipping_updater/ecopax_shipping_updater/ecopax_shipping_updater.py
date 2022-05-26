from datetime import datetime
from http.server import executable
import tarfile
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


chrome_options = Options()
#chrome_options.headless = True

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

def cosco_search(container_num):
    '''
    This function searches the cosco site for the estimated arrival date of a crate
    '''
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    cosco_link = 'https://elines.coscoshipping.com/ebusiness/'
    driver.implicitly_wait(0.5)
    driver.get(cosco_link)

    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button').click()

    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/ul/li[3]').click()
    
    textbox = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/form/div/div/div[1]/input')
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/a').click()

    web_date = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]/p[2]')
    time.sleep(0.5) #do by visibility of element?
    str_date = web_date.get_attribute('textContent')

    year = str_date[0:4]
    month = str_date[5:7]
    day = str_date[8:10]

    driver.close()
    return [month, day, year]


def one_search(container_num):
    one_link = 'https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking'


def hapag_search(container_num):
    '''
    This function searches the hapag-lloyd site for the estimated arrival date of a crate (May be buggy)
    '''
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
    return [month, day, year]

def yangming_search(container_num):
    yangming_link = 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx'

def maersk_search(container_num):
    '''
    This function searches the maersk site for the estimated arrival date of a crate
    '''
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

    return [month_num, day, year]
   

def cma_search(container_num):
    cma_link = 'https://www.cma-cgm.com/ebusiness/tracking'

def msc_search(container_num):
    msc_link = 'https://www.msc.com/en/track-a-shipment'

def evergreen_search(container_num):
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
    
    return[month_num, day, year]



def oocl_search(container_num):
    oocl_link = 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx'
    driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(0.5)
    driver.get(oocl_link)

    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/form/button'))).click()
    except:
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/form/button').click()

    time.sleep(10)


def main():
    custom_sheet_dict = dict()
    rest_sheet_dict = dict()



    #getting data to pull from for both sheets
    customsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\Shipping Excel Sheet.xlsx', sheet_name = 'custom', usecols="E,E:H,H")
    restsheet_data = pd.read_excel(r'C:\Users\jmattison\Desktop\Shipping Excel Sheet.xlsx', sheet_name = 'Rest', usecols = "F:H")

    #Setting up dictionary for row with format: {Container Number:(Carrier, Arrival Date)}
    for index,row in customsheet_data.iterrows():
        custom_sheet_dict[row['Container Number']] = (row['Carrier'], row['Arrival Date'])

    #Setting up dictionary for row with format: {Container Number:(Carrier, Arrival Date)}
    for index, row in restsheet_data.iterrows():
        rest_sheet_dict[row['Container Number']] = (row['Carrier'], row['Arrival Date'])

    #value = cosco_search('TCNU7749090')
    #value = hapag_search('HLXU1143116')
    #value = maersk_search('MSKU9342870')
    #value = evergreen_search('TCNU3811162')
    value = oocl_search('OOCU7767335')

    print("test")

if __name__ == '__main__': 
    main()

