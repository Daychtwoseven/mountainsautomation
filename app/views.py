# Django
from urllib.request import Request, urlopen

import bs4
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect
from selenium.webdriver import ActionChains

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
                            url_47, url_48, url_49, url_50, url_51, url_52, url_53, url_54, url_55, url_56, url_57,
                            url_58, url_59, url_60, url_61, url_62, url_63, url_64, url_65, url_66, url_67, url_68,
                            url_69, url_70,
                            url_71, url_72, url_73, url_74, url_75, url_76, url_77, url_78, url_79, url_80, url_81,
                            url_82, url_83,
                            url_84, url_85, url_86, url_87, url_88, url_89, url_90, url_91, url_92, url_93, url_93,
                            url_94, url_95, url_96, url_97, url_98, url_99, url_100, url_101, url_102, url_103, url_104,
                            url_105, url_106, url_107, url_108, url_109, url_110, url_111, url_112, url_113, url_114,
                            url_115,
                            url_116]

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
    reach = 0

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
        if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        if result_table:
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
            for row in result_tr:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = var_checker(td[1])
                id = var_checker(td[2])
                status = var_checker(td[6])
                name = var_checker(td[4])
                td_status = var_checker(td[6])
                description = var_checker(td[9])
                if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
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
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                  address=address,
                                                  city=city, state=state, zip=zip, applicant=applicant,
                                                  description=description,
                                                  job_value=value)

    main(url.description, values)
    return True


def url_2(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        if result_table:
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
            for row in result_tr:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = td[1].text
                id = td[2].text
                status = td[6].text
                name = td[4].text
                td_status = td[6].text
                description = td[4].text
                if td_status != "" and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
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
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                  address=address,
                                                  city=city, state=state, zip=zip, description=description)

    main(url.description, values)
    return True


