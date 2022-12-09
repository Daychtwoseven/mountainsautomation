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
            website = 'https://aca-prod.accela.com/MENIFEE/Cap/CapHome.aspx?module=Permits&TabName=Permits&TabList=Home'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
            select.select_by_value('Permits/Residential/Solar/NA')
            time.sleep(5)

            start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
            driver.execute_script(f"arguments[0].value = '12/01/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
            driver.execute_script(f"arguments[0].value = '12/08/2022'", end_date)
            time.sleep(5)

            driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
            time.sleep(5)

            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = td[1].text
                id = td[2].text
                name = td[4].text
                status = td[5].text
                href = td[2].find_elements(By.TAG_NAME, 'a')
                print(href)
                if href:
                    req = Request(
                        url=href[0].get_attribute('href'),
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )

                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, 'lxml')

                    firstname = soup.find('span', class_='contactinfo_firstname').text
                    lastname = soup.find('span', class_='contactinfo_lastname').text
                    applicant = f"{firstname} {lastname}"
                    address = soup.find('span', class_='contactinfo_addressline1').text if soup.find('span', class_='contactinfo_addressline1') else ''
                    city_text = soup.find_all('span', class_='contactinfo_region')
                    city = city_text[0].text.replace(',', '')
                    state = 'CA'
                    zip = city_text[2].text.split('-')[0].replace(',', '')

                    #print(f"{address}, {city}, {state}, {zip}")
        except Exception as e:
            print(e)


Selen()
