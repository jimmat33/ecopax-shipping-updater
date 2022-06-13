from ExcelFile import *
import ShippingContainerDB as scDB
from ShippingContainerDB import *
from ShippingUpdaterGUI import *

def main():
    #prompt to update uc chrome and regular chrome if needed, maybe do manually?

    xls = ExcelFile(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Panera Ecopax PET cup Inventory File.xlsx')
    xls.parse_workbook()

    xls_two = ExcelFile(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')
    xls_two.parse_workbook()

    i = 1

    #for every excel file, sort containers, return the list of containers and
    



if __name__ == '__main__': 
    main()
    
    cosco_containers = db_get_containers_by_carrier('Cosco')

    cosco = CoscoSearch(cosco_containers)
    cosco.search()

    i = 0