def url_3(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0

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
                href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
                soup = beautifulsoup(href)
                address_text = soup.find(id='tbl_worklocation').text.split('*')
                contractor = soup.find(id='tbl_licensedps').text
                job_value = soup.find(id='ctl00_PlaceHolderMain_PermitDetailList1_tdADIContent').text

                if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                    if len(address_text) >= 2:
                        address = address_text[0]
                        city_text = address_text[-1].split(' ')
                        zip = city_text[-2]
                        state = city_text[-3]
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
                            '',
                            job_value,
                            '',
                            '',
                            '',
                            contractor
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                  address=address, city=' '.join(city), state=state, zip=zip,
                                                  description=description, job_value=job_value, contractor=contractor)

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    status = var_checker(td[8])
                    name = var_checker(td[4])
                    description = var_checker(td[5])
                    if td[2].find_elements(By.TAG_NAME, 'a'):
                        href = td[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
                        soup = beautifulsoup(href)
                        address_text = soup.find(id='tbl_worklocation').text.split('*')
                        contractor = soup.find(id='tbl_licensedps').text
                        job_value = soup.find(id='ctl00_PlaceHolderMain_PermitDetailList1_tdADIContent').text

                        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                            if len(address_text) >= 2:
                                address = address_text[0]
                                city_text = address_text[-1].split(' ')
                                zip = city_text[-2]
                                state = city_text[-3]
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
                                    '',
                                    job_value,
                                    '',
                                    '',
                                    '',
                                    contractor
                                ]
                                values.append(temp_values)
                                UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                          address=address, city=' '.join(city), state=state, zip=zip,
                                                          description=description, job_value=job_value,
                                                          contractor=contractor)

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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():

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
    reach = 0
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in result_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            address_text = td[4].text.split(',') if td[4] else ''
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_6(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[5].text
            name = td[3].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_7(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[5].text
            name = td[3].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
                    UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                              address=address,
                                              city=city,
                                              state=state, zip=zip)
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_8(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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
            else:
                reach = 1
                break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[5].text
            name = td[3].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
                    UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                              address=address,
                                              city=city,
                                              state=state, zip=zip)
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_9(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[5].text
            name = td[3].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
                    UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                              address=address,
                                              city=city,
                                              state=state, zip=zip)
            else:
                reach = 1
                break

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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if td[1].find_elements(By.TAG_NAME, 'a'):
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
            driver.back()
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[2].text
            name = td[6].text

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if td[1].find_elements(By.TAG_NAME, 'a'):
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
                driver.back()
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_11(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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
        else:
            print(row.text)
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[2].text
            status = td[3].text
            name = td[5].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
                    UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                              address=address,
                                              city=city,
                                              state=state, zip=zip)
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_12(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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

        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 1:
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

        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[2].text
            name = td[5].text
            address_text = td[4].text.split(',')

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 1:
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
                    UrlResults.objects.create(url=url, record_id=id, name=name, date=date, status=status,
                                              address=address,
                                              city=city,
                                              state=state, zip=zip)

            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_13(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and len(address_text) > 2:
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
        else:
            reach = 1

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            status = td[5].text
            address_text = td[4].text.split(',')
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and len(address_text) > 2:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_14(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0

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
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if address_text:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
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
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if address_text:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_15(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        if not UrlResults.objects.filter(record_id=id, date=date).first():
            if status != '' and status != "Pending" and len(address_text) > 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = td[2].text
            id = td[1].text
            status = td[4].text
            description = td[6].text
            name = td[7].text
            address_text = td[5].text.split(',')
            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if status != '' and status != "Pending" and len(address_text) > 1:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_16(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if status != '' and status != "Pending" :
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

        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = td[1].text
            id = td[2].text
            status = td[6].text
            description = td[4].text
            name = td[5].text
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if status != '' and status != "Pending":
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

            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_17(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    time.sleep(5)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/PV/.')
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
        status = td[3].text
        address_text = td[6].text
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if status != '' and status != "Pending":
                address = address_text.split(',')[0]
                city_text = address_text.split(',')[1].split(' ')
                zip = city_text[-1]
                state = city_text[-2]
                city_text.pop(-1)
                city_text.pop(-1)
                city = ' '.join(city_text)
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = td[1].text
            id = td[2].text
            status = td[3].text
            address_text = td[6].text
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if status != '' and status != "Pending":
                    address = address_text.split(',')[0]
                    city_text = address_text.split(',')[1].split(' ')
                    zip = city_text[-1]
                    state = city_text[-2]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
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


def url_18(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if len(address_text) > 1:
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
                                          address=address, city=city, state=state, zip=zip)

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
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
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if len(address_text) > 1:
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
                                              address=address, city=city, state=state, zip=zip)

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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():
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
                driver.back()

        main(url.description, values)

    return True


def url_21(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    time.sleep(15)

    values = []
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = td[1].text
        name = td[5].text
        status = td[7].text
        description = td[4].text
        address_text = td[6].text
        address = address_text.split(',')[0]
        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if len(address_text) > 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            name = td[5].text
            status = td[7].text
            description = td[4].text
            address_text = td[6].text
            address = address_text.split(',')[0]
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                if len(address_text) > 1:
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_22(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0

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
        address_text = td[6].text.split(',')

        if not UrlResults.objects.filter(record_id=id, date=date).first():
            if len(address_text) > 1 and status != '':
                address = address_text[0] if len(address_text) > 1 else ''
                city_text = address_text[1] if len(address_text) > 1 else ''
                city = ' '.join(city_text.split(' ')[0:-2]) if city_text else ''
                state = 'CA'
                zip = city_text.split(' ')[-1][0:5] if city_text else ''
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
                                          address=address, city=city, description=description, state=state, zip=zip)

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
            id = td[2].text
            name = td[5].text
            status = td[7].text
            description = td[5].text
            address_text = td[6].text.split(',')

            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '':
                    address = address_text[0] if len(address_text) > 1 else ''
                    city_text = address_text[1] if len(address_text) > 1 else ''
                    city = ' '.join(city_text.split(' ')[0:-2]) if city_text else ''
                    state = 'CA'
                    zip = city_text.split(' ')[-1][0:5] if city_text else ''
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
                                              address=address, city=city, description=description, state=state, zip=zip)
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
    reach = 0
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
        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if len(address_text) > 1 and status != '':
                city = address_text.split(',')[1] if len(address_text) > 1 else ''
                zip = address_text.split(',')[-1].split(' ')[-1] if len(address_text) > 1 else ''
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = td[1].text
            address_text = td[6].text
            status = td[7].text
            state = 'FL'
            address = address_text.split(',')[0] if len(address_text) > 1 else ''
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '':
                    city = address_text.split(',')[1] if len(address_text) > 1 else ''
                    zip = address_text.split(',')[-1].split(' ')[-1] if len(address_text) > 1 else ''
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
            else:
                reach = 1
                break

    main(url.description, values)
    return True


def url_25(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0

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
            address_text = td[5].text.split(',')
            status = td[6].text
            description = td[7].text
            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '':
                    address = address_text[0]
                    city_text = address_text[1].split(' ')
                    zip = city_text[-1]
                    state = city_text[-2]
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
                        '',
                        '',
                        '',
                        '',
                        '',
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                              address=address, city=city, state=state, zip=zip, description=description)

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if records_table:
                for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
                    id = td[2].text
                    name = td[4].text
                    address_text = td[5].text.split(',')
                    status = td[6].text
                    description = td[7].text
                    if not UrlResults.objects.filter(record_id=id, date=date).first():
                        if len(address_text) > 1 and status != '':
                            address = address_text[0]
                            city_text = address_text[1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
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
                                '',
                                '',
                                '',
                                '',
                                '',
                            ]

                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, status=status, name=name,
                                                      address=address, city=city, state=state, zip=zip,
                                                      description=description)

        main(url.description, values)
        return True


def url_26(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0

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
            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '' and status != 'Pending':
                    city = address_text.split(',')[1].split(' ')[1]
                    zip = address_text.split(',')[1].split(' ')[-1]
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

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = td[1].text
                id = td[2].text
                name = td[4].text
                address_text = td[5].text
                status = td[6].text
                state = 'ID'
                address = address_text.split(',')[0] if len(address_text) > 1 else ''
                if not UrlResults.objects.filter(record_id=id, date=date).first():
                    if len(address_text) > 1 and status != '' and status != 'Pending':
                        city = address_text.split(',')[1].split(' ')[1]
                        zip = address_text.split(',')[1].split(' ')[-1]
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
    reach = 0

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
            address_text = td[5].text.split(',')
            status = td[6].text
            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '' and status != 'Pending':
                    address = address_text[0]
                    city_text = address_text[-1].split(' ')
                    zip = city_text[-1]
                    state = city_text[-2]
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

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if records_table:
                for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = td[1].text
                    id = td[2].text
                    name = td[4].text
                    address_text = td[5].text.split(',')
                    status = td[6].text
                    if not UrlResults.objects.filter(record_id=id, date=date).first():
                        if len(address_text) > 1 and status != '' and status != 'Pending':
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
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
    reach = 0
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
            address_text = td[4].text.split(',')
            status = td[5].text

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '' and status != 'Pending':
                    address = address_text[0]
                    city = address_text[1]
                    state_text = address_text[-1].split(' ')
                    zip = state_text[-1]
                    state = state_text[1]
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
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if records_table:
                for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
                    id = td[1].text
                    name = td[3].text
                    address_text = td[4].text.split(',')
                    status = td[5].text

                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                        date=date).first():
                        if len(address_text) > 1 and status != '' and status != 'Pending':
                            address = address_text[0]
                            city = address_text[1]
                            state_text = address_text[-1].split(' ')
                            zip = state_text[-1]
                            state = state_text[1]
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
                    else:
                        reach = 1
                        break

        main(url.description, values)
        return True


def url_29(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
            address_text = td[6].text.split(',')
            status = td[7].text

            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1 and status != '' and status != 'Pending':
                    address = address_text[0]
                    city = address_text[1]
                    state_text = address_text[-1].split(' ')
                    zip = state_text[-1]
                    state = state_text[-2]
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
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if records_table:
                for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
                    id = td[1].text
                    name = td[5].text
                    address_text = td[6].text.split(',')
                    status = td[7].text

                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                        date=date).first():
                        if len(address_text) > 1 and status != '' and status != 'Pending':
                            address = address_text[0]
                            city = address_text[1]
                            state_text = address_text[-1].split(' ')
                            zip = state_text[-1]
                            state = state_text[-2]
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
                    else:
                        reach = 1
                        break

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
    reach = 0
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
        address_text = td[5].text.split(',')
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if status != '' and len(address_text) > 1:
                address = address_text[0]
                city_text = address_text[-1].split(' ')
                zip = city_text[-1]
                state = city_text[-2]
                city_text.pop(-1)
                city_text.pop(-1)
                city = ' '.join(city_text)
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        if records_table:
            for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = td[1].text
                id = td[3].text
                status = td[2].text
                description = td[6].text
                address_text = td[5].text.split(',')
                if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                    if status != '' and len(address_text) > 1:
                        address = address_text[0]
                        city_text = address_text[-1].split(' ')
                        zip = city_text[-1]
                        state = city_text[-2]
                        city_text.pop(-1)
                        city_text.pop(-1)
                        city = ' '.join(city_text)
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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():

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
    reach = 0
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
            address_text = td[3].text.split(',')
            status = td[4].text
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1:
                    address = address_text[0]
                    city = address_text[1]
                    state_text = address_text[-1].split(' ')
                    zip = state_text[-1]
                    state = state_text[-2]
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

            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            for row in records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
                td = row.find_elements(By.TAG_NAME, 'td')
                date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
                id = td[1].text
                description = td[2].text
                address_text = td[3].text.split(',')
                status = td[4].text
                if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                    if len(address_text) > 1:
                        address = address_text[0]
                        city = address_text[1]
                        state_text = address_text[-1].split(' ')
                        zip = state_text[-1]
                        state = state_text[-2]
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
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status,
                                                  description=description,
                                                  address=address, city=city, state=state, zip=zip)

                else:
                    reach = 1
                    break

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
    reach = 0
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
        address_text = var_checker(td[5]).split(',')
        if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
            if len(address_text) >= 1:
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
        else:
            reach = 1
            break

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[1].text, '%m/%d/%Y').date()
            id = var_checker(td[2])
            status = var_checker(td[6])
            description = var_checker(td[8])
            name = var_checker(td[4])
            address_text = var_checker(td[5]).split(',')
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) >= 1:
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
            else:
                reach = 1
                break
    main(url.description, values)
    return True


def url_37(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
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
        address_text = var_checker(td[4]).split(',')
        if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            if len(address_text) > 1:
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

    while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
        driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(10)
        records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[5])
            address_text = var_checker(td[4]).split(',')
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if len(address_text) > 1:
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
    reach = 0

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
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            description = var_checker(td[4])
            status = var_checker(td[9])
            name = var_checker(td[5])
            address_text = var_checker(td[6]).split(',')
            if not UrlResults.objects.filter(record_id=id, date=date).first():
                if len(address_text) > 1:
                    address = address_text[0].replace('City of San Antonio', '')
                    city = 'San Antonio'
                    zip = address_text[-1].split(' ')[-1]
                    state = 'TX'
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
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if records_table:
                records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
                for i in range(0, len(records_tr) - 1):
                    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
                    records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
                    td = records_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    description = var_checker(td[4])
                    status = var_checker(td[9])
                    name = var_checker(td[5])
                    address_text = var_checker(td[6]).split(',')
                    if not UrlResults.objects.filter(record_id=id, date=date).first():
                        if len(address_text) > 1:
                            address = address_text[0].replace('City of San Antonio', '')
                            city = 'San Antonio'
                            zip = address_text[-1].split(' ')[-1]
                            state = 'TX'
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
                    else:
                        reach = 1
                        break
                        
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
    time.sleep(15)
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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():

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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():
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
    for i in range(0, 99):
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
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
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
                                                  city=city, description=description,
                                                  state=state, zip=zip, name=name)
            i += 1
            element_start_count += 1

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


def url_58(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'FL'
                        city = 'Deltona'
                        address_text.remove("DELTONA")
                        address_text.remove("FL")
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city,
                                                  state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_59(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'TX'
                        city = 'SUGAR LAND'
                        address_text.remove("TX")
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city,
                                                  state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_60(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_ddlModule'))
    select.select_by_value('Permits')

    time.sleep(10)
    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
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
                    state = 'VA'
                    city = 'Virgina Beach'
                    zip = city_text[-2]
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


def url_61(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Kern Residential/Energy/Solar')
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
            if td[2].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():
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
                    state = city_text[-2]
                    city = None
                    zip = city_text[-1][0:5]
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
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return True


def url_62(date_start, date_end, url):
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
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id, date=date).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))

                owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[ '
                                                       '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                       '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                       '2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td[ '
                                                         '2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[ '
                                                           '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                           '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[3]/td')

                description = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                             '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr['
                                                             '2]/td[1]/div/span/table/tbody/tr/td[2]')
                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    description = var_checker(description[0]) if description else ''
                    city_text = var_checker(city_text[0]).split(' ')
                    state = city_text[-2]
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
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return True


def url_63(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'FL'
                        address_text.pop(-1)
                        address_text.remove("FL")
                        city = ' '.join(address_text[3:])
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city,
                                                  state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_64(date_start, date_end, url):
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

                description = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                             '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr['
                                                             '2]/td[1]/div/span/table/tbody/tr/td[2]')

                if owner and address and city_text:
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    description = var_checker(description[0]) if description else ''
                    city_text = var_checker(city_text[0]).split(' ')
                    state = city_text[-2]
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
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return True


def url_65(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/PV System/Residential/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(10)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            id = var_checker(td[1])
            status = var_checker(td[6])
            description = var_checker(td[5])
            if td[1].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
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
                    state = 'CO'
                    city = None
                    zip = city_text[-1] if len(city_text[-1]) >= 5 else city_text[-2]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        '',
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
                    UrlResults.objects.create(url=url, record_id=id, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip,
                                              description=description)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))
        main(url.description, values)
    return


def url_66(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    search = driver.find_element(By.ID, 'searchValue')
    search.send_keys('solar')

    driver.find_element(By.ID, 'bsearch').click()
    time.sleep(10)
    records_table = driver.find_element(By.CLASS_NAME, 'cv-searchresults')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.CLASS_NAME, 'cv-searchresults')
            records_tr = records_table.find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
            if records_tr[i].find_elements(By.TAG_NAME, 'a'):
                href = records_tr[i].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                soup = beautifulsoup(href)
                application_date = datetime.strptime(
                    var_checker(soup.find(id='blkdateApplication').find('div', class_='inputText')), '%m/%d/%Y').date()
                id = var_checker(soup.find(id='blkapplicationNumber').find('div', class_='inputText'))
                if date_start <= application_date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                                date=application_date).first():
                    status = var_checker(soup.find(id='blkapplicationStatus').find('div', class_='inputText'))
                    description = var_checker(soup.find(id='blkdescription').find('div', class_='inputText'))
                    owner = var_checker(soup.find(id='blkownerName').find('div', class_='inputText'))
                    location = soup.find(id='locations').find_all('a')
                    address_text = var_checker(location[-1]).split(',')
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
                    temp_values = [
                        url.description,
                        '',
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
                    UrlResults.objects.create(url=url, record_id=id, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip,
                                              description=description)
        main(url.description, values)
    return True


def url_67(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)

    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'maindatatable')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(1, len(records_tr)):
            records_table = driver.find_element(By.ID, 'maindatatable')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            date = datetime.strptime(var_checker(records_tr[i].find_element(By.XPATH,
                                                                            f'/html/body/div[1]/main/div[2]/div/div/div[1]/table/tbody/tr[{i}]/td[1]')),
                                     '%m/%d/%Y').date()
            id = var_checker(records_tr[i].find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/div/div['
                                                                  f'1]/table/tbody/tr[{i}]/th/a'))
            status = var_checker(records_tr[i].find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/div/div['
                                                                      f'1]/table/tbody/tr[{i}]/td[3]'))
            address = var_checker(records_tr[i].find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/div/div['
                                                                       f'1]/table/tbody/tr[{i}]/td[2]'))
            description = var_checker(records_tr[i].find_element(By.XPATH, f'/html/body/div[1]/main/div['
                                                                           f'2]/div/div/div[1]/table/tbody/tr[{i}]/td[4]'))

            if date_start <= date <= date_end and id and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                       url_id=url.id).first():
                records_tr[i].find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/div/div['
                                                     f'1]/table/tbody/tr[{i}]/th/a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/div/h2')))

                applicant = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div['
                                                           '1]/div/div/div/div[4]/div[2]')
                if applicant:
                    applicant = var_checker(applicant[0])
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        '',
                        description,
                        address,
                        '',
                        '',
                        '',
                        applicant,
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, status=status, address=address,
                                              description=description, date=date, applicant=applicant)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'maindatatable')))
        main(url.description, values)
    return


