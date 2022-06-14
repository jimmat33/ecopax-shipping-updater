import os
import sqlite3 as sl
from ShippingContainer import *
from datetime import datetime

def compare_dates(old_date, new_date):
    try:
        dt_old_date = datetime.strptime(old_date, "%m/%d/%Y")
        dt_new_date = datetime.strptime(new_date, "%m/%d/%Y")

        if dt_new_date <= datetime.today():
            return 2
        elif dt_old_date < dt_new_date:
            return 1
        elif dt_old_date > dt_new_date:
            return 1
        else:
           return 0
    except Exception:
        return -1


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



def db_get_containers_by_carrier(carrier_company):
    db_connection = db_connect()
    container_list = []

    with db_connection:
        try:
            cur = db_connection.cursor()

            get_sql_statement = ''' SELECT ContainerNum, CarrierCompany, ArrivalDate, Filepath, SheetName, ContainerNumCellLocation, DateCellLocation FROM ShippingContainerTable WHERE CarrierCompany =? AND ArrivalDate !=? '''

            cur.execute(get_sql_statement, [carrier_company, 'arrived'])

            container_list = cur.fetchall()
        except:
            pass

        db_connection.commit()


    db_connection.close()

    return container_list


def db_add_container(cont, tab):
    db_connection = db_connect()

    if isinstance(cont, ShippingContainer):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cont_prop = cont.get_properties() + [dt_string, 'False']

    with db_connection:
        if tab == 'reg':
            try:
                cur = db_connection.cursor()
             
                add_sql_statement = ''' INSERT INTO ShippingContainerTable(ContainerNum, CarrierCompany, ArrivalDate, FilePath, SheetName, ContainerNumCellLocation, DateCellLocation, DateAdded, ArrivalDateChanged) VALUES(?,?,?,?,?,?,?,?,?) '''

                cur.execute(add_sql_statement, cont_prop)
            except Exception:

                get_old_data_sql_statement = ''' SELECT FilePath, SheetName, ContainerNumCellLocation, DateCellLocation FROM ShippingContainerTable WHERE ContainerNum =? '''
        
                cur.execute(get_old_data_sql_statement, [cont_prop[0]])
                loc_list = cur.fetchall()

                old_container_num_location = loc_list[0][2]
                old_date_location = loc_list[0][3]
                old_file_path = loc_list[0][0]
                old_sheet = loc_list[0][1]

                if old_file_path != cont_prop[3]:
                    updated_file_path = old_file_path + '<' + cont_prop[3]
                    updated_sheet = old_sheet + '<' + cont_prop[4]
                    updated_num_loc = old_container_num_location + '<' + cont_prop[5]
                    updated_date_loc = old_date_location + '<' + cont_prop[6]

                elif old_sheet != cont_prop[4]:
                    updated_file_path = old_file_path
                    updated_sheet = old_sheet + '<' + cont_prop[4]
                    updated_num_loc = old_container_num_location + '<' + cont_prop[5]
                    updated_date_loc = old_date_location + '<' + cont_prop[6]
                else:
                    updated_file_path = old_file_path
                    updated_sheet = old_sheet
                    updated_num_loc = old_container_num_location
                    updated_date_loc = old_date_location

                updated_props = [cont_prop[2], updated_num_loc, updated_date_loc, updated_file_path, updated_sheet, cont_prop[0]]

                try:
                    old_file_path = old_file_path.split('<')
                    old_sheet_list = old_sheet.split('<')
                    old_loc_list = old_container_num_location.split('<')

                    if cont_prop[3] not in old_file_path:
                        update_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDate  =?, ContainerNumCellLocation =?, DateCellLocation =?, Filepath =?, SheetName =? WHERE ContainerNum =? '''

                        cur.execute(update_sql_statement, updated_props)

                    if cont_prop[4] not in old_sheet_list:
                        update_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDate  =?, ContainerNumCellLocation =?, DateCellLocation =?, Filepath =?, SheetName =? WHERE ContainerNum =? '''

                        cur.execute(update_sql_statement, updated_props)

                except Exception:
                    pass

        else:
            try:
                cur = db_connection.cursor()
             
                add_sql_statement = ''' INSERT INTO NoSearchContainerTable(ContainerRowNum, FilePath, SheetName) VALUES(?,?,?) '''

                cur.execute(add_sql_statement, cont)
            except Exception:
                pass

        db_connection.commit()


    db_connection.close()


def db_update_container(cont_num, cont_date):
    db_connection = db_connect()
    date_comp = 1
    update_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDate =?, ArrivalDateChanged =? WHERE ContainerNum =? '''

    with db_connection:
        try:

            cur = db_connection.cursor()

            get_old_data_sql_statement = ''' SELECT ArrivalDate, CarrierCompany FROM ShippingContainerTable WHERE ContainerNum =? '''
        
            cur.execute(get_old_data_sql_statement, [cont_num])
            arrival_list = cur.fetchall()

            if arrival_list[0][0] == None:
                check_arrival = ''
            else:
                check_arrival = arrival_list[0][0].strip().lower()

            if check_arrival != 'arrived':
                if cont_date[0:5] != 'ERROR' and arrival_list[0][0] != None:
                    date_comp = compare_dates(arrival_list[0][0], cont_date)
                    if date_comp == -1:
                        if arrival_list[0][1] == 'Evergreen':
                            cur.execute(update_sql_statement, ['arrived', 'True', cont_num])
                        else:
                            cur.execute(update_sql_statement, ['Date Error', 'True', cont_num])
                    if date_comp == 1:
                        cur.execute(update_sql_statement, [cont_date, 'True', cont_num])
                    elif date_comp == 2:
                        cur.execute(update_sql_statement, ['arrived', 'True', cont_num])
                elif arrival_list[0][0] == None:
                    try:
                        dt_new_date = datetime.strptime(cont_date, "%m/%d/%Y")
                        if dt_new_date <= datetime.today():
                            cur.execute(update_sql_statement, ['arrived', 'True', cont_num])
                        else:
                            cur.execute(update_sql_statement, [cont_date, 'True', cont_num])
                    except:
                        cur.execute(update_sql_statement, ['Date Error', 'True', cont_num])
                else:
                    if arrival_list[0][1] == 'Evergreen':
                        cur.execute(update_sql_statement, ['arrived', 'True', cont_num])
                    else:
                        cur.execute(update_sql_statement, ['Date Error', 'True', cont_num])


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

            get_sql_statement = ''' SELECT DateCellColumn, ContainerNumCellColumn, CarrierCellColumn FROM ExcelFileTable WHERE FilePath =? AND SheetName =? '''

            cur.execute(get_sql_statement, [file_path, sheet_name])

            rows = cur.fetchall()

    db_connection.commit()


    db_connection.close()

    return rows

