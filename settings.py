class Settings:
    def __init__(
            self,
            room_id="793400",
            list_selector="li.Barrage-listItem",
            name_selector=".Barrage-nickName",
            content_selector=".Barrage-content"):
        """

        :param list_selector: selector of the list of danmus
        :param name_selector:  selector of each danmu's username
        :param content_selector: selector of each danmu's content
        """
        self.list_selector = list_selector
        self.name_selector = name_selector
        self.content_selector = content_selector
        self.url = f"https://www.douyu.com/{room_id}"
