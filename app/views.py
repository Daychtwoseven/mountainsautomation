# Django
from urllib.request import Request, urlopen

import bs4
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import threading
import time


def index_page(request, action=None):
    try:
        today = datetime.now()
        context = {
            'data': UrlResults.objects.all()
        }
        if action is not None:
            if action == "reset-database":
                UrlResults.objects.all().delete()
                return redirect('app-index-page')
        else:
            if request.method == "POST":
                if request.POST.get('url'):
                    url = Urls.objects.get(id=request.POST.get('url'))
                    url_req = False
                    message = None
                    if url.id == 1:
                        url_req = url_1(request, url)
                    elif url.id == 2:
                        url_req = url_2(request, url)
                    elif url.id == 3:
                        url_req = url_3(request, url)
                    elif url.id == 4:
                        url_req = url_4(request, url)
                    elif url.id == 5:
                        url_req = url_5(request, url)
                    elif url.id == 6:
                        url_req = url_6(request, url)
                    elif url.id == 7:
                        url_req = url_7(request, url)
                    elif url.id == 8:
                        url_req = url_8(request, url)
                    elif url.id == 9:
                        url_req = url_9(request, url)
                    elif url.id == 10:
                        url_req = url_10(request, url)
                    elif url.id == 11:
                        url_req = url_11(request, url)
                    elif url.id == 12:
                        url_req = url_12(request, url)
                    elif url.id == 13:
                        url_req = url_13(request, url)
                    elif url.id == 14:
                        url_req = url_14(request, url)
                    elif url.id == 15:
                        url_req = url_15(request, url)
                    elif url.id == 16:
                        url_req = url_16(request, url)
                    elif url.id == 17:
                        url_req = url_17(request, url)
                    elif url.id == 18:
                        url_req = url_18(request, url)
                    elif url.id == 19:
                        url_req = url_19(request, url)
                    elif url.id == 20:
                        url_req = url_20(request, url)
                    elif url.id == 21:
                        url_req = url_21(request, url)
                    elif url.id == 22:
                        url_req = url_22(request, url)
                    elif url.id == 23:
                        url_req = url_23(request, url)
                    elif url.id == 24:
                        url_req = url_24(request, url)
                    elif url.id == 25:
                        url_req = url_25(request, url)
                    elif url.id == 26:
                        url_req = url_26(request, url)
                    elif url.id == 27:
                        url_req = url_27(request, url)
                    elif url.id == 28:
                        url_req = url_28(request, url)
                    elif url.id == 29:
                        url_req = url_29(request, url)
                    elif url.id == 30:
                        url_req = url_30(request, url)
                    elif url.id == 31:
                        url_req = url_31(request, url)
                    elif url.id == 32:
                        url_req = url_32(request, url)
                    elif url.id == 33:
                        url_req = url_33(request, url)
                    elif url.id == 34:
                        url_req = url_34(request, url)
                    if url_req:
                        return JsonResponse({'statusMsg': 'Success'}, status=200)
                    else:
                        return JsonResponse({'statusMsg': message}, status=404)

                url_func = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12,
                            url_13,
                            url_14, url_15, url_16, url_17, url_18, url_19, url_20, url_21, url_22, url_23, url_24,
                            url_25, url_26, url_27, url_28, url_29, url_30, url_31, url_32, url_33, url_34]

                counter = 0
                success = 0
                for i in Urls.objects.all():
                    if i.is_active:
                        print(f"Running City: {i.description}")
                        url_req = url_func[counter](request, i)
                        if url_req:
                            success += 1
                    counter += 1
                """
                threads = []
                for i in Urls.objects.all():
                    if i.is_active:
                        t = threading.Thread(target=url_func[counter], args=(request, i))
                        t.start()
                        threads.append(t)

                    counter += 1

                for thread in threads:
                    thread.join()
                """

                return JsonResponse({'statusMsg': 'Success'}, status=200)

            return render(request, 'index.html', context)
    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)


