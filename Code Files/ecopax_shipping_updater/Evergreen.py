import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class EvergreenSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.evergreen_search_link = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
        self.return_dict = dict()
        self.error_list = []


    def get_options(self, options):
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
       #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')


    def get_month_num(self, month):
        '''
        This function takes a month as a word and returns it as the respective number of the month for
        proper date formatting
        '''
        if month == 'January' or month == 'JAN' or month == 'Jan':
            return '01'
        elif month == 'February' or month == 'FEB' or month == 'Feb':
            return '02'
        elif month == 'March' or month == 'MAR' or month == 'Mar':
            return '03'
        elif month == 'April' or month == 'APR' or month == 'Apr':
            return '04'
        elif month == 'May' or month == 'MAY' or month == 'May':
            return '05'
        elif month == 'June' or month == 'JUN' or month == 'Jun':
            return '06'
        elif month == 'July' or month == 'JUL' or month == 'Jul':
            return '07'
        elif month == 'August' or month == 'AUG' or month == 'Aug':
            return '08'
        elif month == 'September' or month == 'SEP' or month == 'Sep':
            return '09'
        elif month == 'October' or month == 'OCT' or month == 'Oct':
            return '10'
        elif month == 'November' or month == 'NOV' or month == 'Nov':
            return '11'
        elif month == 'December' or month == 'DEC' or month == 'Dec':
            return '12'
        else:
            return 'ERROR'

    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.evergreen_search_link)

            print('\n[Connection Alert] Driver Connection to Evergreen Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  Evergreen Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def bypass_tos(self, driver):
        try:
            driver.find_element(By.XPATH, '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input').click()
        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to bypass Evergreen TOS')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')

    def pull_date(self, driver, i):
        try:
            str_date = driver.find_element(By.XPATH, '/html/body/div[5]/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td').get_attribute('textContent')

            month = str_date[28:31]
            day = str_date[32:34]
            year = str_date[35:]

            month_num = self.get_month_num(month)

            #adding entry to data structure
            self.return_dict[self.container_num_list[i]] = [month_num, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date Evergreen')
            print(f'                             Container Num {self.container_num_list[i]} ')
            print('==============================================================================================\n')


    def original_search(self, driver, i):
        try:
            #accessign textbox, inputting number and clicking search
            textbox = driver.find_element(By.XPATH, '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]')                                        
            textbox.clear()
            textbox.send_keys(self.container_num_list[i])
            driver.find_element(By.XPATH, '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]').click()

        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Evergreen search textbox')
            print('==============================================================================================\n')

    def modify_search(self, driver, i):
        try:
            #accessign textbox, inputting number and clicking search
            textbox = driver.find_element(By.XPATH, '/html/body/div[5]/center/table[1]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[2]/input[1]')                                        
            textbox.clear()
            textbox.send_keys(self.container_num_list[i])
            driver.find_element(By.XPATH, '/html/body/div[5]/center/table[1]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[2]/input[2]').click()

        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Evergreen search textbox')
            print('==============================================================================================\n')


    def search(self, container_num_list):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.connect(driver)

        self.bypass_tos(driver)

        if len(self.error_list) != 0:
            return {}

        self.original_search(driver, 0)

        self.pull_date(driver, 0)

        i = 1

        while i < len(container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(2)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()

        return self.return_dict








