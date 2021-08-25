from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException, ElementNotVisibleException
import time




# Configuration
# selectors format
# sys.setrecursionlimit(2000)
danmu_instance_selector = 'li.Barrage-listItem'
danmu_instance_nickname_selector = '.Barrage-nickName'
danmu_instance_content_selector = '.Barrage-content'
url = 'https://www.douyu.com/312212'
# url = 'http://localhost:8888/danmu.html'
danmus = []

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

id = 1

while True:

    time.sleep(1)


    name_selector = f"li.Barrage-listItem:nth-child({id}) .Barrage-nickName"

    if id < 300:
        id += 1
        print(f"id {name_selector}")

        try:
            name = driver.find_element_by_css_selector(name_selector).text
        except NoSuchElementException as e:
            print(e)
            name = 'unknown'

        print(name)




