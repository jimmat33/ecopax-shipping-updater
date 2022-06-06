import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CoscoSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.cosco_search_link = 'https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=CONTAINER&number=' + container_num_list[0]
        self.return_dict = dict()


    def get_options(self, options_obj):
        options_obj.add_experimental_option('excludeSwitches', ['enable-logging'])
        options_obj.add_argument('--headless')
        options_obj.add_argument('--disable-gpu')
        options_obj.add_argument("--incognito")


    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.cosco_search_link)

            print('\n[Connection Alert] Driver Connection to Cosco Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  Cosco Site Connection Failed')
            print('==============================================================================================\n')
            return {}


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

            #adding date to storage data structure
            self.return_dict[self.container_num_list[0]] = [month, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date Cosco')
            print(f'                             Container Num {self.container_num_list[i]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            textbox = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[2]/form/div/div[1]/div/div/div[1]/input')
            textbox.clear()
            textbox.send_keys(self.container_num_list[i])
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[2]/form/div/div[2]/button').click()
        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify search Textbox')
            print('==============================================================================================\n')


    def search(self, container_num_list):
        '''
        This function searches the cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.connect(driver)

        self.pull_date(driver, 0)

        i = 1

        while i < len(container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(3)

                self.pull_date()

            except Exception:
                pass

            i += 1

        driver.close()

        return self.return_dict




