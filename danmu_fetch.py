from settings import Settings
from fetcher import Fetcher

if __name__ == '__main__':
    settings = Settings()
    fetcher = Fetcher(settings)

    fetcher.run_fetch()

    fetcher.driver.quit()
    print("Driver Closed. Bye")
