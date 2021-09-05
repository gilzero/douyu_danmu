from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException, ElementNotVisibleException
import time
from bs4 import BeautifulSoup
import lxml

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

        # There is documentation about use selenium to excute javascript to get element value.
        # It could be a better solution, as the li keep rolling and cycling. WebElements travase might not be
        # a ideal solution, not efficient and elements went stale constantly, and you load new elements to checking
        # could be way more complicated and ineffiecient than execute js to get new li, in this case.
        # https://www.selenium.dev/documentation/webdriver/browser_manipulation/#execute-script

        if self._find_initial_danmu():
            print("Continue fetching ...")

            offset = 0

            # rewrite with js execution

            while True:
                timeout_regular = 5
                print(f"Waiting for {timeout_regular}s ...")
                time.sleep(timeout_regular)
                print("Waiting Done. Loading New Danmu...")

                # Get length of elements
                element_count = int(self.driver.execute_script(self.settings.js_element_count))

                # Get HTML
                items_html = self.driver.execute_script(self.settings.js_elements_html)

                # Parse with soup
                soup = BeautifulSoup(items_html, 'lxml')
                # print(soup)
                soup_list = soup.select(self.settings.soup_list_selector)
                # print(soup_list)

                for item in soup_list:
                    unique_id_tag = item.attrs['id']
                    # print(unique_id_tag)

                    text = item.text
                    # print(text)
                    # print(type(item))

                    # username = item.select('.Barrage-nickName')

                    item_html = str(item)

                    item_soup = BeautifulSoup(item_html, 'lxml')

                    try:
                        nickname = item_soup.select('.Barrage-nickName')[0].text.strip()
                    except:
                        # print(NoSuchElementException)
                        nickname = 'anonymous'

                    try:
                        content = item_soup.select('.Barrage-content')[0].text.strip()
                    except:
                        # print(NoSuchElementException)
                        content = '[Not a danmu, but an action. e.g gifting / visiting ...]'


                    print(f"[{soup_list.index(item)} {unique_id_tag}] {nickname}: {content}")




                # for i in range(offset, element_count):
                #     pass


                # update offset
                offset += element_count


            # while offset < 200:
            #     timeout_regular = 5
            #     print(f"Waiting for {timeout_regular}s ...")
            #     time.sleep(timeout_regular)
            #     print("Waiting Done. Loading New Danmu...")
            #
            #     elements = self.driver.find_elements_by_css_selector(self.settings.list_selector)
            #     num_items = len(elements)
            #
            #     print(f"\noffset: {offset}, num_items: {num_items}\n")
            #
            #     for i in range(offset, num_items):
            #         print(f"i: {i}")
            #         js = "return document.getElementById('js-barrage-list').innerHTML"
            #         js1 = "return document.getElementById('js-barrage-list').innerText"
            #         js2 = "return document.getElementById('js-barrage-list').childElementCount"
            #         html = self.driver.execute_script(js2)
            #         print(f"html: {html}")
            #
            #         # got html code. use soup to parse it.
            #
            #
            #         # can also use dictionary difference to substract new
            #
            #     # update offset
            #     offset = num_items
            #
            #
            #     # when offset reach 200, refresh the page
            #     if offset >= 199:
            #         break



        else:
            print("Unable to contine. No danmu found?")
            return
