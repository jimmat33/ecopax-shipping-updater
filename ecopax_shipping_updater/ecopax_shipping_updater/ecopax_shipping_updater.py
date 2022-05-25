from http.server import executable
import numpy
import sys
import pprint
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(executable_path=r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\chromedriver.exe')#, options=chrome_options)

def cosco_search(container_num):
    '''
    This function searches the cosco site for the estimated arrival date of a crate
    '''
    cosco_link = 'https://elines.coscoshipping.com/ebusiness/'
    driver.implicitly_wait(0.5)
    driver.get(cosco_link)

    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button').click()

    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/ul/li[3]').click()
    
    textbox = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/form/div/div/div[1]/input')
    textbox.send_keys(container_num)

    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/a').click()

    web_date = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]/p[2]')
    time.sleep(0.5)
    str_date = web_date.get_attribute('textContent')

    year = str_date[0:4]
    month = str_date[5:7]
    day = str_date[8:10]

    return [month, day, year]


def one_search(container_num):
    one_link = 'https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking'

def hapag_search(container_num):
    hapag_link = 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html'

def yangming_search(container_num):
    yangming_link = 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx'

def maersk_search(container_num):
    maersk_link = 'https://www.maersk.com/tracking/'

def cma_search(container_num):
    cma_link = 'https://www.cma-cgm.com/ebusiness/tracking'

def msc_search(container_num):
    msc_link = 'https://www.msc.com/en/track-a-shipment'

def evergreen_search(container_num):
    evergreen_link = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'

def oocl_search(container_num):
    oocl_link = 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx'


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

print("test")
driver.close()

