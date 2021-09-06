from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from datetime import datetime
from bs4 import BeautifulSoup
import lxml
from danmu import Danmu
import pandas as pd


class Fetcher:
    """ The core fetcher class doing fetching work. """

    def __init__(self, settings):
        """ Initializer """
        self.settings = settings
        self.updated_batch_ids = []  # A list contains unique li ID attribute value. For checking new found or existing.
        self.danmus = []  # A list contains all valid pure danmu objects

        # Chrome Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images': 2}})

        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
        self.driver.get(settings.url)

        print(self.driver.title)

    def run_fetch(self):
        # There is documentation about use selenium to execute javascript to get element value.
        # It could be a better solution, as the li(s) keep rolling and cycling, WebElements traverse might not be
        # an ideal solution, WebElements went stale constantly, if you load new WebElements to check
        # could be way more complicated and inefficient than executing js to get new li(s), in this case.
        # https://www.selenium.dev/documentation/webdriver/browser_manipulation/#execute-script

        if self._find_initial_danmu():

            # Holder of previous batch loop's id values. Empty it for each while loop.
            self.updated_batch_ids = []

            # fetch looping condition. e.g reach a total number, or a time interval.
            while len(self.danmus) < self.settings.max_results:
                # Loop for every x seconds.
                self._regular_wait(self.settings.wait)

                # Get Elements HTML. For every loop. We check new html for those danmu ul.li.li..... section
                elements_html = self.driver.execute_script(self.settings.js_elements_html)

                # Parse the elements html. Extracting Danmu(s)
                self._parse_elements(elements_html)

        else:
            # Initial danmu not found.
            print(f"🚫 Unable to locate a danmu. (Maybe not a legit room?) Bye.")
            self.driver.quit()
            return

    @staticmethod
    def _regular_wait(sec: int):
        """
        Internal utility function. Wait for a while
        (Fetch every x seconds) Turn off the wait to make it live update, however,
        it will be resource-heavy, memory, cpus consumptions will be high. So Better to wait. For x value,
        tune the time. E.g: if for super explosive danmu (top-tier streamers), can set to shorter.
        """

        # print(f"⏲️ Waiting for {sec}s ...")
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
        :param html: html string got from every while loop.
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

                # Get each single li item as soup object
                danmu_soup = BeautifulSoup(str(item), 'lxml')

                # Extract info with soup methods
                self._extract_danmu(unique_id_tag, danmu_soup)
            else:
                # it is already extracted. skip it
                # print(f"🐍 Unique id {unique_id_tag} is in previous fetched batch. Skip")
                pass

    def _extract_danmu(self, danmu_id: str, danmu_soup: BeautifulSoup):
        """
        Internal helpler function. Extract danmu information.
        :param danmu_id: unique li id tag attribute.
        :param danmu_soup: BeautifulSoup object representing a single danmu li
        :return:
        """

        # Get danmu info: nickname, content, ...
        nickname = danmu_soup.select(self.settings.name_selector)[0].text if danmu_soup.select(
            self.settings.name_selector) else ''
        content = danmu_soup.select(self.settings.content_selector)[0].text if danmu_soup.select(
            self.settings.content_selector) else ''

        # Instantiate new Danmu object if is a valid pure danmu, and add to our 'danmus' list object.
        # We can do analysis later with all danmus from that list object.
        if self._check_valid(nickname, content):
            danmu = Danmu(danmu_id, nickname, content)
            danmu.to_str()
            self.danmus.append(danmu)

        # Append id to updated_batch_ids
        self.updated_batch_ids.append(danmu_id)

    def export_to_csv(self):
        """ Export danmus data to csv with pandas """
        # ids = [danmu.id for danmu in self.danmus]
        # nicknames = [danmu.nickname for danmu in self.danmus]
        # contents = [danmu.content for danmu in self.danmus]
        # times = [danmu.time for danmu in self.danmus]


        data_dict = {
            "id": [danmu.id for danmu in self.danmus],
            "nickname": [danmu.nickname for danmu in self.danmus],
            "content": [danmu.content for danmu in self.danmus],
            "time": [danmu.time for danmu in self.danmus]
        }

        df = pd.DataFrame(data_dict)
        file_path = 'csv/' + self.settings.room_id + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv'
        df.to_csv(file_path)
        print(f"Exported to csv: {file_path}")
