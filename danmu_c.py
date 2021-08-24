from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException, \
    ElementNotSelectableException
import time
from bs4 import BeautifulSoup
import lxml

'''
use explicit wait to initial. 
because the danmu div take some times to show up in DOM. (more 'inteligent' way)
the server speed, internet speed, cpu etc varies, so you never not when ready. 
after initialized, use implicit wait to auto load new danmu if found in DOM

https://www.browserstack.com/guide/wait-commands-in-selenium-webdriver
'''

# configuration
# selectors format
danmu_instance_selector = 'li.Barrage-listItem'
danmu_instance_nickname_selector = '.Barrage-nickName'
danmu_instance_content_selector = '.Barrage-content'
url = 'https://www.douyu.com/2222'
danmus = []
locator_from = 1
locator_to = 0

# instanciate webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.get(url)
print(driver.title)

timeout_initial = 180
print(f"Trying to locate Danmu, it may take some times ...")
danmu_elements = WebDriverWait(driver, timeout_initial).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, danmu_instance_selector)))
# print(danmu_elements.text)
print("Initialing Done. The very first danmu found.")

'''
soup version

Known issues here: whenever reach 200 results, stop updating. Why.

Why stop everytime reaches 200?
'''
while True:
    # use implicit approach to load new every xx second
    timeout_regular = 5
    print(f"Waiting for {timeout_regular}s ...")
    time.sleep(timeout_regular)
    print("Waiting Done. Loading New Danmu...")

    # danmu_container =  driver.find_element_by_css_selector('ul#js-barrage-list')
    soup = BeautifulSoup(driver.page_source, 'lxml').select('ul#js-barrage-list')[0]
    # print(soup)
    num_of_danmus = len(soup.select('li.Barrage-listItem'))
    print(f"num_of_danmus: {num_of_danmus}")

    if num_of_danmus > 0:
        locator_to = num_of_danmus + 1
        print(f"locator_to: {locator_to}")

        for i in range(locator_from, locator_to):
            # css selector has :nth-child(), but only starts from 1.
            # count starts from 1. so we set intital locator to 1

            # print(i)
            nickname = soup.select(f'li.Barrage-listItem:nth-child({i}) .Barrage-nickName')[0].text



            # content = soup.select(f'li.Barrage-listItem:nth-child({i}) .Barrage-content')[0].text
            content = content = soup.select(f'li.Barrage-listItem:nth-child({i}) .Barrage-content')[0].text if len(soup.select(f'li.Barrage-listItem:nth-child({i}) .Barrage-content')) > 0 else 'no text'




            print(f"{i}: {nickname}: {content}")
            danmus.append({'id': i, 'name': nickname, 'content': content})
            # update locator_from
            locator_from = danmus[-1]['id'] + 1

# close driver
driver.close()