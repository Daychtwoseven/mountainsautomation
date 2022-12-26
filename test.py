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
            website = 'https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)
            time.sleep(5)

            driver.find_element(By.ID, 'BTNREPORTS').click()

            select = Select(driver.find_element(By.ID, 'CMBPERMITTYPE'))
            select.select_by_value('185')

            driver.find_element(By.ID, 'BTNSEARCH').click()

            results_table = driver.find_element(By.ID, 'PERMITSGRID_')

            if results_table:
                results_tr = results_table.find_elements(By.TAG_NAME, 'tr')[1:]

                for i in results_tr:
                    td = i.find_elements(By.TAG_NAME, 'td')
                    action = ActionChains(driver)
                    action.double_click(td[0]).perform()

        except Exception as e:
            print(e)


Selen()