def url_1(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSSubAgency'))
    select.select_by_value('RENO')
    time.sleep(15)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar & EV Chargers/NA')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table_tr = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                      '1]/table/tbody/tr/td/div[2]/div[3]/div/div/div['
                                                      '2]/div[2]/div[3]/div[1]/div/table/tbody/tr')
    for row in records_table_tr[2:-1]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = var_checker(td[1])
        id = var_checker(td[2])
        status = var_checker(td[6])
        name = var_checker(td[4])
        td_status = var_checker(td[6])
        description = var_checker(td[9])
        if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
                req = Request(
                    url=href,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'lxml')
                address_text = soup.find('td', class_='NotBreakWord').text.split(',')
                address = address_text[0]
                city = address_text[1]
                state_text = address_text[2].split(' ')
                new_state_text = []
                invalid_chars = ['', ' ', '*', '/']
                for i in state_text:
                    if i not in invalid_chars:
                        new_state_text.append(i)
                state = new_state_text[0]
                zip = new_state_text[1]
                applicant_text = soup.find_all('td', attrs={'style': 'vertical-align:top'})
                applicant = applicant_text[0].text.replace('*', '')
                job_value_text = soup.find(id='ctl00_PlaceHolderMain_PermitDetailList1_tdADIContent')
                value = job_value_text.find('span', class_='ACA_SmLabel_FontSize').text

                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name, address=address,
                                          city=city, state=state, zip=zip, applicant=applicant, description=description,
                                          job_value=value)

    return True


def url_2(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    time.sleep(15)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('DSD/Project/Standalone/Photovoltaic')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table_tr = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                      '1]/table/tbody/tr/td/div[2]/div[3]/div/div/div['
                                                      '2]/div[2]/div[3]/div[1]/div/table/tbody/tr')
    for row in records_table_tr[2:-1]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[6].text
        name = td[4].text
        td_status = td[6].text
        description = td[4].text
        if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
                req = Request(
                    url=href,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'lxml')
                address_text = soup.find('td', class_='NotBreakWord')
                address = address_text.text.split('*')[0]
                city = 'San Diego'
                state = 'CA'
                zip = None
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name, address=address,
                                          city=city, state=state, zip=zip, description=description)

    return True


def url_3(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/NA')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table_tr = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                      '1]/table/tbody/tr/td/div[2]/div[3]/div/div/div['
                                                      '2]/div[2]/div[3]/div[1]/div/table/tbody/tr')
    for row in records_table_tr[2:-1]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[8].text
        name = td[4].text
        description = td[5].text
        if status != "" and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
                req = Request(
                    url=href,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'lxml')
                address = soup.find('span', class_='contactinfo_addressline1').text

                city_text = soup.find_all('span', class_='contactinfo_region')
                city = city_text[0].text
                state = city_text[1].text
                zip = city_text[2].text

                firstname = soup.find('span', class_='contactinfo_firstname').text
                lastname = soup.find('span', class_='contactinfo_lastname').text

                applicant = f"{firstname} {lastname}"

                job_value_text = soup.find(id='trADIList')
                job_value = job_value_text.find('span', class_='ACA_SmLabel ACA_SmLabel_FontSize').text

                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip, applicant=applicant,
                                          description=description, job_value=job_value)

    return True


def url_4(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table_tr = driver.find_elements(By.XPATH,
                                            '/html/body/form/div[3]/div/div[7]/div[1]/table/tbody/tr/td/div[2]/div['
                                            '3]/div/div/div[2]/div[2]/div[3]/div[1]/div/table/tbody/tr')

    for row in records_table_tr[2:-1]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = var_checker(td[1])
        id = var_checker(td[2])
        status = var_checker(td[5])
        address_text = var_checker(td[4])
        if status != "" and len(address_text) > 1 and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
                req = Request(
                    url=href,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'lxml')
                address = var_checker(soup.find('span', class_='contactinfo_addressline1'))
                city_text = soup.find_all('span', class_='contactinfo_region')
                city = var_checker(city_text[0])
                state = var_checker(city_text[1])
                zip = var_checker(city_text[2])

                firstname = var_checker(soup.find('span', class_='contactinfo_firstname'))
                lastname = var_checker(soup.find('span', class_='contactinfo_lastname'))

                applicant = f"{firstname} {lastname}"

                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address, city=city,
                                          state=state, zip=zip, applicant=applicant)

    return True