def url_68(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    description = var_checker(row.find_element(By.XPATH,
                                                               f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[12]/tyler-highlight/span'))
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'FL'
                        city = 'KISSIMMEE'
                        address_text.remove("KISSIMMEE")
                        address_text.remove("FL")
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                                                  city=city, description=description,
                                                  state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_69(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'cphBody_gvSearch')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        for i in range(1, len(records_tr)):
            records_table = driver.find_element(By.ID, 'cphBody_gvSearch')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[3])[0:10].split('/')
            if len(date[0]) == 1:
                new_day = f"{0}{date[0]}"
                date[0] = new_day
            if len(date[1]) == 1:
                new_day = f"{0}{date[1]}"
                date[1] = new_day
            date = datetime.strptime('/'.join(date)[0:10], '%m/%d/%Y').date()
            id = var_checker(td[0])
            contractor = var_checker(td[4])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                href = f"http://webapp.sjcfl.us/Applications/WATSWebX/Permit/BLPermit.aspx?PermitNo={id}&PopUp=1"
                soup = beautifulsoup(href)
                address = soup.find(id='cphBody_txtPrjAddr')['value']
                state = 'FL'
                city = soup.find(id='cphBody_txtPrjCity')['value']
                zip = soup.find(id='cphBody_txtPrjZip')['value'][0:5]
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    '',
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
                    contractor
                ]
                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                          state=state, zip=zip, contractor=contractor)

        main(url.description, values)
    return


def url_70(date_start, date_end, url):
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
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[ '
                                                         '3]/div[5]/div[1]/div[3]/div['
                                                         '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td['
                                                         '2]/span[1]')
                if address:
                    address = var_checker(address[0])
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(date=date, url=url, record_id=id, status=status, address=address,
                                              name=name)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return


def url_71(date_start, date_end, url):
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
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[4])
            if date_start <= date <= date_end and td[1].find_elements(By.TAG_NAME,
                                                                      'a') and not UrlResults.objects.filter(
                record_id=id).first():
                wait = WebDriverWait(driver, 10)
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                address = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div[1]/div[3]/div['
                                                         '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')
                description = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                             '3]/div[5]/div[2]/div[3]/div[1]/div['
                                                             '1]/table/tbody/tr/td[2]/div/span/table/tbody/tr/td[2]')
                contractor = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                            '3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td['
                                                            '1]/div/span/table/tbody/tr/td[2]')
                if address and description and contractor:
                    address = var_checker(address[0])
                    description = var_checker(description[0])
                    contractor_list = var_checker(contractor[0]).split('\n')[0].split(' ')
                    contractor_list.pop(-1)
                    contractor = ' '.join(contractor_list)
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        '',
                        description,
                        address,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ' '.join(contractor_list)
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(date=date, url=url, record_id=id, status=status, address=address,
                                              description=description, contractor=contractor)
            driver.get(url.url)
            wait.until(
                EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return


def url_72(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    driver.find_element(By.ID, 'Search').click()

    results = driver.find_elements(By.CLASS_NAME, 'search-result-item')
    values = []
    if results:
        for i in range(0, len(results) - 1):
            driver.find_element(By.ID, 'Search').click()
            result = driver.find_elements(By.CLASS_NAME, 'search-result-item')[i]

            if result.find_element(By.TAG_NAME, 'a'):
                result.find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section['
                                                              '2]/div/div/div/div/div/div/div/div[2]/div/form/div['
                                                              '1]/table[1]/tbody/tr[4]/td[2]/span')))

                date = driver.find_elements(By.XPATH, '/html/body/div[1]/section[2]/div/div/div/div/div/div/div/div['
                                                      '2]/div/form/section[1]/div[2]/div/table[2]/tbody/tr[2]/td[2]')

                id = var_checker(driver.find_element(By.XPATH, '/html/body/div[1]/section['
                                                               '2]/div/div/div/div/div/div/div/div[2]/div/form/div['
                                                               '1]/table[1]/tbody/tr[4]/td[2]/span'))
                if date:
                    date = var_checker(date[0]).split('/')
                    if len(date[0]) == 1:
                        new_day = f"{0}{date[0]}"
                        date[0] = new_day
                    if len(date[1]) == 1:
                        new_day = f"{0}{date[1]}"
                        date[1] = new_day

                date = datetime.strptime('/'.join(date)[0:10], '%m/%d/%Y').date()
                if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                    url_id=url.id).first():
                    status = var_checker(driver.find_element(By.XPATH, '/html/body/div[1]/section['
                                                                       '2]/div/div/div/div/div/div/div/div['
                                                                       '2]/div/form/div[1]/table[1]/tbody/tr[4]/td['
                                                                       '2]/div'))
                    address = var_checker(driver.find_element(By.XPATH, '/html/body/div[1]/section['
                                                                        '2]/div/div/div/div/div/div/div/div['
                                                                        '2]/div/form/section[1]/div[2]/div/table['
                                                                        '1]/tbody/tr[2]/td[1]/span'))
                    address_text = var_checker(driver.find_element(By.XPATH,
                                                                   '/html/body/div[1]/section['
                                                                   '2]/div/div/div/div/div/div/div/div['
                                                                   '2]/div/form/section[1]/div[2]/div/table['
                                                                   '1]/tbody/tr[3]/td[1]/span')).split(
                        ',')
                    city = address_text[0]
                    state = address_text[1].split(' ')[1]
                    zip = address_text[1].split(' ')[-1]

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
                        ''
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(date=date, url=url, record_id=id, status=status, address=address,
                                              city=city, zip=zip, state=state)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located((By.ID, 'Search')))
        main(url.description, values)
    return


