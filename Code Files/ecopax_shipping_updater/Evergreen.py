import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ShippingContainerDB import *
from ShippingUpdaterUtility import get_month_num

class EvergreenSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.evergreen_search_link = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
        self.error_list = []
        self._db_changes = 0

    @property
    def db_changes(self):
        return self._db_changes


    def get_options(self, options):
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')

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

            month_num = get_month_num(month)

            formatted_date = month_num + '/' + day + '/' + year

            #adding date to storage database
            db_update_container(self.container_num_list[i][0], formatted_date)
            self._db_changes += 1

        except Exception:
            db_update_container(self.container_num_list[i][0], 'Date Error')
            print('\n==============================================================================================')
            print('                              Failed to find/process date Evergreen')
            print(f'                             Container Num {self.container_num_list[i][0]} ')
            print('==============================================================================================\n')


    def original_search(self, driver, i):
        try:
            #accessign textbox, inputting number and clicking search
            textbox = driver.find_element(By.XPATH, '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]')                                        
            textbox.clear()
            textbox.send_keys(self.container_num_list[i][0])
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
            textbox.send_keys(self.container_num_list[i][0])
            driver.find_element(By.XPATH, '/html/body/div[5]/center/table[1]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[2]/input[2]').click()

        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Evergreen search textbox')
            print('==============================================================================================\n')


    def search_algorithm(self):
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

        while i < len(self.container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(2)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()


def evergreen_search():

    evergreen_search_list = db_get_containers_by_carrier('Evergreen')

    evergreen = EvergreenSearch(evergreen_search_list)

    if len(evergreen_search_list) != 0:
        evergreen.search_algorithm()
        if evergreen.db_changes == 0:
            for i in range(2):
                print('\n[Driver Alert] Trying Evergreen Search Again\n')
                evergreen.search_algorithm()
                if evergreen.db_changes != 0:
                    break
        if evergreen.db_changes == 0:
            print('\n[Driver Alert] Evergreen Search Fatal Error\n')
            for cont in evergreen_search_list:
                cont_props = db_get_container_info(cont)
                db_add_container([cont_props[0][0], cont_props[0][1], cont_props[0][2], cont_props[0][3]], 'no_search')
                db_remove_container(cont)