def url_5(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = var_checker(td[1])
        status = var_checker(td[5])
        name = var_checker(td[3])
        address_text = td[4].text.split(',') if td[4] else ''
        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0] if len(address_text) else ''
            city = address_text[1] if len(address_text) else ''
            state = 'KY'
            zip = address_text[2].split(' ')[2] if len(address_text) > 1 else ''
            print(zip)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address, city=city,
                                      state=state, zip=zip, name=name)

    return True


def url_6(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[5].text
        name = td[3].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'VA'
            zip = address_text[2].split(' ')[2]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_7(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[5].text
        name = td[3].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'VA'
            zip = address_text[2].split(' ')[2]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_8(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[5].text
        name = td[3].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'FL'
            zip = address_text[2].split(' ')[2]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_9(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[5].text
        name = td[3].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'FL'
            zip = address_text[2].split(',')[-1][0:5]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_10(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.CLASS_NAME, 'ACA_GridView ACA_Grid_Caption')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[2].text
        name = td[6].text
        address_text = td[7].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'FL'
            zip = address_text[2].split(' ')[1][4]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_11(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[2].text
        status = td[3].text
        name = td[5].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'FL'
            zip = address_text[-1].split(' ')[1]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_12(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[2].text
        name = td[5].text
        address_text = td[4].text.split(',')

        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'CO'
            zip = address_text[2].split(' ')[2]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_13(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(
        datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    date_end = datetime.strptime(
        datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[5].text
        address_text = td[4].text.split(',')
        if status != '' and len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city = address_text[1]
            state = 'CA'
            zip = address_text[2].split(' ')[2]

            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)

    return True


def url_14(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    time.sleep(15)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/SolarPV/Residential/NA')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[7]/div[1]/table/tbody/tr/td/div['
                                                  '2]/div[3]/div/div/div[2]/div[2]/div[3]/div[1]/div/table')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[7].text
        description = td[4].text
        name = td[5].text
        if status != '' and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
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

                firstname = soup.find('span', class_='contactinfo_firstname').text
                lastname = soup.find('span', class_='contactinfo_lastname').text
                applicant = f"{firstname} {lastname}"

                job_value_text = soup.find(id='ctl00_PlaceHolderMain_PermitDetailList1_tbADIList')
                job_value = job_value_text.find('span', class_='ACA_SmLabel ACA_SmLabel_FontSize').text

                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, description=description, name=name, applicant=applicant,
                                          job_value=job_value,
                                          state=state, zip=zip)

    return True


def url_15(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/NA/NA')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[2].text
        id = td[1].text
        status = td[4].text
        description = td[6].text
        name = td[7].text
        address_text = td[5].text.split(',')
        if status != '' and status != "Pending" and len(address_text) > 1 and not UrlResults.objects.filter(
                record_id=id, date=date).first():
            address = address_text[0]
            city_text = address_text[-1].split(' ')
            city = city_text[1]
            state = 'CA'
            zip = city_text[-1:][0]
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, name=name,
                                      state=state, zip=zip)

    return True


def url_16(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/Permit')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[6].text
        description = td[4].text
        name = td[5].text
        if status != '' and status != "Pending" and not UrlResults.objects.filter(record_id=id, date=date).first():
            href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            if href:
                req = Request(
                    url=href,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )

                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, 'lxml')

                permit_details_table = soup.find('table', class_='table_parent_detail')
                permit_details_tr = permit_details_table.find_all('tr', class_='ACA_FLeft')
                address = None
                city = None
                state = 'NV'
                zip = None
                for row in permit_details_tr[1]:
                    if type(row) is bs4.element.Tag:
                        td = row.table.tr.find_all('td', style="vertical-align:top")
                        applicant = td[0].text
                        address = td[1].text
                        city_text = td[2].text.split(' ')
                        city = ''.join(city_text[0:-3])
                        state = 'NV'
                        zip = city_text[-2]
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, description=description, name=name, applicant=applicant,
                                          state=state, zip=zip)

    return True


def url_17(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/PV/.')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[3].text
        address_text = td[6].text
        address = address_text.split(',')[0]
        city_text = address_text.split(',')[1].split(' ')
        city = ''.join(city_text[0:-2])
        state = 'CA'
        zip = city_text[-1]
        if status != '' and status != "Pending" and not UrlResults.objects.filter(record_id=id, date=date).first():
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address, city=city,
                                      state=state, zip=zip)

    return True


def url_18(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar Photovoltaic System/Residential/NA')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[6].text
        address_text = td[5].text

        description = td[4].text
        address = address_text.split(',')[0]
        city_text = address_text.split(',')[1].split(' ')
        city = ''.join(city_text[0:-2])
        state = 'CA'
        zip = city_text[-1]
        if status != '' and status != "Pending" and not UrlResults.objects.filter(record_id=id, date=date).first():
            UrlResults.objects.create(url=url, record_id=id, description=description, date=date, status=status,
                                      address=address, city=city,
                                      state=state, zip=zip)

    return True


def url_19(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    permit_number = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber')
    permit_number.send_keys('PLEX')
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[5].text
        description = td[4].text
        href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
        if href and status != '' and status != "Pending" and not UrlResults.objects.filter(record_id=id,
                                                                                           date=date).first():
            req = Request(
                url=href,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'lxml')

            firstname = soup.find('span', class_='contactinfo_firstname').text if soup.find('span',
                                                                                            class_='contactinfo_firstname') else ''
            lastname = soup.find('span', class_='contactinfo_lastname').text if soup.find('span',
                                                                                          class_='contactinfo_lastname') else ''
            applicant = f"{firstname} {lastname}"
            address = soup.find('span', class_='contactinfo_addressline1').text if soup.find('span',
                                                                                             class_='contactinfo_addressline1') else ''
            city_text = soup.find_all('span', class_='contactinfo_region')
            city = city_text[0].text
            state = city_text[1].text
            zip = city_text[2].text
            UrlResults.objects.create(url=url, record_id=id, description=description, date=date, status=status,
                                      address=address, applicant=applicant, city=city,
                                      state=state, zip=zip)

    return True


def url_20(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Permits/Residential/Solar/NA')
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        name = td[4].text
        status = td[5].text
        href = td[2].find_elements(By.TAG_NAME, 'a')
        if href and not UrlResults.objects.filter(record_id=id, date=date).first():
            req = Request(
                url=href[0].get_attribute('href'),
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'lxml')

            firstname = soup.find('span', class_='contactinfo_firstname').text
            lastname = soup.find('span', class_='contactinfo_lastname').text
            applicant = f"{firstname} {lastname}"
            address = soup.find('span', class_='contactinfo_addressline1').text if soup.find('span',
                                                                                             class_='contactinfo_addressline1') else ''
            city_text = soup.find_all('span', class_='contactinfo_region')
            city = city_text[0].text.replace(',', '')
            state = 'CA'
            zip = city_text[2].text.split('-')[0].replace(',', '')

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                      address=address, applicant=applicant, city=city,
                                      state=state, zip=zip)

    return True


def url_21(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[0].text
        id = td[1].text
        name = td[5].text
        status = td[7].text
        description = td[4].text
        address_text = td[6].text
        address = address_text.split(',')[0]
        if len(address_text) > 1 and not UrlResults.objects.filter(record_id=id, date=date).first():
            state = 'CA'
            city = address_text.split(',')[1]
            zip = address_text.split(',')[2].split(' ')[-1]

            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                      address=address, city=city, description=description,
                                      state=state, zip=zip)

    return True


def url_22(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/PVR/Photovoltaic Residential')
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    date_start_str = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end_str = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start_str}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end_str}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
        id = td[2].text
        name = td[5].text
        status = td[7].text
        description = td[5].text
        address_text = td[6].text
        address = address_text.split(',')[0] if len(address_text) > 1 else ''
        city_text = address_text.split(',')[1] if len(address_text) > 1 else ''
        city = ' '.join(city_text.split(' ')[0:-2]) if city_text else ''
        state = 'CA'
        zip = city_text.split(' ')[-1][0:5] if city_text else ''
        if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id,
                date=date).first():
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                      address=address, city=city, description=description,
                                      state=state, zip=zip)

    return True


def url_23(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()
    time.sleep(40)
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        address_text = td[3].text
        status = td[4].text
        state = 'CA'
        address = address_text.split(',')[0] if len(address_text) > 1 else ''
        city = address_text.split(',')[1] if len(address_text) > 1 else ''
        zip = address_text.split(',')[-1].split(' ')[-1] if len(address_text) > 1 else ''
        if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id,
                date=date).first():
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                      address=address, city=city, state=state, zip=zip)

    return True


def url_24(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()
    time.sleep(15)
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        address_text = td[6].text
        status = td[7].text
        state = 'FL'
        address = address_text.split(',')[0] if len(address_text) > 1 else ''
        city = address_text.split(',')[1] if len(address_text) > 1 else ''
        zip = address_text.split(',')[-1].split(' ')[-1] if len(address_text) > 1 else ''
        if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id,
                date=date).first():
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                      address=address, city=city, state=state, zip=zip)

    return True


def url_25(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/BRSP')
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    date_start_str = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end_str = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start_str}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end_str}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
            id = td[2].text
            name = td[4].text
            address_text = td[5].text
            status = td[6].text
            description = td[7].text
            state = 'NM'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = ''.join(address_text.split(',')[1].split(' ')[1:-2]) if len(address_text) > 1 else ''
            zip = address_text.split(',')[1].split(' ')[-1] if len(address_text) > 1 else ''
            if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id,
                    date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip, description=description)

        return True


def url_26(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Dev-Services/DS Residential/Electrical/Solar')
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = td[1].text
            id = td[2].text
            name = td[4].text
            address_text = td[5].text
            status = td[6].text
            state = 'ID'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = address_text.split(',')[1].split(' ')[1]
            zip = address_text.split(',')[1].split(' ')[-1]
            if len(address_text) > 1 and status != '' and status != 'Pending' and not UrlResults.objects.filter(
                    record_id=id,
                    date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)

        return True


def url_27(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/NA')
    time.sleep(15)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = td[1].text
            id = td[2].text
            name = td[4].text
            address_text = td[5].text
            status = td[6].text
            state = 'AZ'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = ''.join(address_text.split(',')[1].split(' ')[0:-2])
            zip = address_text.split(',')[1].split(' ')[-1]
            if len(address_text) > 1 and status != '' and status != 'Pending' and not UrlResults.objects.filter(
                    record_id=id,
                    date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)

        return True


def url_28(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        print(len(records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]))
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            name = td[3].text
            address_text = td[4].text
            status = td[5].text
            state = 'AZ'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = address_text.split(',')[1] if len(address_text) > 1 else ''
            zip = address_text.split(',')[-1].split(' ')[-1]
            if len(address_text) > 1 and status != '' and status != 'Pending' and date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id, date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)

        return True


def url_29(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            name = td[5].text
            address_text = td[6].text
            status = td[7].text
            state = 'ID'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = address_text.split(',')[1] if len(address_text) > 1 else ''
            zip = address_text.split(',')[-1].split(' ')[-1]
            if len(address_text) > 1 and status != '' and status != 'Pending' and date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id, date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)

        return True


def url_30(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_CapView_ddlModule"]'))
    select.select_by_value('Contractors')
    time.sleep(5)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]

        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            name = td[2].text
            status = td[4].text
            if td[1].find_elements(By.TAG_NAME, 'a'):
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(EC.presence_of_element_located((By.XPATH, '//*['
                                                                     '@id'
                                                                     '="ctl00_PlaceHolderMain_shPermitDetail_lblSectionTitle"]')))
                firstname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div['
                                                           '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                           '1]/table/tbody/tr/td['
                                                           '1]/div/span/table/tbody/tr/td[2]/div/span[1]')
                lastname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div['
                                                          '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                          '1]/table/tbody/tr/td[1]/div/span/table/tbody/tr/td['
                                                          '2]/div/span[2]')

                applicant = None
                address = None
                city = None
                state = None
                zip = None
                if firstname and lastname:
                    applicant = f"{firstname[0].text} {lastname[0].text}"
                    address = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                            '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                            '1]/div/span/table/tbody/tr/td[2]/div/span[4]').text
                    city = driver.find_element(By.XPATH,
                                               '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                               '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                               '1]/div/span/table/tbody/tr/td[2]/div/span[5]').text
                    state = driver.find_element(By.XPATH,
                                                '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                '1]/div/span/table/tbody/tr/td[2]/div/span[6]').text
                    zip = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                        '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                        '1]/div/span/table/tbody/tr/td[2]/div/span[7]').text

                if date_start <= date <= date_end and not UrlResults.objects.filter(
                        record_id=id, date=date).first():
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                              applicant=applicant,
                                              address=address, city=city, state=state, zip=zip)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))

        return True


