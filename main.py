from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from bs4 import BeautifulSoup
import lxml

# url = 'http://pythonscraping.com/pages/javascript/redirectDemo1.html'
url = 'https://www.douyu.com/9149560'

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.get(url)


# initial wait for js fully loaded
print('start waiting 60s ...')
time.sleep(300)
print('waited')


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
# /html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li[34]
# /html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li[62]
# /html/body/section/main/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[3]/div/div/div[1]/ul/li[65]


result = driver.find_element_by_id(danmu_wrapper_id)
print(result)

soup = BeautifulSoup(driver.page_source, 'lxml').find(id=danmu_wrapper_id)
print(soup)







driver.close()