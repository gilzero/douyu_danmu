class Settings:
    """
    Class for Settings object
    """
    def __init__(self, room_id="92000", wait=0.5, max_results=50):
        """

        :param room_id: Stream room id
        :param wait: regular wait every x seconds to parse danmu(s)
        """
        self.room_id = room_id
        self.wait = wait
        self.max_results = max_results
        self.list_selector = "li.Barrage-listItem"
        self.name_selector = ".Barrage-nickName"
        self.content_selector = ".Barrage-content"
        self.url = f"https://www.douyu.com/{room_id}"
        self.js_element_count = "return document.getElementById('js-barrage-list').childElementCount"
        self.js_elements_html = "return document.getElementById('js-barrage-list').innerHTML"
        self.soup_list_selector = "li.Barrage-listItem"

