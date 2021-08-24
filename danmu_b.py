from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
# import sys

'''
use explicit wait to initial. 
because the danmu div take some times to show up in DOM. (more 'inteligent' way)
the server speed, internet speed, cpu etc varies, so you never not when ready. 
after initialized, use implicit wait to auto load new danmu if found in DOM

https://www.browserstack.com/guide/wait-commands-in-selenium-webdriver
'''

# Configuration
# selectors format
# sys.setrecursionlimit(2000)
danmu_instance_selector = 'li.Barrage-listItem'
danmu_instance_nickname_selector = '.Barrage-nickName'
danmu_instance_content_selector = '.Barrage-content'
url = 'https://www.douyu.com/2222'
danmus = []
locator_from = 1
locator_to = 0

# Instanciate WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.get(url)
print(driver.title)

# Initial finding of danmu DOM. Because javascrip loading after html page ready in DOM. Set a max 3 mins to wait for
# danmu DOM appears.
timeout_initial = 180
print(f"Trying to locate Danmu, it may take some times ...")
danmu_elements = WebDriverWait(driver, timeout_initial).until(EC.presence_of_element_located((By.CSS_SELECTOR, danmu_instance_selector)))
print("The very first danmu found.")

'''
Known issues here: whenever reach 200 results, stop updating. Why?
Maybe the recursive limit?
https://www.pythoncentral.io/resetting-the-recursion-limit/

Try another loop method. 
'''
while True:
    # use implicit approach to load new every xx second
    timeout_regular = 5
    print(f"Waiting for {timeout_regular}s ...")
    time.sleep(timeout_regular)
    print("Waiting Done. Loading New Danmu...")

    num_of_danmus = len(driver.find_elements_by_css_selector(danmu_instance_selector))

    if num_of_danmus > 0:
        locator_to = num_of_danmus + 1
        print(f"locator_to: {locator_to}")

        for i in range(locator_from, locator_to):
            # css selector has :nth-child(), but only starts from 1.
            # count starts from 1. so we set intital locator to 1

            # print(i)
            try:
                nickname = driver.find_element_by_css_selector(
                    f'li.Barrage-listItem:nth-child({i}) .Barrage-nickName').text
            except NoSuchElementException:
                # print(NoSuchElementException)
                nickname = 'anonymous'

            try:
                content = driver.find_element_by_css_selector(
                    f'li.Barrage-listItem:nth-child({i}) .Barrage-content').text
            except NoSuchElementException:
                # print(NoSuchElementException)
                content = '[Not a danmu, but an action. e.g gifting / visiting ...]'

            print(f"{i}: {nickname}: {content}")
            danmus.append({'id': i, 'name': nickname, 'content': content})
            # update locator_from
            locator_from = danmus[-1]['id'] + 1



# close driver
driver.close()