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
            website = 'https://citizenaccess.arapahoegov.com/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)
            select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_CapView_ddlModule"]'))
            select.select_by_value('Contractors')
            time.sleep(5)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')

            if records_table:
                records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]

                for i in range(0, 9):
                    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                                 3:-2]
                    td = records_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = td[0].text
                    name = td[2].text
                    status = td[4].text
                    applicant = None
                    if td[1].find_elements(By.TAG_NAME, 'a'):
                        wait = WebDriverWait(driver, 10)
                        td[1].find_element(By.TAG_NAME, 'a').click()
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*['
                                                                             '@id'
                                                                             '="ctl00_PlaceHolderMain_shPermitDetail_lblSectionTitle"]')))
                        print(driver.find_element(By.XPATH, '//*['
                                                            '@id'
                                                            '="ctl00_PlaceHolderMain_shPermitDetail_lblSectionTitle"]'))
                        firstname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div['
                                                                   '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                                   '1]/table/tbody/tr/td['
                                                                   '1]/div/span/table/tbody/tr/td[2]/div/span[1]')
                        lastname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div['
                                                                  '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                                  '1]/table/tbody/tr/td[1]/div/span/table/tbody/tr/td['
                                                                  '2]/div/span[2]')
                        print(firstname)
                        if firstname and lastname:
                            applicant = f"{firstname[0].text} {lastname[0].text}"

                        print(applicant)
                        driver.get(website)
                        wait.until(
                            EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))

        except Exception as e:
            print(e)


Selen()
