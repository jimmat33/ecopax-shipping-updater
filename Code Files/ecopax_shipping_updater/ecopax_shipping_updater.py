from ExcelFile import *
import ShippingContainerDB as scDB
from ShippingContainerDB import *
from ShippingUpdaterGUI import *

def main():
    #prompt to update uc chrome and regular chrome if needed, maybe do manually?

    xls = ExcelFile(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Panera Ecopax PET cup Inventory File.xlsx')
    xls.parse_workbook()
    i = 1

    #for every excel file, sort containers, return the list of containers and
    



if __name__ == '__main__': 
    main()
    '''
    gui_framework = ShippingUpdaterGUI()
    gui_framework.run_gui()
       
    on open:
    multiprocess excel spreadsheets

    on search button click:
    multiprocess search


    '''
