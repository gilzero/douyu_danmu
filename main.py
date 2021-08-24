from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd
from bs4 import BeautifulSoup
import lxml


def wait_to_load(second):
    print(f'start waiting {second}s ...')
    time.sleep(second)
    print('waited')


# url = 'http://pythonscraping.com/pages/javascript/redirectDemo1.html'
url = 'https://www.douyu.com/312212' #zixun

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.get(url)
print(driver.title)
print(driver.name)


# initial wait for js fully loaded
wait_to_load(30)


# selectors
danmu_wrapper_id = 'js-barrage-list'
danmu_instance_wraper_selector = 'li.Barrage-listItem'
danmu_instance_nickname_selector = '.Barrage-nickName'
danmu_instance_content_selector = '.Barrage-content'
danmu_instance_fullxpath = '/html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li'



# ul#js-barrage-list    all danmu wrapper
# li.Barrage-listItem    every individual danmu wrapper
# .Barrage-nickName  danmu user name
# .Barrage-content   danmu content

# full xpath copied from chrome. the last i incremental as more danmu showing
# /html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li[62]
# /html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li[65]

danmus = []

element_container = driver.find_element_by_id(danmu_wrapper_id)
element_danmus = driver.find_elements_by_css_selector(danmu_instance_wraper_selector)

for i in range(len(element_danmus)):

    nickname = element_danmus[i].find_element_by_css_selector(danmu_instance_nickname_selector).text
    # print(f"nickname: {nickname}")

    try:
        content = element_danmus[i].find_element_by_css_selector(danmu_instance_content_selector).text
    except NoSuchElementException as e:
        print(e)
        content = 'nothing'

    # content = element_danmus[i].find_element_by_css_selector(danmu_instance_content_selector).text if element_danmus[i].find_element_by_css_selector(danmu_instance_content_selector) is not None else ''
    print(f"{nickname}: {content}")








# soup = BeautifulSoup(driver.page_source, 'lxml').find(id=danmu_wrapper_id)
# print(soup)






driver.close()