'''
! Module of Database functions

This module houses all of the database functions for use
throughout the program
'''
import os
import sqlite3 as sl
from datetime import datetime
import shipping_container


def comp_dates(dt_old_date, new_date):
    '''
    Compares 2 dates

    This function is a helper function that takes 2 dates and compares
    them to see if the date needs to be changed in the database

    Parameters
    ----------
    old_date : date.datetime
        The date pulled from the database
    new_date : string
        The date pulled from the webscraper

    Returns
    -------
    str
        Arrived : Set date to 'arrived'
        new : Set date to date pulled from website
        old : Do nothing, keep date pulled from database
        Date Error : Error, set date to 'Date Error'

    '''
    return_value = ''
    try:
        dt_new_date = datetime.strptime(new_date, "%m/%d/%Y")

        if dt_new_date <= datetime.today():
            return_value = 'Arrived'
        elif dt_old_date == dt_new_date:
            return_value = 'old'
        else:
            return_value = 'new'
    except ValueError as comp_date_error:
        print('\n' + comp_date_error + '\n')
        return_value = 'Date Error'

    return return_value


def db_connect():
    '''
    Creates a connnection to the database

    This function creates a connection to the database for
    use throughout all database actions

    Parameters
    ----------
    None

    Returns
    -------
    database connection object
        A database connection to the shipping-container.db file
    '''

    db_file_name = os.path.abspath('shipping-container.db')
    db_conn = None

    try:
        db_conn = sl.connect(db_file_name)
    except sl.Error as conn_error:
        print('\n' + conn_error + '\n')

    return db_conn


def db_get_no_search_cont():
    '''
    Gets containers that were not searched

    This function connects to the database and retrieves
    all the containers from the NoSearchTable

    Parameters
    ----------
    None

    Returns
    -------
    list
        A list of shipping container objects with 'no search' as the Carrier Name
    '''
    db_connection = db_connect()
    cont_list = []

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT ContainerNum, FilePath, SheetName, ContainerNumCellLocation
                                FROM NoSearchContainerTable '''

        cur.execute(get_sql_statement)
        rows = cur.fetchall()

        db_connection.commit()

    db_connection.close()

    for row in rows:
        cont_num = row[0]
        cont_fp = row[1].split('<')
        cont_sheet = row[2].split('<')
        cont_num_loc = row[3].split('<')

        cont = shipping_container
        cont.cont_num = cont_num
        cont.carrier_company = None
        cont.arrival_date = None
        cont.wb_file_path = cont_fp
        cont.wb_sheet = cont_sheet
        cont.container_num_cell_location = cont_num_loc
        cont.date_cell_location = None

        cont_list.append(cont)

    return cont_list


def db_set_all_cont_false():
    '''
    Sets all containers date changed property to 'False' in the database

    This function connects to the database and sets the date changed
    property to 'False' for every entry.  This is run at the end of the
    program to avoid errors when running more than 1 search in an
    application instance

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDateChanged =? '''
        cur.execute(get_sql_statement, ['False'])
        db_connection.commit()

    db_connection.close()


def db_get_all_containers(search_type):
    '''
    Gets all containers from database

    This function connects to the database and gets all of the
    containers from the database

    Parameters
    ----------
    search_type : str
        The type of search to be run (unmod, gui, modified)

    Returns
    -------
    list
        A list of shipping container objects dependent on search_type
    '''
    db_connection = db_connect()
    cont_list = []

    with db_connection:
        cur = db_connection.cursor()

        if search_type == 'unmod':
            get_sql_statement = ''' SELECT ContainerNum, CarrierCompany, ArrivalDate, FilePath,
                                    SheetName, ContainerNumCellLocation, DateCellLocation
                                    FROM ShippingContainerTable WHERE ArrivalDateChanged =? '''
            cur.execute(get_sql_statement, ['False'])
        elif search_type == 'gui':
            get_sql_statement = ''' SELECT ContainerNum, CarrierCompany, ArrivalDate, FilePath
                                    FROM ShippingContainerTable '''
            cur.execute(get_sql_statement)
        else:
            get_sql_statement = ''' SELECT ContainerNum, CarrierCompany, ArrivalDate, FilePath,
                                    SheetName, ContainerNumCellLocation, DateCellLocation
                                    FROM ShippingContainerTable WHERE ArrivalDateChanged =? '''
            cur.execute(get_sql_statement, ['True'])

        rows = cur.fetchall()

        db_connection.commit()

    db_connection.close()

    for row in rows:
        cont_num = row[0]
        carrier = row[1]
        arrival_date = row[2]
        cont_fp = row[3].split('<')
        cont_sheet = row[4].split('<')
        cont_num_loc = row[5].split('<')
        cont_date_loc = row[6].split('<')

        cont = shipping_container
        cont.cont_num = cont_num
        cont.carrier_company = carrier
        cont.arrival_date = arrival_date
        cont.wb_file_path = cont_fp
        cont.wb_sheet = cont_sheet
        cont.container_num_cell_location = cont_num_loc
        cont.date_cell_location = cont_date_loc

        cont_list.append(cont)

    return cont_list


def db_get_all_excel_files():
    '''
    Gets all excel file filepaths and sheets from database

    This function connects to the database and gets
    all of the excel file entries' filepaths and sheets
    in the ExcelFileTable

    Parameters
    ----------
    None

    Returns
    -------
    list
        Returns a list of excel file properties
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT FilePath, SheetName FROM ExcelFileTable '''
        cur.execute(get_sql_statement)
        rows = cur.fetchall()

        db_connection.commit()

    db_connection.close()

    return rows


def db_get_cont_info(cont_num):
    '''
    Gets information about a shipping container

    This function connects to the database and finds the
    properties of a specific container entry based on the
    given container number

    Parameters
    ----------
    cont_num : str
        A container number to be searched for

    Returns
    -------
    list
        A list of properties all properties associated with the container
        number in the database
    '''
    db_connection = db_connect()
    prop_list = []

    with db_connection:
        cur = db_connection.cursor()
        get_sql_statement = ''' SELECT ContainerNum, Filepath, SheetName,
                                ContainerNumCellLocation, ArrivalDate
                                FROM ShippingContainerTable WHERE ContainerNum =? '''
        cur.execute(get_sql_statement, [cont_num[0]])

        prop_list = cur.fetchall()
        db_connection.commit()

    db_connection.close()

    return prop_list


def db_remove_cont(cont_num):
    '''
    Removes shipping container from database

    This function removes shipping containers from the connected
    database based on container number

    Parameters
    ----------
    cont_num : str
        A container number to be searched for

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        try:
            cur = db_connection.cursor()
            remove_sql_statement = ''' DELETE FROM ShippingContainerTable WHERE ContainerNum =? '''
            cur.execute(remove_sql_statement, [cont_num])
        except sl.Error as delete_error:
            print('\n' + delete_error + '\n')

        db_connection.commit()

    db_connection.close()


