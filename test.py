from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from datetime import datetime
import pytz
import time
import bs4


class Selen:

    def __init__(self):

        try:
            mst_tz = pytz.timezone("MST")
            date_today_in_mst = datetime.now(mst_tz).date().strftime("%m/%d/%Y")
            options = Options()
            website = 'https://epicla.lacounty.gov/energov_prod/SelfService/#/search'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)
            time.sleep(10)

            select = Select(driver.find_element(By.ID, 'SearchModule'))
            select.select_by_value('number:2')

            driver.find_element(By.ID, 'button-Advanced').click()

            project_name = driver.find_element(By.ID, 'PermitCriteria_ProjectName')
            project_name.send_keys('solar')

            description = driver.find_element(By.ID, 'PermitCriteria_Description')
            description.send_keys('solar')

            start_date = driver.find_element(By.ID, 'ApplyDateFrom')
            driver.execute_script(f"arguments[0].value = '12/18/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ApplyDateTo')
            driver.execute_script(f"arguments[0].value = '12/19/2022'", end_date)
            time.sleep(5)

            driver.find_element(By.ID, 'button-Search').click()
            time.sleep(5)

            page_length = driver.find_element(By.ID, 'pageSizeList')
            select.select_by_value('100')

            time.sleep(20)
        except Exception as e:
            print(e)


Selen()