def url_73(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'CA'
                        city = None
                        address_text.remove("CA")
                        address_text.pop(-1)
                        city = ''.join(address_text[-1])
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city, state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_74(date_start, date_end, url):
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
    for i in range(0, 99):
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
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        state = 'CA'
                        city = None
                        address_text.remove("CA")
                        address_text.pop(-1)
                        city = ''.join(address_text[-1])
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city, state=state, zip=zip)
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_75(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    search = driver.find_element(By.ID, 'dup_AllContractorsName_1012604_S0')
    search.send_keys('solar')

    driver.find_element(By.ID, 'ctl00_cphBottomFunctionBand_ctl03_PerformSearch').click()
    time.sleep(5)

    pane = driver.find_element(By.ID, 'ctl00_cphPaneBand_pnlPaneBand')
    if pane:
        tbody = pane.find_elements(By.TAG_NAME, 'tbody')
        tbody.pop(-1)
        if tbody:
            for i in tbody:
                tr = i.find_element(By.TAG_NAME, 'tr')
                if tr:
                    td = tr.find_elements(By.TAG_NAME, 'td')
                    id = var_checker(td[2])
                    status = var_checker(td[4])
                    location = var_checker(td[3]).split(',')
                    address = location[0]
                    state = location[-1].split(' ')[1]
                    zip = location[-1].split(' ')[-1]
                    city = location[1]

                    date = datetime.strptime(td[5].text, '%b %d, %Y').date()
                    if date_start <= date <= date_end:
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
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, status=status, address=address,
                                                  city=city, state=state, zip=zip)

            main(url.description, values)
    return True


def url_76(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)

    search = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber"]')
    search.send_keys('BON')

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
        date = var_checker(td[5])
        id = var_checker(td[1])
        status = var_checker(td[4])
        description = var_checker(td[3])
        address_text = var_checker(td[2])
        if len(address_text) > 1 and not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
            address_text = address_text.split(',')
            state = 'CA'
            address = ' '.join(address_text[0])
            city_text = address_text[1].split(' ')
            zip = city_text[-1]
            city_text.pop(-1)
            city_text.remove('CA')
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
                                      city=city, description=description, state=state, zip=zip)
    main(url.description, values)
    return True


def url_77(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    values = []
    for row in records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]:
        td = row.find_elements(By.TAG_NAME, 'td')
        date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
        id = var_checker(td[1])
        status = var_checker(td[5])
        name = var_checker(td[3])
        address_text = var_checker(td[4])
        if date_start <= date <= date_end and len(address_text) > 1 and not UrlResults.objects.filter(record_id=id,
                                                                                                      date=date).first():
            address_text = var_checker(td[4]).split(',')
            address = address_text[0]
            city = address_text[1]
            state_text = address_text[-1].split(' ')
            state = state_text[1]
            zip = state_text[2]

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


