import multiprocessing
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



    start_time = time.perf_counter()
    
    p1 = multiprocessing.Process(target=cosco_search)
    p2 = multiprocessing.Process(target=evergreen_search)
    p3 = multiprocessing.Process(target=hmm_search)
    p4 = multiprocessing.Process(target=maersk_search)
    p5 = multiprocessing.Process(target=one_search)
    p6 = multiprocessing.Process(target=hapag_search)

    cma_list = get_divided_containers_by_carrier('CMA CGM')
    cma_process_lst = []

    for lst_chunk in cma_list:
        p_cma = multiprocessing.Process(target=cma_search, args=(lst_chunk,))
        cma_process_lst.append(p_cma)

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    for srch_process in cma_process_lst:
        srch_process.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()

    for srch_process in cma_process_lst:
        srch_process.join()



    print(f'\n\nDone, Time Ran: {(time.perf_counter() - start_time)/60} minutes')
    

