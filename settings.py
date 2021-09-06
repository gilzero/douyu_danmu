class Settings:
    def __init__(
            self,
            room_id="66699",
            list_selector="li.Barrage-listItem",
            name_selector=".Barrage-nickName",
            content_selector=".Barrage-content",
            js_element_count="return document.getElementById('js-barrage-list').childElementCount",
            js_elements_html="return document.getElementById('js-barrage-list').innerHTML",
            soup_list_selector="li.Barrage-listItem"):
        """

        :param list_selector: selector of the list of danmus
        :param name_selector:  selector of each danmu's username
        :param content_selector: selector of each danmu's content
        """
        self.list_selector = list_selector
        self.name_selector = name_selector
        self.content_selector = content_selector
        self.url = f"https://www.douyu.com/{room_id}"
        self.js_element_count = js_element_count
        self.js_elements_html = js_elements_html
        self.soup_list_selector = soup_list_selector

