from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lxml import etree
import pytz
import time
import bs4


class Selen:

    def __init__(self):

        try:
            mst_tz = pytz.timezone("MST")
            date_today_in_mst = datetime.now(mst_tz).date().strftime("%m/%d/%Y")
            options = Options()
            options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
            website = 'https://aca-prod.accela.com/MONTEREY/Cap/CapHome.aspx?module=Building&TabName=Building'

            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
            select.select_by_value('Building/Solar/PV/.')
            time.sleep(10)

            """
            start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
            driver.execute_script("arguments[0].value = '12/01/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
            driver.execute_script("arguments[0].value = '12/02/2022'", end_date)
            """


            driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()

            time.sleep(20)
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            print(len(records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]))
            for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
                td[2].find_element(By.TAG_NAME, 'a').send_keys(Keys.CONTROL + 't')
                id = td[2].text
                status = td[7].text
                description = td[4].text
                name = td[5].text



                """
                print(f"DATE: {date_today_in_mst} | Address: {address} | City: {' '.join(city_text[0:len(city_text)-2])} | "
                      f"State: {city_text[-2]} | Zip: {city_text[-1]} | Description: {tds[4].text} | Status: {tds[7].text}")
                """



        except Exception as e:
            print(e)


Selen()
