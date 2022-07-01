"""
Drives the main code instance

This file is used to create a gui instance and freeze multiprocessing
when the file is compiled in exe format

Use: pylint <filename> for static code quality checks
Use: radon <cc, mi, raw, hal> <filename>.py for complexity checking
"""
import multiprocessing
import ShippingUpdaterGUI

if __name__ == '__main__':
    multiprocessing.freeze_support()
    gui_frame = ShippingUpdaterGUI.run_gui()