def url_78(date_start, date_end, url):
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
    for i in range(0, 99):
        row = driver.find_element(By.ID, f'entityRecordDiv{i}')
        date = row.find_elements(By.XPATH,
                                 f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[5]/span')
        if date:
            date = datetime.strptime(date[0].text, '%m/%d/%Y').date()

            if date_start <= date <= date_end:
                id = row.find_element(By.XPATH,
                                      f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[2]/a/tyler-highlight/span').text
                address_text = row.find_element(By.XPATH,
                                                f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[11]/tyler-highlight/span').text.split(
                    ' ')
                if len(address_text) > 1:
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1]
                    description = row.find_element(By.XPATH,
                                                   f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[12]/tyler-highlight/span')
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        description = var_checker(description) if description else ''
                        zip = address_text[-1]
                        state = 'CA'
                        city = 'HAYWARD'
                        address_text.remove("CA")
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_79(date_start, date_end, url):
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
    for i in range(0, 99):
        row = driver.find_element(By.ID, f'entityRecordDiv{i}')
        date = row.find_elements(By.XPATH,
                                 f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[5]/span')
        if date:
            date = datetime.strptime(date[0].text, '%m/%d/%Y').date()

            if date_start <= date <= date_end:
                id = row.find_element(By.XPATH,
                                      f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[2]/a/tyler-highlight/span').text
                address_text = row.find_element(By.XPATH,
                                                f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[11]/tyler-highlight/span').text.split(
                    ' ')
                if len(address_text) > 1:
                    status = row.find_element(By.XPATH,
                                              f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div['
                                              f'2]/div[{element_start_count}]/div[2]/div[8]/tyler-highlight/span').text
                    zip = address_text[-1].split('-')[0]
                    description = row.find_element(By.XPATH,
                                                   f'/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[5]/div[2]/div[{element_start_count}]/div[2]/div[12]/tyler-highlight/span')
                    if zip.isnumeric() and not UrlResults.objects.filter(record_id=id, date=date,
                                                                         url_id=url.id).first():
                        description = var_checker(description) if description else ''
                        state = 'FL'
                        city = 'Miami Beach'
                        address_text.remove("FL")
                        address_text.pop(-1)
                        address = ' '.join(address_text)
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
            i += 1
            element_start_count += 1

    main(url.description, values)
    return True


def url_80(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()

    wait = WebDriverWait(driver, 10)

    records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if records_table:
        values = []
        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(td[0].text, '%m/%d/%Y').date()
            id = var_checker(td[2])
            name = var_checker(td[3])
            status = var_checker(td[4])
            if td[2].find_elements(By.TAG_NAME,
                                   'a') and date_start <= date <= date_end and not UrlResults.objects.filter(
                record_id=id,
                date=date).first():
                td[2].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                description = driver.find_elements(By.XPATH,
                                                   '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[1]/div/span/table/tbody/tr/td[2]')
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH,
                                                 '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr/td[2]/table/tbody/tr[3]/td')
                contractor = driver.find_elements(By.XPATH,
                                                  '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[2]/div/span/table/tbody/tr/td[2]')

                if description and owner and address and city_text and contractor:
                    description = var_checker(description[0])
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    contractor = var_checker(contractor[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    state = city_text[1]
                    zip = city_text[-1][0:5]
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
                        contractor
                    ]

                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, status=status, owner=owner,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description, contractor=contractor)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')))
        main(url.description, values)
    return True


def url_81(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []
    wait = WebDriverWait(driver, 10)

    project_name = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_txtGSProjectName')
    project_name.send_keys('solar')

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(10)
    records_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if records_table:
        records_tr = records_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[3:-2]
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[
                         3:-2]
            td = records_tr[i].find_elements(By.TAG_NAME, 'td')
            id = var_checker(td[1])
            name = var_checker(td[3])
            if td[1].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id).first():
                td[1].find_element(By.TAG_NAME, 'a').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                description = driver.find_elements(By.XPATH,
                                                   '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[2]/div/span/table/tbody/tr/td[2]')
                owner = driver.find_elements(By.XPATH,
                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
                address = driver.find_elements(By.XPATH,
                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')
                city_text = driver.find_elements(By.XPATH,
                                                 '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[3]/td')
                status = var_checker(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblRecordStatus"]'))
                if description and owner and address and city_text:
                    description = var_checker(description[0])
                    owner = var_checker(owner[0])
                    address = var_checker(address[0])
                    city_text = var_checker(city_text[0]).split(' ')
                    city_text.pop(-1)
                    state = city_text[-2]
                    zip = city_text[-1]
                    city_text.pop(-1)
                    city_text.pop(-1)
                    city = ' '.join(city_text)
                    temp_values = [
                        url.description,
                        '',
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
                    UrlResults.objects.create(url=url, record_id=id, owner=owner, status=status,
                                              address=address, city=city, state=state, zip=zip, name=name,
                                              description=description)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located((By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')))

    else:
        description = driver.find_elements(By.XPATH,
                                           '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[2]/div/span/table/tbody/tr/td[2]')
        owner = driver.find_elements(By.XPATH,
                                     '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[1]/td')
        address = driver.find_elements(By.XPATH,
                                       '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[2]/td')
        city_text = driver.find_elements(By.XPATH,
                                         '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td/div/span/table/tbody/tr/td[2]/table/tbody/tr[3]/td')
        status = var_checker(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblRecordStatus"]'))
        id = var_checker(driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]'))

        if description and owner and address and city_text:
            print()
            description = var_checker(description[0])
            owner = var_checker(owner[0])
            address = var_checker(address[0])
            city_text = var_checker(city_text[0]).split(' ')
            city_text.pop(-1)
            state = city_text[-2]
            zip = city_text[-1]
            city_text.pop(-1)
            city_text.pop(-1)
            city = ' '.join(city_text)
            temp_values = [
                url.description,
                '',
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
            UrlResults.objects.create(url=url, record_id=id, owner=owner, status=status,
                                      address=address, city=city, state=state, zip=zip,
                                      description=description)
    main(url.description, values)
    return True


def url_82(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []

    select = Select(driver.find_element(By.ID, 'listPermitType'))
    select.select_by_value('SLVR')

    start_date = driver.find_element(By.ID, 'txtStartDate')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.ID, 'txtEndDate')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'btnSearch').click()

    time.sleep(10)

    records_table = driver.find_element(By.CLASS_NAME, 'permits-listing')
    if records_table:

        records_tr = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[1:]

        element_count = 2
        for i in range(0, len(records_tr) - 1):
            records_table = driver.find_element(By.CLASS_NAME, 'permits-listing')
            row = records_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[1:]
            date = var_checker(row[i].find_element(By.XPATH, f'//*[@id="lvPermits_ctrl{i}_lblIssued"]'))
            id = var_checker(row[i].find_element(By.XPATH,
                                                 f'/html/body/div[5]/div[1]/form/div[5]/table/tbody/tr[{element_count}]/td[1]/a'))
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                href = row[i].find_element(By.XPATH,
                                           f'/html/body/div[5]/div[1]/form/div[5]/table/tbody/tr[{element_count}]/td[2]/div/a').get_attribute(
                    'href')
                soup = beautifulsoup(href)
                details = soup.find_all('td', class_='property_item')

                owner = details[0].text
                address_text = details[7].text.split(',')
                description = details[10].text

                state = 'FL'
                zip = address_text[-1]
                address_text = details[7].text.split(',')[0].split(' ')
                address_text.pop(-1)
                city = address_text[-1]
                address_text.pop(-1)
                address = ' '.join(address_text)
                i += 1
                element_count += 1

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
                    owner,
                    '',
                    '',
                    '',
                    '',
                    ''
                ]

                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, owner=owner, address=address, city=city,
                                          state=state, zip=zip, description=description)

    main(url.description, values)
    return True


def url_83(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    values = []

    id = 'S22004723'
    for i in range(0, 100):
        result = UrlResults.objects.filter(url_id=83).last()

        print(result)
        if not result:
            search = driver.find_element(By.ID,
                                         'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_permitnumber_BP_ReferenceFile')
            search.send_keys(id)

            driver.find_element(By.ID,
                                'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_SearchBtnWProgress_btnSearch').click()
            time.sleep(5)

            result_table = driver.find_element(By.ID, 'detail_list_resp_3')
            result_tr = result_table.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr')
            if result_tr.text == "No data available in table":
                break
            else:
                td = result_tr.find_elements(By.TAG_NAME, 'td')
                print(td)
                date = var_checker(td[2])
                status = var_checker(td[6])
                if td[0].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id,
                                                                                           date=date).first():
                    td[0].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.ID, 'permitDetails2')))

                    description = driver.find_elements(By.XPATH,
                                                       '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                       '6]/table/tbody/tr[8]/td') if driver.find_elements(By.XPATH,
                                                                                                          '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[5]/table/tbody/tr[8]/td')
                    owner = driver.find_elements(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_FolderDetail_tdData3"]')
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                        '6]/table/tbody/tr[6]/td[1]') if driver.find_elements(By.XPATH,
                                                                                                              '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[7]/table/tbody/tr/td[1]')
                    contractor = driver.find_elements(By.XPATH,
                                                      '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                      '12]/table/tbody/tr[2]/td[2]') if driver.find_elements(By.XPATH,
                                                                                                             '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[11]/table/tbody/tr[2]/td[2]')

                if description and owner and address_text:
                    description = var_checker(description[0]) if description else ''
                    owner = var_checker(owner[0]) if owner else ''
                    contractor = var_checker(contractor[0]) if contractor else ''
                    address_text = var_checker(address_text[0]).split(' ') if address_text else ''
                    if address_text[-1] == '' and len(address_text) > 1:
                        address_text.pop(-1)
                    zip = address_text[-1] if len(address_text) > 1 else ''
                    state = 'FL'
                    address_text.remove('FL') if len(address_text) > 1 else ''
                    address_text.pop(-1) if len(address_text) > 1 else ''
                    city = address_text[-1] if len(address_text) > 1 else ''
                    address_text.pop(-1) if len(address_text) > 1 else ''
                    address = ' '.join(address_text)
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
                        contractor
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, owner=owner, address=address,
                                              city=city, contractor=contractor, status=status,
                                              state=state, zip=zip, description=description)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located(
                        (By.ID, 'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_permitnumber_BP_ReferenceFile')))
        else:
            last_id = int(''.join(str(result.record_id)[1:]))
            id = f"S{last_id + 1}"
            print(id)
            search = driver.find_element(By.ID,
                                         'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_permitnumber_BP_ReferenceFile')
            search.send_keys(id)

            driver.find_element(By.ID,
                                'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_SearchBtnWProgress_btnSearch').click()
            time.sleep(10)

            result_table = driver.find_element(By.ID, 'detail_list_resp_3')
            result_tr = result_table.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr')
            print(result_tr.text)
            if result_tr.text == "No data available in table":
                UrlResults.objects.create(url=url, record_id=id)
                driver.get(url.url)
                wait.until(
                    EC.presence_of_element_located(
                        (By.ID, 'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_permitnumber_BP_ReferenceFile')))
            else:
                td = result_tr.find_elements(By.TAG_NAME, 'td')
                date = var_checker(td[2])
                status = var_checker(td[6])

                if td[0].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id,
                                                                                           date=date).first():
                    td[0].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.ID, 'permitDetails2')))

                    description = driver.find_elements(By.XPATH,
                                                       '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                       '6]/table/tbody/tr[8]/td') if driver.find_elements(By.XPATH,
                                                                                                          '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[5]/table/tbody/tr[8]/td')
                    owner = driver.find_elements(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_FolderDetail_tdData3"]')
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                        '6]/table/tbody/tr[6]/td[1]') if driver.find_elements(By.XPATH,
                                                                                                              '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[7]/table/tbody/tr/td[1]')
                    contractor = driver.find_elements(By.XPATH,
                                                      '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div['
                                                      '12]/table/tbody/tr[2]/td[2]') if driver.find_elements(By.XPATH,
                                                                                                             '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[4]/div[2]') else driver.find_elements(
                        By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[4]/div/form/div[11]/table/tbody/tr[2]/td[2]')

                    print(description)
                    print(owner)
                    print(address_text)
                    print(contractor)
                    if description and owner and address_text:
                        description = var_checker(description[0]) if description else ''
                        owner = var_checker(owner[0]) if owner else ''
                        contractor = var_checker(contractor[0]) if contractor else ''
                        address_text = var_checker(address_text[0]).split(' ') if address_text else ''
                        if address_text[-1] == '' and len(address_text) > 1:
                            address_text.pop(-1)
                        zip = address_text[-1] if len(address_text) > 1 else ''
                        state = 'FL'
                        address_text.remove('FL') if len(address_text) > 1 else ''
                        address_text.pop(-1) if len(address_text) > 1 else ''
                        city = address_text[-1] if len(address_text) > 1 else ''
                        address_text.pop(-1) if len(address_text) > 1 else ''
                        address = ' '.join(address_text)

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
                            contractor
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, owner=owner, address=address,
                                                  city=city, contractor=contractor, status=status,
                                                  state=state, zip=zip, description=description)
                    driver.get(url.url)
                    wait.until(
                        EC.presence_of_element_located(
                            (By.ID, 'ContentPlaceHolder1_ucHeaderAndSearchBP_uc_permitnumber_BP_ReferenceFile')))

    main(url.description, values)
    return True


