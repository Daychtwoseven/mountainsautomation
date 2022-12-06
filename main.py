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
            website = 'https://citizenportal.slcgov.com/Citizen/Cap/CapHome.aspx?module=Building&TabName=Building'

            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
            select.select_by_value('Building/SolarPV/Residential/NA')
            time.sleep(3)

            start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
            driver.execute_script("arguments[0].value = '12/01/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
            driver.execute_script("arguments[0].value = '12/02/2022'", end_date)

            driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()

            time.sleep(5)
            records_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[7]/div[1]/table/tbody/tr/td/div[2]/div[3]/div/div/div[2]/div[2]/div[3]/div[1]/div/table/tbody/tr')
            for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
                id = td[2].text
                status = td[7].text
                description = td[4].text
                name = td[5].text
                if status != '':
                    href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    req = Request(
                        url=href,
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )

                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, 'lxml')
                    address = soup.find('span', class_='contactinfo_addressline1').text
                    city_text = soup.find_all('span', class_='contactinfo_region')
                    city = city_text[0].text
                    state = city_text[1].text.replace(',', '')
                    zip = city_text[2].text

                    firstname = soup.find('span', class_='contactinfo_firstname')
                    lastname = soup.find('span', class_='contactinfo_lastname')

                    job_value_text = soup.find(id='ctl00_PlaceHolderMain_PermitDetailList1_tbADIList')
                    job_value = job_value_text.find('span', class_='ACA_SmLabel ACA_SmLabel_FontSize').text
                    print(job_value)



                """
                print(f"DATE: {date_today_in_mst} | Address: {address} | City: {' '.join(city_text[0:len(city_text)-2])} | "
                      f"State: {city_text[-2]} | Zip: {city_text[-1]} | Description: {tds[4].text} | Status: {tds[7].text}")
                """



        except Exception as e:
            print(e)


Selen()
