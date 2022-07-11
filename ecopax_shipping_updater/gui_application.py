'''
class docstring
'''
import tkinter as tk
from tkinter import Button, Label, Frame, ttk, Scrollbar, filedialog
import tkinter.font
import multiprocessing
import time
import os
import operator
from openpyxl import load_workbook
import ExcelFile
from shipping_container_db import (db_get_all_containers, db_get_all_excel_filepaths,
                                   db_remove_excel_file, db_get_all_excel_files,
                                   db_set_all_cont_false, db_get_all_errors,
                                   db_get_cont_by_carrier, db_clear_database)
from CMA import cma_search
from Cosco import cosco_search
from Evergreen import evergreen_search
from HapagLloyd import hapag_search
from HMM import hmm_search
from Maersk import maersk_search
from ONE import one_search
from shipping_updater_utility import get_divided_containers_by_carrier, modify_sheets


class ShippingUpdaterGUI():
    '''
    docstr
    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.root = tk.Tk()
        self.error_index = 1
        self.excel_index = 1
        self.cont_table_index = 1
        self.xcel_file_list = []
        self.error_list = []
        self.start_time = 0

        # All widget instantiations ----------------------------------------------------------

        self.import_sheet_button = Button(self.root, text='Import Spreadsheet', state='normal',
                                          command=self.import_spreadsheet_btn_click)
        self.remove_sheet_button = Button(self.root, text='Remove Spreadsheet', state='normal',
                                          command=self.remove_spreadsheet_btn_click)
        self.run_search_button = Button(self.root, text='Run Search', state='normal',
                                        command=self.run_search_btn_click)
        self.cont_frame = Frame(self.root)
        self.error_log_frame = Frame(self.root)
        self.excel_sheet_frame = Frame(self.root)
        self.time_ran_label = Label(self.root, text='', state='normal')
        self.cont_num_label = Label(self.root, text='Total Containers: 0', state='normal')

        self.init_widgits()

    def run_gui(self):
        '''
        docstr
        '''
        self.root.title("Ecopax Shipping Updater")
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        img = tk.PhotoImage(file=(os.path.abspath('gui_icon.png')))
        self.root.tk.call('wm', 'iconphoto', self.root._w, img)  # pylint: disable=W0212
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(1, self.on_open)
        self.root.mainloop()

    def init_widgits(self):
        '''
        docstr
        '''
        self.time_ran_label.place(x=25, y=252, height=25)
        self.cont_num_label.place(x=330, y=265, height=25)
        self.import_sheet_button.place(x=25, y=50, width=220, height=55)
        self.remove_sheet_button.place(x=25, y=120, width=220, height=55)
        self.run_search_button.place(x=25, y=190, width=220, height=55)

        self.init_trvws()

    def init_trvws(self):
        '''
        docstr
        '''
        # container table
        self.cont_frame.place(x=323, y=295, width=462, height=293)

        # table scrollbars
        report_vertical_scroll = Scrollbar(self.cont_frame)
        report_vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.cont_frame = ttk.Treeview(self.cont_frame, yscrollcommand=report_vertical_scroll.set)

        report_vertical_scroll.config(command=self.cont_frame.yview)

        # setting up table
        self.cont_frame['columns'] = ('cont_num', 'cont_carrier', 'cont_date', 'fp')
        self.cont_frame.column('#0', width=0, stretch=tk.NO)
        self.cont_frame.column('cont_num', anchor=tk.CENTER, width=134)
        self.cont_frame.column('cont_carrier', anchor=tk.CENTER, width=134)
        self.cont_frame.column('cont_date', anchor=tk.CENTER, width=170)
        self.cont_frame.column('fp', width=0, stretch=tk.NO)

        self.cont_frame.heading('#0', text='', anchor=tk.CENTER)
        self.cont_frame.heading('cont_num', text='Container Number', anchor=tk.CENTER)
        self.cont_frame.heading('cont_carrier', text='Container Carrier', anchor=tk.CENTER)
        self.cont_frame.heading('cont_date', text='Due to Dock Date', anchor=tk.CENTER)
        self.cont_frame.heading('fp', text='', anchor=tk.CENTER)
        self.cont_frame.pack()

        # error log frame
        self.error_log_frame.place(x=260, y=35, width=525, height=240)

        error_vertical_scroll = Scrollbar(self.error_log_frame)
        error_vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        error_horizontal_scroll = Scrollbar(self.error_log_frame, orient='horizontal')
        error_horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.error_log_frame = ttk.Treeview(self.error_log_frame,
                                            yscrollcommand=error_vertical_scroll.set,
                                            xscrollcommand=error_horizontal_scroll.set)

        error_vertical_scroll.config(command=self.error_log_frame.yview)
        error_horizontal_scroll.config(command=self.error_log_frame.xview)

        # setting up table
        self.error_log_frame['columns'] = ('error_log')
        self.error_log_frame.column('#0', width=0, stretch=tk.NO)
        self.error_log_frame.column('error_log', anchor=tk.CENTER, width=499)

        self.error_log_frame.heading('#0', text='', anchor=tk.CENTER)
        self.error_log_frame.heading('error_log', text='Errors', anchor=tk.CENTER)

        self.error_log_frame.pack()

        # excel sheet table
        self.excel_sheet_frame.place(x=15, y=295, width=293, height=290)

        # table scrollbars
        excel_vertical_scroll = Scrollbar(self.excel_sheet_frame)
        excel_vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        excel_horizontal_scroll = Scrollbar(self.excel_sheet_frame, orient='horizontal')
        excel_horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.excel_sheet_frame = ttk.Treeview(self.excel_sheet_frame,
                                              yscrollcommand=excel_vertical_scroll.set,
                                              xscrollcommand=excel_horizontal_scroll.set)

        excel_vertical_scroll.config(command=self.excel_sheet_frame.yview)
        excel_horizontal_scroll.config(command=self.excel_sheet_frame.xview)

        # setting up table
        self.excel_sheet_frame['columns'] = ('file_name')
        self.excel_sheet_frame.column('#0', width=0, stretch=tk.NO)
        self.excel_sheet_frame.column('file_name', anchor=tk.W, width=400)

        self.excel_sheet_frame.heading('#0', text='', anchor=tk.CENTER)
        self.excel_sheet_frame.heading('file_name', text='Excel File Name', anchor=tk.W)

        self.excel_sheet_frame.pack()

    def import_spreadsheet_btn_click(self):
        '''
        docstr
        '''
        process_lst = []

        filename_list = filedialog.askopenfilenames(initialdir="", title="Select a File",
                                                    filetypes=(("all files", "*.*"),))
        for f_p in filename_list:
            excel_file = ExcelFile(f_p)  # pylint: disable=E1102

            self.xcel_file_list.append(excel_file)

            file_name = f_p.split('/')[-1]

            self.excel_sheet_frame.insert(parent='', index='end', iid=self.excel_index,
                                          text='', values=(file_name,))
            self.excel_index += 1

        if len(self.xcel_file_list) == 1:
            self.xcel_file_list[0].parse_workbook()
        else:
            for xcel_file in self.xcel_file_list:
                xcel_process = multiprocessing.Process(target=xcel_file.parse_workbook)
                process_lst.append(xcel_process)

            for prse_process in process_lst:
                prse_process.start()

            for prse_process in process_lst:
                prse_process.join()

        container_lst = db_get_all_containers('gui')
        sorted_list = sorted(container_lst, key=operator.itemgetter(1))

        for cont in sorted_list:
            self.cont_frame.insert(parent='', index='end', iid=self.cont_table_index,
                                   text='', values=(cont[0], cont[1], cont[2], cont[3],))
            self.cont_table_index += 1

        tf_items = self.get_all_treeview_items(self.cont_frame)
        cont_num_list = []
        cont_num_list = [cont_num_list.append(val[0]) for val in tf_items]

        cont_len = len(cont_num_list)
        self.cont_num_label['text'] = f'Total Containers: {cont_len}'

    def remove_spreadsheet_btn_click(self):
        '''
        docstr
        '''
        try:
            # check to see if line below assigns a value to selected_item_index
            selected_item_index = self.excel_sheet_frame.focus()  # pylint: disable=E1111
            item = self.excel_sheet_frame.item(self.excel_sheet_frame.focus())
            if selected_item_index != '':

                file_name = str(item['values'][0])
                filepath_list = db_get_all_excel_filepaths()
                filepath = ''

                for data in filepath_list:
                    if data[0].find(file_name) != -1:
                        filepath = data[0]

                db_remove_excel_file(filepath)

                self.excel_sheet_frame.delete(selected_item_index)

            self.clear_trvw(selected_item_index, filepath)

        except Exception as rem_err:  # pylint: disable=W0703
            print('\n' + rem_err + '\n')
            self.clear_trvw(selected_item_index, filepath)

    def clear_trvw(self, selected_item_index, filepath):
        '''
        docstr
        '''
        entries_in_trvw_lst = self.cont_frame.get_children()

        self.excel_sheet_frame.delete(selected_item_index)

        for trvw_item in entries_in_trvw_lst:
            if self.cont_frame.item(trvw_item)['values']['fp'] == filepath:
                self.excel_sheet_frame.delete(trvw_item)

        tf_items = self.get_all_treeview_items(self.cont_frame)
        cont_num_list = []
        cont_num_list = [cont_num_list.append(val[0]) for val in tf_items]

        cont_len = len(cont_num_list)
        self.cont_num_label['text'] = f'Total Containers: {cont_len}'

    def run_search_btn_click(self):
        '''
        docstr
        '''
        self.time_ran_label['text'] = ''

        is_running = True
        process_type = 'multi'

        self.start_time = time.perf_counter()

        excel_file_list = db_get_all_excel_files()
        for xcel_sheet in excel_file_list:
            try:
                test_wb = load_workbook(filename=xcel_sheet[0])
                test_wb.save(xcel_sheet[0])
            except PermissionError as open_err:
                print('\n' + open_err + '\n')
                error_message = f'Please close file:\n\n {xcel_sheet[0]}'
                tkinter.messagebox.showwarning(title='Open Excel File Error', message=error_message)
                is_running = False
                break

        if is_running and process_type == 'multi':
            self.multi_search()

            for item in self.cont_frame.get_children():
                self.cont_frame.delete(item)

            self.cont_table_index = 1
            container_lst = db_get_all_containers('gui')
            sorted_list = sorted(container_lst, key=operator.itemgetter(1))

            for cont in sorted_list:
                self.cont_frame.insert(parent='', index='end', iid=self.cont_table_index,
                                       text='', values=(cont[0], cont[1], cont[2], cont[3],))
                self.cont_table_index += 1

            db_set_all_cont_false()

            error_lst = db_get_all_errors()

            for err in error_lst:
                self.error_log_frame.insert(parent='', index='end', iid=self.error_index,
                                            text='', values=(err[0],))
                self.error_index += 1

            time_ran = round(((time.perf_counter() - self.start_time) / 60), 2)

            self.time_ran_label['text'] = f'Time Ran: {time_ran} Minutes'

        elif is_running and process_type == 'reg':
            self.seq_search()
        else:

            print('Run search btn clicked')

    def multi_search(self):
        '''
        docstr
        '''
        p_1 = multiprocessing.Process(target=cosco_search)
        p_2 = multiprocessing.Process(target=evergreen_search)
        p_4 = multiprocessing.Process(target=maersk_search)
        p_5 = multiprocessing.Process(target=one_search)

        cma_list = get_divided_containers_by_carrier('CMA CGM')
        cma_process_lst = []

        for lst_chunk in cma_list:
            p_cma = multiprocessing.Process(target=cma_search, args=(lst_chunk,))
            cma_process_lst.append(p_cma)

        p_1.start()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started Cosco')
        p_2.start()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started Evergreen')
        p_4.start()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started maersk')
        p_5.start()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started one')

        for srch_process in cma_process_lst:
            srch_process.start()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started cma')

        p_1.join()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished Cosco')
        p_2.join()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished Evergreen')
        p_4.join()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished maersk')
        p_5.join()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished one')

        for srch_process in cma_process_lst:
            srch_process.join()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished cma')

        hmm_search()
        hapag_search()

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished search')
        print(f'\n\nDone, Time Ran: {(time.perf_counter() - self.start_time)/60} minutes')

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Started sheet modification')
        modify_sheets()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Finished sheet modification')

    def seq_search(self):
        '''
        Docstring
        '''

        cosco_search()

        evergreen_search()

        hmm_search()

        maersk_search()

        one_search()

        hapag_search()

        cma_cont_list = db_get_cont_by_carrier('CMA CGM')
        cma_search(cma_cont_list)

    def get_all_treeview_items(self, tv_frame):
        '''
        docstr
        '''
        values_lst = []
        entries_in_trvw_lst = tv_frame.get_children()

        for trvw_item in entries_in_trvw_lst:
            itemvals = tv_frame.item(trvw_item)['values']
            values_lst.append(itemvals)

        return values_lst

    def on_closing(self):
        '''
        docstr
        '''
        db_clear_database()

        path_dir = os.path.abspath('Audio Captcha Files')
        for f_n in os.listdir(path_dir):
            os.remove(os.path.join(path_dir, f_n))

        self.root.destroy()

    def on_open(self):
        '''
        docstr
        '''
        path_dir = os.path.abspath('Excel File Cache')
        for f_n in os.listdir(path_dir):
            os.remove(os.path.join(path_dir, f_n))
