from ShippingUpdaterUtility import *
from CMA import cma_search
from Cosco import cosco_search
from Evergreen import evergreen_search
from HapagLloyd import hapag_search
from HMM import hmm_search
from Maersk import maersk_search
from ONE import one_search
from ExcelFile import *


def main():
    #prompt to update uc chrome and regular chrome if needed, maybe do manually?

    xls_two = ExcelFile(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet.xlsx')
    xls_two.parse_workbook()
   
    
    i = 1
    



if __name__ == '__main__': 
    main()
    '''
    cosco_search()
    
    evergreen_search()
    '''
    hmm_search()
    '''
    maersk_search()

    one_search()

    cma_search()

    hapag_search()
    '''

