import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ShippingContainerDB import db_update_container

class CoscoSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.cosco_search_link = 'https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=CONTAINER&number=' + self.container_num_list[0][0]
        self._error_list = []

    @property
    def error_list(self):
        return self._error_list
    @error_list.setter
    def error_list(self, new_error_list):
        self._error_list = new_error_list


    def get_options(self, options):
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')

    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.cosco_search_link)

            print(f'\n[Connection Alert] Driver Connection to Cosco Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  Cosco Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver, i):
        try:
            #finding estimated arrival date in website table
            web_date = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]/p[2]')
        
            #waiting to get date from page and pulling data
            time.sleep(3) 

            str_date = web_date.get_attribute('textContent')

            #properly formatting date of first index in list
            year = str_date[0:4]
            month = str_date[5:7]
            day = str_date[8:10]

            formatted_date = month + '/' + day + '/' + year

            #adding date to storage database
            db_update_container(self.container_num_list[i][0], formatted_date)

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date Cosco')
            print(f'                             Container Num {self.container_num_list[i][0]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            textbox = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[2]/form/div/div[1]/div/div/div[1]/input')
            textbox.clear()
            textbox.send_keys(self.container_num_list[i][0])
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[2]/form/div/div[2]/button').click()
        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Cosco search Textbox')
            print('==============================================================================================\n')


    def search(self):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.connect(driver)

        if len(self.error_list) != 0:
            return {}

        self.pull_date(driver, 0)

        i = 1

        while i < len(self.container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(3)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()




