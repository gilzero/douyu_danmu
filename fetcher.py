from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException, ElementNotVisibleException
import time

class Fetcher:
    """ The core fetcher class doing fetching work. """

    def __init__(self, settings):
        """ Initializer """

        self.settings = settings
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=self.chrome_options)
        self.driver.get(settings.url)
        print(self.driver.title)
        # self.driver.close()


    def _find_initial_danmu(self):

        # Initial finding of danmu DOM. Because js loading after html page ready in DOM. Set a max 3 mins to wait for
        # danmu DOM appears. It depends on your machine and network.
        timeout_initial = 180
        print(f"Trying to locate the very first danmu, it may take some times ...")
        danmu_elements = WebDriverWait(self.driver, timeout_initial).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.settings.list_selector)))
        print(f"The very first danmu found.")

        if danmu_elements:
            return True
        else:
            self.driver.close()
            return False


    def run_fetch(self):

        if self._find_initial_danmu():
            print("Continue fetching ...")

            offset = 0

            while offset < 200:
                timeout_regular = 5
                print(f"Waiting for {timeout_regular}s ...")
                time.sleep(timeout_regular)
                print("Waiting Done. Loading New Danmu...")

                elements = self.driver.find_elements_by_css_selector(self.settings.list_selector)
                num_items = len(elements)

                print(f"\noffset: {offset}, num_items: {num_items}\n")

                for i in range(offset, num_items):
                    print(f"i: {i}")
                    try:
                        nickname = elements[i].find_element_by_css_selector('.Barrage-nickName').text
                    except NoSuchElementException:
                        # print(NoSuchElementException)
                        nickname = 'anonymous'

                    try:
                        content = elements[i].find_element_by_css_selector('.Barrage-content').text
                    except NoSuchElementException:
                        # print(NoSuchElementException)
                        content = '[Not a danmu, but an action. e.g gifting / visiting ...]'

                    print(f"{i}: {nickname}: {content}")


                # update offset
                offset = num_items


                # when offset reach 200, refresh the page
                if offset >= 199:
                    print(f"offset: {offset}, refresh the page.")
                    self.driver.refresh()


        else:
            print("Unable to contine. No danmu found?")
            return
