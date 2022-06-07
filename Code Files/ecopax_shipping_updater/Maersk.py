from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ecopax_shipping_updater import get_month_num

class MaerskSearch(object):

    def __init__(self, container_num):
        self.container_num = container_num
        self.maersk_search_link ='https://www.maersk.com/tracking/' + self.container_num
        self.return_list = []
        self.error_list = []


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
            except:
                driver.find_element(By.CLASS_NAME, 'coi-banner__accept--fixed-margin').click()
    
        except Exception:
            print('\n==============================================================================================')
            print('                                Maersk TOS Bypass Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver):
        try:
            str_text = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/div[3]/dl/dd[1]'))).get_attribute('textContent')

            year = str(str_text[-5:-1].strip())

            month = str((str_text[3:-5]).strip())
            month_num = get_month_num(month)

            day = str(str_text[0:3].strip())

            self.return_list = [month_num, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date Maersk')
            print(f'                             Container Num {self.container_num} ')
            print('==============================================================================================\n')



    def search(self, container_num):
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

        return self.return_list