def url_31(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(
        driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]'))
    select.select_by_value('PnD/Building/Miscellaneous_1/Electrical')
    time.sleep(5)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

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
            date = td[1].text
            id = td[2].text
            name = td[5].text
            status = td[7].text
            if td[2].find_elements(By.TAG_NAME, 'a'):
                wait = WebDriverWait(driver, 10)
                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                firstname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[1]')
                lastname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                          '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                          '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[2]')

                applicant = None
                address = None
                city = None
                state = None
                zip = None
                if firstname and lastname:
                    applicant = f"{firstname[0].text} {lastname[0].text}"
                    address = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                            '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                            '1]/div/span/table/tbody/tr/td[2]/div/span[4]').text.replace(
                        ',', '')
                    city = driver.find_element(By.XPATH,
                                               '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                               '2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td['
                                               '1]/div/span/table/tbody/tr/td[2]/div/span[5]').text.replace(',', '')
                    state = driver.find_element(By.XPATH,
                                                '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td['
                                                '1]/div/span/table/tbody/tr/td[2]/div/span[6]').text.replace(
                        ',', '')
                    zip = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                        '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td['
                                                        '1]/div/span/table/tbody/tr/td[2]/div/span[7]').text.replace(
                        ',', '')

                    if not UrlResults.objects.filter(
                            record_id=id, date=date).first():
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                  applicant=applicant,
                                                  address=address, city=city, state=state, zip=zip)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))

        return True


