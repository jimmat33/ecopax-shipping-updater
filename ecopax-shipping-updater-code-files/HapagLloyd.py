import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    import undetected_chromedriver as uc
except Exception:
    db_add_error('Chrome Needs to be Updated - Cannot Search')
    
    

from selenium.webdriver.common.by import By
from ShippingContainerDB import *

class HapagSearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.hapag_search_link = 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html'
        self.error_list = []
        self._db_changes = 0

    @property
    def db_changes(self):
        return self._db_changes

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
        time.sleep(7)

        try:
            try:
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-recommended-btn-handler"]'))).click()

            except Exception:
                 WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "save-preference-btn-handler onetrust-close-btn-handler"))).click()

            time.sleep(0.5)
    
        except Exception:
            print('\n==============================================================================================')
            print('                                Hapag-Lloyd TOS Bypass Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver, i):
        time.sleep(5)
        try:
            table_text = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table')
            str_text = table_text.get_attribute('textContent')
            index = str_text.find("Vessel arrival")

            target_text = str_text[index:]
            date_text = target_text[(target_text.find("20")):]

            year = date_text[0:4]
            month = date_text[5:7]
            day = date_text[8:10]

            formatted_date = month + '/' + day + '/' + year

            #adding date to storage database
            db_update_container(self.container_num_list[i][0], formatted_date)
            self._db_changes += 1
        except TimeoutError:
            driver.refresh()

        except Exception:
            db_update_container(self.container_num_list[i][0], 'Date Error')
            print('\n==============================================================================================')
            print('                              Failed to find/process date Hapag-Lloyd')
            print(f'                             Container Num {self.container_num_list[i][0]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            textbox = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input')
            textbox.clear()
            textbox.send_keys(self.container_num_list[i][0])

            driver.find_element(By.ID, 'tracing_by_container_f:hl25').click()

        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify Hapag-Lloyd search Textbox')
            print('==============================================================================================\n')


    def search_algorithm(self):
        '''
        This function searches the Hapag-Lloyd site for the estimated arrival date of a list of crate numbers
        '''
        driver = uc.Chrome()
        driver.set_page_load_timeout(25)

        self.connect(driver)

        self.bypass_tos(driver)

        if len(self.error_list) != 0:
            driver.close()
            return {}
        
        time.sleep(5)
        self.modify_search(driver, 0)

        self.pull_date(driver, 0)

        i = 1

        while i < len(self.container_num_list):
            try:
                self.modify_search(driver, i)

                time.sleep(1)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()


def hapag_search():

    hapag_search_list = db_get_containers_by_carrier('Hapag-Lloyd')

    hapag = HapagSearch(hapag_search_list)

    if len(hapag_search_list) != 0:
        hapag.search_algorithm()
        if hapag.db_changes == 0:
            for i in range(5):
                print('\n[Driver Alert] Trying Hapag-Lloyd Search Again\n')
                hapag.search_algorithm()
                if hapag.db_changes != 0:
                    break
        if hapag.db_changes == 0:
            print('\n[Driver Alert] Hapag-Lloyd Search Fatal Error\n')
            for cont in hapag_search_list:
                cont_props = db_get_container_info(cont)
                db_add_container([cont_props[0][0], cont_props[0][1], cont_props[0][2], cont_props[0][3]], 'no_search')
                db_remove_container(cont)

            db_add_error('Hapag-Lloyd Search Failed')









