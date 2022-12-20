from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from datetime import datetime
import pytz
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Selen:

    def __init__(self):

        try:
            website = 'https://epicla.lacounty.gov/energov_prod/SelfService/#/search?m=1&fm=2&ps=300&pn=1&em=true&st=solar'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)

            time.sleep(30)
            select = Select(driver.find_element(By.ID, 'PermitCriteria_SortBy'))
            select.select_by_value('string:IssueDate')

            time.sleep(2)

            select = Select(driver.find_element(By.ID, 'SortAscending'))
            select.select_by_value('boolean:false')
            time.sleep(10)

            element_start_count = 9
            for i in range(0, 299):
                row = driver.find_element(By.ID, f'entityRecordDiv{i}')
                issued_date = row.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[5]/span')
                if issued_date:
                    issued_date = datetime.strptime(issued_date[0].text, '%m/%d/%Y').date()
                    start_date = datetime.strptime('12/01/2022', '%m/%d/%Y').date()
                    end_date = datetime.strptime('12/20/2022', '%m/%d/%Y').date()

                    if start_date <= issued_date <= end_date:
                        id = row.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[2]/a/tyler-highlight/span').text
                        address_text = row.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[11]/tyler-highlight/span').text.split(' ')
                        description = row.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[12]/tyler-highlight/span').text
                        zip = address_text[-1]
                        state = address_text[-2]
                        city = address_text[-3]
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address = ' '.join(address_text)
                        print(f"{address}, {city}, {state}, {zip}")
                    i += 1
                    element_start_count += 1
                elif not issued_date:
                    break

        except Exception as e:
            print(e)


Selen()