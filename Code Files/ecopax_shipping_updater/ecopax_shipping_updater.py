from ShippingUpdaterGUI import *
import multiprocessing

if __name__ == '__main__': 
    multiprocessing.freeze_support()
    gui_frame = ShippingUpdaterGUI()
    gui_frame.run_gui()
    
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