def url_84(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []

    search = driver.find_element(By.ID, 'InfoReq1_txtSrchKeyword')
    search.clear()
    search.send_keys('solar')
    date_start_inp = driver.find_element(By.ID, 'InfoReq1_txtDateFrom')
    date_start_inp.clear()
    date_start_inp.send_keys(date_start)
    date_end_inp = driver.find_element(By.ID, 'InfoReq1_txtDateTo')
    date_end_inp.clear()
    date_end_inp.send_keys(date_end)
    driver.find_element(By.ID, 'InfoReq1_btnSearchEID').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'InfoReq1_dgKeywordPermits')
    if result_table:
        result_tr = result_table[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[1:-2]

        for i in range(0, len(result_tr) - 1):
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            id = var_checker(td[0])
            address = var_checker(td[1])
            description = var_checker(td[2])
            date = var_checker(td[3])

            if td[0].find_elements(By.TAG_NAME, 'a') and not UrlResults.objects.filter(record_id=id,
                                                                                       date=date).first():
                href = td[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                soup = beautifulsoup(href)

                contractor = var_checker(soup.find(id='InfoReq1_lblCompanyName'))
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    '',
                    '',
                    description,
                    address,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    contractor
                ]
                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                          contractor=contractor, description=description)

    main(url.description, values)
    return True


def url_85(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []

    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/a').click()
    time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div[1]/div/a[1]').click()
    time.sleep(3)

    first_search = Select(driver.find_element(By.ID, 'find3SearchCriteria_0__find3Definition_StoredProcedureName'))
    first_search.select_by_value('dbo.iMSFind3PermitsRecordType')
    time.sleep(2)
    first_search_contain = driver.find_element(By.XPATH, '//*[@id="find3SearchCriteria_0_SearchText"]')
    first_search_contain.send_keys('solar')
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="create"]').click()
    time.sleep(3)

    first_search = Select(
        driver.find_element(By.ID, 'find3SearchCriteria_1__find3Definition_StoredProcedureName'))
    first_search.select_by_value('dbo.iMSFind3PermitsPermitNumber')
    time.sleep(2)
    first_search_contain = driver.find_element(By.XPATH, '//*[@id="find3SearchCriteria_1_SearchText"]')
    first_search_contain.send_keys('BL22-17')
    time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/div[3]/form/div[2]/div/button').click()
    time.sleep(5)

    results = driver.find_elements(By.CLASS_NAME, 'recordrow')
    for row in results:
        href = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        description = var_checker(row.find_elements(By.TAG_NAME, 'strong')[3])
        if href:
            soup = beautifulsoup(href)
            row = soup.find('div', class_='row tilecontainer')
            print(row)
            col = row.find_all('div', class_='col-md-4 tile')
            for i in col:
                print(i.text)
    main(url.description, values)
    return True


