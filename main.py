from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            website = 'https://accela.maricopa.gov/CitizenAccessMCOSS/Cap/CapHome.aspx?module=PnD&TabName=PnD'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)


            select = Select(
                driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]'))
            select.select_by_value('PnD/Building/Miscellaneous_1/Electrical')
            time.sleep(5)

            start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
            driver.execute_script(f"arguments[0].value = '12/01/2022'", start_date)

            end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
            driver.execute_script(f"arguments[0].value = '12/13/2022'", end_date)
            driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
            time.sleep(15)

            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')

            if records_table:
                records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]

                for i in range(0, len(records_tr) - 1):
                    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
                    records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                                 3:-2]
                    td = records_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
                    id = td[2].text
                    name = td[5].text
                    status = td[7].text
                    if td[2].find_elements(By.TAG_NAME, 'a'):
                        wait = WebDriverWait(driver, 10)
                        td[2].find_element(By.TAG_NAME, 'a').click()
                        wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                        firstname = driver.find_elements(By.XPATH,
                                                         '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                         '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[1]')
                        lastname = driver.find_elements(By.XPATH,
                                                        '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                        '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                        '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[2]')

                        applicant = None
                        address = None
                        city = None
                        state = None
                        zip = None
                        if firstname and lastname:
                            applicant = f"{firstname[0].text} {lastname[0].text}"
                            address = driver.find_element(By.XPATH,
                                                          '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                          '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                          '1]/div/span/table/tbody/tr/td[2]/div/span[4]').text.replace(',', '')
                            city = driver.find_element(By.XPATH,
                                                       '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[5]').text.replace(',', '')
                            state = driver.find_element(By.XPATH,
                                                        '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[6]').text.replace(',', '')
                            zip = driver.find_element(By.XPATH,
                                                      '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                      '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td['
                                                      '1]/div/span/table/tbody/tr/td[2]/div/span[7]').text.replace(',', '')

                            print(f"{address}, {city}, {state}, {zip}")

                        driver.get(website)
                        #print(i)
                        wait.until(
                            EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))

            print('done all')

        except Exception as e:
            print(e)


Selen()
