from ShippingUpdaterGUI import *
import multiprocessing

if __name__ == '__main__': 
    '''
    import nose2
    nose2.main()
    '''
    multiprocessing.freeze_support()
    gui_frame = ShippingUpdaterGUI()
    gui_frame.run_gui()
    
'''
Needs to install:

'''