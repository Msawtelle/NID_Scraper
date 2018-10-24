import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import random
import pandas as pd

def main():
    url = 'http://nid.usace.army.mil/cm_apex/f?p=838:12'
    id ='P12_ORGANIZATION'
    org = 'Academia' # See Army Corps of Engineers website for other organizational options
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    filename_foramt = 'NID/NID_{}.csv'
    for state in states:
        print('searching NID for information about {}'.format(state))
        driver = webdriver.Firefox()
        filename = filename_foramt.format(state)
        driver.get(url)
        select = Select(driver.find_element_by_id(id))
        select.select_by_visible_text(org)
        time.sleep(1.5+random.random())
        driver.find_element_by_partial_link_text('Report').click()
        driver.find_element_by_id('apexir_SEARCHDROPROOT').click()
        time.sleep(1.5+random.random())
        driver.find_element_by_id('STATE').click()
        search_bar = driver.find_element_by_id('apexir_SEARCH')
        time.sleep(1.5+random.random())
        search_bar.send_keys(state)
        time.sleep(1.5+random.random())
        driver.find_element_by_class_name('apexir-go-button').click()
        time.sleep(1.5+random.random())
        driver.find_element_by_xpath('/html/body/form/div[5]/table/tbody/tr\
                                     /td[1]/table[2]/tbody/tr/td/div[1]/div[2]\
                                     /div[2]/div[2]/div[4]/table/tbody/tr[2]/td\
                                     /table/tbody/tr[2]/td[1]/a/img').click()
        time.sleep(1.5+random.random())
        row_count = driver.find_element_by_id('apexir_rowcount').text
        number_of_dams = int(row_count[9:])
        for i in range(number_of_dams):
            if i == 0:
                page_source = driver.page_source
                tables = pd.read_html(page_source)[6].T
                driver.find_element_by_id('apexir_btn_NEXT').click()
                time.sleep(0.5+random.random())
            elif i == number_of_dams-1:
                page_source = driver.page_source
                next_table = pd.read_html(page_source)[6].T
                tables = tables.append(next_table.iloc[[1]],ignore_index=True)
                tables.to_csv(filename)
                driver.quit()
                print('finished querying NID for information about {}: {} results'.format(state, number_of_dams))
                time.sleep(10+random.random())
            else:
                page_source = driver.page_source
                next_table = pd.read_html(page_source)[6].T
                tables = tables.append(next_table.iloc[[1]],ignore_index=True)
                driver.find_element_by_id('apexir_btn_NEXT').click()
                time.sleep(0.5+random.random())

if __name__ == '__main__':
    main()