def db_get_cont_by_carrier(carrier):
    '''
    Gets specific carrier's containers from database

    This function connects to the database and pulls out
    all of the container numbers that correspond to the given
    carrier

    Parameters
    ----------
    carrier : str
        The name of the carrier to pull containers for

    Returns
    list
        A list of tuples where each tuple contains a container number string
    '''
    db_connection = db_connect()
    container_list = []

    with db_connection:
        try:
            cur = db_connection.cursor()

            get_sql_statement = ''' SELECT ContainerNum, CarrierCompany, ArrivalDate, Filepath,
                                    SheetName, ContainerNumCellLocation, DateCellLocation
                                    FROM ShippingContainerTable WHERE CarrierCompany =?
                                        AND (ArrivalDate !=? OR ArrivalDate IS NULL) '''

            cur.execute(get_sql_statement, [carrier, 'arrived'])

            container_list = cur.fetchall()
        except sl.Error as fetch_error:
            print('\n' + fetch_error + '\n')

        db_connection.commit()

    db_connection.close()

    return container_list


def check_cont_updates(cont_prop_lst, db_return):
    '''
    Gets new property list for a given container

    This function compares the current list of container properties
    in the database and the new instance of container properties and
    adds new filepaths, sheet names, container num cell locations and
    container date cell locations where necessary

    Parameters
    ----------
    cont_prop_lst : list
        A list of properties for the new container instance
    db_return : list
        A list of tuples that contain container properties pulled
        from the database

    Returns
    -------
    list
        A list of updated properties so the container can be
        correctly updated in the database
    '''
    old_container_num_location = db_return[0][2]
    old_date_location = db_return[0][3]
    old_file_path = db_return[0][0]
    old_sheet = db_return[0][1]

    if old_file_path != cont_prop_lst[3]:
        updated_file_path = old_file_path + '<' + cont_prop_lst[3]
        updated_sheet = old_sheet + '<' + cont_prop_lst[4]
        updated_num_loc = old_container_num_location + '<' + cont_prop_lst[5]
        updated_date_loc = old_date_location + '<' + cont_prop_lst[6]
    elif old_sheet != cont_prop_lst[4]:
        updated_file_path = old_file_path
        updated_sheet = old_sheet + '<' + cont_prop_lst[4]
        updated_num_loc = old_container_num_location + '<' + cont_prop_lst[5]
        updated_date_loc = old_date_location + '<' + cont_prop_lst[6]
    elif (old_sheet == cont_prop_lst[4] and
            (old_container_num_location != cont_prop_lst[5]
                and old_date_location != cont_prop_lst[6])):
        updated_file_path = old_file_path
        updated_sheet = old_sheet
        updated_num_loc = cont_prop_lst[5]
        updated_date_loc = cont_prop_lst[6]
    else:
        updated_file_path = old_file_path
        updated_sheet = old_sheet
        updated_num_loc = old_container_num_location
        updated_date_loc = old_date_location

    return [cont_prop_lst[2], updated_num_loc, updated_date_loc,
            updated_file_path, updated_sheet, cont_prop_lst[0]]


