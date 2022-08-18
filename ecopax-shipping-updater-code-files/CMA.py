import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from ShippingContainerDB import *
from ShippingUpdaterUtility import get_month_num, get_date_from_cma, random_sleep
import os
from os import listdir
from os.path import isfile, join
from datetime import date, timedelta
import string
import traceback

class CMASearch(object):

    def __init__(self, container_num_list):
        self.container_num_list = container_num_list
        self.cma_search_link = 'https://www.cma-cgm.com/ebusiness/tracking'
        self.speech_to_text_link = 'https://speech-to-text-demo.ng.bluemix.net/'
        self.error_list = []
        self._db_changes = 0

        self.use_path = os.path.abspath('Audio Captcha Files')

    @property
    def db_changes(self):
        return self._db_changes


    def get_options(self, options):
        prefs = {"profile.default_content_settings.popups": 0, "download.default_directory": self.use_path, "directory_upgrade": True}

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument("--mute-audio")
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
            time.sleep(2)
            frame = driver.find_element(By.CSS_SELECTOR, 'body > iframe')
            driver.switch_to.frame(frame)

            time.sleep(2)
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div/div[3]/div/div/div[2]/div[1]'))).click()
            except Exception:
                pass
            
            random_sleep()
            time.sleep(3)

            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/a[4]'))).click()
            except Exception:
                pass

            time.sleep(5)
            audio_src_link = WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.TAG_NAME, 'audio'))).get_attribute('currentSrc')

            audio_file_name = audio_src_link[36:]

            time.sleep(2)
            driver.execute_script("window.open('');")
  
            # Switch to the new window and open new URL
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            driver.get(audio_src_link)

            random_sleep()

            driver.execute_script('''let aLink = document.createElement("a");let videoSrc = document.querySelector("video").firstChild.src;aLink.href = videoSrc;aLink.download = "";aLink.click();aLink.remove();''')


            driver.execute_script("window.open('');")
  
            # Switch to the new window and open new URL
            driver.switch_to.window(driver.window_handles[2])

            time.sleep(2)

            driver.get(self.speech_to_text_link)

            time.sleep(5)
                
            root = driver.find_element(By.ID, 'root').find_elements(By.CLASS_NAME, 'dropzone _container _container_large')
            btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')

            send_keys_str = self.use_path + '\\' + audio_file_name

            btn.send_keys(send_keys_str)

            time.sleep(15)
            #btn.send_keys(path)

            # Audio to text is processing
            text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements(By.TAG_NAME, 'span')

            result = " ".join( [ each.text for each in text ] )
            key_str = result[33:-1]

            driver.switch_to.window(driver.window_handles[0])

            random_sleep()

            frame = driver.find_element(By.CSS_SELECTOR, 'body > iframe')
            driver.switch_to.frame(frame)
            time.sleep(2)

            textbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/input')

            for num in key_str:
                random_sleep()
                textbox.send_keys(num)
                time.sleep(0.5)

            random_sleep()
            time.sleep(4)

            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[4]'))).click()

            os.remove(send_keys_str)
            time.sleep(5)

        except Exception:
            print('\n===============================================================================================')
            print('                              CMA CGM Audio Captcha Bypass Failed')
            print('===============================================================================================\n')

            try:
                os.remove(send_keys_str)
            except:
                pass

            self.error_list.append('ERROR') 


    def pull_date(self, driver, i):
        try:     
            try:
                #getting and formatting date
                random_sleep()

                str_date = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#trackingsearchsection > div > section > div > div > div'))).get_attribute('textContent')

                #getting workable date
                useable_date = get_date_from_cma(str_date)

                if useable_date == 'ERROR':
                    days_remaining = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CLASS_NAME, 'remaining'))).get_attribute('innerText')
                    days_added = int(days_remaining[11:].strip(string.ascii_letters))
                    date_est = date.today() + timedelta(days = days_added)

                    formatted_date = date_est.strftime('%m/%d/%Y')

                    db_update_container(self.container_num_list[i][0], formatted_date)
                    self._db_changes += 1
                else:
                    #getting month as a number
                    month = get_month_num(useable_date[3:6])

                    day = useable_date[0:2]
                    year = useable_date[7:]

                    formatted_date = month + '/' + day + '/' + year

                    #adding date to storage database
                    db_update_container(self.container_num_list[i][0], formatted_date)
                    self._db_changes += 1

            except NoSuchElementException:
                driver.refresh()

        except Exception:
            db_update_container(self.container_num_list[i][0], 'Date Error')
            print('\n==============================================================================================')
            print('                              Failed to find/process date CMA CGM')
            print(f'                             Container Num {self.container_num_list[i][0]} ')
            print('==============================================================================================\n')


    def modify_search(self, driver, i):
       try:     
            #Finding textbox and entering container number without captcha, then clicking search
            random_sleep()

            #WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')))

            #textbox = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]')
            time.sleep(3)
            textbox = driver.find_element(By.ID, 'Reference')
            textbox.clear()

            random_sleep()

            textbox.send_keys(self.container_num_list[i][0])

            random_sleep()
            time.sleep(5)

            try:
                time.sleep(1)
                try:
                    driver.find_element(By.XPATH, '/html/body/div[2]/main/section/div/div[2]/fieldset/form[3]/p/button').click()
                except Exception:
                    driver.find_element(By.CLASS_NAME,'o-button primary').click()
                #WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/section/div/div[2]/fieldset/form[3]/p/button'))).click()
            except Exception:
                pass

       except Exception:
            traceback.print_exc()
            print('\n==============================================================================================')
            print('                                  Failed to modify CMA CGM search Textbox')
            print('==============================================================================================\n')
            self.error_list.append('ERROR')


    def search_algorithm(self):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(25)

        self.connect(driver)

        self.bypass_audio_captcha(driver)

        driver.switch_to.default_content()

        self.modify_search(driver, 0)
        if len(self.error_list) != 0:
            return {}

        self.pull_date(driver, 0)

        i = 1

        while i < len(self.container_num_list):
            try:
                self.modify_search(driver, i)
                if len(self.error_list) != 0:
                    return {}

                time.sleep(1)

                self.pull_date(driver, i)

            except Exception:
                pass

            i += 1

        driver.close()


def cma_search(cma_search_list):

    cma = CMASearch(cma_search_list)

    if len(cma_search_list) != 0:
        cma.search_algorithm()
        if cma.db_changes == 0:
            for i in range(3):
                print('\n[Driver Alert] Trying CMA CGM Search Again\n')
                time.sleep(7)
                cma.search_algorithm()
                if cma.db_changes != 0:
                    break
        if cma.db_changes == 0:
            print('\n[Driver Alert] CMA CGM Search Fatal Error\n')
            for cont in cma_search_list:
                cont_props = db_get_container_info(cont)
                db_add_container([cont_props[0][0], cont_props[0][1], cont_props[0][2], cont_props[0][3]], 'no_search')
                db_remove_container(cont)

            db_add_error('Part of CMA CGM Search Failed')
