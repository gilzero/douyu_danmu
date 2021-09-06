from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from bs4 import BeautifulSoup
import lxml
from danmu import Danmu


class Fetcher:
    """ The core fetcher class doing fetching work. """

    def __init__(self, settings):
        """ Initializer """
        self.settings = settings
        self.updated_batch_ids = []
        self.danmus = []

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images': 2}})

        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
        self.driver.get(settings.url)

        print(self.driver.title)

    def run_fetch(self):
        # There is documentation about use selenium to excute javascript to get element value.
        # It could be a better solution, as the li keep rolling and cycling. WebElements traverse might not be
        # a ideal solution, not efficient and elements went stale constantly, and you load new elements to checking
        # could be way more complicated and inefficient than execute js to get new li, in this case.
        # https://www.selenium.dev/documentation/webdriver/browser_manipulation/#execute-script

        if self._find_initial_danmu():

            # Holder of previous batch loop's id values. Empty it for each while loop.
            self.updated_batch_ids = []

            while True:
                # Fetch every x seconds. Recommend to wait. If turn off the wait regular, can make it live update.
                # But super resource-heave, memory, cpu consumption will be high. Better to wait. For how long,
                # you can tune the time. if for super explosive danmu (super big streamer), can set to shorter.
                self._regular_wait(3)

                # Get Elements HTML
                items_html = self.driver.execute_script(self.settings.js_elements_html)

                # Parse the elements html. Extracting Danmu(s)
                self._parse_elements(items_html)

        else:
            # Initial danmu not found.
            print(f"🚫 Unable to locate danmu. (Maybe not a legit room?) Bye.")
            self.driver.quit()
            return

    @staticmethod
    def _regular_wait(sec: int):
        """ Internal utility function. Wait for a while"""
        print(f"⏲️ Waiting for {sec}s ...")
        time.sleep(sec)
        # print("⏲️ Waiting Done. Loading New Danmu...")
        # print("Continue fetching ...")

    def _find_initial_danmu(self):
        # Initial finding of danmu DOM. Because js loading after html page ready in DOM. Set a max 3 mins to wait for
        # danmu DOM appears. It depends on your machine and network.
        # 180 seconds max
        print(f"⏲️ Trying to locate the very first danmu. Waiting.")
        danmu_elements = WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.settings.list_selector)))
        print(f"✅ The very first danmu found.")

        return True if danmu_elements else False

    @staticmethod
    def _check_valid(nickname, content):
        """
        Internal utility function.
        Check if is a valid danmu. People actually saying some content.
        It's called before instantiate a new Danmu()
        :return: Boolean
        """
        return True if (nickname and content) else False

    def _parse_elements(self, html: str):
        """
        Parsing the danmus part html. barebones structure is like: <ul><li>../li><li>../li><li>../li>...</ul>
        :param html:
        :return:
        """

        # Parse with soup
        soup = BeautifulSoup(html, 'lxml')
        # soup_list is the soup containing multiple li(s)
        soup_list = soup.select(self.settings.soup_list_selector)

        # Loop for every li element
        for item in soup_list:
            # Get Unique li ID attribute value. Each list has a dynamically generated unique ID.
            unique_id_tag = item.attrs['id']

            if unique_id_tag not in self.updated_batch_ids:
                # This is a new 'li'

                # Extract info with soup methods
                # Get each list as soup object
                item_soup = BeautifulSoup(str(item), 'lxml')

                # Get danmu info: nickname, content, ...
                nickname = item_soup.select(self.settings.name_selector)[0].text if item_soup.select(
                    self.settings.name_selector) else ''
                content = item_soup.select(self.settings.content_selector)[0].text if item_soup.select(
                    self.settings.content_selector) else ''

                if self._check_valid(nickname, content):
                    # Instantiate new Danmu object
                    danmu = Danmu(unique_id_tag, nickname, content)
                    danmu.to_str()

                # Append id to updated_id_list
                self.updated_batch_ids.append(unique_id_tag)
            else:
                # it is already extracted. skip it
                # print(f"🐍 Unique id {unique_id_tag} is in previous fetched batch. Skip")
                pass
