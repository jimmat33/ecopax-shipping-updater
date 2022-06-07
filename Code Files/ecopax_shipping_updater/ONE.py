import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

class ONESearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.one_search_link = 'https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking'
        self.return_dict = dict()
        self.error_list = []


    def get_options(self, options_obj):
        options_obj.add_experimental_option('excludeSwitches', ['enable-logging'])
        options_obj.add_argument('--headless')
        options_obj.add_argument('--disable-gpu')
        options_obj.add_argument("--incognito")


    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.one_search_link)

            print('\n[Connection Alert] Driver Connection to ONE Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  ONE Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def original_search(self, driver):
        try:
            #Finding the frame so site can be interactive
            frame = driver.find_element(By.CSS_SELECTOR, '#__next > main > div > div.MainLayout_one-container__4HS_a > div > div.IframeCurrentEcom_wrapper__qvnCe > iframe')
            driver.switch_to.frame(frame)

            #Selecting container number from dropdown
            select = Select(driver.find_element(By.NAME, 'searchType'))
            select.select_by_visible_text('Container No.')

            #Entering container number in textbox and clicking for search
            textbox = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/table/tbody/tr/td/div/textarea')
            textbox.clear()
            textbox.send_keys(self.container_num_list[0])
            driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/div[1]/div[1]/button/span').click()

            time.sleep(0.5)

        except:
            print('\n==============================================================================================')
            print('                                  Failed to use ONE Search')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver, i):
        try:
            arrival_text = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/div[8]/table/tbody/tr[10]/td[4]').get_attribute('textContent')

            #date formatting
            month = arrival_text[-11:-9]
            day = arrival_text[-8:-6]
            year = arrival_text[-16:-12]

            #adding date to storage data structure
            self.return_dict[self.container_num_list[i]] = [month, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date ONE')
            print(f'                             Container Num {self.container_num_list[i]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            textbox = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/table/tbody/tr/td/div/textarea')
            textbox.clear()
            textbox.send_keys(self.container_num_list[i])
            driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/form/div[1]/div[1]/button/span').click()
        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify ONE search Textbox')
            print('==============================================================================================\n')


    def search(self, container_num_list):
        '''
        This function searches the ONE site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.connect(driver)

        self.original_search(driver)

        if len(self.error_list) != 0:
            return {}

        self.pull_date(driver, 0)

        i = 1

        while i < len(container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(1)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()

        return self.return_dict