def db_add_cont(cont_prop_list, table_type):
    '''
    Adds a container to the database

    This function connects to the database and checks to
    make sure that the database has all of the proper
    excel file and sheet locations if the container is
    already in the database.  If the container is not in
    the database, it will add it

    Parameters
    ----------
    cont_prop_list : list
        A list of container properties to be added
    table_type : str
        A string denoting the table that the container
        properties should be added to

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT FilePath, SheetName, ContainerNumCellLocation,
                                DateCellLocation FROM ShippingContainerTable
                                 WHERE ContainerNum =? '''

        cur.execute(get_sql_statement, [cont_prop_list[0]])
        db_return = cur.fetchall()

        if len(db_return) != 0 and table_type != 'no search':
            new_prop_list = check_cont_updates(cont_prop_list, db_return)

            update_sql_statement = ''' UPDATE ShippingContainerTable SET ArrivalDate =?,
                                       ContainerNumCellLocation =?, DateCellLocation =?,
                                       Filepath =?, SheetName =?
                                        WHERE ContainerNum =? '''
            cur.execute(update_sql_statement, new_prop_list)
        elif table_type == 'reg':
            add_sql_statement = ''' INSERT INTO ShippingContainerTable(ContainerNum, CarrierCompany,
                                    ArrivalDate, FilePath, SheetName, ContainerNumCellLocation,
                                    DateCellLocation, DateAdded, ArrivalDateChanged)
                                     VALUES(?,?,?,?,?,?,?,?,?) '''

            cur.execute(add_sql_statement, cont_prop_list)
        else:
            add_sql_statement = ''' INSERT INTO NoSearchContainerTable(ContainerNum, FilePath,
                                    SheetName, ContainerNumCellLocation)
                                     VALUES(?,?,?,?) '''

            cur.execute(add_sql_statement, cont_prop_list)

        db_connection.commit()

    db_connection.close()


def db_update_cont(cont_num, cont_date):
    '''
    Updates container dates in the database

    This function connects to the database and updates the container
    entry if needed

    Parameters
    ----------
    cont_num : str
        The container number to search for
    cont_date : str
        The date pulled from the web scraper that
        the cont_num corresponds to

    Returns
    -------
    None
    '''
    db_connection = db_connect()
    update_sql_statement = ''' UPDATE ShippingContainerTable
                                SET ArrivalDate =?, ArrivalDateChanged =?
                                 WHERE ContainerNum =? '''

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT ArrivalDate
                                 FROM ShippingContainerTable
                                  WHERE ContainerNum =? '''
        cur.execute(get_sql_statement, [cont_num])
        old_date = cur.fetchall()[0][0]
        date_convertable = False

        try:
            dt_old_date = datetime.strptime(old_date, "%m/%d/%Y")
            date_convertable = True
            date_comp = comp_dates(dt_old_date, cont_date)
        finally:
            pass

        if not(date_convertable) or date_comp == 'new':
            cur.execute(update_sql_statement, [cont_date, 'True', cont_num])

        if date_comp != 'old':
            cur.execute(update_sql_statement, [date_comp, 'True', cont_num])

        db_connection.commit()

    db_connection.close()


def db_add_excel_file(excel_prop_list):
    '''
    Adds an excel file entry to the database

    This function takes a list of excel file properties
    and adds them to the database, or it updates existing
    excel file entries

    Parameters
    ----------
    excel_prop_list : list
        A list of all properties needed to create an excel file entry

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        try:
            cur = db_connection.cursor()

            cur.execute(''' SELECT FilePath, SheetName FROM ExcelFileTable ''')
            rows = cur.fetchall()

            success = False

            for row in rows:
                if row[0] == excel_prop_list[0] and row[1] == excel_prop_list[1]:
                    add_sql_statement = ''' UPDATE ExcelFileTable Set DateCellColumn =?,
                                            ContainerNumCellColumn =?,  CarrierCellColumn =?
                                             WHERE FilePath =? AND SheetName =? '''

                    first_half_list = excel_prop_list[2:]
                    extra_prop_list = excel_prop_list[0:2]

                    cur.execute(add_sql_statement, (first_half_list + extra_prop_list))

                    success = True

            if not success:
                raise sl.Error

        except sl.Error:
            cur = db_connection.cursor()

            insert_sql_statement = ''' INSERT INTO ExcelFileTable(FilePath, SheetName,
                                        DateCellColumn, ContainerNumCellColumn, CarrierCellColumn)
                                         VALUES (?,?,?,?,?) '''

            cur.execute(insert_sql_statement, excel_prop_list)

        db_connection.commit()

    db_connection.close()