def url_86(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    values = []
    first_data = []
    second_data = []
    data = []

    search = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    search.select_by_value('Development/Electrical/Standalone/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH,
                                     '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '12/28/2022'", start_date)
    time.sleep(3)
    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '12/30/2022'", end_date)
    time.sleep(3)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            temp_data = {
                'date': var_checker(td[2]),
                'id': var_checker(td[3]),
                'status': var_checker(td[4]),
                'name': var_checker(td[6]),
                'address': var_checker(td[7])
            }
            first_data.append(temp_data)
        while driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1] and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(3)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2]
            for row in result_tr:
                td = row.find_elements(By.TAG_NAME, 'td')
                temp_data = {
                    'date': var_checker(td[2]),
                    'id': var_checker(td[3]),
                    'status': var_checker(td[4]),
                    'name': var_checker(td[6]),
                    'address': var_checker(td[7])
                }
                first_data.append(temp_data)

    time.sleep(5)
    search = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    search.select_by_value('Development/Electrical/Standalone/NA')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH,
                                     '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '12/28/2022'", start_date)
    time.sleep(3)
    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '12/30/2022'", end_date)
    time.sleep(3)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            temp_data = {
                'date': var_checker(td[2]),
                'id': var_checker(td[3]),
                'status': var_checker(td[4]),
                'name': var_checker(td[6]),
                'address': var_checker(td[7])
            }
            second_data.append(temp_data)
        while driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1] and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(3)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2]
            for row in result_tr:
                td = row.find_elements(By.TAG_NAME, 'td')
                temp_data = {
                    'date': var_checker(td[2]),
                    'id': var_checker(td[3]),
                    'status': var_checker(td[4]),
                    'name': var_checker(td[6]),
                    'address': var_checker(td[7])
                }
                second_data.append(temp_data)

    for i in first_data:
        address = i['address']
        for ii in second_data:
            if address == ii['address']:
                temp_data = {
                    'date': i['date'],
                    'id': i['id'],
                    'status': i['status'],
                    'name': i['name'],
                    'address': i['address']
                }
                data.append(temp_data)

    for row in data:
        if not UrlResults.objects.filter(record_id=row['id'], date=row['date']).first():
            address_text = row['address'].split(',')
            address = address_text[0]
            city_text = address_text[-1].split(' ')
            zip = city_text[-1]
            city_text.pop(-1)
            state = city_text[-1]
            city_text.pop(-1)
            city = ' '.join(city_text)
            temp_values = [
                url.description,
                str(row['date']),
                id,
                '',
                row['name'],
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
            UrlResults.objects.create(url=url, record_id=row['id'], date=row['date'], address=address, city=city,
                                      state=state,
                                      zip=zip, name=row['name'], status=row['status'])
    main(url.description, values)
    return True


def url_87(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            name = var_checker(td[3])
            status = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) > 1:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]

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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, name=name, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    name = var_checker(td[3])
                    status = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) > 1:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]

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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, name=name, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_88(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[4])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[3]).split(',')
                if len(address_text) > 1:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]

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
                        ''
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[4])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[3]).split(',')
                        if len(address_text) > 1:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]

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
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_89(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) > 1:
                    address = address_text[0]
                    city = address_text[1]
                    state = 'CA'
                    zip = address_text[2]

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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) > 1:
                            address = address_text[0]
                            city = address_text[1]
                            state = 'CA'
                            zip = address_text[2]

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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_90(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            name = var_checker(td[3])
            status = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) > 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]

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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, name=name, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    name = var_checker(td[3])
                    status = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) > 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]

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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, name=name, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_91(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            name = var_checker(td[3])
            status = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) > 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]

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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, name=name, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    name = var_checker(td[3])
                    status = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) > 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]

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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, name=name, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_92(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            name = var_checker(td[3])
            status = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id,
                                                                                date=date).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) > 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2][0:5]

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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, name=name, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    name = var_checker(td[3])
                    status = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id,
                            date=date).first():

                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) > 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2][0:5]

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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, name=name, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_93(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    values = []

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/Residential/NA')
    time.sleep(3)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(3)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()

    time.sleep(5)
    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[4])
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                address_text = var_checker(td[3]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city_text = address_text[1].split(' ')
                    state = 'IL'
                    city_text.remove('IL')
                    zip = city_text[-1]
                    city_text.pop(-1)
                    city = ' '.join(city_text)
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
                        ''
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    status = var_checker(td[4])
                    if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                        address_text = var_checker(td[3]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[1].split(' ')
                            state = 'IL'
                            city_text.remove('IL')
                            zip = city_text[-1]
                            city_text.pop(-1)
                            city = ' '.join(city_text)
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
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_94(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[2])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_95(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[8])
            name = var_checker(td[6])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[7]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[8])
                    name = var_checker(td[6])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[7]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_96(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    values = []

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Solar/NA/NA')
    time.sleep(3)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(3)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()

    time.sleep(5)
    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[4])
            description = var_checker(td[8])
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                address = var_checker(td[5])
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    name,
                    description,
                    address,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]
                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                          description=description, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    status = var_checker(td[6])
                    name = var_checker(td[4])
                    description = var_checker(td[8])
                    if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                        address = var_checker(td[5])
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            name,
                            description,
                            address,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                  description=description, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_97(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[5]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
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
                        ''
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[6])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[5]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[-1]
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
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_98(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = 'CA'
                    state_text = address_text[-1].split(' ')
                    if 'CA' in state_text:
                        state_text.remove('CA')
                    zip = state_text[1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = 'CA'
                            state_text = address_text[-1].split(' ')
                            if 'CA' in state_text:
                                state_text.remove('CA')
                            zip = state_text[1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_99(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    values = []

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSLicenseType'))
    select.select_by_value('(CLR) Electrical Contractor, Renewable Energy, Limited')
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[0])
            id = var_checker(td[2])
            status = var_checker(td[3])
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                address = var_checker(td[6])
                temp_values = [
                    url.description,
                    str(date),
                    id,
                    status,
                    '',
                    '',
                    address,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ]
                values.append(temp_values)
                UrlResults.objects.create(url=url, record_id=id, date=date, address=address, zip=zip, status=status)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[0])
                    id = var_checker(td[2])
                    status = var_checker(td[3])
                    if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                        address = var_checker(td[6])
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            '',
                            '',
                            address,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, address=address, zip=zip,
                                                  status=status)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_100(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_101(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address = var_checker(td[4])
                if len(address) != '':
                    temp_values = [
                        url.description,
                        str(date),
                        id,
                        status,
                        name,
                        '',
                        address,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, zip=zip, status=status,
                                              name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address = var_checker(td[4])
                        if len(address) != '':
                            temp_values = [
                                url.description,
                                str(date),
                                id,
                                status,
                                name,
                                '',
                                address,
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, zip=zip,
                                                      status=status,
                                                      name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_102(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status,
                                              name=name)
            else:
                reach = 1
                break
        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status,
                                                      name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_103(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_104(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[7])
            name = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[6]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[7])
                    name = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[6]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_105(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_106(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = address_text[-1].split(' ')[1]
                    zip = address_text[-1].split(' ')[2]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = address_text[-1].split(' ')[1]
                            zip = address_text[-1].split(' ')[2]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_107(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    values = []

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Building/Residential/Photovoltaic')
    time.sleep(3)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[5])
            description = var_checker(td[4])
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                address_text = var_checker(td[6]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city_text = address_text[-1].split(' ')
                    zip = city_text[-1]
                    state = city_text[-2]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, description=description)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(10)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    status = var_checker(td[5])
                    description = var_checker(td[4])
                    if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                        address_text = var_checker(td[6]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, description=description)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_108(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a'):
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                        '3]/div[5]/div[1]/div[3]/div['
                                                        '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')

                    if address_text:
                        address_text = var_checker(address_text[0]).split('\n')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
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
                                '',
                                '',
                                '',
                                '',
                                '',
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    driver.back()
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[6])
                    name = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a'):
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            address_text = driver.find_elements(By.XPATH,
                                                                '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                                '3]/div[5]/div[1]/div[3]/div['
                                                                '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')

                            if address_text:
                                address_text = var_checker(address_text[0]).split('\n')
                                if len(address_text) >= 2:
                                    address = address_text[0]
                                    city_text = address_text[-1].split(' ')
                                    zip = city_text[-1]
                                    state = city_text[-2]
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
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        ''
                                    ]
                                    values.append(temp_values)
                                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                              city=city,
                                                              state=state,
                                                              zip=zip, status=status, name=name)
                            driver.back()
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_109(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id, date=date,
                    url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a'):
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                        '3]/div[5]/div[1]/div[3]/div['
                                                        '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr'
                                                        '/td[2]')

                    if address_text:
                        address_text = var_checker(address_text[0]).split('\n')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
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
                                '',
                                '',
                                '',
                                '',
                                '',
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    driver.back()

            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[6])
                    name = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id, date=date,
                            url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a'):
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            address_text = driver.find_elements(By.XPATH,
                                                                '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                                '3]/div[5]/div[1]/div[3]/div['
                                                                '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr'
                                                                '/td[2]')

                            if address_text:
                                address_text = var_checker(address_text[0]).split('\n')
                                if len(address_text) >= 2:
                                    address = address_text[0]
                                    city_text = address_text[-1].split(' ')
                                    zip = city_text[-1]
                                    state = city_text[-2]
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
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        ''
                                    ]
                                    values.append(temp_values)
                                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                              city=city,
                                                              state=state,
                                                              zip=zip, status=status, name=name)
                            driver.back()

                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_110(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a'):
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    address = driver.find_elements(By.XPATH,
                                                   '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[1]/div[3]/div[1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]/span[1]')

                    if address:
                        address = var_checker(address[0])
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            name,
                            '',
                            address,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, address=address, status=status,
                                                  name=name)
                    driver.back()

            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[6])
                    name = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id, date=date,
                            url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a'):
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            address = driver.find_elements(By.XPATH,
                                                           '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[1]/div[3]/div[1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]/span[1]')

                            if address:
                                address = var_checker(address[0])
                                temp_values = [
                                    url.description,
                                    str(date),
                                    id,
                                    status,
                                    name,
                                    '',
                                    address,
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                ]
                                values.append(temp_values)
                                UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                          status=status,
                                                          name=name)
                            driver.back()

                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_111(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(
                    record_id=id, date=date,
                    url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a'):
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[1]/div[3]/div[1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')

                    if address_text:
                        address_text = var_checker(address_text[0]).split('\n')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = 'CO'
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
                                '',
                                '',
                                '',
                                '',
                                '',
                                ''
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    driver.back()

            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id, date=date,
                            url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a'):
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            address_text = driver.find_elementS(By.XPATH,
                                                                '/html/body/form/div[3]/div[1]/div[7]/div[2]/div[1]/div['
                                                                '3]/div[ '
                                                                '5]/div[1]/div[3]/div['
                                                                '1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')

                            if address_text:
                                address_text = var_checker(address_text[0]).split('\n')
                                if len(address_text) >= 2:
                                    address = address_text[0]
                                    city_text = address_text[-1].split(' ')
                                    zip = city_text[-1]
                                    state = 'CO'
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
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        ''
                                    ]
                                    values.append(temp_values)
                                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                              city=city,
                                                              state=state,
                                                              zip=zip, status=status, name=name)
                            driver.back()

                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_112(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            type = var_checker(td[2])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a') and type == "Residential Alteration Permit":
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    city_text = driver.find_elements(By.XPATH,
                                                     '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                     '5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                     '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                     '2]/table/tbody/tr[3]/td')
                    address_text = driver.find_elements(By.XPATH,
                                                        '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                        '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                        '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                        '2]/table/tbody/tr[2]/td')

                    owner = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                           '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                           '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                           '2]/table/tbody/tr[1]/td')
                    contractor = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                                '1]/div[3]/div[5]/div/div[3]/div[1]/div['
                                                                '1]/table/tbody/tr[1]/td['
                                                                '2]/div/span/table/tbody/tr/td[2]')
                    description = driver.find_elements(By.XPATH, '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                                 '1]/div[3]/div[5]/div/div[3]/div[1]/div['
                                                                 '1]/table/tbody/tr[2]/td['
                                                                 '1]/div/span/table/tbody/tr/td[2]')
                    if city_text and address_text and owner and contractor and description:
                        city_text = var_checker(city_text[0]).split(' ')
                        address = var_checker(address_text[0])
                        owner = var_checker(owner[0])
                        contractor = var_checker(contractor[0])
                        description = var_checker(description[0])
                        zip = city_text[-1]
                        state = city_text[-2]
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
                            contractor
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                  state=state, owner=owner, contractor=contractor,
                                                  zip=zip, status=status, name=name)
                    driver.back()

            else:
                reach = 1
                break
        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    type = var_checker(td[2])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(
                            record_id=id, date=date, url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a') and type == "Residential Alteration Permit":
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            city_text = driver.find_elements(By.XPATH,
                                                             '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div['
                                                             '5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                             '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                             '2]/table/tbody/tr[3]/td')
                            address_text = driver.find_elements(By.XPATH,
                                                                '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                                '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                                '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                                '2]/table/tbody/tr[2]/td')

                            owner = driver.find_elements(By.XPATH,
                                                         '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div['
                                                         '3]/div[5]/div/div[3]/div[1]/div[1]/table/tbody/tr[2]/td['
                                                         '2]/div/span/table/tbody/tr/td/table/tbody/tr/td['
                                                         '2]/table/tbody/tr[1]/td')
                            contractor = driver.find_elements(By.XPATH,
                                                              '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                              '1]/div[3]/div[5]/div/div[3]/div[1]/div['
                                                              '1]/table/tbody/tr[1]/td['
                                                              '2]/div/span/table/tbody/tr/td[2]')
                            description = driver.find_elements(By.XPATH,
                                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div['
                                                               '1]/div[3]/div[5]/div/div[3]/div[1]/div['
                                                               '1]/table/tbody/tr[2]/td['
                                                               '1]/div/span/table/tbody/tr/td[2]')
                            if city_text and address_text and owner and contractor and description:
                                city_text = var_checker(city_text[0]).split(' ')
                                address = var_checker(address_text[0])
                                owner = var_checker(owner[0])
                                contractor = var_checker(contractor[0])
                                description = var_checker(description[0])
                                zip = city_text[-1]
                                state = city_text[-2]
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
                                    contractor
                                ]
                                values.append(temp_values)
                                UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                          state=state, owner=owner, contractor=contractor,
                                                          zip=zip, status=status, name=name)
                            driver.back()

                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_113(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    reach = 0
    values = []

    select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
    select.select_by_value('Building/Residential/Miscellaneous/Solar - Photovoltaic')
    time.sleep(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]')
    driver.execute_script(f"arguments[0].value = '{date_start}'", start_date)

    end_date = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]')
    driver.execute_script(f"arguments[0].value = '{date_end}'", end_date)
    time.sleep(5)

    driver.find_element(By.ID, 'ctl00_PlaceHolderMain_btnNewSearch').click()
    time.sleep(5)

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = var_checker(td[1])
            id = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[4])
            address_text = var_checker(td[5]).split(',')
            if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                if len(address_text) >= 2:
                    address = address_text[0]
                    city_text = address_text[-1].split(' ')
                    zip = city_text[-1]
                    state = city_text[-2]
                    city = ' '.join(city_text)

                    href = td[2].find_elements(By.TAG_NAME, 'a')
                    contractor = ''
                    description = ''
                    if href:
                        soup = beautifulsoup(href[0].get_attribute('href'))
                        details = soup.find_all('table', class_='table_child')
                        if details:
                            contractor = details[1].text
                            description = details[2].text
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
                        contractor
                    ]
                    values.append(temp_values)
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                              state=state, contractor=contractor, zip=zip, status=status, name=name)

            else:
                reach = 1
                break
        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME,
                    'aca_pagination_PrevNext') else \
                    result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = var_checker(td[1])
                    id = var_checker(td[2])
                    status = var_checker(td[6])
                    name = var_checker(td[4])
                    address_text = var_checker(td[5]).split(',')
                    if not UrlResults.objects.filter(record_id=id, date=date, url_id=url.id).first():
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city_text = address_text[-1].split(' ')
                            zip = city_text[-1]
                            state = city_text[-2]
                            city = ' '.join(city_text)

                            href = td[2].find_elements(By.TAG_NAME, 'a')
                            contractor = ''
                            description = ''
                            if href:
                                soup = beautifulsoup(href[0].get_attribute('href'))
                                details = soup.find_all('table', class_='table_child')
                                if len(details) >= 2:
                                    contractor = details[1].text
                                elif len(details) >= 3:
                                    contractor = details[1].text
                                    description = details[2].text
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
                                contractor
                            ]
                            values.append(temp_values)
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state, contractor=contractor, zip=zip, status=status,
                                                      name=name)

                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_114(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = 'CA'
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = 'CA'
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_115(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for row in result_tr:
            td = row.find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            status = var_checker(td[5])
            name = var_checker(td[3])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                address_text = var_checker(td[4]).split(',')
                if len(address_text) >= 2:
                    address = address_text[0]
                    city = address_text[1]
                    state = 'CA'
                    zip = address_text[-1].split(' ')[-1]
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
                    UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city, state=state,
                                              zip=zip, status=status, name=name)
            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[-1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for row in result_tr:
                    td = row.find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    status = var_checker(td[5])
                    name = var_checker(td[3])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        address_text = var_checker(td[4]).split(',')
                        if len(address_text) >= 2:
                            address = address_text[0]
                            city = address_text[1]
                            state = 'CA'
                            zip = address_text[-1].split(' ')[-1]
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
                            UrlResults.objects.create(url=url, record_id=id, date=date, address=address, city=city,
                                                      state=state,
                                                      zip=zip, status=status, name=name)
                    else:
                        reach = 1
                        break

    main(url.description, values)
    return True


def url_116(date_start, date_end, url):
    driver = chrome_driver()
    driver.get(url.url)
    wait = WebDriverWait(driver, 10)
    date_start = datetime.strptime(date_start, '%m/%d/%Y').date()
    date_end = datetime.strptime(date_end, '%m/%d/%Y').date()
    reach = 0
    values = []

    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
    if result_table:
        result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(By.CLASS_NAME,
                                                                                                   'aca_pagination_PrevNext') else \
            result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
        for i in range(0, len(result_tr) - 1):
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                               3:]
            td = result_tr[i].find_elements(By.TAG_NAME, 'td')
            date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
            id = var_checker(td[1])
            type = var_checker(td[2])
            status = var_checker(td[6])
            name = var_checker(td[5])
            if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                url_id=url.id).first():
                if td[1].find_elements(By.TAG_NAME, 'a') and type == "PV - Roof Mount":
                    td[1].find_element(By.TAG_NAME, 'a').click()
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                    address = driver.find_elements(By.XPATH,
                                                   '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[1]/div[3]/div[1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')
                    contractor = driver.find_elements(By.XPATH,
                                                      '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/div/span/table/tbody/tr/td[2]')
                    description = driver.find_elements(By.XPATH,
                                                       '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td[2]/div/span/table/tbody/tr/td[2]')
                    if address and contractor and description:
                        address = var_checker(address[0])
                        contractor = var_checker(contractor[0])
                        description = var_checker(description[0])
                        temp_values = [
                            url.description,
                            str(date),
                            id,
                            status,
                            name,
                            description,
                            address,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            contractor
                        ]
                        values.append(temp_values)
                        UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                  contractor=contractor, status=status, name=name)
                    driver.back()

            else:
                reach = 1
                break

        while reach == 0 and driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext') and \
                driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_elements(By.TAG_NAME, 'a'):
            driver.find_elements(By.CLASS_NAME, 'aca_pagination_PrevNext')[1].find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
            if result_table:
                result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                    By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[3:]
                for i in range(0, len(result_tr) - 1):
                    result_table = driver.find_elements(By.ID, 'ctl00_PlaceHolderMain_CapView_gdvPermitList')
                    result_tr = result_table[0].find_elements(By.TAG_NAME, 'tr')[3:-2] if driver.find_elements(
                        By.CLASS_NAME, 'aca_pagination_PrevNext') else result_table[0].find_elements(By.TAG_NAME, 'tr')[
                                                                       3:]
                    td = result_tr[i].find_elements(By.TAG_NAME, 'td')
                    date = datetime.strptime(var_checker(td[0]), '%m/%d/%Y').date()
                    id = var_checker(td[1])
                    type = var_checker(td[2])
                    status = var_checker(td[6])
                    name = var_checker(td[5])
                    if date_start <= date <= date_end and not UrlResults.objects.filter(record_id=id, date=date,
                                                                                        url_id=url.id).first():
                        if td[1].find_elements(By.TAG_NAME, 'a') and type == "PV - Roof Mount":
                            td[1].find_element(By.TAG_NAME, 'a').click()
                            wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="ctl00_PlaceHolderMain_lblPermitNumber"]')))
                            address = driver.find_elements(By.XPATH,
                                                           '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[1]/div[3]/div[1]/div/div/table/tbody/tr/td/div/span/table/tbody/tr/td[2]')
                            contractor = driver.find_elements(By.XPATH,
                                                              '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/div/span/table/tbody/tr/td[2]')
                            description = driver.find_elements(By.XPATH,
                                                               '/html/body/form/div[4]/div[1]/div[7]/div[2]/div[1]/div[3]/div[5]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td[2]/div/span/table/tbody/tr/td[2]')
                            if address and contractor and description:
                                address = var_checker(address[0])
                                contractor = var_checker(contractor[0])
                                description = var_checker(description[0])
                                temp_values = [
                                    url.description,
                                    str(date),
                                    id,
                                    status,
                                    name,
                                    description,
                                    address,
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    contractor
                                ]
                                values.append(temp_values)
                                UrlResults.objects.create(url=url, record_id=id, date=date, address=address,
                                                          contractor=contractor, status=status, name=name)
                            driver.back()

                    else:
                        reach = 1
                        break

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
