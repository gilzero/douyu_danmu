from datetime import datetime


class Danmu:
    """ Class for Danmu
    (This is class for Pure content only. Disregard of info/action danmu, no gifting, entering, etc
    """

    def __init__(self, id, nickname: str, content: str):
        """
        Initializer
        :param nickname: User's name
        :param content: Valid content of a danmu.
        """
        self.id = id
        self.nickname = nickname.strip().rstrip('：')
        self.content = content.strip()
        self.time = datetime.now().isoformat("_", "seconds")

    def to_str(self):
        """ Print danmu """
        print(f"📜 [{self.id}] {self.nickname}: {self.content} @ {self.time}")
