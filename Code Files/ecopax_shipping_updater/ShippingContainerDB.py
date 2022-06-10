import sqlite3 as sl
from sqlite3 import *
from ShippingContainer import *
import os
from datetime import datetime

def db_connect():
    db_file_name = os.path.abspath('shipping-container.db')
    db_conn = None

    try: 
        db_conn = sl.connect(db_file_name)
    except Error as e:
        print('\n')
        print(e)
        print('\n')

    return db_conn


def db_get_container_list(carrier_company):
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        sql_statement = ''' Select ContainerNum, CarrierCompany, ArrivalDate, Filepath, SheetName, ContainerNumCellLocation, DateCellLocation WHERE CarrieCompany =?'''




def db_add_container(cont, tab):
    db_connection = db_connect()

    with db_connection:
        if tab == 'reg':
            try:
                cur = db_connection.cursor()
             
                add_sql_statement = ''' INSERT INTO ShippingContainerTable(ContainerNum, CarrierCompany, ArrivalDate, FilePath, SheetName, ContainerNumCellLocation, DateCellLocation, DateAdded, ArrivalDateChanged) VALUES(?,?,?,?,?,?,?,?,?) '''

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                cont_prop = cont.get_properties() + [dt_string, 'False']

                cur.execute(add_sql_statement, cont_prop)
            except Exception:

                update_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDate  =? Where ContainerNum =? '''

                cont_properties = cont.get_properties()

                cur.execute(update_sql_statement, [cont_properties[2], cont_properties[0]])

        else:
            try:
                cur = db_connection.cursor()
             
                add_sql_statement = ''' INSERT INTO NoSearchContainerTable(ContainerRowNum, FilePath, SheetName) VALUES(?,?,?) '''

                cur.execute(add_sql_statement, cont)
            except Exception:
                pass

        db_connection.commit()


    db_connection.close()

def db_remove_container():
    pass

def db_add_excel_file(excel_prop_list):
    db_connection = db_connect()

    with db_connection:
        try:
            cur = db_connection.cursor()

            cur.execute(''' SELECT FilePath, SheetName FROM ExcelFileTable ''')
            rows = cur.fetchall()

            success = False

            for row in rows:
                if row[0] == excel_prop_list[0] and row[1] == excel_prop_list[1]:
                    add_sql_statement = ''' UPDATE ExcelFileTable Set DateCellColumn =?, ContainerNumCellColumn =?,  CarrierCellColumn=? WHERE FilePath =? AND SheetName=? '''

                    first_half_list = excel_prop_list[2:]
                    extra_prop_list = excel_prop_list[0:2]

                    cur.execute(add_sql_statement, (first_half_list + extra_prop_list))

                    success = True

            if success == False:
                raise ValueError('Not in sheet')

        except Exception:
            cur = db_connection.cursor()
             
            insert_sql_statement = ''' INSERT INTO ExcelFileTable(FilePath, SheetName, DateCellColumn, ContainerNumCellColumn, CarrierCellColumn) VALUES (?,?,?,?,?) '''

            cur.execute(insert_sql_statement, excel_prop_list)
        

        db_connection.commit()


    db_connection.close()


    def db_get_excel_file_info(file_path, sheet_name):
        db_connection = db_connect()

        with db_connection:
                cur = db_connection.cursor()

                get_sql_statement(''' SELECT DateCellColumn, ContainerNumCellColumn, CarrierCellColumn FROM ExcelFileTable WHERE FilePath =? AND SheetName =? ''')

                rows = cur.execute(insert_sql_statement, [file_path, sheet_name])

       db_connection.commit()


    db_connection.close()

    return rows

