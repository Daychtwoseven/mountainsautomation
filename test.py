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
            website = 'https://ims.palmbayflorida.org/ims/Find3/Results?cat=Permits'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/a').click()
            time.sleep(3)

            driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div[1]/div/a[1]').click()
            time.sleep(3)

            first_search = Select(driver.find_element(By.ID, 'find3SearchCriteria_0__find3Definition_StoredProcedureName'))
            first_search.select_by_value('dbo.iMSFind3PermitsRecordType')
            time.sleep(2)
            first_search_contain = driver.find_element(By.XPATH, '//*[@id="find3SearchCriteria_0_SearchText"]')
            first_search_contain.send_keys('solar')
            time.sleep(3)

            driver.find_element(By.XPATH, '//*[@id="create"]').click()
            time.sleep(3)

            first_search = Select(
                driver.find_element(By.ID, 'find3SearchCriteria_1__find3Definition_StoredProcedureName'))
            first_search.select_by_value('dbo.iMSFind3PermitsPermitNumber')
            time.sleep(2)
            first_search_contain = driver.find_element(By.XPATH, '//*[@id="find3SearchCriteria_1_SearchText"]')
            first_search_contain.send_keys('BL22-17')
            time.sleep(3)

            driver.find_element(By.XPATH, '/html/body/div[3]/form/div[2]/div/button').click()
            time.sleep(5)

            results = driver.find_elements(By.CLASS_NAME, 'recordrow')
            print(results)

        except Exception as e:
            print(e)


Selen()
