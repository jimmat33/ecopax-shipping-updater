import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from os import listdir
from os.path import isfile, join


class CMASearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.cma_search_link = 'https://www.cma-cgm.com/ebusiness/tracking'
        self.speech_to_text_link = 'https://speech-to-text-demo.ng.bluemix.net/'
        self.return_dict = dict()
        self.error_list = []

        abs_path = os.path.abspath('ecopax-shipping-updater')
        self.use_path = abs_path + '\\' + 'Audio Captcha Files'

    def random_sleep(self):
        sleep_time = random.uniform(0.25, 1.25)
        time.sleep(sleep_time)

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

    def get_date_from_cma(self, given_str):
        '''
        This function is specifically used for CMA CGM, it takes the raw data from their website and
        returns a string that can be used to create the proper date for adding to the container's
        dictionary entry
        '''
        start_index = 0

        #This if block is checking for the days of the week and then using that as a basis for the starting index of the date
        if given_str.find("Sunday") != -1:
            start_index = given_str.find("Sunday") + len("Sunday") + 1
        elif given_str.find("Monday") != -1:
            start_index = given_str.find("Monday") + len("Monday") + 1
        elif given_str.find("Tuesday") != -1:
            start_index = given_str.find("Tuesday") + len("Tuesday") + 1 
        elif given_str.find("Wednesday") != -1:
            start_index = given_str.find("Wednesday") + len("Wednesday") + 1
        elif given_str.find("Thursday") != -1:
            start_index = given_str.find("Thursday") + len("Thursday") + 1
        elif given_str.find("Friday") != -1:
            start_index = given_str.find("Friday") + len("Friday") + 1
        elif given_str.find("Saturday") != -1:
            start_index = given_str.find("Saturday") + len("Saturday") + 1
        elif given_str.find("Sunday") != -1:
            start_index = given_str.find("Sunday") + len("Sunday") + 1
        else:
            return 'ERROR'

        actual_date = given_str[start_index:(start_index + 11)]

        return actual_date


    def get_options(self, options):
        prefs = {"profile.default_content_settings.popups": 0, "download.default_directory": self.use_path, "directory_upgrade": True}

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_experimental_option("prefs", prefs)


    def connect(self, driver):
        try: 
            driver.implicitly_wait(0.5)
            driver.get(self.cma_search_link)

            print('\n[Connection Alert] Driver Connection to CMA CGM Site Successful\n')

        except Exception:
            print('\n==============================================================================================')
            print('                                  CMA CGM Site Connection Failed')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def bypass_audio_captcha(self, driver):
        try:
            time.sleep(1)
            frame = driver.find_element_by_css_selector('body > iframe')
            driver.switch_to.frame(frame)

            time.sleep(2)
            try:
                WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div/div[3]/div/div/div[2]/div[1]'))).click()
            except Exception:
                pass
            
            self.random_sleep()
            time.sleep(3)

            try:
                WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/a[4]'))).click()
            except Exception:
                pass

            time.sleep(5)
            audio_src_link = WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.TAG_NAME, 'audio'))).get_attribute('currentSrc')

            time.sleep(2)
            driver.execute_script("window.open('');")
  
            # Switch to the new window and open new URL
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            driver.get(audio_src_link)

            self.random_sleep()

            driver.execute_script('''let aLink = document.createElement("a");let videoSrc = document.querySelector("video").firstChild.src;aLink.href = videoSrc;aLink.download = "";aLink.click();aLink.remove();''')


            driver.execute_script("window.open('');")
  
            # Switch to the new window and open new URL
            driver.switch_to.window(driver.window_handles[2])

            time.sleep(2)

            driver.get(self.speech_to_text_link)

            onlyfiles = [f for f in listdir(self.use_path) if isfile(join(self.use_path, f))]

            time.sleep(5)
                
            root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
            btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')

            file_str = onlyfiles[0]
            send_keys_str = self.use_path + '\\' + file_str

            btn.send_keys(send_keys_str)

            time.sleep(15)
            #btn.send_keys(path)

            # Audio to text is processing
            text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')

            result = " ".join( [ each.text for each in text ] )
            key_str = result[33:-1]

            driver.switch_to.window(driver.window_handles[0])

            self.random_sleep()

            frame = driver.find_element_by_css_selector('body > iframe')
            driver.switch_to.frame(frame)
            time.sleep(2)

            textbox = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/input')

            for num in key_str:
                self.random_sleep()
                textbox.send_keys(num)
                time.sleep(0.5)

            self.random_sleep()
            time.sleep(4)
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[4]').click()

            os.remove(send_keys_str)

        except Exception:
            print('\n===============================================================================================')
            print('                              CMA CGM Audio Captcha Bypass Failed')
            print('===============================================================================================\n')
            self.error_list.append('ERROR') 


    def pull_date(self, driver, i):
        try:
            #getting and formatting date
            self.random_sleep()

            str_date = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#trackingsearchsection > div > section > div > div > div'))).get_attribute('textContent')

            #getting workable date
            useable_date = self.get_date_from_cma(str_date)

            #if usable no usable date
            if useable_date == 'ERROR':

                #adding date to storage structure
                self.return_dict[self.container_num_list[i]] = 'ERROR'
            else:
                #getting month as a number
                month = self.get_month_num(useable_date[3:6])

                #if getting month causes error
                if month == 'ERROR':
                    self.return_dict[self.container_num_list[i]] = 'ERROR'
                else:
                    day = useable_date[0:2]
                    year = useable_date[7:]

                    #adding date to storage structure
                    self.return_dict[self.container_num_list[i]] = [month, day, year]

        except Exception:
            print('\n==============================================================================================')
            print('                              Failed to find/process date CMA CGM')
            print(f'                             Container Num {self.container_num_list[i]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
        try:
            #Finding textbox and entering container number without captcha, then clicking search
            self.random_sleep()

            WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')))

            textbox = driver.find_element(By.XPATH, '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')
            textbox.clear()

            self.random_sleep()

            textbox.send_keys(self.container_num_list[i])

            self.random_sleep()
            time.sleep(2)

            driver.find_element(By.XPATH, '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/p/button').click()

        except Exception:
            print('\n==============================================================================================')
            print('                                  Failed to modify CMA CGM search Textbox')
            print('==============================================================================================\n')


    def search(self, container_num_list):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.connect(driver)

        self.bypass_audio_captcha(driver)

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




