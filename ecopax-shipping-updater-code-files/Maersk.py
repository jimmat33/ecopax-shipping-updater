import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ShippingContainerDB import *
from ShippingUpdaterUtility import get_month_num
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class MaerskSearch(object):

    def __init__(self, container_num):
        self.container_num = container_num
        self.maersk_search_link ='https://www.maersk.com/tracking/' + self.container_num[0]
        self.error_list = []
        self._db_changes = 0

    @property
    def db_changes(self):
        return self._db_changes

    def get_options(self, options_obj):
        options_obj.add_experimental_option('excludeSwitches', ['enable-logging'])
        options_obj.add_argument('--disable-gpu')
        options_obj.add_argument("--incognito")

    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.maersk_search_link)

            print('\n[Connection Alert] Driver Connection to Maersk Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  Maersk Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def bypass_tos(self, driver):
        try:
            try:
                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/button[3]'))).click()
            except Exception:
                driver.find_element(By.CLASS_NAME, 'coi-banner__accept--fixed-margin').click()
    
        except Exception:
            print('\n==============================================================================================')
            print('                                Maersk TOS Bypass Failed')
            print('==============================================================================================\n')


    def pull_date(self, driver):
        try:
            driver.find_element(By.XPATH, '/html/body/main/div/div/form/div/div[2]/mc-button').click()

            str_text = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/div[3]/dl/dd[1]'))).get_attribute('textContent')

            year = str(str_text[-5:-1].strip())

            month = str((str_text[3:-5]).strip())
            month_num = get_month_num(month)

            day = str(str_text[0:3].strip())

            formatted_date = month_num + '/' + day + '/' + year

            #adding date to storage database
            db_update_container(self.container_num[0], formatted_date)
            self._db_changes += 1

        except Exception:
            traceback.print_exc()
            db_update_container(self.container_num[0], 'Date Error')
            print('\n==============================================================================================')
            print('                              Failed to find/process date Maersk')
            print(f'                             Container Num {self.container_num[0]} ')
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
            return []

        self.pull_date(driver)

        driver.close()



def maersk_search():
     maersk_containers = db_get_containers_by_carrier('Maersk')

     if len(maersk_containers) != 0:
        for container_num in maersk_containers:
            maersk_cont = MaerskSearch(container_num)
            maersk_cont.search_algorithm()
            
            if maersk_cont.db_changes == 0:
                for i in range(2):
                    print('\n[Driver Alert] Trying Maersk Search Again\n')
                    for container_num in maersk_containers:
                        maersk_cont = MaerskSearch(container_num)
                        maersk_cont.search_algorithm()

                    if maersk_cont.db_changes != 0:
                        break
            if maersk_cont.db_changes == 0:
                print('\n[Driver Alert] Maersk Search Fatal Error\n')
                cont_props = db_get_container_info(container_num)
                db_add_container([cont_props[0][0], cont_props[0][1], cont_props[0][2], cont_props[0][3]], 'no_search')
                db_remove_container(container_num)

                db_add_error('Maersk Search Failed')