def url_32(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    time.sleep(15)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Misc/Solar Electric Panels/NA')
    time.sleep(15)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[3].text
        status = td[2].text
        description = td[6].text
        address_text = td[5].text
        if status != '' and len(address_text) > 1 and not UrlResults.objects.filter(record_id=id, date=date).first():
            address = address_text.split(',')[0]
            city = 'Oakland'
            state = 'CA'
            zip = address_text.split(',')[1].split(' ')[-1]

            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, state=state, zip=zip)

    return True


def url_33(request, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
    time.sleep(15)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Building Department Web Permit/Residential Solar/NA')
    time.sleep(15)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[3].text
        status = td[5].text

        UrlResults.objects.create(url=url, record_id=id, date=date, status=status)

    return True


def url_34(request, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date()
    date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            description = td[2].text
            address_text = td[3].text
            status = td[4].text
            state = 'TX'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            city = address_text.split(',')[1] if len(address_text) > 1 else ''
            zip = address_text.split(',')[-1].split(' ')[-1]
            if len(address_text) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id, date=date).first():
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, description=description,
                                          address=address, city=city, state=state, zip=zip)

        return True


def chrome_driver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver


def var_checker(data):
    if data:
        return data.text
    return ''

# next_page = current data
# while next_page
# for i in range(0, 10):
# if i == 9:
# scrape the data
#
