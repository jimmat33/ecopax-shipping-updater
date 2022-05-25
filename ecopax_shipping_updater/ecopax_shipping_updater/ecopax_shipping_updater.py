import numpy
import sys
import pprint
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook

def cosco_search(container_num):
    cosco_link = 'https://elines.coscoshipping.com/ebusiness/'

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




