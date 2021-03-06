from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException, ElementNotSelectableException
import time


def wait_to_load(second):
    print(f'Initial Start Waiting {second}s ...')
    time.sleep(second)
    print('Waited')


# url = 'http://localhost:8888/danmu.html'
url = 'https://www.douyu.com/111111'

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.get(url)
print(driver.title)


# initial wait for js fully loaded
driver.implicitly_wait(60)
# wait_to_load(60)


# selectors format
danmu_instance_wraper_selector = 'li.Barrage-listItem'
danmu_instance_nickname_selector = '.Barrage-nickName'
danmu_instance_content_selector = '.Barrage-content'

# initialize empty danmu list of dictionaries
danmus = []

element_danmus = driver.find_elements_by_css_selector(danmu_instance_wraper_selector)
initial_length = len(element_danmus)

print(f"number of danmu elements: {initial_length}")

for i in range(len(element_danmus)):

    try:
        nickname = element_danmus[i].find_element_by_css_selector(danmu_instance_nickname_selector).text
    except NoSuchElementException:
        # print(NoSuchElementException)
        nickname = 'anonymous'


    try:
        content = element_danmus[i].find_element_by_css_selector(danmu_instance_content_selector).text
    except NoSuchElementException:
        # print(NoSuchElementException)
        content = '[Not a danmu, but an action. e.g gifting / visiting ...]'

    print(f"{i}: {nickname}: {content}")

    danmus.append({'danmuid': i, 'name': nickname, 'content': content})


locator_from = len(danmus)
checker_selector = f"li:nth-child({locator_from})"

timeout = 120 # wait every x second to check
wait = WebDriverWait(driver, timeout, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])


while True:
    locator_from = len(danmus)
    checker_selector = f"li:nth-child({locator_from})"

    if wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, checker_selector))) is not None:
        locator_to = len(driver.find_elements_by_css_selector(danmu_instance_wraper_selector))
        # print(f"from: {locator_from}")
        # print(f"to: {locator_to}")

        for i in range(locator_from, locator_to + 1):
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

            danmus.append({'danmuid': i, 'name': nickname, 'content': content})




# if wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, checker_selector))) is not None:
#     locator_to = len(driver.find_elements_by_css_selector(danmu_instance_wraper_selector))
#     print(f"from: {locator_from}")
#     print(f"to: {locator_to}")
#
#     for i in range(locator_from, locator_to+1):
#         try:
#             nickname = driver.find_element_by_css_selector(f'li.Barrage-listItem:nth-child({i}) .Barrage-nickName').text
#         except NoSuchElementException:
#             # print(NoSuchElementException)
#             nickname = 'anonymous'
#
#         try:
#             content = driver.find_element_by_css_selector(f'li.Barrage-listItem:nth-child({i}) .Barrage-content').text
#         except NoSuchElementException:
#             # print(NoSuchElementException)
#             content = '[Not a danmu, but an action. e.g gifting / visiting ...]'
#
#         print(f"{i}: {nickname}: {content}")
#
#         danmus.append({'danmuid': i, 'name': nickname, 'content': content})



# print(danmus)
driver.close()