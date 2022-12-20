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
from gsheetapi import main
import threading
import time
import random


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
                date_start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d').date().strftime(
                    '%m/%d/%Y')
                date_end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
                if request.POST.get('url'):
                    url = Urls.objects.get(id=request.POST.get('url'))
                    url_req = exec(f"url_{url.id}(date_start, date_end, url)")
                    return JsonResponse({'statusMsg': 'Success'}, status=200)

                url_func = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12,
                            url_13,
                            url_14, url_15, url_16, url_17, url_18, url_19, url_20, url_21, url_22, url_23, url_24,
                            url_25, url_26, url_27, url_28, url_29, url_30, url_31, url_32, url_33, url_34, url_35,
                            url_36, url_37, url_38, url_39, url_40, url_41, url_42, url_43, url_44, url_45, url_46,
                            url_47, url_48, url_49, url_50, url_51, url_52, url_53, url_54, url_55, url_56]

                counter = 0
                threads = []
                for i in Urls.objects.all():
                    if i.is_active:
                        t = threading.Thread(target=url_func[counter], args=(date_start, date_end, i))
                        t.start()
                        threads.append(t)

                    counter += 1

                for thread in threads:
                    thread.join()

                return JsonResponse({'statusMsg': 'Success'}, status=200)

            return render(request, 'index.html', context)
    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)


def url_1(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

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
    values = []
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

                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    city,
                    state,
                    zip,
                    applicant,
                    '',
                    '',
                    '',
                    '',
                    '',
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name, address=address,
                                          city=city, state=state, zip=zip, applicant=applicant, description=description,
                                          job_value=value)
    main(url.description, values)
    return True


def url_2(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    time.sleep(15)

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
    values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name, address=address,
                                          city=city, state=state, zip=zip, description=description)
    main(url.description, values)
    return True


def url_3(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/NA')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table_tr = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                      '1]/table/tbody/tr/td/div[2]/div[3]/div/div/div['
                                                      '2]/div[2]/div[3]/div[1]/div/table/tbody/tr')

    if records_table_tr:
        values = []
        for i in range(0, len(records_table_tr[2:-1])):
            records_table_tr = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                              '1]/table/tbody/tr/td/div[2]/div[3]/div/div/div['
                                                              '2]/div[2]/div[3]/div[1]/div/table/tbody/tr')[2:-1]
            td = records_table_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[8])
            name = var_checker(td[4])
            description = var_checker(td[5])
            if td[2].find_elements(By.TAG_NAME, 'a'):
                wait = WebDriverWait(driver, 10)
                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                               '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                               '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr['
                                               '2]/td')
                job_value = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[2]/table/tbody/tr['
                                                           '2]/td[2]/div/span[1]/table/tbody/tr[2]/td/div/div/span[2]')
                if owner and address and job_value and not UrlResults.objects.filter(record_id=id, date=date).first():
                    owner = f"{var_checker(owner[0])}"
                    address = var_checker(address[0])

                    city_text = var_checker(
                        driver.find_element(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                      '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                      '1]/table/tbody/tr[2]/td['
                                                      '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                      '2]/table/tbody/tr[3]/td')).split(' ')

                    if len(city_text) <= 2:
                        city_text = var_checker(
                            driver.find_element(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                          '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                          '2]/td[2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                          '2]/table/tbody/tr[4]/td')).split(' ')
                    state = 'FL'
                    zip = city_text[-1].split('-')[0]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)

                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        var_checker(job_value[0]),
                        '',
                        '',
                        '',
                    ]
                    values.append(temp_values)
                    print(var_checker(job_value[0]) if job_value else '')
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                              address=address, city=' '.join(city), state=state, zip=zip, owner=owner,
                                              description=description,
                                              job_value=var_checker(job_value[0]))

            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_4(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(10)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            owner = None
            address = None
            city_text = None
            state = None
            city = None
            zip = None
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date).first():

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                             '5]/div/div[3]/div[1]/div[1]/table/tbody/tr['
                                             '2]/td/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr['
                                             '1]/td')

                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                               '5]/div/div[3]/div[1]/div[1]/table/tbody/tr['
                                               '2]/td/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                               '2]/table/tbody/tr[2]/td')
                if owner and address:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(
                        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                      '5]/div/div[3]/div[1]/div[1]/table/tbody/tr['
                                                      '2]/td/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                      '2]/table/tbody/tr[3]/td'))

                    city = city_text.split(' ')[0]

                    state = city_text.split(' ')[1]
                    zip = city_text.split(' ')[-1]

                    if owner and not UrlResults.objects.filter(
                            record_id=id, date=date).first():
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            '',
                            '',
                            address,
                            city,
                            state,
                            zip,
                            '',
                            owner,
                            '',
                            '',
                            '',
                            '',
                        ]

                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                                  address=address, city=city, state=state, zip=zip)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_5(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address, city=city,
                                      state=state, zip=zip, name=name)
    main(url.description, values)
    return True