def db_get_excel_file_info(file_path, sheet_name):
    '''
    Gets the column data types

    This function gets all the data types of the pertitent columns
    from the database based on a filepath and sheet name

    Parameters
    ---------
    file_path : str
        A string of a filepath
    sheet_name : str
        The name of an excel sheet on the given filepath

    Returns
    list
        A list of column numbers for the necessary
        data points
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT DateCellColumn, ContainerNumCellColumn, CarrierCellColumn
                                 FROM ExcelFileTable WHERE FilePath =?
                                  AND SheetName =? '''

        cur.execute(get_sql_statement, [file_path, sheet_name])

        rows = cur.fetchall()

        db_connection.commit()

    db_connection.close()

    return rows


def db_get_all_excel_filepaths():
    '''
    Gets all excel file filepaths

    This function connects to the database and pulls all of
    the excel filepaths from each entry in the ExcelFileTable

    Parameters
    ----------
    None

    Returns
    --------
    list
        A list of tuples containing excel filepath strings
    '''
    db_connection = db_connect()
    file_list = []

    with db_connection:
        cur = db_connection.cursor()

        get_file_sql_statement = ''' SELECT FilePath FROM ExcelFileTable'''

        try:
            cur.execute(get_file_sql_statement)

        except sl.Error:
            pass

        file_list = cur.fetchall()
        db_connection.commit()

    db_connection.close()

    return file_list


def db_remove_excel_file(file_path):
    '''
    Removes an excel file from all aspects of the database

    This fucntion connects to the database and removes any data related to a specific
    filepath from all database tables

    Parameters
    ----------
    file_path : str
        A string of an excel workbook filepath

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        remove_file_sql_statement_1 = ''' DELETE FROM NoSearchContainerTable WHERE FilePath =? '''
        remove_file_sql_statement_2 = ''' DELETE FROM ShippingContainerTable WHERE FilePath =? '''
        remove_file_sql_statement_3 = ''' DELETE FROM ExcelFileTable WHERE FilePath =? '''

        try:
            cur.execute(remove_file_sql_statement_1, [file_path])
            cur.execute(remove_file_sql_statement_2, [file_path])
            cur.execute(remove_file_sql_statement_3, [file_path])
        except sl.Error:
            pass

        db_connection.commit()

    db_connection.close()


def db_clear_database():
    '''
    Truncates all database data

    This function connects the database and removes all the data
    from every table

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        remove_file_sql_statement_1 = ''' DELETE FROM NoSearchContainerTable '''
        remove_file_sql_statement_2 = ''' DELETE FROM ShippingContainerTable '''
        remove_file_sql_statement_3 = ''' DELETE FROM ExcelFileTable '''
        remove_file_sql_statement_4 = ''' DELETE FROM ErrorTable '''

        try:
            cur.execute(remove_file_sql_statement_1)
            cur.execute(remove_file_sql_statement_2)
            cur.execute(remove_file_sql_statement_3)
            cur.execute(remove_file_sql_statement_4)
        except sl.Error:
            pass

        db_connection.commit()

    db_connection.close()


def db_add_error(error_str):
    '''
    Adds an error entry to the database

    This function connects to the database and adds an
    error entry to the ErrorTable

    Parameters
    ----------
    error_str : str
        A string containing an error message

    Returns
    -------
    None
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        add_sql_statement = ''' INSERT INTO ErrorTable(ErrorDesc) VALUES(?) '''

        try:
            cur.execute(add_sql_statement, [error_str])
        except sl.Error:
            pass

        db_connection.commit()

    db_connection.close()


def db_get_all_errors():
    '''
    Gets all errors from the database

    This function connects to the database and gets all the errors
    to populate the error treeview of the gui

    Parameters
    ----------
    None

    Returns
    -------
    list
        A list of tuples containing error strings
    '''
    db_connection = db_connect()

    with db_connection:
        cur = db_connection.cursor()

        get_sql_statement = ''' SELECT ErrorDesc FROM ErrorTable '''

        try:
            cur.execute(get_sql_statement)

            rows = cur.fetchall()
        except sl.Error:
            pass

        db_connection.commit()

    db_connection.close()

    return rows
