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
            website = 'https://ca.columbus.gov/ca/Cap/CapHome.aspx?module=Building&TabName=Building'
            path = "C:/chromedriver.exe"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)
            time.sleep(5)
            permit_number = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber')
            permit_number.send_keys('PLEX')
        except Exception as e:
            print(e)


Selen()