def url_6(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_7(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_8(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_9(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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
            zip = address_text[2].split(',')[-1][0:6]

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                ''
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_10(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    driver.find_element(By.XPATH, '/html/body/section/div[1]/a').click()

    search = driver.find_element(By.ID, 'txtSearchCondition')
    search.send_keys('solar')

    time.sleep(5)

    driver.find_element(By.ID, 'btnSearch').click()

    time.sleep(10)

    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        status = td[2].text
        name = td[6].text

        if td[1].find_elements(By.TAG_NAME, 'a') and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():

            td[1].find_element(By.TAG_NAME, 'a').click()
            wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
            owner = driver.find_elements(By.XPATH,
                                         '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                         '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr/td['
                                         '2]/table/tbody/tr[1]/td')

            address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                     '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                     '2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr['
                                                     '2]/td')

            if owner and address:
                owner = var_checker(owner[0])
                address = var_checker(address[0])
                city_text = driver.find_element(By.XPATH,
                                                '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[3]/td')
                city = 'Plantation'
                zip = city_text.split(' ')[-1]
                state = 'ZIP'

                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    owner,
                    '',
                    '',
                    '',
                    '',
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                          address=address, city=city, state=state, zip=zip, name=name)
        driver.get(url.url)
        wait.until(
            EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
    main(url.description, values)
    return True


def url_11(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_12(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_13(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                '',
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_14(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/SolarPV/Residential/NA')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    values = []
    records_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[7]/div[1]/table/tbody/tr/td/div['
                                                  '2]/div[3]/div/div/div[2]/div[2]/div[3]/div[1]/div/table')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = td[1].text
        id = td[2].text
        status = td[7].text
        description = td[4].text
        name = td[5].text
        address_text = var_checker(td[6])
        if address_text and not UrlResults.objects.filter(record_id=id, date=date).first():
            address = address_text.split(',')[0]
            state = 'UT'
            city_text = address_text.split(',')[-1].split(' ')
            city = None
            zip = city_text[-1].split('-')[0]
            counter = 0
            for row in city_text:
                if row.isdigit():
                    city_text.pop(counter)
                elif row == 'UT' or row == '':
                    city_text.pop(counter)
                counter += 1
            city_text.pop(-1)
            city = ' '.join(city_text)

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, name=name, state=state, zip=zip)
    main(url.description, values)
    return True


def url_15(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

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

    values = []
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
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, name=name,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_16(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(5)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/Permit')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    values = []
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
                city = 'Las Vegas'
                state = 'NV'
                zip = None
                for row in permit_details_tr[1]:
                    if type(row) is bs4.element.Tag:
                        td = row.table.tr.find_all('td', style="vertical-align:top")
                        applicant = td[0].text
                        address = td[1].text
                        city_text = td[2].text.split(' ')
                        state = 'NV'
                        zip = city_text[-2]
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    city,
                    state,
                    zip,
                    applicant,
                    '',
                    '',
                    '',
                    '',
                    '',
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, description=description, name=name, applicant=applicant,
                                          state=state, zip=zip)
    main(url.description, values)
    return True


def url_17(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

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

    values = []
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
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                '',
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address, city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_18(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(5)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar Photovoltaic System/Residential/NA')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = var_checker(td[1])
        id = var_checker(td[2])
        status = var_checker(td[6])
        address_text = var_checker(td[5])
        description = var_checker(td[4])
        address = address_text.split(',')[0]
        city_text = address_text.split(',')[1].split(' ')
        city = 'Alameda'
        state = 'CA'
        zip = city_text[-1]
        if len(address_text) > 1 and not UrlResults.objects.filter(record_id=id, date=date).first():
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                '',
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, description=description, date=date, status=status,
                                      address=address, city=city,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_19(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    time.sleep(5)

    permit_number = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber')
    permit_number.send_keys('PLEX')

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[5])
            description = var_checker(td[4])
            if td[2].find_elements(By.TAG_NAME, 'a'):

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                               '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                               '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')

                if owner and address and not UrlResults.objects.filter(
                        record_id=id, date=date).first():
                    owner = f"{var_checker(owner[0])}"

                    state = "Columbus"
                    address = var_checker(address[0])
                    city = var_checker(driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div['
                                                                     '2]/div[1]/div[3]/div[5]/div[2]/div[3]/div['
                                                                     '1]/div[1]/table/tbody/tr[2]/td['
                                                                     '2]/div/span/table/tbody/tr/td['
                                                                     '2]/table/tbody/tr[3]/td'))

                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        '',
                        description,
                        address,
                        city if city != 'COLUMBUS' and city != 'Columbus' else '',
                        state,
                        '',
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address,
                                              city=city if city != 'COLUMBUS' and city != 'Columbus' else '',
                                              state=state,
                                              description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
    main(url.description, values)
    return True


def url_20(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Permits/Residential/Solar/NA')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[5])
            name = var_checker(td[4])
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                first_name = driver.find_elements(By.CLASS_NAME, 'contactinfo_firstname')
                last_name = driver.find_elements(By.CLASS_NAME, 'contactinfo_lastname')
                address = driver.find_elements(By.CLASS_NAME, 'contactinfo_addressline1')
                city_text = driver.find_elements(By.CLASS_NAME, 'contactinfo_region')

                if first_name and last_name and address and city_text:
                    applicant = f"{var_checker(first_name[0])} {var_checker(last_name[0])}"
                    address = var_checker(address[0])
                    state = 'UT'
                    city = var_checker(city_text[0])
                    zip = var_checker(city_text[-1]).split('-')[0]
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        '',
                        applicant,
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, applicant=applicant,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)

    return True


def url_21(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)

    values = []
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

            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                      address=address, city=city, description=description,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_22(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/PVR/Photovoltaic Residential')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    values = []
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
        date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
        date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
        if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id,
                date=date).first():
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                      address=address, city=city, description=description,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_23(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(30)

    values = []
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
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                '',
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                      address=address, city=city, state=state, zip=zip)
    main(url.description, values)
    return True


def url_24(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(15)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
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
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                '',
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                      address=address, city=city, state=state, zip=zip)
    main(url.description, values)
    return True


def url_25(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/BRSP')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    values = []
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
            date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
            date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
            if len(address_text) > 1 and status != '' and date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id,
                    date=date).first():
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip, description=description)
        main(url.description, values)
        return True


def url_26(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Dev-Services/DS Residential/Electrical/Solar')
    time.sleep(15)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(15)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)
        return True


def url_27(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

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

    values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)
        return True


def url_28(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)
        return True


def url_29(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)
        return True


def url_30(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_CapView_ddlModule"]'))
    select.select_by_value('Contractors')
    time.sleep(5)

    values = []
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
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        applicant,
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                              applicant=applicant,
                                              address=address, city=city, state=state, zip=zip)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
        return True


def url_31(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(
        driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]'))
    select.select_by_value('PnD/Building/Miscellaneous_1/Electrical')
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(15)

    values = []
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

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                firstname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[1]')
                lastname = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                          '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                          '1]/td[1]/div/span/table/tbody/tr/td[2]/div/span[2]')

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
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            name,
                            '',
                            address,
                            city,
                            state,
                            zip,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]

                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                  applicant=applicant,
                                                  address=address, city=city, state=state, zip=zip)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
        return True


def url_32(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
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

    values = []
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
            temp_values = [
                url.description,
                str(date),
                id,
                '',
                '',
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
                ''
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, state=state, zip=zip)
    main(url.description, values)
    return True


def url_33(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Building Department Web Permit/Residential Solar/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = td[1].text
            id = td[2].text
            status = td[5].text
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date).first():

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner_details = driver.find_elements(By.XPATH,
                                                     '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                     '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                     '2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr')

                address = None
                city = None
                state = None
                zip = None
                if owner_details:
                    owner = f"{var_checker(owner_details[0])}"
                    address = var_checker(
                        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                      '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                      '2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr['
                                                      '2]/td'))

                    owner_details = driver.find_elements(By.XPATH,
                                                         '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[ '
                                                         '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                         '2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr')
                    city_text = var_checker(owner_details[-1])
                    city = city_text.split(' ')[0]

                    state = city_text.split(' ')[1]
                    zip = city_text.split(' ')[-1][0:5]

                    if not UrlResults.objects.filter(
                            record_id=id, date=date).first():
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            '',
                            '',
                            address,
                            city,
                            state,
                            zip,
                            '',
                            owner,
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]

                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                                  address=address, city=city, state=state, zip=zip)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_34(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    time.sleep(30)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
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
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    '',
                    description,
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, description=description,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)
    return True


def url_35(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if td[2].find_elements(By.TAG_NAME, 'a'):

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                               '5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                               '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')

                if owner and address and not UrlResults.objects.filter(
                        record_id=id, date=date).first():
                    owner = f"{var_checker(owner[0])}"
                    address = var_checker(address[0])

                    city_text = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                              '1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                              '1]/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr/td['
                                                              '2]/table/tbody/tr[3]/td')
                    city = var_checker(city_text).split(' ')[0]

                    state = var_checker(city_text).split(' ')[1]
                    zip = var_checker(city_text).split(' ')[-1]
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_36(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/NA/NA')
    time.sleep(10)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(10)
    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
        id = var_checker(td[2])
        status = var_checker(td[6])
        description = var_checker(td[8])
        name = var_checker(td[4])
        address_text = var_checker(td[5]).split(',') if var_checker(td[5]) else None
        if address_text and len(
                address_text[0].split(' ')) > 1 and date_start <= date <= date_end and not UrlResults.objects.filter(
            record_id=id, date=date).first():
            state = 'FL'
            address = ' '.join(address_text[0].split(' ')[0:len(address_text[0].split(' ')) - 2])
            city = address_text[0].split(' ')[-2]
            zip = address_text[0].split(' ')[-1]
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                description,
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
                ''
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, description=description, name=name,
                                      state=state, zip=zip)
    main(url.description, values)
    return True


def url_37(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(10)
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    values = []
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = var_checker(td[1])
        id = var_checker(td[2])
        status = var_checker(td[6])
        name = var_checker(td[5])
        address_text = var_checker(td[4]).split(',') if var_checker(td[4]) else None
        if address_text and date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                             date=date).first():
            state = 'VA'
            address = ' '.join(address_text[0].split(' ')[0:-2])
            city = address_text[0].split(' ')[-1]
            zip = address_text[1].split(' ')[2]
            temp_values = [
                url.description,
                str(date),
                id,
                status,
                name,
                '',
                address,
                city,
                state,
                zip,
                '',
                '',
                '',
                '',
                '',
                '',
                ''
            ]

            values.append(temp_values)
            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                      city=city, name=name, state=state, zip=zip)
    main(url.description, values)
    return True


def url_38(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Permits/Solar - Photovoltaic Permit/Permit')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            description = var_checker(td[4])
            status = var_checker(td[9])
            name = var_checker(td[5])
            address_text = var_checker(td[6])
            address = address_text.split(',')[0].replace('City of San Antonio', '')
            city = 'San Antonio'
            zip = address_text.split(',')[-1].split(' ')[-1]
            state = 'TX'
            if not UrlResults.objects.filter(
                    record_id=id, date=date).first():
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, description=description,
                                          address=address, city=city, state=state, zip=zip, name=name)
        main(url.description, values)
    return True


def url_39(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Solar PV/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            description = var_checker(td[5])
            status = var_checker(td[7])
            name = var_checker(td[6])
            address_text = var_checker(td[4])
            address = address_text.split(',')[0]
            city = 'Atlanta'
            zip = address_text.split(',')[-1].split(' ')[-1]
            state = 'GA'
            if td[2].find_elements(By.TAG_NAME, 'a'):

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td')

                if owner and not UrlResults.objects.filter(
                        record_id=id, date=date).first():
                    owner = f"{var_checker(owner[0])}"
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_40(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/NA/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            description = var_checker(td[8])
            status = var_checker(td[6])
            name = var_checker(td[4])
            address_text = var_checker(td[5])
            address = address_text.split(',')[0]
            city = 'DELAND'
            zip = address_text.split(',')[-1].split(' ')[-1]
            state = 'FL'
            if td[2].find_elements(By.TAG_NAME, 'a'):

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td')

                if owner and not UrlResults.objects.filter(
                        record_id=id, date=date).first():
                    owner = f"{var_checker(owner[0])}"
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_41(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[7]/div['
                                                  '1]/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/div/div['
                                                  '2]/table')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            values = []
            records_table = driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[7]/div['
                                                          '1]/table/tbody/tr/td/div/table/tbody/tr['
                                                          '1]/td/div/div/div/div/div[ '
                                                          '2]/table')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            name = var_checker(td[5])
            status = var_checker(td[6])
            if td[1].find_elements(By.TAG_NAME,
                                   'a') and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id, date=date).first():

                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                             '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td')

                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')
                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0])

                    city = 'Tampa'
                    zip = city_text.split(' ')[-1].split('-')[0]
                    state = 'FL'
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/div/div[7]/div['
                                                          '1]/table/tbody/tr/td/div/table/tbody/tr['
                                                          '1]/td/div/div/div/div/div[ '
                                                          '2]/table')))
        main(url.description, values)
    return True


def url_42(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                  '1]/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/div/div['
                                                  '2]/table')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[7]/div['
                                                          '1]/table/tbody/tr/td/div/table/tbody/tr['
                                                          '1]/td/div/div/div/div/div[2]/table')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[7])
            name = var_checker(td[5])
            address_text = var_checker(td[6])
            if date_start <= date <= date_end and len(address_text) > 1 and not UrlResults.objects.filter(
                    record_id=id, date=date).first():
                address = address_text.split(',')[0]
                city = 'Visalia'
                zip = address_text.split(',')[-1].split(' ')[-1]
                state = 'CA'
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                          address=address, city=city, state=state, zip=zip, name=name)
        main(url.description, values)
    return True


def url_43(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSSubAgency'))
    select.select_by_value('WASHOE')
    time.sleep(5)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Energy Permit/NA/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[4])
            description = var_checker(td[9])
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date).first():

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                           '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'NV'
                    zip = city_text[-1]
                    city_text.pop(-1)
                    counter = 0
                    for row in city_text:
                        if row == 'NV':
                            city_text.pop(counter)
                        counter += 1

                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description)

            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_44(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Permits/Residential/Solar/NA')
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[1]), '%m/%d/%Y').date()
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[4])
            if date_start <= date <= date_end and td[2].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():

                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                contractor_text = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div['
                                                                 '1]/div[3]/div[5]/div/div[3]/div['
                                                                 '1]/div/table/tbody/tr/td['
                                                                 '1]/div/span/table/tbody/tr/td[2]')

                if contractor_text:
                    contractor_text = var_checker(contractor_text[0]).split('\n')
                    owner = contractor_text[0]
                    address = contractor_text[1]
                    city_text = contractor_text[2].split(',')
                    state = 'CA'
                    city = city_text[0]
                    zip = city_text[-1]
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)

            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_45(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Trades/Electrical/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[6])
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[7])
            description = var_checker(td[8])
            if td[1].find_elements(By.TAG_NAME,
                                   'a') and 'solar' in description.lower() and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[ '
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[ '
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'FL'
                    city = None
                    zip = city_text[-2]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_46(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Accessories/Residential/Solar Photovoltaic')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[5])
            description = var_checker(td[4])
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr['
                                                           '3]/td')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'FL'
                    city = None
                    zip = city_text[-1]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        '',
                        description,
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_47(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[7])
            name = var_checker(td[6])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div/main/div/div/div/div[1]/div['
                                                       '7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                       '1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div/main/div/div/div/div[1]/div['
                                                         '7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div['
                                                         '1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div/main/div/div/div/div['
                                                           '1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div['
                                                           '1]/div[1]/table/tbody/tr[2]/td['
                                                           '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'FL'
                    city = None
                    zip = city_text[-1]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return True


def url_48(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[7])
            name = var_checker(td[5])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr['
                                                           '3]/td')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'FL'
                    city = None
                    zip = city_text[-1].split('-')[0]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)

    return True


def url_49(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')
                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'FL'
                    city = None
                    zip = city_text[-1].split('-')[0]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)

    return True


def url_50(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                       '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                           '2]/td[2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')
                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = 'TX'
                    city = None
                    zip = city_text[-1].split('-')[0]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        owner,
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)

    return True


def url_51(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    time.sleep(30)
    select = Select(driver.find_element(By.ID, 'PermitCriteria_SortBy'))
    select.select_by_value('string:IssueDate')

    time.sleep(2)

    select = Select(driver.find_element(By.ID, 'SortAscending'))
    select.select_by_value('boolean:false')
    time.sleep(10)

    element_start_count = 9
    values = []
    for i in range(0, 299):
        row = driver.find_element(By.ID, f'entityRecordDiv{i}')
        date = row.find_elements(By.XPATH,
                                 f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[5]/span')
        if date:
            date = datetime.strptime(date[0].text, '%m/%d/%Y').date()

            if date_start <= date <= date_end:
                id = row.find_element(By.XPATH,
                                      f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[2]/a/tyler-highlight/span').text
                address_text = row.find_element(By.XPATH,
                                                f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div['
                                                f'5]/div[2]/div[{element_start_count}]/div[2]/div['
                                                f'11]/tyler-highlight/span').text.split(
                    ' ')
                if len(address_text) > 1:
                    description = row.find_element(By.XPATH,
                                                   f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div['
                                                   f'5]/div[ '
                                                   f'2]/div[{element_start_count}]/div[2]/div['
                                                   f'12]/tyler-highlight/span').text
                    status = row.find_element(By.XPATH,
                                              '/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              '2]/div[9]/div[2]/div[8]/label').text
                    name = row.find_element(By.XPATH,
                                            '/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                            '2]/div[ '
                                            '9]/div[2]/div[6]/label').text

                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date).first():
                        state = address_text[-2]
                        city = address_text[-3]
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address = ' '.join(address_text)
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            name,
                            description,
                            address,
                            city,
                            state,
                            zip,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city,
                                                  state=state, zip=zip, name=name)
            i += 1
            element_start_count += 1
        elif not date:
            break

    main(url.description, values)
    return True


def url_52(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            address_text = var_checker(td[4])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                address = address_text.split(',')[0]
                city = 'CONCORD'
                state = 'CA'
                zip = address_text.split(',')[-1].split(' ')[-1]

                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    '',
                    '',
                    address,
                    'CONCORD',
                    'CA',
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                          address=address, city=city, state=state, zip=zip)
        main(url.description, values)

    return True


def url_53(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[1]/div[3]/div['
                                                         '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td['
                                                         '2]/span')
                if address:
                    address = var_checker(address[0])
                    state = 'CA'
                    city = 'Santa Rosa'
                    zip = '95403'
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                              city=city, state=state, zip=zip, name=name)

            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)

    return True


def url_54(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                             '2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                             '2]/td/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr['
                                             '1]/td')

                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div['
                                               '2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                               '2]/td/div/span/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr['
                                               '2]/td')
                if owner and address:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    state = 'AZ'
                    city = 'Pima County'
                    zip = '85719'
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        city,
                        state,
                        zip,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                              city=city, state=state, zip=zip, name=name, owner=owner)

            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)

    return True


def url_55(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            address_text = var_checker(td[4])
            if address_text != '' and date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                                             'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():

                address = address_text.split(',')[0]
                state = 'CA'
                city = 'Lake County'
                zip = address_text.split(',')[-1].split(' ')[1]
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, state=state, zip=zip, name=name)
        main(url.description, values)

    return True


def url_56(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[4])
            address_text = var_checker(td[5])
            if address_text != '' and date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                                             'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():

                address = address_text.split(',')[0]
                state = 'CA'
                city = 'Roseville'
                zip = address_text.split(',')[-1].split(' ')[-1]
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    '',
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, state=state, zip=zip, name=name)
        main(url.description, values)

    return True


def url_57(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    time.sleep(5)

    start_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_lblGSExpand').click()
    time.sleep(2)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_0'))
    select.select_by_value('Residential')

    time.sleep(2)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_1'))
    select.select_by_value('Solar Array')

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-1]
        values = []
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[1]), '%m/%d/%Y').date()
            id = var_checker(td[2])
            status = var_checker(td[6])
            description = var_checker(td[4])
            address_text = var_checker(td[5])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                                             'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():

                address = address_text.split(',')[0]
                city_text = address_text.split(',')[-1].split(' ')
                state = 'CA'
                zip = city_text[-1]
                city_text.pop(-1)
                city_text.pop(-1)
                city = ' '.join(city_text)
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    '',
                    description,
                    address,
                    city,
                    state,
                    zip,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                          city=city, state=state, zip=zip, description=description)
        main(url.description, values)

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


def beautifulsoup(url):
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'lxml')
    return soup


def containsNumber(value):
    if True in [char.isdigit() for char in value]:
        return True
    return False

# next_page = current data
# while next_page
# for i in range(0, 10):
# if i == 9:
# scrape the data
#
