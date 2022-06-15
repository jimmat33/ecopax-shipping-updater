import threading
from ShippingUpdaterUtility import *
from CMA import cma_search
from Cosco import cosco_search
from Evergreen import evergreen_search
from HapagLloyd import hapag_search
from HMM import hmm_search
from Maersk import maersk_search
from ONE import one_search
from ExcelFile import *
import time


def main():
    #prompt to update uc chrome and regular chrome if needed, maybe do manually?

    xls_1 = ExcelFile(r'C:\Users\jmattison\Desktop\ecopax-shipping-updater\Shipping Excel Sheet Test.xlsx')
    xls_1.parse_workbook()

    

#py2exe for executable 

if __name__ == '__main__': 
    start_time = time.time()
    main()
    '''
    cosco_search()
    
    evergreen_search()
    
    hmm_search()
    
    maersk_search()
    
    one_search()
    
    cma_cont_list = db_get_containers_by_carrier('CMA CGM')
    cma_search(cma_cont_list)
    
    hapag_search()
    '''




    
    t1 = threading.Thread(target=cosco_search)
    t2 = threading.Thread(target=evergreen_search)
    t3 = threading.Thread(target=hmm_search)
    t4 = threading.Thread(target=maersk_search)
    t5 = threading.Thread(target=one_search)
    t6 = threading.Thread(target=hapag_search)

    cma_list = get_divided_containers_by_carrier('CMA CGM')
    cma_thread_lst = []

    for lst_chunk in cma_list:
        t_cma = threading.Thread(target=cma_search, args=(lst_chunk,))
        cma_thread_lst.append(t_cma)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    for srch_thread in cma_thread_lst:
        srch_thread.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()


    for srch_thread in cma_thread_lst:
        srch_thread.join()

    print(f'\n\nDone, Time Ran: {time.time() - start_time}')
    

