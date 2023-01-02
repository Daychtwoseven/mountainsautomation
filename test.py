from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from datetime import datetime
import pytz
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
class Selen:

    def __init__(self):

        try:
            website = 'https://permits.mynevadacounty.com/CitizenAccess/Cap/CapHome.aspx?module=Building'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            time.sleep(5)
            start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
            driver.execute_script(f"arguments[0].value = '12/19/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
            driver.execute_script(f"arguments[0].value = '12/20/2022'", end_date)
            time.sleep(10)

            collapseable = driver.find_elements(By.ID, 'imgGSExpandCollapse')
            print(driver)

            select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_0"]'))
            select.select_by_value('Residential')

            time.sleep(2)

            select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_1"]'))
            select.select_by_value('Solar Array')

            driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
            time.sleep(5)

        except Exception as e:
            print(e)


Selen()

"""


class Selen:

    def __init__(self):

        try:
            website = 'https://aca-prod.accela.com/SBCO/Cap/GlobalSearchResults.aspx?QueryText=solar'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            wait = WebDriverWait(driver, 10)
            driver.get(website)

            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    if td[1].find_elements(By.TAG_NAME, 'a'):
                        td[1].find_element(By.TAG_NAME, 'a').click()
                        wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                        location = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                                 '1]/div[3]/div[5]/div[1]/div[3]/div['
                                                                 '1]/div/div/table/tbody/tr/td/div/span/table/tbody'
                                                                 '/tr/td[2]').text
                        print(location)
                        driver.get(website)
                        wait.until(
                            EC.presence_of_element_located(
                                (By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))

                while driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME,
                                                                                                         'a'):
                    driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME,
                                                                                                    'a').click()
                    time.sleep(10)
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    if result_table:
                        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                            By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME,
                                                                                                         'tr')[3:]
                        for i in range(0, len(result_tr) - 1):
                            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(
                                By.TAG_NAME, 'tr')[
                                                                               3:]
                            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                            if td[1].find_elements(By.TAG_NAME, 'a'):
                                td[1].find_element(By.TAG_NAME, 'a').click()
                                wait.until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                                location = driver.find_element(By.XPATH,
                                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                               '1]/div[3]/div[5]/div[1]/div[3]/div['
                                                               '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr'
                                                               '/td[2]').text
                                print(location)
                                driver.get(website)
                                wait.until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))

        except Exception as e:
                print(e)


Selen()
