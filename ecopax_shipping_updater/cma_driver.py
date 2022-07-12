'''
module docstr
'''
import os
import string
import time
import urllib.request
from datetime import date, timedelta
from plistlib import InvalidFileException
import speech_recognition as sr
from pydub import AudioSegment
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from browser_search import BrowserSearch
from shipping_container_db import (db_get_cont_info, db_add_cont, db_remove_cont, db_add_error,
                                   db_update_cont)
from shipping_updater_utility import (get_date_from_cma, get_month_num,
                                      random_sleep)


class CMASearch(BrowserSearch):
    '''
    docstr
    '''
    # pylint: disable=W0703
    # pylint: disable=C0301
    def __init__(self, container_num_list):
        '''
        docstr
        '''
        self.container_num_list = container_num_list
        self.cma_search_link = 'https://www.cma-cgm.com/ebusiness/tracking'
        self.error_list = []
        self._db_changes = 0

        abs_path = os.path.abspath('Audio Captcha Files')
        self.use_path = abs_path

    @property
    def db_changes(self):
        '''
        docstr
        '''
        return self._db_changes

    def get_options(self, options):
        '''
        docstr
        '''
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": self.use_path,
                 "directory_upgrade": True}

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument("--mute-audio")
        options.add_experimental_option("prefs", prefs)

    def connect(self, driver):
        '''
        docstr
        '''
        try:
            driver.get(self.cma_search_link)

            print('\n[Connection Alert] Driver Connection to CMA CGM Site Successful\n')

        except Exception:
            print('\n============================================================================')
            print('                      CMA CGM Site Connection Failed')
            print('============================================================================\n')
            self.error_list.append('ERROR')

    def bypass_audio_captcha(self, driver):
        '''
        docstr
        '''
        try:
            audio_file_info_lst = self.download_captcha_audio(driver)
            audio_src_link = audio_file_info_lst[0]
            send_keys_str = audio_file_info_lst[1]

            try:
                urllib.request.urlretrieve(audio_src_link, send_keys_str)
            except Exception:
                try:
                    urllib.request.urlretrieve(audio_src_link, send_keys_str)
                except Exception as exc:
                    raise InvalidFileException from exc

            ret_list = self.get_code_from_audio(send_keys_str)
            numeric_string = ret_list[0]
            dst = ret_list[1]

            textbox = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/input')
            textbox.send_keys(numeric_string)

            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/div/div[2]/div[4]'))
            ).click()

            os.remove(send_keys_str)
            time.sleep(2)
            os.remove(dst)

        except Exception as err_new:
            print('\n' + str(err_new) + '\n')
            print('\n============================================================================')
            print('                     CMA CGM Audio Captcha Bypass Failed')
            print('============================================================================\n')

    def download_captcha_audio(self, driver):
        '''
        docstr
        '''
        time.sleep(2)
        frame = driver.find_element_by_css_selector('body > iframe')
        driver.switch_to.frame(frame)

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div[3]/div/div[3]/div/div/div[2]/div[1]'))
            ).click()
        except Exception:
            pass

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/a[4]'))
            ).click()
        except Exception:
            pass

        time.sleep(3)
        audio_src_link = WebDriverWait(driver, 10).until(EC.invisibility_of_element(
            (By.TAG_NAME, 'audio'))
        ).get_attribute('currentSrc')

        audio_file_name = audio_src_link[36:]
        send_keys_str = self.use_path + '\\' + audio_file_name

        return(audio_src_link, send_keys_str)

    def get_code_from_audio(self, send_keys_str):
        '''
        docstr
        '''
        spl_fp = send_keys_str.split('.')
        spl_fp[-1] = '.wav'
        new_fp_str = ''.join(spl_fp)
        dst = new_fp_str

        sound = AudioSegment.from_mp3(send_keys_str)
        sound.export(dst, format="wav")

        audio_source_file = sr.AudioFile(new_fp_str)

        speech_recog = sr.Recognizer()
        speech_recog.energy_threshold = 300

        with audio_source_file as source:
            audio_data = speech_recog.record(source)
            result = speech_recog.recognize_google(audio_data)

        numeric_filter = filter(str.isdigit, result)
        numeric_string = "".join(numeric_filter)

        return (numeric_string, dst)

    def pull_date(self, driver, i):
        '''
        docstr
        '''
        try:
            try:
                # getting and formatting date
                random_sleep()

                str_date = WebDriverWait(driver, 12).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#trackingsearchsection > div > section > div > div > div'))
                ).get_attribute('textContent')

                # getting workable date
                useable_date = get_date_from_cma(str_date)

                if useable_date == 'ERROR':
                    days_remaining = WebDriverWait(driver, 12).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, 'remaining'))
                    ).get_attribute('innerText')

                    days_added = int(days_remaining[11:].strip(string.ascii_letters))
                    date_est = date.today() + timedelta(days=days_added)

                    formatted_date = date_est.strftime('%m/%d/%Y')

                    db_update_cont(self.container_num_list[i][0], formatted_date)
                    self._db_changes += 1
                else:
                    # getting month as a number
                    month = get_month_num(useable_date[3:6])

                    day = useable_date[0:2]
                    year = useable_date[7:]

                    formatted_date = month + '/' + day + '/' + year

                    # adding date to storage database
                    db_update_cont(self.container_num_list[i][0], formatted_date)
                    self._db_changes += 1

            except NoSuchElementException:
                driver.refresh()

        except Exception:
            db_update_cont(self.container_num_list[i][0], 'Date Error')
            print('\n=============================================================================')
            print('                              Failed to find/process date CMA CGM')
            print(f'                             Container Num {self.container_num_list[i][0]} ')
            print('=============================================================================\n')

    def modify_search(self, driver, i):
        try:
            # Finding textbox and entering container number without captcha, then clicking search
            random_sleep()

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH,
                 '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]'))
            )

            textbox = driver.find_element(
                (By.XPATH,
                 '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/div/span[1]/input[2]'))
            textbox.clear()
            textbox.send_keys(self.container_num_list[i][0])

            self.try_srch_click(driver)

        except Exception as err_new:
            print('\n' + str(err_new) + '\n')
            print('\n============================================================================')
            print('                    Failed to modify CMA CGM search Textbox')
            print('============================================================================\n')
            self.error_list.append('ERROR')

    def try_srch_click(self, driver):  # noqa: C901
        '''
        docstr
        '''
        try:
            WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                (By.XPATH, '//p/button'))
            ).click()
        except Exception:
            try:
                WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                    (By.XPATH,
                     '/html/body/div[3]/main/section/div/div[2]/fieldset/form[3]/p/button'))
                ).click()
            except Exception:
                try:
                    WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#btnTracking'))
                    ).click()
                except Exception:
                    try:
                        WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                            (By.ID, 'btnTracking'))
                        ).click()
                    except Exception:
                        try:
                            WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                                (By.CLASS_NAME, 'o-button primary'))
                            ).click()
                        except Exception:
                            try:
                                WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                                    (By.NAME, 'search'))
                                ).click()
                            except Exception:
                                try:
                                    WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                                        (By.TAG_NAME, 'p'))
                                    ).click()
                                except Exception as exc:
                                    print(exc)
                                    raise NoSuchElementException from exc

    def search_algorithm(self):
        '''
        This function searches the Cosco site for the estimated arrival date of a list of crate
        numbers
        '''
        options = webdriver.ChromeOptions()
        self.get_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(25)

        self.connect(driver)

        self.bypass_audio_captcha(driver)

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
    '''
    docstr
    '''
    cma = CMASearch(cma_search_list)

    if len(cma_search_list) != 0:
        cma.search_algorithm()
        if cma.db_changes == 0:
            for i in range(3):
                print('\n[Driver Alert] Trying CMA CGM Search Again\n')
                time.sleep(i)
                cma.search_algorithm()
                if cma.db_changes != 0:
                    break
        if cma.db_changes == 0:
            print('\n[Driver Alert] CMA CGM Search Fatal Error\n')
            for cont in cma_search_list:
                cont_props = db_get_cont_info(cont)
                db_add_cont([cont_props[0][0], cont_props[0][1], cont_props[0][2],
                            cont_props[0][3]], 'no_search')
                db_remove_cont(cont)

            db_add_error('Part of CMA CGM Search Failed')
