from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

class HMMSearch(object):

    def __init__(self, container_num):
        self.container_num = container_num
        self.hmm_search_link = 'https://www.hmm21.com/cms/company/engn/index.jsp?type=2&number=' + self.container_num + '&is_quick=Y&quick_params='
        self.return_list = []
        self.error_list = []


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
            str_date = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/form[1]/div/div[6]/table/tbody/tr[3]/td[5]/span'))).get_attribute('textContent')

            month = str_date[3:6]
            day = str_date[0:2]
            year = str_date[7:11:]

            month_num = self.get_month_num(month)  

            #adding date to data structure
            return [month_num, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date HMM')
            print(f'                             Container Num {self.container_num} ')
            print('==============================================================================================\n')



    def search(self, container_num):
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

        driver.close()

        return self.return_list








