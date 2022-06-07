import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class HapagSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.hapag_search_link = 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html'
        self.return_dict = dict()
        self.error_list = []

    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.hapag_search_link)

            print('\n[Connection Alert] Driver Connection to Hapag-Lloyd Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  Hapag=Lloyd Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def bypass_tos(self, driver):
        try:
            try:
                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[2]/div[3]/div[1]/button[2]'))).click()

                driver.minimize_window()
            except:
                driver.find_element(By.ID, "accept=recommended=btn=handler").click()

                driver.minimize_window()

            time.sleep(0.5)
    
        except Exception:
            print('\n==============================================================================================')
            print('                                Hapag-Lloyd TOS Bypass Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver, i):
        try:
            table_text = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table')
            str_text = table_text.get_attribute('textContent')
            index = str_text.find("Vessel arrival")

            target_text = str_text[269:]
            date_text = target_text[(target_text.find("20")):]

            year = date_text[0:4]
            month = date_text[5:7]
            day = date_text[8:10]

            self.return_dict[self.container_num_list[i]] = [month, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date Hapag-Lloyd')
            print(f'                             Container Num {self.container_num_list[i]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            textbox = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input')
            textbox.clear()
            textbox.send_keys(self.container_num_list[i])
            driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/button').click()
        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Hapag-Lloyd search Textbox')
            print('==============================================================================================\n')


    def search(self, container_num_list):
        '''
        This function searches the Hapag-Lloyd site for the estimated arrival date of a list of crate numbers
        '''
        driver = uc.Chrome()

        self.connect(driver)

        self.bypass_tos(driver)

        if len(self.error_list) != 0:
            return {}
        
        self.modify_search(driver, 0)

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








