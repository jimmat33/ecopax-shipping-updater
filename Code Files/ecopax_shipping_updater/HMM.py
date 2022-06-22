from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from ShippingContainerDB import *
from ShippingUpdaterUtility import get_month_num


class HMMSearch(object):

    def __init__(self, container_num):
        self.container_num = container_num
        self.hmm_search_link = 'https://www.hmm21.com/cms/company/engn/index.jsp?type=2&number=' + self.container_num[0] + '&is_quick=Y&quick_params='
        self.return_list = []
        self.error_list = []
        self._db_changes = 0

    @property
    def db_changes(self):
        return self._db_changes

    def get_options(self, options_obj):
        options_obj.add_argument('--disable-gpu')
        options_obj.add_argument("--incognito")


    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.hmm_search_link)

            print('\n[Connection Alert] Driver Connection to HMM Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  HMM Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')

    
    def modify_search(self, driver):
        try:
            selector = Select(driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/form/fieldset/p/span[1]/select'))
            selector.select_by_visible_text('Container No.')

            driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/form/fieldset/p/span[3]/a').click()

            # Store the ID of the original window
            original_window = driver.current_window_handle

            wait = WebDriverWait(driver, 3)

            wait.until(EC.number_of_windows_to_be(2))

            # Loop through until we find a new window handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            # Wait for the new tab to finish loading content
            wait.until(EC.title_is("HMM Customer Plus"))

            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/button[2]'))).click()

        except:
            print('\n==============================================================================================')
            print('                                  Failed to use HMM site search')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def pull_date(self, driver):
        try:
            #switching to frame to get date
            frame = driver.find_element(By.CSS_SELECTOR, '#_frame1')
            driver.switch_to.frame(frame)

            #finding and processing date
            str_date = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/form[1]/div/div[6]/table/tbody/tr[3]/td[4]/span'))).get_attribute('textContent')

            month = str_date[3:6]
            day = str_date[0:2]
            year = str_date[7:11:]

            month_num = get_month_num(month)  

            formatted_date = month_num + '/' + day + '/' + year

            #adding date to storage database
            db_update_container(self.container_num[0], formatted_date)
            

            driver.close()

            driver.switch_to.window(driver.window_handles[0])

            driver.close()

            self._db_changes += 1

        except Exception:
            db_update_container(self.container_num[0][0], 'Date Error')
            print('\n==============================================================================================')
            print('                              Failed to find/process date HMM')
            print(f'                              Container Num {self.container_num[0]} ')
            print('==============================================================================================\n')



    def search_algorithm(self):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = uc.Chrome(options=options)

        self.connect(driver)

        self.modify_search(driver)

        if len(self.error_list) != 0:
            return []

        self.pull_date(driver)



def hmm_search():
     hmm_containers = db_get_containers_by_carrier('HMM')

     if len(hmm_containers) != 0:
        for container_num in hmm_containers:
            hmm_cont = HMMSearch(container_num)
            hmm_cont.search_algorithm()
            
            if hmm_cont.db_changes == 0:
                for i in range(2):
                    print('\n[Driver Alert] Trying HMM Search Again\n')
                    for container_num in hmm_containers:
                        hmm_cont = HMMSearch(container_num)
                        hmm_cont.search_algorithm()

                    if hmm_cont.db_changes != 0:
                        break
            if hmm_cont.db_changes == 0:
                print('\n[Driver Alert] HMM Search Fatal Error\n')
                cont_props = db_get_container_info(container_num)
                db_add_container([cont_props[0][0], cont_props[0][1], cont_props[0][2], cont_props[0][3]], 'no_search')
                db_remove_container(container_num)







