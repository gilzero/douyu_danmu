from settings import Settings
from fetcher import Fetcher

if __name__ == '__main__':
    settings = Settings()

    fetcher = Fetcher(settings)
    print(f"script {fetcher.settings.js_element_count}")
    # fetcher.run_fetch()

    fetcher.run_fetch()

    fetcher.driver.quit()
    print("driver closed")
